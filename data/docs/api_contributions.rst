========================
 Campaign Contributions 
========================

End Point
=========

JSON response format::

    http://transparencydata.com/api/1.0/contributions.json

CSV response format::

    http://transparencydata.com/api/1.0/contributions.csv

Excel response format::

    http://transparencydata.com/api/1.0/contributions.xls

Parameters
==========

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
    *DEPRECATED* please use organization_ft

for_against
    When organizations run ads against a candidate, they are counted as independent expenditures with the candidate as the recipient. This parameter can be used to filter contributions meant for the candidate and those meant to be against the candidate.

    =======  ==============================================
    Options  Description
    =======  ==============================================
    for      contributions made in support of the candidate
    against  contributions made against the candidate
    =======  ==============================================

organization_ft
	full-text search on employer, organization, and parent organization

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
========

Contributions from the states of Maryland and Virginia to Barbara Mikulski during the 2008 campaign cycle as JSON::

    /api/1.0/contributions.json?apikey=<key>&contributor_state=md|va&recipient_ft=mikulski&cycle=2008

Contributions from Alaskans to upper and lower state legislature candidates in 2002 as CSV::

    /api/1.0/contributions.csv?apikey=<key>&contributor_state=ak&date=><|2002-01-01|2002-12-31&seat=state:upper|state:lower

