$().ready(function() {
    
    TD.GrantsFilter = new TD.DataFilter();
    
    TD.GrantsFilter.specificPath = 'grants';
    
    TD.GrantsFilter.shouldUseBulk = function() {
        var values = _.keys(this.values());
        values = _.without(values, 'fiscal_year');
        var useBulk = values.length == 0;
        if (useBulk) {
            $('#suggestbulk').dialog('open');    
        }
        return useBulk;
    };
    
    TD.GrantsFilter.row_content = function(row) {
        var content = '<td class="fiscal_year">' + row.fiscal_year + '</td>';
        content += '<td class="amount_total">$' + TD.Utils.currencyFormat(row.amount_total) + '</td>';
        content += '<td class="recipient_name">' + row.recipient_name + '</td>';
        content += '<td class="cfda_program_title">' + row.cfda_program_title + '</td>';
        content += '<td class="agency_name">' + row.agency_name + '</td>';
        return content
    };

    TD.GrantsFilter.init = function() {

        TD.GrantsFilter.registerFilter({
            name: 'agency_ft',
            label: 'Agency',
            help: 'The name of the agency that awarded the grant.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.GrantsFilter.registerFilter({
            name: 'amount_total',
            label: 'Amount (total)',
            help: 'This is the total amount of the grant.',
            field: TD.DataFilter.OperatorField
        });

        TD.GrantsFilter.registerFilter({
            name: 'assistance_type',
            label: 'Assistance Type',
            help: 'The type of grant given.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['02','Block grant'],
                ['03','Formula grant'],
                ['04','Project grant'],
                ['05','Cooperative agreement'],
                ['06','Direct payment for specified use, as a subsidy or other non-reimbursable direct financial aid'],
                ['07','Direct loan'],
                ['08','Guaranteed/insured loan'],
                ['09','Insurance'],
                ['10','Direct payment with unrestricted use'],
                ['11','Other reimbursable, contingent, intangible or indirect financial assistance'],
            ]
        });

        TD.GrantsFilter.registerFilter({
            name: 'fiscal_year',
            label: 'Fiscal Year',
            help: 'The year in which the grant was issued.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['1998','1998'], ['1999','1999'],
                ['2000','2000'], ['2001','2001'],
                ['2002','2002'], ['2003','2003'],
                ['2004','2004'], ['2005','2005'],
                ['2006','2006'], ['2007','2007'],
                ['2008','2008'], ['2009','2009'],
                ['2010','2010']
            ]
        });

        TD.GrantsFilter.registerFilter({
            name: 'recipient_ft',
            label: 'Recipient',
            help: 'The name of the organization that received the grant.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.GrantsFilter.registerFilter({
            name: 'recipient_state',
            label: 'Recipient State',
            help: 'State in which the recipient resides.',
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

        TD.GrantsFilter.registerFilter({
            name: 'recipient_type',
            label: 'Recipient Type',
            help: 'The type of recipient to whom the grant was given.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['00','State government'],
                ['01','County government'],
                ['02','City or township government'],
                ['04','Special district government'],
                ['05','Independent school district'],
                ['06','State controlled institution of higher education'],
                ['11','Indian tribe'],
                ['12','Other nonprofit'],
                ['20','Private higher education'],
                ['21','individual'],
                ['22','Profit organization'],
                ['23','Small business'],
                ['25','Other'],
            ]
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('fiscal_year=2010');
            this.loadHash();
        }
        
    };

});