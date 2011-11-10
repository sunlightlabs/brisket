===========================
Contribution Aggregates API
===========================


Politician Methods
==================

These methods return information about a particular politician, specified by entity ID.

Top Contributors
----------------

Return the top contributing organizations, ranked by total dollars given. An organization's giving is broken down into money given directly (by the organization's PAC) versus money given by individuals employed by or associated with the organization.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/f990d08287c34c389cfabe3cbf3dde99/contributors.json?apikey=<your-key>``

::

    [{"employee_amount": "42925.00", 
      "total_amount": "114500.00", 
      "total_count": "67", 
      "name": "AK Steel", 
      "direct_count": "26", 
      "employee_count": "41", 
      "id": "a8853010eeca4e27b495d3eabf001b2a", 
      "direct_amount": "71575.00"},
     {"employee_amount": "1500.00", 
     "total_amount": "88850.00", 
     "total_count": "48", 
     "name": "National Assn of Realtors", 
     "direct_count": "45", 
     "employee_count": "3", 
     "id": "bb98402bd4d3471cad392a671ecd733a", 
     "direct_amount": "87350.00"},
    {"employee_amount": "4000.00", 
     "total_amount": "86700.00", 
     "total_count": "43", 
     "name": "United Parcel Service", 
     "direct_count": "39", 
     "employee_count": "4", 
     "id": "c2daded88a9f4cc78cd513b0bf4c43fc", 
     "direct_amount": "82700.00"},
    ...]
    
Top Sectors
-----------

Return what each sector gave to the politician.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/sectors.json``

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
    ``K`` Lawyers and Lobbyists
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

``http://transparencydata.com/api/1.0/aggregates/pol/f990d08287c34c389cfabe3cbf3dde99/contributors/sectors.json?apikey=<your-key>``

::

    [{"sector": "F", "count": "3124", "amount": "3790515.00"},
     {"sector": "N", "count": "2210", "amount": "2434479.00"},
     {"sector": "H", "count": "1075", "amount": "1548447.00"},
     {"sector": "A", "count": "1497", "amount": "1431438.00"},
     {"sector": "Y", "count": "2302", "amount": "1367578.00"},
     {"sector": "E", "count": "775", "amount": "991898.00"},
     {"sector": "B", "count": "654", "amount": "829613.00"},
     {"sector": "M", "count": "588", "amount": "812732.00"},
     {"sector": "W", "count": "1401", "amount": "797909.00"},
     {"sector": "K", "count": "961", "amount": "780381.00"}]


Top Industries
--------------

Return the top industries contributing to the politician. Industries are a more fine-grained breakdown than sectors. For a definition of industries see `here <http://assets.transparencydata.org.s3.amazonaws.com/docs/catcodes.csv>`_.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/industries.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/f990d08287c34c389cfabe3cbf3dde99/contributors/industries.json?apikey=<your-key>``

::

    [{"count": "1889", 
     "amount": "1143143.00", 
     "id": "0171a70d50e8471d94c6e7083ca154c8", 
     "should_show_entity": false, 
     "name": "EMPLOYER LISTED/CATEGORY UNKNOWN"},
    {"count": "939", 
     "amount": "1047096.00", 
     "id": "8ada0fc2d6994f2ab06c7e025dff2284", 
     "should_show_entity": true, "name": "INSURANCE"},
    {"count": "563", 
     "amount": "802886.00", 
     "id": "0af3f418f426497e8bbf916bfc074ebc", 
     "should_show_entity": true, 
     "name": "SECURITIES & INVESTMENT"},
     ...]


Local Breakdown
---------------

Return a breakdown of how much of the money raised was from contributors in the politician's state versus outside the politician's state.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/local_breakdown.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/f990d08287c34c389cfabe3cbf3dde99/contributors/local_breakdown.json?apikey=<your-key>``

::

    {"in-state": ["7119", "4669953.00"], "out-of-state": ["2431", "1885000.00"]}


Contributor Type Breakdown
--------------------------

Return a breakdown of how much of the money raised was came from individuals versus organizations (PACs).

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/<entity ID>/contributors/type_breakdown.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/pol/f990d08287c34c389cfabe3cbf3dde99/contributors/type_breakdown.json?apikey=<your-key>``

::

    {"Individuals": ["9550", "6554953.00"], "PACs": ["6620", "9991604.00"]}
    
  

