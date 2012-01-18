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


Politician Methods
==================


In-state vs. Out-of-state
-------------------------

Return the portion of sponsored earmarks that went to this member's home state.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/5a1a3576871e459e9bb0af1a1d5cd826/earmarks/local_breakdown.json?apikey=<your-key>&cycle=2010``

::

    {"in-state": [159, "164221700.00"], 
     "out-of-state": [4, "7660000.00"], 
     "unknown": [1, "300000.00"]}


Top Earmarks
------------

Returns the top sponsored earmarks, by dollar amount.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/5a1a3576871e459e9bb0af1a1d5cd826/earmarks.json?apikey=<your-key>&cycle=2010``

::

    [{
        "members": 
        [
            {"party": "R", "state": "FL", "name": "Mel Martinez", "id": "0f982d0dca7740529c4c0e6769d2dca4"}, 
            {"party": "D", "state": "FL", "name": "Bill Nelson", "id": "5a1a3576871e459e9bb0af1a1d5cd826"}, 
            {"party": "R", "state": "FL", "name": "Bill Posey", "id": "928f43cea01e4f08a33f4b24971594b5"}
        ], 
        "amount": "8400000.00", 
        "fiscal_year": 2010, 
        "recipients": [], 
        "description": "Combat Weapons Training Facility"
    },
    {
        "members": 
        [
            {"party": "D", "state": "FL", "name": "Kathy Castor", "id": "22a4f5a7316245dc9ec38941732d398e"}, 
            {"party": "D", "state": "FL", "name": "Bill Nelson", "id": "5a1a3576871e459e9bb0af1a1d5cd826"}, 
            {"party": "R", "state": "FL", "name": "Gus Bilirakis", "id": "acca025fab5a42a58eb102ab71f16a79"}, 
            {"party": "R", "state": "FL", "name": "Bill Young", "id": ""}
        ], 
        "amount": "6000000.00", 
        "fiscal_year": 2010, 
        "recipients": 
        [
            {"name": "Moffit Cancer Center (Tampa)", "id": ""}
        ], 
        "description": "National Functional Genomics Center"
    },
    {
        "members": 
        [
            {"party": "D", "state": "AR", "name": "Mark Pryor", "id": "046ce370088a489997d92271f36249ca"}, 
            {"party": "D", "state": "FL", "name": "Allen Boyd", "id": "539581bfae27483086c096c1cc2d8f10"}, 
            {"party": "D", "state": "FL", "name": "Bill Nelson", "id": "5a1a3576871e459e9bb0af1a1d5cd826"}, 
            {"party": "D", "state": "HI", "name": "Mazie K Hirono", "id": "79f92c32d0a244009c8c296dd4daff30"}, 
            {"party": "D", "state": "FL", "name": "Corrine Brown", "id": "9a5019c0036d4badb0e385efb0cfb375"}, 
            {"party": "D", "state": "HI", "name": "Daniel K Akaka", "id": "ae21d1af545f4940a60cbe9db77afff4"}, 
            {"party": "D", "state": "AR", "name": "Blanche Lincoln", "id": "b5f229d227ea4433891edb1c2131bcab"}, 
            {"party": "D", "state": "AR", "name": "Marion Berry", "id": "db5a12384e7e4fcd8ce168a71ccf9b56"}, 
            {"party": "D", "state": "FL", "name": "Meek", "id": ""}
        ], 
        "amount": "4800000.00", 
        "fiscal_year": 2010, 
        "recipients": 
        [
            {"name": "Arkansas State University (Berry)", "id": ""}, 
            {"name": "Florida A&M University (Brown", "id": ""}, 
            {"name": "University of Hawaii", "id": "dcd5591de57d4b05b26894a9c9575bf7"}
        ], 
        "description": "Standoff Improvised Explosive Detection Program"
    },
    ...]