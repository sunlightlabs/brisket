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
    ``urn:nimsp:recipient``    A NIMSP ID for a politician. Integer-valued.
    ========================== ===============================================================================

    More namespaces may be added in the future as other ID schemes are reconciled with the TransparencyData dataset.
    
id
    The ID of the entity in the given namespace.
    
Example
~~~~~~~

``http://transparencydata.com/api/1.0/entities/id_lookup.json?apikey=<your-key>&namespace=urn:crp:recipient&id=N00007360``

::

    [{"id": "ff96aa62d48f48e5a1e284efe74a0ba8"}]


Entity Overview
---------------

Return general information about a particular entity.

End Point
~~~~~~~~~

``http://transparencydata.com/api/1.0/entities/<entity ID>.json``

Parameters
~~~~~~~~~~

cycle
    Return contribution totals for the given cycle. When not given, returns totals for all cycles.
    
Example
~~~~~~~

``http://transparencydata.com/api/1.0/entities/ff96aa62d48f48e5a1e284efe74a0ba8.json?apikey=<your-key>``

::

    {"external_ids": [{"namespace": "urn:crp:recipient", "id": "N00007360"}], 
     "contributions": {"contributor_amount": "0", 
                       "contributor_count": 0, 
                       "recipient_amount": "11749535.00", 
                       "recipient_count": 9320}, 
     "name": "Nancy Pelosi (D)", 
     "id": "ff96aa62d48f48e5a1e284efe74a0ba8"}
