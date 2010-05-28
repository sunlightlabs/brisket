============================
 Federal Grants Data Schema
============================

fiscal_year
	The fiscal year in which the grant was awarded.

record_type

record_flag

cfda_program_number
	Catalog of Federal Domestic Assistance identifier.

cfda_program_title
	Name of Catalog of Federal Domestic Assistance program under which the grant was awarded.

state_application_id
	A number assigned by state (as opposed to federal) review agencies to the award during the grant application process.

recipient_id

recipient_name
	The reported name of the grant recipient.

recipient_city
	The city of the grant recipient.

recipient_city_code
	The FIPS code of the grant recipient's city.

recipient_county
	The county of the grant recipient.

recipient_county_code
	The FIPS code of the grant recipient's county.

recipient_state
	The state of the grant recipient.

recipient_state_code
	The FIPS code of the grant recipient's state.

recipient_zipcode
	The zipcode of the grant recipient.

recipient_country_code
	The FIPS code of the grant recipient's country.

recipient_district
	The congressional district in which the grant was awarded.

recipient_type
	The recipient type.
	
	==== ================================================
	Code Meaning
	==== ================================================
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
	==== ================================================

recipient_category
	A broad category added by USASpending.gov
	
	==== ================
	Code Meaning
	==== ================
	f	 For Profit
	g	 Government
	h	 Higher Education
	i	 Individual
	n	 Nonprofit
	o	 Other
	==== ================

recipient_address1, recipient_address2, recipient_address3
	The grant recipients street address.

recipient_duns
	The Dun and Bradstreet number of the grant recipient.

recipient_parent_duns
	The Dun and Bradstreet number of the grant recipient's parent organization.

action_date
	The data on which the grant was awarded.

action_type
	The type of action for the record: whether it is a new assistance action, a continuation, a revision, or a funding adjustment.
	
	==== =======================================
	Code Meaning
	==== =======================================
	A	 New assistance action
	B	 Continuation
	C	 Revision
	D	 Funding adjustment to completed project
	==== =======================================
	
agency_name
	The name of the federal agency that awarded the grant.

agency_code
	The code of the federal agency that awarded the grant.

agency_category

award_id

federal_award_id
	An agency-specific unique ID number for each individual assistance award. There may be more than one action record per assistance award, because of continuations, revisions, funding adjustments, corrections, etc.

federal_award_mod
	A modification number used to indicate action records that modify a previous action record with the same federal award ID.
	
amount_federal
	Grant amount from federal funds in US dollars.

amount_nonfederal
	Grant amount from non-federal funds in US dollars.

amount_total
	Total of federal and non-federal grant amount in US dollars.

amount_loan
	The face value of the direct loan or loan guarantee.

amount_subsidy_cost
	The original subsidy cost of the direct loan or loan guarantee.

assistance_type
	The type of assistance provided by the award.

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

assistance_category
	The original Federal Assistance Awards Data System assistance type code, modified by USAspending.gov into a set of broader categories.

	==== =================================
	Code Meaning
	==== =================================
	d	 Direct Payments
	g	 Grants and Cooperative Agreements
	i	 Insurance
	l	 Loans
	o	 Other
	==== =================================

correction
	Indicates that the action record is either a correction of a record from a previous quarter or a late reported record from a previous quarter.
	
place_code
	A code for the principal place of performance for the award. The first two digits are the state FIPS code, the next five the county FIPS (three digits followed by \*\*) or city FIPS code. 00\*\*\*\*\* = multi-state, 00FORGN = foreign country.
	
place_state
	The state in which the activity funded by the grant is performed.

place_state_code
	The FIPS code for the state in which the activity funded by the grant is performed.

place_city
	The city in which the activity funded by the grant is performed.
	
place_zipcode
	The zipcode in which the activity funded by the grant is performed.

place_district
	The congressional district in which the activity funded by the grant is performed.

place_country_code
	The FIPS code for the country in which the activity funded by the grant is performed.

project_description
	Description of the project that was funded.

psta_agency_code
	Agency Code part (First 2 characters) of Treasury Account Symbol (9 characters) assigned by U.S. Department of Treasury.
	
psta_account_code
	Account Code part (3rd to 6th characters) of Treasury Account Symbol (9 characters) assigned by U.S. Department of Treasury.

psta_subaccount_code
	Sub-Account Code part (7th to 9th characters) of Treasury Account Symbol (9 characters) assigned by U.S. Department of Treasury.

bfi
	Distinguisher for different fund types, such as the funding provided by the Recovery Act.

uri
	An agency defined identifier that is unique for every reported action.