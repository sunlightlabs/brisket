====================================
 Campaign Contributions Data Schema 
====================================

cycle
	The election cycle in which the contribution was given. Valid values are even years between 1990 and 2010 (inclusive).

transaction_namespace
	Indicates the source of the contribution record.
	
	=========================  =============================
	Value					   Description
	=========================  =============================
	``urn:fec:transaction``    federal contributions \(CRP\)
	``urn:nimsp:transaction``  state contributions \(NIMSP\)
	=========================  =============================

transaction_id
	Unique record ID given to the contribution by the FEC (federal) or NIMSP (state). Federal records are only guaranteed to be unique per year so they are prepended with the cycle.

transaction_type
	Transaction type assigned by the FEC. State records do not yet have transaction types.

filing_id
	Unique identifier for the actual filing with the FEC. State records do not yet have filing identifiers.

is_amendment
	``TRUE`` if transaction is an amendment to a previously reported contribution, otherwise ``FALSE``.

amount
	Amount of the contribution in US dollars.

date
	Date the contribution was made.

contributor_name
	Name of the person or organization making the contribution.

contributor_ext_id
	The NIMSP or CRP ID of the contributor, if an ID exists.

contributor_type
	``I`` for individual or ``C`` for PAC. NIMSP (state) records do not have a contributor type.

contributor_occupation
	The self-reported occupation of the contributor.

contributor_employer
	The self-reported employer of the contributor.

contributor_gender
	``M`` for male, ``F`` for female. Gender will only be found on CRP (federal) records.

contributor_address
	The self-reported address of the contributor.

contributor_city 
	The self-reported city of the contributor.

contributor_state
	The self-reported state of the contributor as the two-letter state abbreviation.

contributor_zipcode
	The self-reported ZIPCode of the contributor.

contributor_category
	The five character industry `category code <http://assets.transparencydata.org.s3.amazonaws.com/docs/catcodes.csv>`_ of the contributor assigned by CRP or NIMSP.

organization_name
	The name of the organization related to the contributor (employee, owner, spouse of owner, etc.). CRP or NIMSP standardized name.

organization_ext_id
	The NIMSP or CRP ID of the organization, if an ID exists.

parent_organization_name
	The name of the parent organization if one exists. CRP or NIMSP standardized name.

parent_organization_ext_id
	The NIMSP or CRP ID of the parent organization, if an ID exists.

recipient_name
	Name of the candidate or organization receiving the contribution.

recipient_ext_id
	The NIMSP or CRP ID of the recipient.

recipient_party
	The political party to which the recipient belongs. ``3`` for third party, ``D`` for Democratic Party, ``I`` for independent, ``R`` for Republican Party, and ``U`` for unknown.

recipient_type
	``C`` for committees, ``O`` for organizations, ``P`` for politicians.

recipient_category
	The five character industry category code of the recipient assigned by CRP or NIMSP. A full listing of categories and category orders can be found in catcodes.csv.

recipient_category_order
	The three character industry code of the recipient assigned by CRP or NIMSP. A full listing of categories and category orders can be found in catcodes.csv.

committee_name
	The name of the committee associated with the recipient of the contribution. This may be a parent committee or the election committee for the candidate.

committee_ext_id
	The NIMSP or CRP ID of the committee.

committee_party
	The political party to which the committee belongs. ``3`` for third party, ``D`` for Democratic Party, ``I`` for independent, ``R`` for Republican Party, and ``U`` for unknown.

election_type
	``G`` for general, ``P`` for primary.

district
	The district that the candidate represents, if there is one. The district is as the state abbreviation followed by the district number. For example: ``CA-12``.
	
seat
	The type of office being sought by the candidate.

	==================  ==================================
	Value               Description
	==================  ==================================
	federal:senate      US Senate
	federal:house       US House of Representatives
	federal:president   US President
	state:upper         upper chamber of state legislature
	state:lower         lower chamber of state legislature
	state:governor      state governor
	==================  ==================================

seat_status
	``I`` for incumbent, ``O`` for open. The value will be filled in as available in the source data.

seat_result
	``W`` for win, ``L`` for loss. The value will be filled in as available in the source data.
