==========
Entity API
==========

Search by Name
--------------

Search for entities--that is, politicians, individuals, or organizations--with the given name. Returns basic information about the the contributions to and from each entity, as well as an ID that can be used in other API methods to retrieve more information.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/entities.json``


Parameters
~~~~~~~~~~

search
    The query string. Spaces should be URL-encoded or represented as ``+``. There are no logic operators or grouping.


Example
~~~~~~~

``http://transparencydata.com/api/1.0/entities.json?apikey=<your-key>&search=nancy+pelosi``

::

    [{"name": "Van Scoyoc, Greg", 
      "count_given": 0, 
      "firm_income": 0.0, 
      "count_lobbied": 11, 
      "seat": null, 
      "total_received": 0.0, 
      "state": null, 
      "lobbying_firm": null, 
      "count_received": 0, 
      "party": null, 
      "total_given": 0.0, 
      "type": "individual", 
      "id": "0f7e17d91acc42369d7a0a2438b37161", 
      "non_firm_spending": 0.0},
     {"name": "Van Scoyoc Kelly", 
     "count_given": 0, 
     "firm_income": 890000.0, 
     "count_lobbied": 47, 
     "seat": null, 
     "total_received": 0.0, 
     "state": null, 
     "lobbying_firm": true, 
     "count_received": 0, 
     "party": null, 
     "total_given": 0.0, 
     "type": "organization", 
     "id": "69509241c4cc458f8473356144a65e3f", 
     "non_firm_spending": 0.0},
    {"name": "VAN SCOYOC, JIM", 
     "count_given": 0, 
     "firm_income": 0.0, 
     "count_lobbied": 0, 
     "seat": "state:lower", 
     "total_received": 2960.0, 
     "state": "IA", 
     "lobbying_firm": null, 
     "count_received": 24, 
     "party": "D", 
     "total_given": 0.0, 
     "type": "politician", 
     "id": "83a0032965834f80a1dfbda9d2da82ad", 
     "non_firm_spending": 0.0},
    ...]

      
ID Lookup
---------

Look up the entity ID based on an ID from a different data set. Currently we provide a mapping from the ID schemes used by Center for Reponsive Politics (CRP) and the National Institute for Money in State Politics (NIMSP), and BioGuide. The result is a JSON object listing the TransparencyData IDs matching the given external ID.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/entities/id_lookup.json``

Parameters
~~~~~~~~~~

namespace
    The dataset and data type of the ID. Currently allowed values are:
    
    ========================== ===============================================================================
    namespace                  Description
    ========================== ===============================================================================
    ``urn:crp:individual``     A CRP ID for an individual contributor or lobbyist. Begins with ``U`` or ``C``.
    ``urn:crp:organization``   A CRP ID for an organization. Begins with ``D``.
    ``urn:crp:recipient``      A CRP ID for a politician. Begins with ``N``.
    ``urn:nimsp:organization`` A NIMSP ID for an organization. Integer-valued.
    ``urn:nimsp:recipient``    A universal (not per-cycle) NIMSP ID for a politician. Integer-valued.
    ========================== ===============================================================================

    More namespaces may be added in the future as other ID schemes are reconciled with the TransparencyData dataset.
    
id
    The ID of the entity in the given namespace.
    
Example
~~~~~~~

``http://transparencydata.com/api/1.0/entities/id_lookup.json?apikey=<your-key>&namespace=urn:crp:recipient&id=N00007360``

::

    [{"id": "85ab2e74589a414495d18cc7a9233981"}]

Entity Overview
---------------

Return general information about a particular entity.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/entities/<entity ID>.json``

    
Example
~~~~~~~

``http://transparencydata.com/api/1.0/entities/ff96aa62d48f48e5a1e284efe74a0ba8.json?apikey=<your-key>``

::

    {"name": "Walt Disney Co", 
     "totals": 
     {
        "1990": 
            {"contributor_count": 485, 
             "recipient_amount": 146589.0, 
             "grant_count": 0, 
             "lobbying_count": 0, 
             "firm_income": 0.0, 
             "contract_amount": 0.0, 
             "contributor_amount": 437624.0, 
             "loan_amount": 0.0, 
             "earmark_amount": 0.0, 
             "earmark_count": 0, 
             "grant_amount": 0.0, 
             "loan_count": 0, 
             "contract_count": 0, 
             "recipient_count": 103, 
             "non_firm_spending": 0.0},
        "1992": 
        ...<continues for all years with data. Year "-1" is a sum of all years>...
    }, 
    "external_ids": 
    [
        {"namespace": "urn:crp:organization", "id": "D000000128"}, 
        {"namespace": "urn:nimsp:organization", "id": "2779"}
    ], 
    "type": "organization", 
    "id": "204b089d9d614fa6b77db666d76d9f3c", 
    "metadata": 
    {
        "bio": "<p>The Walt Disney Company (NYSE: DIS) is the largest media and entertainment conglomerate in the world.  Founded on October 16, 1923 by brothers Walt Disney and Roy Disney as the Disney Brothers Cartoon Studio, the company was reincorporated as Walt Disney Productions in 1929. Walt Disney Productions established itself as a leader in the American animation industry before diversifying into live-action film production, television, and travel. Taking on its current name in 1986, The Walt Disney Company expanded its existing operations and also started divisions focused upon theatre, radio, publishing, and online media. In addition, it has created new divisions of the company in order to market more mature content than it typically associates with its flagship family-oriented brands.</p>",
        "source_name": "wikipedia_info", 
        "bio_url": "http://en.wikipedia.org/wiki/The_Walt_Disney_Company", 
        "lobbying_firm": false, 
        "entity": "204b089d9d614fa6b77db666d76d9f3c", 
        "industry_entity": "f50cf984a2e3477c8167d32e2b14e052", 
        "child_entities": 
        [
            {"type": "organization", "name": "ABC Inc", "id": "7015fb28d53b4d2abbb720e451daa22f"}, 
            {"type": "organization", "name": "Disney Worldwide Services", "id": "103c611727ac46939eee5f1d0079c369"}
        ], 
        "parent_entity": null}}


Entity List
===========

Used to iterate through every entity in Transparency Data. Can return up to 10,000 entities in a single call.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/entities/list.json

Parameters
~~~~~~~~~~

start
    The starting record to return.

end
    The last record to return (exclusive.)

count
    When present, return only the total number of entities.
    
Examples
~~~~~~~~

``http://transparencydata.com/api/1.0/entities/list.json?count=1&apikey=<your-key>``

::

    {"count": 134223}
    
``http://transparencydata.com/api/1.0/entities/list.json?count&start=0&end=3&apikey=<your-key>``

::

    [{"type": "organization", 
      "id": "00007acb09ff4c2bbe45e1faaa41317c", 
      "name": "Rooney Holdings"},
     {"type": "politician", 
      "id": "00008c8d5eb645a7a4f3dd626d631a71", 
      "name": "OLKOWSKI, JOYCE"},
     {"type": "individual", 
      "id": "0000b10d2f1e4abbb69cd56faf1d9454", 
      "name": "Lynch, Kevin A"}]
