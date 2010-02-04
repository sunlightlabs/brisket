$().ready(function() {

    TD.DataFilter.registerFilter({
        name: 'amount',
        label: 'Amount',
        help: 'This is the amount of the contribution',
        field: TD.DataFilter.OperatorField
    });
    
    TD.DataFilter.registerFilter({
        name: 'cycle',
        label: 'Cycle',
        help: 'Election cycles. Odd cycles have only state-level contributions',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['1990','1990'], ['1991','1991'], ['1992','1992'],
            ['1993','1993'], ['1994','1994'], ['1995','1995'],
            ['1996','1996'], ['1997','1997'], ['1998','1998'],
            ['1999','1999'], ['2000','2000'], ['2001','2001'],
            ['2002','2002'], ['2003','2003'], ['2004','2004'],
            ['2005','2005'], ['2006','2006'], ['2007','2007'],
            ['2008','2008'], ['2009','2009'], ['2010','2010']
        ]
    });
    
    TD.DataFilter.registerFilter({
        name: 'contributor_ft',
        label: 'Contributor',
        help: 'Name of individual or PAC that made contribution',
        field: TD.DataFilter.TextField,
        allowMultipleFields: true,
    });
    
    TD.DataFilter.registerFilter({
        name: 'date',
        label: 'Date',
        help: 'This is the date of the contribution',
        field: TD.DataFilter.DateRangeField
    });
    
    TD.DataFilter.registerFilter({
        name: 'transaction_namespace',
        label: 'Federal/State',
        help: 'State or federal office',
        field: TD.DataFilter.DropDownField,
        options: [
            ['urn:fec:transaction','Federal'],
            ['urn:nimsp:transaction','State']
        ]
    });
    
    TD.DataFilter.registerFilter({
        label: 'Office',
        name: 'seat',
        help: 'Office for which candidate is running',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['federal:senate', 'US Senate'],
            ['federal:house', 'US House of Representatives'],
            ['federal:president', 'US President'],
            ['state:upper', 'State Upper Chamber'],
            ['state:lower', 'State Lower Chamber'],
            ['state:governor', 'State Governor']
        ]
    });
    
    // TD.DataFilter.registerFilter({
    //     name: 'organization_ft',
    //     label: 'Employer',
    //     help: 'Employer of individual that made contribution',
    //     field: TD.DataFilter.TextField,
    //     allowMultipleFields: true,
    // });
    
    TD.DataFilter.registerFilter({
        name: 'recipient_ft',
        label: 'Recipient',
        help: 'Name of candidate or PAC that received contribution',
        field: TD.DataFilter.TextField,
        allowMultipleFields: true,
    });
    
    TD.DataFilter.registerFilter({
        name: 'state',
        label: 'State',
        help: 'State from which the contribution was made',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['AL', 'Alabama'],          ['AK', 'Alaska'],       ['AZ', 'Arizona'],      ['AR', 'Arkansas'],
            ['CA', 'California'],       ['CO', 'Colorado'],     ['CT', 'Connecticut'],  ['DE', 'Delaware'],
            ['DC', 'District of Columbia'],
            ['FL', 'Florida'],          ['GA', 'Georgia'],      ['HI', 'Hawaii'],       ['ID', 'Idaho'],
            ['IL', 'Illinois'],         ['IN', 'Indiana'],      ['IA', 'Iowa'],         ['KS', 'Kansas'],
            ['KY', 'Kentucky'],         ['LA', 'Louisiana'],    ['ME', 'Maine'],        ['MD', 'Maryland'],
            ['MA', 'Massachusetts'],    ['MI', 'Michigan'],     ['MN', 'Minnesota'],    ['MS', 'Mississippi'],
            ['MO', 'Missouri'],         ['MT', 'Montana'],      ['NE', 'Nebraska'],     ['NV', 'Nevada'],
            ['NH', 'New Hampshire'],    ['NJ', 'New Jersey'],   ['NM', 'New Mexico'],   ['NY', 'New York'],
            ['NC', 'North Carolina'],   ['ND', 'North Dakota'], ['OH', 'Ohio'],         ['OK', 'Oklahoma'],
            ['OR', 'Oregon'],           ['PA', 'Pennsylvania'], ['RI', 'Rhode Island'], ['SC', 'South Carolina'],
            ['SD', 'South Dakota'],     ['TN', 'Tennessee'],    ['TX', 'Texas'],        ['UT', 'Utah'],
            ['VT', 'Vermont'],          ['VA', 'Virginia'],     ['WA', 'Washington'],   ['WV', 'West Virginia'],
            ['WI', 'Wisconsin'],        ['WY', 'Wyoming']
        ]
    });

    TD.DataFilter.init();

});