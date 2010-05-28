================
 Federal Grants 
================

End Point
=========

JSON response format::

	http://transparencydata.com/api/1.0/grants.json

CSV response format::

	http://transparencydata.com/api/1.0/grants.csv

Excel response format::

	http://transparencydata.com/api/1.0/grants.xls

Parameters
==========

agency_ft
	Full-text search on the reported name of the federal agency awarding the grant.

amount_total
	Total amount of the grant in US dollars in one of the following formats:
	
	=======	 ============================
	Example	 Description
	=======	 ============================
	500		 exactly 500 dollars
	\>\|500	 greater than or equal to 500
	\<\|500	 less than or equal to 500
	=======	 ============================

assistance_type
	A general code for the type of grant awarded.
	
	==== ===========================================================================
	Code Meaning
	==== ===========================================================================
	02	 Block grant
	03	 Formula grant
	04	 Project grant
	05	 Cooperative agreement
	06	 Direct payment, as a subsidy or other non-reimbursable direct financial aid
	07	 Direct loan
	08	 Guaranteed/insured loan
	09	 Insurance
	10	 Direct payment with unrestricted use
	11	 Other reimbursable, contingent, intangible or indirect financial assistance
	==== ===========================================================================

fiscal_year
	The year in which the grant was awarded. A YYYY formatted year, 2000 - 2010.
	
	=========  ============
	Example	   Description
	=========  ============
	2006	   2006
	2006|2008  2006 OR 2008
	=========  ============

recipient_ft
	Full-text search on the reported name of the grant recipient.

recipient_state
	Two-letter abbreviation of the state in which the grant was awarded.

recipient_type
	The type of entity that received the grant.
	
	==== =================================================
	Code Meaning
	==== =================================================
	00	 State government
	01	 County government
	02	 City or township government
	04	 Special district government
	05	 Independent school district
	06	 State controlled institution of higher education
	11	 Indian tribe
	12	 Other nonprofit
	20	 Private higher education
	21	 individual
	22	 Profit organization
	23	 Small business
	25	 Other
	==== =================================================

