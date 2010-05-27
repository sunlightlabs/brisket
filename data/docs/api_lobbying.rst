==========
 Lobbying 
==========

End Point
=========

**Lobbying data is not available in CSV since its nested structure does not lend itself to the format.**

JSON response format::

    http://transparencydata.com/api/1.0/lobbying.json

Excel response format::

    http://transparencydata.com/api/1.0/lobbying.xls

Parameters
==========

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