==============================
 Federal Lobbying Data Schema 
==============================

Lobbying
========

transaction_id
	The registration ID assigned by the Senate Office of Public Records.

transaction_type
	The type of filing as reported by the Senate Office of Public Records.
	http://assets.transparencydata.org.s3.amazonaws.com/docs/transaction_types-20100402.csv

transaction_type_desc
	Readable description of the transaction_type.

year
	The year in which the registration was filed. Valid years are 1998-2009.
	
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

amount
    The amount spent on lobbying in US dollars.

registrant_name
	Name of the person or organization filing the lobbyist registration. This is typically the firm that employs the lobbyists. Use the registrant_is_firm field to filter on firms v. individuals.
	
registrant_is_firm
	``true`` if registrant is a lobbying firm.

client_name
	Name of the client for which the lobbyist is working.

client_category
	The five character industry category code of the client assigned by CRP.
	http://assets.transparencydata.org.s3.amazonaws.com/docs/catcodes-20100402.csv
	
client_ext_id
	CRP ID of the client if one exists.

client_parent_name
	Name of the parent organization of the client.

Lobbyists
=========

lobbyists.lobbyist_name
	Name of the lobbyist involved in the lobbying activity.

lobbyists.lobbyist_ext_id
	Lobbyist ID assigned by CRP.

lobbyists.candidate_ext_id
	Candidate ID, if the lobbyist was ever a candidate, assigned by CRP.

lobbyists.government_position
	Position in the federal government if the lobbyist even held one.

lobbyists.member_of_congress
	``true`` if the lobbyist was ever a member of Congress.

Issues
======

issues.year
	The year in which the registration was filed. Valid years are 1998-2009.

issues.general_issue_code
	The code that represents the issue on which the lobbying was conducted.
	
issues.general_issue
	The name of the issue on which the lobbying was conducted.
	
issues.specific_issue
	A description of the specific lobbying.

Agencies
========

agencies.agency_name
	The name of the federal agency that was lobbied.

agencies.agency_ext_id
	The CRP ID of the agency that was lobbied.