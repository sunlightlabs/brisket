import logging, csv, codecs

from django.core.management.base import BaseCommand, CommandError
from django.db                   import connection, transaction


class Command(BaseCommand):
    args = '<file> <batch_size>'
    # possible options:
    #   (if batching added, batch limit)
    # overwrite existing/refresh vs. only fill in missing
    # delete or mark ones no longer found (how do we want to deal w/ this?) maybe update a "no longer found on" date column

    help = 'Load Wikipedia info'

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

    def handle(self, *args, **options):
        self.log.info("Starting to load Wikipedia bios...")
        cursor = connection.cursor()
        self.log.debug("Args given: {0}".format(args))

        # set defaults
        file = args[0] if len(args) > 0 else None
        if not file:
            self.log.fatal("A valid filename must be passed as an argument.")
            return

        batch_size = args[1] if len(args) > 1 else 500

        # initialize reader
        reader = UnicodeReader(open(file))

        rows = []
        count = 0
    
        for (entity_id, url, bio, date) in reader:
            count += 1
            #self.log.debug(count)

            rows.append((entity_id, url, bio, date))

            if len(rows) >= batch_size:
                self.log.debug("{0}: Starting batch insert...".format(count))
                self.delete_and_insert(rows, cursor)
                rows = []

        # insert the last chunk
        if len(rows):
            self.log.info("Starting the last batch with row {0} and batch size {1}".format(count, len(rows)))
            self.delete_and_insert(rows, cursor)

        self.log.info("Done.")


    @transaction.commit_manually
    def delete_and_insert(self, rows, cursor):
        rows_with_bios = [line for line in rows if line[1]]

        self.log.info("Creating temp table tmp_matchbox_wikipediainfo")
        cursor.execute("create temp table tmp_matchbox_wikipediainfo on commit drop as select * from matchbox_wikipediainfo limit 0");

        self.log.info("Starting insert into tmp_matchbox_wikipediainfo")

        values_string = ",".join(["(%s, %s, %s, %s)" for x in rows_with_bios])
        insert_sql = "insert into tmp_matchbox_wikipediainfo (entity_id, bio_url, bio, scraped_on) values %s" % values_string
        cursor.execute(insert_sql, [item for sublist in rows_with_bios for item in sublist])

        self.log.info("Finished inserting into temp table. {0} rows inserted.".format(len(rows_with_bios)))

        self.log.info("Starting delete of rows to replace...")
        cursor.execute("""delete from matchbox_wikipediainfo where entity_id in (
            select entity_id from tmp_matchbox_wikipediainfo
        )""")

        self.log.info("Inserting from temp table into real table.")
        cursor.execute("""
            insert into matchbox_wikipediainfo (entity_id, bio_url, bio, scraped_on)
                select entity_id, bio_url, bio, scraped_on from tmp_matchbox_wikipediainfo
        """)
        transaction.commit()

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
                     





