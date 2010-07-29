CREATE TABLE "matchbox_bioguideinfo" (
    "id" serial NOT NULL PRIMARY KEY,
    "entity_id" varchar(32) NOT NULL REFERENCES "matchbox_entity" ("id") DEFERRABLE INITIALLY DEFERRED,
    "bioguide_id" varchar(7),
    "bio" text,
    "years_of_service" varchar(32),
    "photo_url" varchar(200),
    "created_on" date NOT NULL default (current_date)
    "updated_on" date
)
;
CREATE TABLE "matchbox_wikipediainfo" (
    "id" serial NOT NULL PRIMARY KEY,
    "entity_id" varchar(32) NOT NULL REFERENCES "matchbox_entity" ("id") DEFERRABLE INITIALLY DEFERRED,
    "bio" text,
    "bio_url" varchar(200),
    "scraped_on" timestamp,
    "created_on" date NOT NULL default (current_date),
    "updated_on" date
)
;
CREATE TABLE "matchbox_sunlightinfo" (
    "id" serial NOT NULL PRIMARY KEY,
    "entity_id" varchar(32) NOT NULL REFERENCES "matchbox_entity" ("id") DEFERRABLE INITIALLY DEFERRED,
    "bio" text,
    "photo_url" varchar(200),
    "notes" varchar(255),
    "created_on" date NOT NULL default (current_date),
    "updated_on" date
)
;

commit;
