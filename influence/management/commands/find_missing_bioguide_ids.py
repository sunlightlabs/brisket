import re, urllib, urllib2

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db                   import connection, transaction
from influence                   import helpers

try:
    import json
except:
    import simplejson as json

class Command(BaseCommand):
    args = '<limit>'
    help = 'Fills in missing Bioguide ID\'s'

    def handle(self, *args, **options):
        print "Starting..."
        cursor = connection.cursor()

        cursor.execute("""select
                entity_id,
                name
            from
                matchbox_entity e
                inner join matchbox_entityattribute ea
                    on e.id = ea.entity_id
                inner join matchbox_politicianmetadata pm
                    using (entity_id)
            where
                seat like 'federal%%'
                and bioguide_id is null""")
        ids_and_names = cursor.fetchall()
        print "{0} federal politicians without bioguide ids found".format(len(ids_and_names))

        count_found = 0
        found_ids = []

        for (entity_id, name) in ids_and_names:

            bioguide_id = self.get_bioguide_id(name)

            if bioguide_id:
                count_found += 1

                sql = "update matchbox_entityattribute set bioguide_id = '%s' where entity_id = '%s'"
                bound_sql = sql % (bioguide_id, entity_id)
                print bound_sql

                cursor.execute(bound_sql)

        print "{0} federal politicians without bioguide ids found.".format(len(ids_and_names))
        print "{0} updated.".format(count_found)

        transaction.commit()


    def get_bioguide_id(self, full_name):
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

        #print "Searching bioguide for: %s" % name_first_last

        arguments = urllib.urlencode({
            'apikey': settings.API_KEY,
            'name': name_first_last,
            'all_legislators': 1,
        })

        url = "http://services.sunlightlabs.com/api/legislators.search.json?"
        api_call = url + arguments
        #print api_call
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

