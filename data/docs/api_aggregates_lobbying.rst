=======================
Lobbying Aggregates API
=======================

Lobbying information is available for three types of entities: individual lobbyists, clients and lobbying firms. Lobbying firms are identified by ``metadata.lobbying_firm=true`` in the entity overview. Lobbying firms are also referred to as "registrants", since they are required to register their activities. Non-lobbying firms are considered clients, in that they primarily hire other firms to lobbying on their behalf. 


Client Methods
==============


Lobbying Firms Hired (Registrants)
----------------------------------

Return the top lobbying firms hired by this organization, along with the number of contracts and total amount paid.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/204b089d9d614fa6b77db666d76d9f3c/registrants.json?apikey=<your-key>``

::

    [{"registrant_name": "Verner, Liipfert et al", 
      "count": 5, 
      "amount": "1040000.00", 
      "registrant_entity": "c6ec3e5f6a314fb7bf193eae16ffab20"},
     {"registrant_name": "Cassidy & Assoc", 
      "count": 19, 
      "amount": "820000.00", 
      "registrant_entity": "c731bfe879c44d6fae99d482d04f1c57"},
     {"registrant_name": "American Continental Group", 
      "count": 15, "amount": "630000.00", 
      "registrant_entity": "61e214d53e50485fad7e7671c00fa132"}, 
     ...]


Issues Lobbied
--------------

Return the top issues that the client lobbied. Lobbying disclosures do not report dollar amounts per issue area, so issues are ranked solely on the number of contracts listing the issue.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/204b089d9d614fa6b77db666d76d9f3c/issues.json?apikey=<your-key>``

::

    [{"count": 68, 
      "issue": "Copyright, Patent & Trademark"},
     {"count": 63, 
      "issue": "Radio & TV Broadcasting"},
     {"count": 42, 
      "issue": "Taxes"},
     ...]


Lobbyists Employed
------------------

Return the individual lobbyists employed. Lobbying disclosures do not report dollar amounts per individual lobbyists, so lobbyists are ranked solely on the number of contracts in which they appear.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/204b089d9d614fa6b77db666d76d9f3c/lobbyists.json?apikey=<your-key>``

::

    [{"count": 30, 
      "lobbyist_name": "Bates, Richard M", 
      "lobbyist_entity": "189d005ede0c446fab5631b805e5f87a"},
     {"count": 27, 
      "lobbyist_name": "Padden, Preston R", 
      "lobbyist_entity": "22c39241a8c946dabdc5c1cb4946862b"},
     {"count": 24, 
      "lobbyist_name": "Fox, Susan", 
      "lobbyist_entity": "144b9e8a1fb0407a995b2f663d91004b"},
     ...]


Lobbying Firm (Registrant) Methods
==================================

Clients
-------

Return the clients that hired this firm, along with the number of contracts and total amount paid.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/52a1620b2ff543ebb74718fbff742529/registrant/clients.json?apikey=<your-key>``

::

    [{"count": 30, 
      "client_name": "Mars Inc", 
      "client_entity": "5c566a10eeda41c68bce88d0acefc23b", 
      "amount": "19470000.00"},
     {"count": 15, 
      "client_name": "Assn of Trial Lawyers of America", 
      "client_entity": "d3db6dd51bef4b758300d6ea611f71ae", 
      "amount": "8380000.00"},
     {"count": 24, 
      "client_name": "Hoffmann-La Roche", 
      "client_entity": "59e5eeff40a54fc69ce21961e00465f2", 
      "amount": "6075000.00"},
     ...]


Issues Lobbied
--------------

Return the top issues on which this firm lobbied. Lobbying disclosures do not report dollar amounts per issue area, so issues are ranked solely on the number of contracts listing the issue.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/52a1620b2ff543ebb74718fbff742529/registrant/issues.json?apikey=<your-key>``

::

    [{"count": 1674, 
      "issue": "Fed Budget & Appropriations"},
     {"count": 1007, 
      "issue": "Transportation"},
     {"count": 991, 
      "issue": "Health Issues"},
     ...]


Lobbyists Employed
------------------

Return the individual lobbyists employed. Lobbying disclosures do not report dollar amounts per individual lobbyists, so lobbyists are ranked solely on the number of contracts in which they appear.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/52a1620b2ff543ebb74718fbff742529/registrant/lobbyists.json?apikey=<your-key>``

::

    [{"count": 730, 
      "lobbyist_name": "Newberry, Edward", 
      "lobbyist_entity": "4878346af9654feaab10ed775d67664f"},
     {"count": 719, 
      "lobbyist_name": "Boggs, Thomas Hale Jr", 
      "lobbyist_entity": "56014031e60e4df6903025bd26e60b61"},
     {"count": 611, 
      "lobbyist_name": "Jonas, John", 
      "lobbyist_entity": "25b8cdcc5b914402967c91fd542f055e"},
     ...]
 

Individual Lobbyist Methods
===========================

Lobbying disclosures do not associate dollar amounts to individual lobbyists. All lobbyist methods return only the number of times the lobbyist was mentioned in a disclosure report.

Employers (Registrants)
-----------------------

Return the lobbying firms that employed this lobbyist.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/161d40ee83574de29095686c93b1bf74/registrants.json?apikey=<your-key>``

::

    [{"registrant_name": "Van Scoyoc Assoc", 
      "count": 6019, 
      "registrant_entity": "d5bc3b5e617b43ed89e73000de9ff379"},
     {"registrant_name": "Capitol Decisions", 
      "count": 560, 
      "registrant_entity": "65d93269015e46b1b1f40e7e1ba3d138"},
     {"registrant_name": "Van Scoyoc Kelly", 
      "count": 39, 
      "registrant_entity": "69509241c4cc458f8473356144a65e3f"},
     ...]


Clients
-------

Return the clients on whose behalf the lobbying was done.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/161d40ee83574de29095686c93b1bf74/clients.json?apikey=<your-key>``

::

    [{"count": 34, 
      "client_name": "Computer Sciences Corp", 
      "client_entity": "7c291abf9d574ed7b474f122a0750c61"},
     {"count": 30, 
      "client_name": "American Library Assn", 
      "client_entity": "fb6a9ea4870541c6a69772de4cad89ba"},
     {"count": 30, 
      "client_name": "Federation of State Humanities Council", 
      "client_entity": null},
     ...]


Issues Lobbied
--------------

Return the top issues on which this lobbyist worked.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/161d40ee83574de29095686c93b1bf74/issues.json?apikey=<your-key>``

::

    [{"count": 5146, 
      "issue": "Fed Budget & Appropriations"},
     {"count": 1545, 
      "issue": "Defense"},
     {"count": 1302, 
      "issue": "Education"},
     ...]

