=======================
 Transparency Data API
=======================	

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

These parameters are common to all API methods.

apikey
    Required if the ``X-APIKEY`` HTTP header is not used.

page
    The page of results to return; defaults to 1.

per_page
    The number of results to return per page, defaults to 1,000. The maximum number of records per page is 100,000.

Contributions
=============

End Point
---------

JSON response format::

    http://transparencydata.com/api/1.0/contributions.json

CSV response format::

    http://transparencydata.com/api/1.0/contributions.csv

Parameters
----------

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

for_against
    When organizations run ads against a candidate, they are counted as independent expenditures with the candidate as the recipient. This parameter can be used to filter contributions meant for the candidate and those meant to be against the candidate.

    =======  ==============================================
    Options  Description
    =======  ==============================================
    for      contributions made in support of the candidate
    against  contributions made against the candidate
    =======  ==============================================

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

Examples
--------

Contributions from the states of Maryland and Virginia to Barbara Mikulski during the 2008 campaign cycle as JSON::

    /api/1.0/contributions.json?apikey=<key>&contributor_state=md|va&recipient_ft=mikulski&cycle=2008

Contributions from Alaskans to upper and lower state legislature candidates in 2002 as CSV::

    /api/1.0/contributions.csv?apikey=<key>&contributor_state=ak&date=><|2002-01-01|2002-12-31&seat=state:upper|state:lower


Lobbying
========

End Point
---------

Lobbying data is available only in JSON format since its nested structure does not lend itself to CSV. JSON response format::

    http://transparencydata.com/api/1.0/lobbying.json

Parameters
----------

amount
    The amount spent on lobbying in US dollars in one of the following formats:
    
    =======  ============================
    Example  Description
    =======  ============================
    500      exactly 500 dollars
    \>\|500  greater than or equal to 500
    \<\|500  less than or equal to 500
    =======  ============================

client_ft
    Full-text search on the name of the client for which the lobbyist is working.

client_parent_ft
	Full-text search on the name of the parent organization of the client.

filing_type
	Type of filing as identified by CRP. CRP recommends the following rules be used:
	
	* Do not total e records unless they are larger than the associated s record.
	* Count c records in both total and industry when filing_included_nsfs is ``n``. Don't count it in total or industry when filing_included_nsfs is ``y``.
	* Count b records in both total and industry when filing_included_nsfs is ``n``. Exclude from total and include in industry but subtract it from the total of the parent when filing_included_nsfs ``y``.
	
	==== =============================================================================
	Code Meaning
	==== =============================================================================
	n    non self filer parent
	m    non self filer subsidiary for a non self filer parent
	x    self filer subsidiary for a non self filer parent
	p    self filer parent
	i    non self filer for a self filer parent that has same catorder as the parent
	s    self filer subsidiary for a self filer parent
	e    non self filer subsidiary for a self file subsidiary
	c    non self filer subsidiary for a self filer parent with same catorder
	b    non self filer subsidiary for a self filer parent that has different catorder
	==== =============================================================================
	

lobbyist_ft
	Full-text search on the name of the lobbyist involved in the lobbying activity.

registrant_ft
	Full-text search on the name of the person or organization filing the lobbyist registration. This is typically the firm that employs the lobbyists. Use the registrant_is_firm field to filter on firms v. individuals.

transaction_id
	Report ID given by the Senate Office of Public Records.

transaction_type
	The type of filing as reported by the Senate Office of Public Records.
	http://assets.transparencydata.org.s3.amazonaws.com/docs/transaction_types-20100402.csv

year
	The year in which the registration was filed. A YYYY formatted year, 1998 - 2010.
    
    =========  ============
    Example    Description
    =========  ============
    2006       2006
    2006|2008  2006 OR 2008
    =========  ============