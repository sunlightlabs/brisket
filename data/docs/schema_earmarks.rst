===============
Earmarks Schema
===============

fiscal_year
    The fiscal year for the bill in which the earmark appears. 

final_amount
    The earmark amount in the final version of the bill.
    
budget_amount
    The earmark amount in the President's budget proposal.
    
house_amount
    The earmark amount in the version of the bill passed by the House.
    
senate_amount
    The earmark amount in the version of the bill passed by the Senate.
    
omni_amount
    The earmark amount in the omnibus appropriations bill.
    
bill, bill_section, bill_subsection
    The bill, section and subsection where the earmark appears.
    
description
    The earmark description.
    
notes
    Notes added by Taxpayers for Commons Sense.
    
presidential
    Presidential earmarks are earmarks that appear in the President's initial budget proposal.
    
    ===== =======
    Value Meaning
    ===== =======
    blank Not in the President's budget.
    ``p`` Included in the President's budget.
    ``u`` Included in the President's budget and undisclosed.
    ``m`` Included in the President's budget and sponsored by members.
    ``j`` Judiciary.
    ===== =======

undisclosed
    Taxpayers for Common Sense's determination of whether the earmarks was disclosed by congress. Undisclosed earmarks are found by reading the bill text.
    
    ===== =======
    Value Meaning
    ===== =======
    blank Disclosed in congressional earmark reports.
    ``u`` Not disclosed by congress but found in bill text.
    ``p`` Not disclosed and in President's budget.
    ``o`` O & M-Disclosed
    ``m`` O & M-Undisclosed
    ===== =======
    
members
    The members that sponsored the earmark. Taxpayers for Common Sense lists the members by last name, state and party. We have attempted to expand these to full names, where possible. Due to formatting irregularities, state, party or full name are sometimes missing.
    
location
    The city and states where the earmark will be spent, when known.
    
recipients
    The organization that will receive the earmark, when known.
