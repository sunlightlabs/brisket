===========================
Contribution Aggregates API
===========================

License
=======

Data returned by this service is subject to the use restrictions set by the Federal Election Commission. By accessing this data, you understand that you are using the data subject to all applicable local, state and federal law, including FEC restrictions.

All data licensed under the Creative Commons BY-NC-SA license. By downloading data and accessing the API you are agreeing to the terms of the license.

Federal campaign contribution and lobbying records must be attributed to OpenSecrets.org.

State campaign contribution records must be attributed to FollowTheMoney.org.

Authentication
==============

An API key is required to access the Transparency Data API. `Registration is easy <http://services.sunlightlabs.com/accounts/register/>`_ and if you already have a `Sunlight Data Services <http://services.sunlightlabs.com/accounts/register/>`_ key you can use it here.

The API key *must* be as either an ``apikey`` query string parameter or as a ``X-APIKEY`` HTTP request parameter. Example::

    http://transparencydata.com/api/1.0/contributions.csv?apikey=<key>&...

Common Parameters
=================

apikey
    Required if the ``X-APIKEY`` HTTP header is not used.

cycle
    Applicable to all methods that return data for a particular entity. Restricts the data to that two-year election cycle. Use only even four-digit integers. If no cycle is given then data return is an aggregate over all years for which there is data.
    
limit
    Applicable to all methods that return a 'Top N' list. Determines the maximum number of results returned. Default is 10.
    
Search Methods
==============

Search by Name
--------------

Search for entities--that is, politicians, individuals, or organizations--with the given name. Returns basic information about the the contributions to and from each entity, as well as an ID that can be used in other API methods to retrieve more information.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/entities.json


Parameters
~~~~~~~~~~

search
    The query string. Spaces should be URL-encoded or represented as ``+``. There are no logic operators or grouping.


Example
~~~~~~~

http://transparencydata.com/api/1.0/entities.json?apikey=<your-key>&search=nancy+pelosi

::

    [{"name": "Nancy Pelosi for Congress", 
      "type": "organization", 
      "total_received": "0", 
      "count_received": 0, 
      "total_given": "8625826.00", 
      "count_given": 1319, 
      "id": "8b2fed0a4a7e47e98147cdc2b335e614"},
     {"name": "Nancy Pelosi (D)", 
      "type": "politician", 
      "total_received": "11749535.00", 
      "count_received": 9320, 
      "total_given": "0", 
      "count_given": 0, 
      "id": "ff96aa62d48f48e5a1e284efe74a0ba8"}]

ID Lookup
---------

Look up the entity ID based on an ID from a different data set. Currently we provide a mapping from the ID schemes used by Center for Reponsive Politics (CRP) and the National Institute for Money in State Politics (NIMSP). The result is a JSON object listing the TransparencyData IDs matching the given external ID.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/entities/id_lookup.json

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
    ``urn:nimsp:recipient``    A NIMSP ID for a politician. Integer-valued.
    ========================== ===============================================================================

    More namespaces may be added in the future as other ID schemes are reconciled with the TransparencyData dataset.
    
id
    The ID of the entity in the given namespace.
    
Example
~~~~~~~

http://transparencydata.com/api/1.0/entities/id_lookup.json?apikey=<your-key>&namespace=urn:crp:recipient&id=N00007360

::

    [{"id": "ff96aa62d48f48e5a1e284efe74a0ba8"}]


Entity Overview
---------------

Returns general information about a particular entity.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/entities/<entity ID>.json

Parameters
~~~~~~~~~~

cycle
    Return contribution totals for the given cycle. When not given, returns totals for all cycles.
    
Example
~~~~~~~

http://transparencydata.com/api/1.0/entities/ff96aa62d48f48e5a1e284efe74a0ba8.json?apikey=<your-key>

::

    {"external_ids": [{"namespace": "urn:crp:recipient", "id": "N00007360"}], 
     "contributions": {"contributor_amount": "0", 
                       "contributor_count": 0, 
                       "recipient_amount": "11749535.00", 
                       "recipient_count": 9320}, 
     "name": "Nancy Pelosi (D)", 
     "id": "ff96aa62d48f48e5a1e284efe74a0ba8"}



Politician Methods
==================

