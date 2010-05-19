

Lobbying Aggregates
===================

The following terms are used in the lobbying aggregates API:

registrant
	A lobbying firm. Referred to as 'registrants' in the lobbying data because they are responsible for registering the lobbying activity with the House or Senate.
	
client
	A company or other organization that hires a registrant to lobby for it. An organization may also lobby for itself directly, in which case it will appear as a registrant and a client.
	
lobbyist
	An individual employee of a registrant, lobbying on behalf of a client.

A note about counts and top lists: registrants are required for each client to submit a total amount spent, a list of issues and agencies lobbied, and the individual lobbyists involved. The structure of the data does not allow us to assign a dollar amount to particular issues or lobbyists. Thus the top issues and top lobbyists calls rank issues and lobbyists based on the number of times that issue or lobbyist is listed on a disclosure form. These rankings are not particularly meaningful; they are included only as a means of obtaining a list of issues and lobbyists that are probably important to that registrant or client.



Registrant Methods
==================


Top Clients
-----------

Return the top client that hired this firm.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/<entity ID>/registrant/clients.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/1900f08eabfe4d708387a2625ba5506d/registrant/clients.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"count": 4, "client_name": "Intellectual Ventures LLC", "client_entity": "e316f513e8b54c109650c1a80bb9d7e3", "amount": "360000.00"},
	 {"count": 4, "client_name": "Anadarko Petroleum", "client_entity": "54c37116b52f438c933251f7862c808f", "amount": "300000.00"},
	 {"count": 4, "client_name": "General Electric", "client_entity": "54b1d18817674af69455c1662ad47907", "amount": "300000.00"}]
	
	
Top Lobbyists
~~~~~~~~~~~~~

Return the top lobbyists employeed by this lobbying firm, ranked by the number of times the lobbyist appears on a disclosure form.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/<entity ID>/registrant/lobbyists.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/1900f08eabfe4d708387a2625ba5506d/registrant/lobbyists.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"count": 62, "lobbyist_name": "Marshall, Hazen", "lobbyist_entity": "29dd30d38f8947a0998fdef9513fe21d"},
	 {"count": 57, "lobbyist_name": "Nickles, Don", "lobbyist_entity": "94343e226e884b1ea80a6b8feae86d7e"},
	 {"count": 51, "lobbyist_name": "Hughes, Stacey", "lobbyist_entity": "c6267282c6c44c02a2c3177269357ed4"}]
	

Top Issues
~~~~~~~~~~

Return the top issues lobbyied on by the firm, rankd by the number of times the issue appears on a disclosure form.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/<entity ID>/registrant/issues.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/1900f08eabfe4d708387a2625ba5506d/registrant/issues.json?apikey=<your-key>&cycle=2010&limit=3``

::
	
	[{"count": 49, "issue": "Taxes"},
	 {"count": 41, "issue": "Fed Budget & Appropriations"},
	 {"count": 39, "issue": "Health Issues"}]
	

Organization Methods
====================

Top Registrants
---------------

Return the top lobbying firms hired by this client, ranked by dollars spent. The organization itself may appear on this list if it lobbied directly.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/<entity ID>/registrants.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/9a5132373c2c49609842661825992527/registrants.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"registrant_name": "American Bankers Assn", "count": 4, "amount": "8370000.00", "registrant_entity": "9a5132373c2c49609842661825992527"},
	 {"registrant_name": "New York Bankers Assn", "count": 4, "amount": "590000.00", "registrant_entity": "8eb41edaf53f404b93640dd5398fb279"},
	 {"registrant_name": "Glover Park Group", "count": 4, "amount": "320000.00", "registrant_entity": "828c55c3662f49d5943a1a5a1257f133"}]
	

Top Lobbyists
-------------

Return the top lobbyists working for this client organization, ranked by the number of times the lobbyist appears on a disclosure form.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/<entity ID>/lobbyists.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/9a5132373c2c49609842661825992527/lobbyists.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"count": 8, "lobbyist_name": "Clayton, Kenneth", "lobbyist_entity": "027c33848bec4c34935fd9d2bdf35d32"},
	 {"count": 8, "lobbyist_name": "Callaghan, Dawn", "lobbyist_entity": "ecc17aeb8fdd4f18b8c85279c5cbeff7"},
	 {"count": 8, "lobbyist_name": "Lowenthal, Andrew", "lobbyist_entity": "9892fa5d165a4ae8a4a24e265ac00802"}]
	
	
Top Issues
----------

Return the top issues, ranked by the number of times the issue appears on a disclosure form.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/<entity ID>/issues.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/org/9a5132373c2c49609842661825992527/issues.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"count": 30, "issue": "Banking"},
	 {"count": 13, "issue": "Finance"},
	 {"count": 10, "issue": "Taxes"}]
	
	
Individual Lobbyist Methods
===========================

Top Registrants 
---------------

Return the top lobbying firms for which this lobbyist worked, ranked by the number of times the lobbyist appears on disclosure forms.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/indiv/<entity ID>/registrants.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/indiv/dbd759e1814c40c58b16df2a4af1d6dc/registrants.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"registrant_name": "Van Scoyoc Assoc", "count": 1081, "registrant_entity": "643ed098473e4358a6b0ed051429f733"},
	 {"registrant_name": "Capitol Decisions", "count": 93, "registrant_entity": "fc99e8139a8a4990bc46eb424392117a"}]
	
Top Clients
-----------

Return the top clients for whom this lobbyist lobbied, ranked by the number of times the lobbyist appears on disclosure forms.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/indiv/<entity ID>/clients.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/indiv/dbd759e1814c40c58b16df2a4af1d6dc/clients.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"count": 8, "client_name": "Samuel Roberts Noble Foundation", "client_entity": ""},
	 {"count": 7, "client_name": "Technologies & Devices International", "client_entity": ""},
	 {"count": 6, "client_name": "Univ of Pennsylvania School of Medicine", "client_entity": "d5e15728b2ec40e3ad95fd23114f2425"}]
	
Top Issues
----------

Return the top issues on which this lobbyist lobbyied, ranked by the number of times the lobbyist appears on disclosure forms.

End Point
~~~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/indiv/<entity ID>/issues.json``

Example
~~~~~~~

``http://209.190.229.203:8000/api/1.0/aggregates/indiv/dbd759e1814c40c58b16df2a4af1d6dc/issues.json?apikey=<your-key>&cycle=2010&limit=3``

::

	[{"count": 712, "issue": "Fed Budget & Appropriations"},
	 {"count": 218, "issue": "Defense"},
	 {"count": 140, "issue": "Education"}]
