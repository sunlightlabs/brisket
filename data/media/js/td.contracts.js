$().ready(function() {
    
    TD.ContractsFilter = new TD.DataFilter();
    
    TD.ContractsFilter.downloadPath = "/contracts/download/";
    TD.ContractsFilter.previewPath = "/contracts/";
    
    TD.ContractsFilter.shouldUseBulk = function() {
        var values = _.keys(this.values());
        values = _.without(values, 'fiscal_year');
        var useBulk = values.length == 0;
        if (useBulk) {
            $('#suggestbulk').dialog('open');    
        }
        return useBulk;
    };
    
    TD.ContractsFilter.preview = function() {
        if ($('#mainTable').length > 0) {
            if (!this.shouldUseBulk()) {
                var params = this.values();
                var qs = TD.Utils.toQueryString(params);
                TD.HashMonitor.setAnchor(qs);
                this.previewNode.removeClass('enabled');
                $('div#tableScroll').hide();
                $('div#nodata').hide();
                $('div#loading').show();
                $('#mainTable tbody').empty();
                $('span#previewCount').html('...');
                $('span#recordCount').html('...');
                $.getJSON('/data/contracts/', params, function(data) {
                    if (data.length === 0) {
                        $('div#nodata').show();
                    } else {
                        for (var i = 0; i < data.length; i++) {
                            var contract = data[i];
                            var className = (i % 2 == 0) ? 'even' : 'odd';
                            var content = '<tr class="' + className + '">';
                            content += '<td class="fiscal_year">' + contract.fiscal_year + '</td>';
                            content += '<td class="current_amount">$' + TD.Utils.currencyFormat(contract.current_amount) + '</td>';
                            content += '<td class="vendor_name">' + contract.vendor_name + '</td>';
                            content += '<td class="contract_description">' + contract.contract_description + '</td>';
                            content += '<td class="agency_name">' + contract.agency_name + '</td>';
                            content += '</tr>';
                            $('#mainTable tbody').append(content);
                        }
                        $('span#previewCount').html(data.length);
                        TD.ContractsFilter.downloadNode.addClass('enabled');
                        $('div#nodata').hide();
                        $('div#tableScroll').show();
                    }
                    $('div#loading').hide();
                    if (data.length < 30) {
                        $('span#recordCount').html(data.length);
                    } else {
                        $.get('/data/contracts/count/', params, function(data) {
                            $('span#recordCount').html(data);
                        });
                    }
                });
            }
        }
    };
    
    TD.ContractsFilter.init = function() {

        TD.ContractsFilter.registerFilter({
            name: 'agency_ft',
            label: 'Agency',
            help: 'The name of the agency that awarded the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractsFilter.registerFilter({
            name: 'obligated_amount',
            label: 'Amount (obligated)',
            help: 'The base cost of the contract.',
            field: TD.DataFilter.OperatorField
        });

        TD.ContractsFilter.registerFilter({
            name: 'current_amount',
            label: 'Amount (current)',
            help: 'The current value of the contract (base cost + exercised options).',
            field: TD.DataFilter.OperatorField
        });

        TD.ContractsFilter.registerFilter({
            name: 'maximum_amount',
            label: 'Amount (maximum)',
            help: 'The maximum value of the contract if all options are exercised.',
            field: TD.DataFilter.OperatorField
        });

        TD.ContractsFilter.registerFilter({
            name: 'assistance_type',
            label: 'Assistance Type',
            help: 'The type of contract given.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['02','Block contra'],
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

        TD.ContractsFilter.registerFilter({
            name: 'fiscal_year',
            label: 'Fiscal Year',
            help: 'The year in which the contract was issued.',
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

        TD.ContractsFilter.registerFilter({
            name: 'recipient_ft',
            label: 'Recipient',
            help: 'The name of the organization that received the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractsFilter.registerFilter({
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

        TD.ContractsFilter.registerFilter({
            name: 'recipient_type',
            label: 'Recipient Type',
            help: 'The type of recipient to whom the contract was given.',
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
            TD.HashMonitor.setAnchor('fiscal_year=2009');
            this.loadHash();
        }
        
    };

});