=======================
 Transparency Data API
=======================

Contributions
=============

End Point
---------

JSON response format::

    http://transparencydata.com/api/1.0/contributions.json

CSV response format::

    http://transparencydata.com/api/1.0/contributions.csv

Authentication
--------------

An API key is required to access the Transparency Data API. `Registration is easy <http://services.sunlightlabs.com/accounts/register/>`_ and if you already have a `Sunlight Data Services <http://services.sunlightlabs.com/accounts/register/>`_ key you can use it here.

The API key *must* be as either an ``apikey`` query string parameter or as a ``X-APIKEY`` HTTP request parameter. Example::

    http://transparencydata.com/api/1.0/contributions.csv?apikey=<key>&...

Parameters
----------------

Meta
....

apikey
    Required if the ``X-APIKEY`` HTTP header is not used.

page
    The page of results to return; defaults to 1.

per_page
    The number of results to return per page, defaults to 1,000. The maximum number of records per page is 100,000.

Querying
........

amount
    The amount of the contribution in US dollars in one of the following formats:
    
    =======  ============================
    Example  Description
    =======  ============================
    500      exactly 500 dollars
    \>\|500  greater than or equal to 500
    \<\|500  less than or equal to 500
    =======  ============================

contributor_ft
    Full-text search on name of individual, PAC, organization, or employer.

contributor_state
    Two-letter abbreviation of state from which the contribution was made.

cycle
    A YYYY formatted year, 1990 - 2010.
    
    =========  ==================
    Example    Description
    =========  ==================
    2006       the 2006 cycle
    2006|2008  2006 OR 2008 cycle
    =========  ==================

date
    date of the contribution in ISO date format
    
    ===========================  =============================================
    Example                      Description
    ===========================  =============================================
    2006-08-06                   exactly on August 6, 2006
    >\<\|2006-08-06\|2006-09-12  between August 6, 2006 and September 12, 2006
    ===========================  =============================================

employer_ft
    full-text search on name of an individual's employer

recipient_ft
    full-text search on name of PAC or candidate receiving the contribution

recipient_state
    two-letter abbreviation of state in which the candidate receiving the contribution is running

seat
    type of office being sought

    ==================  ==================================
    Options             Description
    ==================  ==================================
    federal:senate      US Senate
    federal:house       US House of Representatives
    federal:president   US President
    state:upper         upper chamber of state legislature
    state:lower         lower chamber of state legislature
    state:governor      state governor
    ==================  ==================================
    
    Multiple values must be separated by a pipe character.
    
    ============================  =====================
    Example                       Description
    ============================  =====================
    federal:senate                only the US Senate
    federal:senate|federal:house  US Senate OR US House
    ============================  =====================


transaction_namespace
    filters on federal or state contributions

    =========================  =====================
    Options                    Description
    =========================  =====================
    ``urn:fec:transaction``    federal contributions
    ``urn:nimsp:transaction``  state contributions
    =========================  =====================
    