These methods all return information about a particular politician, specified by entity ID.

Top Contributors
----------------

Returns the top contributoring organizations, ranked by total dollars given. An organization's giving is broken down into money given directly (by the organization's PAC) versus money given by individuals employed by or associated with the organization.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors.json

Example
~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/ff96aa62d48f48e5a1e284efe74a0ba8/contributors.json?apikey=<you-key>&limit=3

::

    [{"employee_amount": "54800.00", 
      "total_amount": "87100.00", 
      "total_count": 74, 
      "name": "Akin, Gump et al", 
      "direct_count": 16, 
      "employee_count": 58, 
      "id": "2c6f93b70b1d4e5eaa942ab9c83a21c0", 
      "direct_amount": "32300.00"},
     {"employee_amount": "3500.00", 
      "total_amount": "86000.00", 
      "total_count": 29, 
      "name": "American Fedn of St/Cnty/Munic Employees", 
      "direct_count": 25, 
      "employee_count": 4, 
      "id": "dbc095a6bc9343f5a9867352a1a00dae", 
      "direct_amount": "82500.00"},
     {"employee_amount": "0", 
      "total_amount": "82000.00", 
      "total_count": 31, 
      "name": "United Auto Workers", 
      "direct_count": 31, 
      "employee_count": 0, 
      "id": "1108378c9e4344cb9f86473b4d5621f1", 
      "direct_amount": "82000.00"}]

Top Sectors
-----------

Returns what each sector gave to the politician.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/sectors.json

The sectors are identified by a single-letter code, as coded by CRP. The sector codes are:

    ===== =============================
    Code  Description
    ===== =============================
    ``A`` Agribusiness
    ``B`` Communications/Electronics
    ``C`` Construction
    ``D`` Defense
    ``E`` Energy/Natural Resources
    ``F`` Finance/Insurance/Real Estate
    ``H`` Health
    ``K`` Lowyers and Lobbyists
    ``M`` Transportation
    ``N`` Misc. Business
    ``Q`` Ideology/Single Issue
    ``P`` Labor
    ``W`` Other
    ``Y`` Unknown
    ``Z`` Adminstrative Use
    ===== =============================

Example
~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/ff96aa62d48f48e5a1e284efe74a0ba8/contributors/sectors.json?apikey=<your-key>

::

    [{"sector": "F", "count": 1665, "amount": "2230822.00"},
     {"sector": "P", "count": 971, "amount": "2033800.00"},
     {"sector": "Q", "count": 1108, "amount": "1198013.00"},
     {"sector": "K", "count": 1207, "amount": "1161794.00"},
     {"sector": "H", "count": 692, "amount": "1058000.00"},
     {"sector": "N", "count": 761, "amount": "959437.00"},
     {"sector": "B", "count": 446, "amount": "685969.00"},
     {"sector": "Y", "count": 794, "amount": "587916.00"},
     {"sector": "W", "count": 546, "amount": "525825.00"},
     {"sector": "E", "count": 186, "amount": "237600.00"}]

Top Industries within Sector
----------------------------

Returns the top contributing industries within a particular sector. Industries are identified by the three character category code assigned by CRP or NIMSP. See http://assets.transparencydata.org.s3.amazonaws.com/docs/catcodes-20100402.csv.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/sector/<sector>/industries.json

Example
~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/ff96aa62d48f48e5a1e284efe74a0ba8/contributors/sector/F/industries.json?apikey=<your-key>&limit=3

::

    [{"count": 387, "industry": "F07", "amount": "590200.00"},
     {"count": 432, "industry": "F10", "amount": "553222.00"},
     {"count": 238, "industry": "F09", "amount": "323500.00"}]

Local Breakdown
---------------

Return a breakdown of how much of the money raised was from contributors in the politician's state versus outside the politician's state.

End Point
~~~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/local_breakdown.json

Example
~~~~~~~

http://transparencydata.com/api/1.0/aggregates/pol/ff96aa62d48f48e5a1e284efe74a0ba8/contributors/local_breakdown.json?apikey=<your-key>&limit=3

::

    {"in-state": [3852, "3672843.00"], "out-of-state": [5048, "7712269.00"]}

Organization Methods
====================


Individual Methods
==================