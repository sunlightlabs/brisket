======================
Earmark Aggregates API
======================

Organization Methods
====================

Top Earmarks
------------

Return the top earmarks received, by dollar amount.

Examples
~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/2d625ce311ff4aa091ae66f440c2a62f/earmarks.json?apikey=<your-key>``

::

    [{
        "members": 
        [
            {"party": "D", "state": "IL", "name": "Roland Burris", "id": "c852c26ea375407f82fb1a53bb8ca006"}
        ], 
        "amount": "4000000.00", 
        "fiscal_year": 2010, 
        "recipients": 
        [
            {"name": "Honeywell International", "id": "2d625ce311ff4aa091ae66f440c2a62f"}
        ], 
        "description": "Bio-synthetic Paraffinic Kerosene Production"
     },
     {
        "members": 
        [
            {"party": "R", "state": "FL", "name": "C.W. Bill Young", "id": ""}
        ], 
        "amount": "4000000.00", 
        "fiscal_year": 2008, 
        "recipients": 
        [
            {"name": "Honeywell International", "id": "2d625ce311ff4aa091ae66f440c2a62f"}
        ], 
        "description": "Rocket Systems Launch Program (SPACE) -- Ballistic Missile Technology"
     },
     {
        "members": 
        [
            {"party": "D", "state": "FL", "name": "Bill Nelson", "id": "5a1a3576871e459e9bb0af1a1d5cd826"}, 
            {"party": "R", "state": "FL", "name": "C.W. Bill Young", "id": ""}
        ], 
        "amount": "4000000.00", 
        "fiscal_year": 2008, 
        "recipients": 
        [
            {"name": "Honeywell International", "id": "2d625ce311ff4aa091ae66f440c2a62f"}
        ], 
        "description": "Rocket Systems Launch Program (SPACE) -- Ballistic Missile Range Safety Technology"
     },
    ...]