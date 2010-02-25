=======================
 Transparency Data API
=======================

----------------
 Authentication
----------------

An API key is required to access the Transparency Data API.
<a href="http://services.sunlightlabs.com/accounts/register/">Registration is easy</a> and if you already have a <a href="http://services.sunlightlabs.com/accounts/register/">Sunlight Data Services</a> key you can use it here.


cycle
    a YYYY formatted year, 1990 - 2010. supports multiple pipe-separated values: 2006|2008

    2006
        only the 2006 cycle
    
    2006|2008
        2006 or 2008 cycle


contributor_ft
    full-text search on name of individual, PAC, organization, or employer


contributor_state
    two-letter abbreviation of state from which the contribution was made


recipient_ft
    full-text search on name of PAC or candidate receiving the contribution


recipient_state
    two-letter abbreviation of state in which the candidate receiving the contribution is running


seat
	type of office being sought
	
	- federal:senate
	- federal:house
	- federal:president
	- state:upper
	- state:lower
	- state:governor

amount
    the amount of the contribution in US dollars in one of the following formats
    
    500
        exactly 500 dollars
	>|500
	    greater than or equal to 500
    <|500
        less than or equal to 500