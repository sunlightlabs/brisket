import re, urllib, urllib2, logging, sys, time

from django.conf                 import settings
from django.core.management.base import BaseCommand, CommandError
from django.db                   import connection, transaction
from influence                   import helpers
from BeautifulSoup               import BeautifulSoup

try:
    import json
except:
    import simplejson as json

class Command(BaseCommand):
    args = '<limit> <offset (optional)>'
    # possible options:
    # overwrite existing/refresh vs. only fill in missing
    # delete or mark ones no longer found (how do we want to deal w/ this?) maybe update a "no longer found on" date column

    help = 'Populate Bioguide info'

    def __init__(self):
        self.set_up_logger()

    def set_up_logger(self):
        # create logger
        self.log = logging.getLogger("command")
        self.log.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

    @transaction.commit_manually
    def handle(self, *args, **options):
        self.log.info("Starting...")

        # chunk size
        limit = int(args[0]) if args and len(args) else 500
        offset = int(args[1]) if args and len(args) > 1 else 0
        cursor = connection.cursor()

        # get count
        cursor.execute("""
            select
                count(*)
            from
                matchbox_entity e
                inner join matchbox_politicianmetadata pm
                    on e.id = pm.entity_id
            where
                seat like 'federal%%'
        """)
        total = cursor.fetchone()

        transaction.rollback()

        count = 0

        while count < total:
            count += limit

            # loop until we're at the count, doing chunks along the way.

            limit_clause = "limit {0}".format(limit) if limit else ''
            offset_clause = "offset {0}".format(offset) if limit else ''

            select_sql = """
                select
                    entity_id,
                    name
                from
                    matchbox_entity e
                    inner join matchbox_politicianmetadata pm
                        on e.id = pm.entity_id
                where
                    seat like 'federal%%'
                order by
                    entity_id
                {0}
                {1}
            """.format(limit_clause, offset_clause)

            self.log.debug(select_sql)
            cursor.execute(select_sql)
            ids_and_names = cursor.fetchall()
            transaction.rollback()

            if not len(ids_and_names):
                self.log.info("No more found. Done.")
                return

            # we shouldn't need the offset again in this iteration, so move it over by the amount of the limit
            offset += limit

            self.log.info("Chunk of {0} federal politicians located to find bioguide ids for".format(len(ids_and_names)))

            count_found = 0
            found_ids_and_info = []

            for (entity_id, name) in ids_and_names:

                bioguide_id = self.get_bioguide_id(entity_id, name)

                if bioguide_id:
                    self.log.info("Found bioguide id for {0}.".format(name))
                    count_found += 1
                    bio, photo_url, years = self.get_bioguide_info(bioguide_id)

                    if len(years) > 32:
                        self.log.warn("Years of service is too long! Value: {0}".format(years))
                        return

                    found_ids_and_info.append((entity_id, bioguide_id, bio, photo_url, years))

            self.log.info("Creating temp table tmp_matchbox_bioguideinfo")
            cursor.execute("create temp table tmp_matchbox_bioguideinfo on commit drop as select * from matchbox_bioguideinfo limit 0");


            self.log.info("Inserting into tmp_matchbox_bioguideinfo...")

            values_string = ",".join(["(%s, %s, %s, %s, %s)" for x in found_ids_and_info])
            insert_sql = "insert into tmp_matchbox_bioguideinfo (entity_id, bioguide_id, bio, photo_url, years_of_service) values %s" % values_string
            cursor.execute(insert_sql, [item for sublist in found_ids_and_info for item in sublist])

            self.log.info("Finished inserting into temp table. {0} rows inserted.".format(count_found))


            self.log.info("Deleting rows to replace in matchbox_bioguideinfo")
            cursor.execute("""delete from matchbox_bioguideinfo where entity_id in (
                select entity_id from tmp_matchbox_bioguideinfo
            )""")


            self.log.info("Inserting from temp table into real table.")
            cursor.execute("""insert into matchbox_bioguideinfo (entity_id, bioguide_id, bio, photo_url, years_of_service)
                select entity_id, bioguide_id, bio, photo_url, years_of_service from tmp_matchbox_bioguideinfo""")

            transaction.commit()

        self.log.info("Done.")


    def get_bioguide_id(self, entity_id, full_name):
        ''' attempt to determine the bioguide_id of this legislastor, or
        return None. removes some basic formatting and trailing party
        designators'''
        name = helpers.standardize_politician_name(full_name) # strip party, etc...

        # this is a fix for the legislator search API's poor performance with middle initials
        # it may be removed later on if James can fix the API
        name_parts = re.search(r'^(?P<first>\w+)(?P<middle> \w\.?)?(?P<last_w_suffix> (?P<last>\w+)(?P<suffix> ([js]r|I{2,})\.?)?\s*)$', name, re.IGNORECASE)

        if name_parts:
            name_first_last = "%s %s" % name_parts.group('first', 'last')
            last_name       = name_parts.group('last')
        else:
            name_first_last, last_name = name, name

        arguments = urllib.urlencode({
            'apikey': settings.API_KEY,
            'name': name_first_last,
            'all_legislators': 1,
        })

        url = "http://services.sunlightlabs.com/api/legislators.search.json?"
        api_call = url + arguments

        try:
            fp = urllib2.urlopen(api_call)
        except urllib2.URLError:
            self.log.info("Lookup failed. Waiting 5 seconds to try one more time...")
            time.sleep(5)
            fp = urllib2.urlopen(api_call)

        js = json.loads(fp.read())
        try:
            #legislators.search method returns a set of results, sorted by
            #decreasing 'quality' of the result. take here the best
            #match-- the first one.
            first_match = js['response']['results'][0]['result']['legislator']

            # unsuccessful runs for federal office can result in federal campaign contributions,
            # but no bioguide info. in that case, the search API can throw really crazy guesses at us.
            # make sure the match is at least sane by checking the last name.
            if re.match(first_match['lastname'], last_name, re.IGNORECASE):
                return first_match['bioguide_id']
        except:
            return None

    def get_bioguide_info(self, bioguide_id):
        # scrape congress' bioguide site for years of service and official bio
        html = urllib2.urlopen("http://bioguide.congress.gov/scripts/biodisplay.pl?index=%s" % bioguide_id).read()
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

        years_of_service = soup.findAll('table')[1].find('tr').findAll('td')[1].findAll('font')[2].next.next.next.strip()

        bio_a = soup.findAll('table')[1].find('tr').findAll('td')[1].find('p').find('font').extract().renderContents()
        bio_b = soup.findAll('table')[1].find('tr').findAll('td')[1].find('p').renderContents()
        biography = bio_a.strip()+' '+bio_b.strip()

        arguments = urllib.urlencode({
            'apikey': settings.API_KEY,
            'bioguide_id': bioguide_id,
            'all_legislators': 1,
        })
        api_call = "http://services.sunlightlabs.com/api/legislators.get.json?" + arguments
        fp = urllib2.urlopen(api_call)
        js = json.loads(fp.read())
        meta = js['response']['legislator']

        # append additional info and return
        photo_url = self.photo_url(bioguide_id)
        return biography, photo_url, years_of_service

    def photo_url(self, bioguide_id):
        return "http://assets.sunlightfoundation.com/moc/100x125/%s.jpg" % bioguide_id if bioguide_id else None

