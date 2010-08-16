update matchbox_bioguideinfo set bio_url = 'http://bioguide.congress.gov/scripts/biodisplay.pl?index=' || bioguide_id;
commit;
