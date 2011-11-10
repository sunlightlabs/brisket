===================
 Federal Contracts 
===================

End Point
=========

JSON response format::

	http://transparencydata.com/api/1.0/contracts.json

CSV response format::

	http://transparencydata.com/api/1.0/contracts.csv

Excel response format::

	http://transparencydata.com/api/1.0/contracts.xls

Parameters
==========

agency_id
	The FIPS code for the agency.
	
agency_name
	Full-text search on the name of the agency.

contracting_agency_id
	The FIPS code for the contracting agency.

contracting_agency_name
	Full-text search on the name of the contracting agency.
	
current_amount
	Current value of the contract in US dollars in one of the following formats:
	
	=======	 ============================
	Example	 Description
	=======	 ============================
	500		 exactly 500 dollars
	\>\|500	 greater than or equal to 500
	\<\|500	 less than or equal to 500
	=======	 ============================

fiscal_year
	The year in which the grant was awarded. A YYYY formatted year, 2006 - 2010.
	
	=========  ============
	Example	   Description
	=========  ============
	2006	   2006
	2006|2008  2006 OR 2008
	=========  ============

maximum_amount
 	Maximum possible value of the contract in US dollars in one of the following formats:

	=======	 ============================
	Example	 Description
	=======	 ============================
	500		 exactly 500 dollars
	\>\|500	 greater than or equal to 500
	\<\|500	 less than or equal to 500
	=======	 ============================

place_district
	The congressional district in which the contract action will be performed.

place_state_code
	FIPS code for state in which the contract action will be performed.

requesting_agency_id
	The FIPS code for the requesting agency.

requesting_agency_name
	Full-text search on the name of the contracting agency.

obligated_amount
	The amount obligated or de-obligated by the transaction in US dollars in one of the following formats:

	=======	 ============================
	Example	 Description
	=======	 ============================
	500		 exactly 500 dollars
	\>\|500	 greater than or equal to 500
	\<\|500	 less than or equal to 500
	=======	 ============================

vendor_city
	Full-text search on the name of the primary city in which the contractor does business.

vendor_district
	The primary congressional district in which the contractor does business.

vendor_duns
	The Dun and Bradstreet number assigned to the contractor.

vendor_name
	Full-text search on the name of the contractor.

vendor_parent_duns
	The Dun and Bradstreet number assigned to the corporate parent of the contractor.

vendor_state
	The primary state in which the contractor does business.

vendor_zipcode
	The primary zipcode in which the contractor does business.
	