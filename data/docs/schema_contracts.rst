===============================
 Federal Contracts Data Schema
===============================

id
	Unique record identifier.

transaction_number
	Unique identifier for the contract transaction.

fiscal_year
	The year in which the contract was awarded.

last_modified_date
	The date that this record was last modified.

piid
	When reporting orders under Indefinite Delivery Vehicles (IDV) such as a GWAC, IDC, FSS, BOA, or BPA, report the Procurement Instrument Identifier (Contract Number or Agreement Number) of the IDV. For the initial load of a BPA under a FSS, this is the FSS contract number. Note: BOAs and BPAs are with industry and not with other Federal Agencies.

parent_id
	ID of the original contract record identifier.

award_id
	Award identifier.

modification_number
	An identifier issued by an agency that uniquely identifies one modification for one contract, agreement, order, etc.

modification_reason
	Reason for contract modification.
	http://transparencydata.com/docs/lookup/contracts/mod_reasons/

agency_name
	The name of the agency awarding the contract.

agency_id
	FIPS identifier for the agency awarding the contract.

contracting_agency_name
	The name of the agency responsible for the contracting process.

contracting_agency_id
	FIPS identifier for the agency responsible for the contracting process.

contracting_office_id
	Agency specific identifier for the office responsible for the contracting process.

requesting_agency_name
	The name of the agency requesting the contract.

requesting_agency_id
	FIPS identifier for the agency requesting the contract.

requesting_office_id
	Agency specific identifier for the office requesting the contract.

major_program_code
	The agency determined code for a major program within the agency.

idv_agency_fee
	The fee charged to the requesting agency by the contracting agency for the cost of the contracting process.

cotr_name
	The name of the person responsible for overseeing the contracting process.

cotr_other_name
	The name of an additional COTR involved in the process.

contract_action_type
	The type of action used to award the contract.
	http://transparencydata.com/docs/lookup/contracts/action_types/

contract_bundling_type
	http://transparencydata.com/docs/lookup/contracts/bundling/

contract_competitiveness
	The level of competition during the contracting process.
	http://transparencydata.com/docs/lookup/contracts/competitiveness/

contract_description
	A text description of the purpose and result of the contract.

contract_financing
	The type of financing that will be used to pay the contractor.
	http://transparencydata.com/docs/lookup/contracts/financing/

contract_nia_code
	A code that represents the national interest for which the contract is created.
	http://transparencydata.com/docs/lookup/contracts/nia_codes/

contract_nocompete_reason
	The reason the contract was not competed.
	http://transparencydata.com/docs/lookup/contracts/nocompete_reasons/

contract_offers_received
	The number of offers/proposals received during the competition process.

contract_pricing_type
	The type of pricing used to compensate the contractor.
	http://transparencydata.com/docs/lookup/contracts/pricing_types/

contract_set_aside
	http://transparencydata.com/docs/lookup/contracts/set_asides/

subcontract_plan
	The plan the contractor has for using subcontractors.
	http://transparencydata.com/docs/lookup/contracts/subcontract_plans/

number_of_actions
	The number input by the agency that identifies number of actions that are reported in one modification.

consolidated_contract
	True if contract action is consolidated.

multiyear_contract
	Indicates that the contract is for services or supplies that go beyond 1 year, but less than 5 years.

performance_based_contract
	Indicates whether the contract is performance based or not.
	http://transparencydata.com/docs/lookup/contracts/ynx/

signed_date
	The date that both parties signed the contract.

effective_date
	The date on which the contract will begin.

completion_date
	The current completion date for the contract. If options have been executed, this date can be greater than the completion_date on the original record.

maximum_date
	The date of completion if all contract options are awarded.

renewal_date
	The date of contract renewal.

cancellation_date
	The date of cancellation if the contract is ended early.

obligated_amount
	The amount of money obligated or de-obligated in this transaction.

current_amount
	The current cost of the contract.

maximum_amount
	The maximum cost of the contract if all options and extensions are executed.

price_difference
	The percent difference between the award price and the lowest priced offer from a responsive, responsible non-HUBZone or non-SDB.

cost_data_obtained
	Whether or not cost data was obtained or waived.
	http://transparencydata.com/docs/lookup/contracts/cost_obtained/

purchase_card_as_payment
	Indicates that a purchase card was used to pay the contractor.

vendor_name
	Name of the contractor.

vendor_business_name
	Additional name used by the contractor for conducting business.

vendor_employees
	The number of people employed by the contractor.

vendor_annual_revenue
	The annual revenue of the contractor.

vendor_street_address
	Street address of the contractor.

vendor_street_address2
	Additional street address of the contractor.

vendor_street_address3
	Additional street address of the contractor.

vendor_city
	The primary city in which the contractor conducts business.

vendor_state
	The primary state in which the contractor conducts business.

vendor_zipcode
	The primary zip code in which the contractor conducts business.

vendor_district
	The primary congressional district in which the contractor conducts business.

vendor_country_code
	FIPS code indicating the country in which the contractor operates.

vendor_duns
	The Dun and Bradstreet identifier for the contractor.

vendor_parent_duns
	The Dun and Bradstreet identifier for the contractor's corporate parent.

vendor_phone
	The phone number for the contractor.

vendor_fax
	The fax number for the contractor.

vendor_ccr_exception
	The reason a vendor/contractor not registered in the mandated CCR system may be used in a purchase.
	http://transparencydata.com/docs/lookup/contracts/ccr_exceptions/

place_district
	The congressional district in which the contract action will be performed.

place_location_code
	FIPS identifier for the location in which the contract action will be performed.

place_state_code
	FIPS identifier for the state in which the contract action will be performed.

product_origin_country
	FIPS identifier for the country of origin for the product being purchased by the contract.

product_origin
	Indicates the origin of the product being purchased.
	http://transparencydata.com/docs/lookup/contracts/product_origin/

producer_type
	Indicates the type and nationality of the manufacturing organization.
	http://transparencydata.com/docs/lookup/contracts/org_types/

statutory_authority
	The statutory authority under which the agency is authorized to execute the contract.

product_service_code
	The code that best identifies the product or service procured. Codes are defined in the Product and Service Codes Manual.
	
naics_code
	The North American Industry Classification System (NAICS) codes designate major sectors of the economies of Mexico, Canada, and the United States.

solicitation_id
	Identifier used to link transactions in FPDS-NG to solicitation information.

supports_goodness
	A designator of contract actions that support a declared contingency operation, a declared humanitarian operation or a declared peacekeeping operation.

dod_system_code
	Indicates the DoD system or equipment for which the contract is being awarded.

it_commercial_availability
	Indicates the commercial availability of the contract being purchased.
	http://transparencydata.com/docs/lookup/contracts/commercial/

cas_clause
	http://transparencydata.com/docs/lookup/contracts/ynx/

recovered_material_clause
	http://transparencydata.com/docs/lookup/contracts/rm_clauses/

fed_biz_opps
	Indicates whether or not the contract was listed in Fed Biz Opps.
	http://transparencydata.com/docs/lookup/contracts/ynx/

government_property
	Indicates whether or not government property will be furnished for the contract.



	