=======================
 Transparency Data API
=======================

----------------
 Authentication
----------------

An API key is required to access the Transparency Data API.
<a href="http://services.sunlightlabs.com/accounts/register/">Registration is easy</a> and if you already have a <a href="http://services.sunlightlabs.com/accounts/register/">Sunlight Data Services</a> key you can use it here.

amount
    the amount of the contribution in US dollars in one of the following formats
    
    =======  ============================
    Example  Description
    =======  ============================
    500      exactly 500 dollars
    \>\|500  greater than or equal to 500
    \<\|500  less than or equal to 500
    =======  ============================

contributor_ft
    full-text search on name of individual, PAC, organization, or employer

contributor_state
    two-letter abbreviation of state from which the contribution was made

cycle
    a YYYY formatted year, 1990 - 2010
    
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
    