Individual Methods
==================  

These methods return information about a particular individual, specified by entity ID.


Top Recipient Organizations
---------------------------

Return the top organizations to which this individual has given money.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/<entity ID>/recipient_orgs.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/f2405f007737426cb793c9b4bea091ce/recipient_orgs.json?apikey=<your-key>``

::

    [{"count": "2", 
      "recipient_entity": null, 
      "amount": "300000.00", 
      "recipient_name": "NO ON PROP. 1D  AND 1E"},
     {"count": "15", 
      "recipient_entity": "e497407d2e834cd48e126093ed0416e5", 
      "amount": "119300.00", 
      "recipient_name": "DNC Services Corp"},
     {"count": "15", 
      "recipient_entity": null, 
      "amount": "77750.00", 
      "recipient_name": "Democratic Senatorial Campaign Cmte"},
      ...]
    

Top Recipient Politicians
-------------------------

Return the top politicians to which this individual has given money.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/<entity ID>/recipient_pols.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/f2405f007737426cb793c9b4bea091ce/recipient_pols.json?apikey=<your-key>``

::

    [{"count": "2", 
      "state": "CA", 
      "recipient_name": "BROWN, JERRY", 
      "amount": "50000.00", 
      "recipient_entity": "9e2fefcd6d094276a82eef1845059e7e", 
      "party": "D"},
     {"count": "2", 
      "state": "CA", 
      "recipient_name": "DAVIS, GRAY", 
      "amount": "15000.00", 
      "recipient_entity": "4816628601604c35b2ab1638c2b11c1b", 
      "party": "D"},
     {"count": "5", 
      "state": "NY", 
      "recipient_name": "CUOMO, ANDREW", 
      "amount": "13978.00", 
      "recipient_entity": "d83c5450d5604928ad35103ae2588e6f", 
      "party": "D"},
      ...]
    

Party Breakdown
---------------

Return how much this individual gave to each party.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/<entity ID>/recipients/party_breakdown.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/indiv/f2405f007737426cb793c9b4bea091ce/recipients/party_breakdown.json?apikey=<your-key>``
::

    {"Republicans": ["1", "500.00"], "Other": ["7", "330540.00"], "Democrats": ["293", "787193.00"]}


Organization Methods
====================

These methods return information about an organization's giving. "Organization" is an intentionally vague designation covering corportations, PACs, unions, trade groups, and other groups.

Top Recipients
--------------

Return the top recipients of money from this organization.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/<entity ID>/recipients.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/4ef624f6877a49f2b591b2a8af4c5bf5/recipients.json?apikey=<your-key>&limit=3``

::

    [{"employee_amount": "57658.00", 
      "total_amount": "57658.00", 
      "total_count": 57, 
      "name": "Barack Obama (D)", 
      "direct_count": 0, 
      "employee_count": 57, 
      "id": "4cc67d4c54214b858a4b72d97b3905ea", 
      "direct_amount": "0"},
     {"employee_amount": "21400.00", 
      "total_amount": "21400.00", 
      "total_count": 24, 
      "name": "Hillary Clinton (D)", 
      "direct_count": 0, 
      "employee_count": 24, 
      "id": "48253d1b86f446c8b584f9d6a31450c1", 
      "direct_amount": "0"},
     {"employee_amount": "17500.00", 
      "total_amount": "17500.00", 
      "total_count": 7, 
      "name": "Harold E Ford Jr (D)", 
      "direct_count": 0, 
      "employee_count": 7, 
      "id": "3b3c79d8f4264fd19999409bd97bd161", 
      "direct_amount": "0"}]
      
Party Breakdown
---------------

Return the portion of giving that went to each party.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/<entity ID>/recipients/party_breakdown.json``     
      
Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/4ef624f6877a49f2b591b2a8af4c5bf5/recipients/party_breakdown.json?apikey=<your-key>``

::

    {"3": [1, "500.00"], "Republicans": [3, "1500.00"], "Democrats": [463, "391247.00"]}
    
    
State/Federal Breakdown
-----------------------

Return the portion of giving that went to state versus federal candidates.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/<entity ID>/recipients/level_breakdown.json``

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/73c18c499c1b4a71b2b042663530e9b7/recipients/level_breakdown.json?apikey=<your-key>``

::

    {"Federal": [3789, "4832720.00"], "State": [154, "74659.96"]}



