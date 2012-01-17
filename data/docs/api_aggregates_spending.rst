====================
Federal Spending API
====================

Organization Methods
====================

Top Grants, Contracts and Loans
-------------------------------

Return the top grants, contracts and loans that contain the name of the organization. Note that in contrast to campaign finance, lobbying and earmark data, where organizations are mostly reliably identified, federal spending data does not standardize recipient names. Therefore results returned here may contain other organizations that happen to have similar names and may miss data where the organization name was written differently.

Example
~~~~~~~

``http://transparencydata.com/api/1.0/aggregates/org/dcd5591de57d4b05b26894a9c9575bf7/fed_spending.json?apikey=<your-key>&cycle=2010``

::

    [{"fiscal_year": 2010, 
      "description": "Hawaii Energy and Environmental Technologies Initiative", 
      "agency_name": "Navy", 
      "recipient_name": "UNIVERSITY OF HAWAII", 
      "amount": "14236487", "type": "g"},
     {"fiscal_year": 2009, 
      "description": "INCREMENTAL FUNDING - TASK ORDER 0002", 
      "agency_name": "", 
      "recipient_name": "UNIVERSITY OF HAWAII", 
      "amount": "9175940.00", 
      "type": "c"},
     {"fiscal_year": 2010, 
      "description": "INCREMENTAL FUNDING - TASK ORDER OOO2 - SPECIAL INVOICE", 
      "agency_name": "", 
      "recipient_name": "UNIVERSITY OF HAWAII", 
      "amount": "7839511.00", 
      "type": "c"},
     ...]