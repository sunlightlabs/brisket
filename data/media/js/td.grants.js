$().ready(function() {
    
    TD.GrantsFilter = new TD.DataFilter();
    
    TD.GrantsFilter.downloadPath = "/grants/download/";
    TD.GrantsFilter.previewPath = "/grants/";
    
    TD.GrantsFilter.shouldUseBulk = function() {
        var values = _.keys(this.values());
        values = _.without(values, 'fiscal_year');
        var useBulk = values.length == 0;
        if (useBulk) {
            $('#suggestbulk').dialog('open');    
        }
        return useBulk;
    };
    
    TD.GrantsFilter.preview = function() {
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
                $.getJSON('/data/grants/', params, function(data) {
                    if (data.length === 0) {
                        $('div#nodata').show();
                    } else {
                        for (var i = 0; i < data.length; i++) {
                            var grant = data[i];
                            var className = (i % 2 == 0) ? 'even' : 'odd';
                            var content = '<tr class="' + className + '">';
                            content += '<td class="fiscal_year">' + grant.fiscal_year + '</td>';
                            content += '<td class="amount_total">$' + TD.Utils.currencyFormat(grant.amount_total) + '</td>';
                            content += '<td class="recipient_name">' + grant.recipient_name + '</td>';
                            content += '<td class="agency_name">' + grant.agency_name + '</td>';
                            content += '</tr>';
                            $('#mainTable tbody').append(content);
                        }
                        $('span#previewCount').html(data.length);
                        TD.GrantsFilter.downloadNode.addClass('enabled');
                        $('div#nodata').hide();
                        $('div#tableScroll').show();
                    }
                    $('div#loading').hide();
                    if (data.length < 30) {
                        $('span#recordCount').html(data.length);
                    } else {
                        $.get('/data/grants/count/', params, function(data) {
                            $('span#recordCount').html(data);
                        });
                    }
                });
            }
        }
    };

    TD.GrantsFilter.init = function() {

        TD.GrantsFilter.registerFilter({
            name: 'amount_total',
            label: 'Amount (total)',
            help: 'This is the total amount of the grant.',
            field: TD.DataFilter.OperatorField
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

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('fiscal_year=2008');
            this.loadHash();
        }
        
    };

});