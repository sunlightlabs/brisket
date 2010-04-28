$().ready(function() {
    
    TD.LobbyingFilter = new TD.DataFilter();
    
    TD.LobbyingFilter.downloadPath = "/lobbying/download/";
    TD.LobbyingFilter.previewPath = "/lobbying/";    
    
    TD.LobbyingFilter.shouldUseBulk = function() {
        var values = _.keys(this.values());
        values = _.without(values, 'year');
        var useBulk = values.length == 0;
        if (useBulk) {
            $('#suggestbulk').dialog('open');    
        }
        return useBulk;
    };
    
    TD.LobbyingFilter.preview = function() {
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
                $.getJSON('/data/lobbying/', params, function(data) {
                    if (data.length === 0) {
                        $('div#nodata').show();
                    } else {
                        for (var i = 0; i < data.length; i++) {
                            var lob = data[i];
                            var className = (i % 2 == 0) ? 'even' : 'odd';
                            // var jurisdiction = (contrib.transaction_namespace == 'urn:fec:transaction') ? 'Federal' : 'State';
                            var content = '<tr class="' + className + '">';
                            content += '<td class="year">' + lob.year + '</td>';
                            content += '<td class="amount">$' + TD.Utils.currencyFormat(lob.amount) + '</td>';
                            content += '<td class="registrant_name">' + lob.registrant_name + '</td>';
                            content += '<td class="client_name">' + lob.client_name + '</td>';
                            content += '<td class="client_parent_name">' + (lob.client_parent_name || '&nbsp;') + '</td>';
                            content += '<td class="lobbyists">';
                            for (var j = 0; j < lob.lobbyists.length; j++) {
                                var lobbyist = lob.lobbyists[j];
                                content += '<p>' + lobbyist.lobbyist_name + '</p>';
                            }
                            content += '</td>';
                            content += '</tr>';
                            $('#mainTable tbody').append(content);
                        }
                        $('span#previewCount').html(data.length);
                        TD.LobbyingFilter.downloadNode.addClass('enabled');
                        $('div#nodata').hide();
                        $('div#tableScroll').show();
                    }
                    $('div#loading').hide();
                    if (data.length < 30) {
                        $('span#recordCount').html(data.length);
                    } else {
                        $.get('/data/lobbying/count/', params, function(data) {
                            $('span#recordCount').html(data);
                        });
                    }
                });
            }
        }
    };

    TD.LobbyingFilter.init = function() {

        TD.LobbyingFilter.registerFilter({
            name: 'amount',
            label: 'Amount',
            help: 'This is the amount of the contribution',
            field: TD.DataFilter.OperatorField
        });

        TD.LobbyingFilter.registerFilter({
            name: 'client_ft',
            label: 'Client',
            help: 'Name of organization that hired or employed the lobbyist.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.LobbyingFilter.registerFilter({
            name: 'client_parent_ft',
            label: 'Client Parent',
            help: 'Name of organization that owns the client.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.LobbyingFilter.registerFilter({
            name: 'issue',
            label: 'Issue',
            help: '',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['ACC','Accounting'], ['ADV','Advertising'],
                ['AER','Aerospace'], ['AGR','Agriculture'],
                ['ALC','Alcohol & Drug Abuse'], ['ANI','Animals'],
                ['APP','Apparel, Clothing, & Textiles'], ['ART','Arts & Entertainment'],
                ['AUT','Automotive Industry'], ['AVI','Aviation, Airlines & Airports'],
                ['BAN','Banking'], ['BNK','Bankruptcy'],
                ['BEV','Beverage Industry'], ['CHM','Chemical Industry'],
                ['CIV','Civil Rights & Civil Liberties'], ['CAW','Clean Air & Water'],
                ['CDT','Commodities'], ['CPI','Computers & Information Tech'],
                ['CON','Constitution'], ['CSP','Consumer Product Safety'],
                ['CPT','Copyright, Patent & Trademark'], ['DEF','Defense'],
                ['DIS','Disaster & Emergency Planning'], ['DOC','District of Columbia'],
                ['ECN','Economics & Econ Development'], ['EDU','Education'],
                ['ENG','Energy & Nuclear Power'], ['ENV','Environment & Superfund'],
                ['FAM','Family, Abortion & Adoption'], ['BUD','Fed Budget & Appropriations'],
                ['FIN','Finance'], ['FIR','Firearms, Guns & Ammunition'],
                ['FOO','Food Industry'], ['FOR','Foreign Relations'],
                ['FUE','Fuel, Gas & Oil'], ['GAM','Gaming, Gambling & Casinos'],
                ['GOV','Government Issues'], ['WAS','Hazardous & Solid Waste'],
                ['HCR','Health Issues'], ['HOM','Homeland Security'],
                ['HOU','Housing'], ['IMM','Immigration'],
                ['IND','Indian/Native American Affairs'], ['INS','Insurance'],
                ['INT','Intelligence'], ['LBR','Labor, Antitrust & Workplace'],
                ['LAW','Law Enforcement & Crime'], ['MAN','Manufacturing'],
                ['MAR','Marine, Boats & Fisheries'], ['MIA','Media Information & Publishing'],
                ['MED','Medical Research & Clin Labs'], ['MMM','Medicare & Medicaid'],
                ['MON','Mining, Money & Gold Standard'], ['NAT','Natural Resources'],
                ['PHA','Pharmacy'], ['POS','Postal'],
                ['COM','Radio & TV Broadcasting'], ['RRR','Railroads'],
                ['RES','Real Estate & Land Use'], ['REL','Religion'],
                ['RET','Retirement'], ['ROD','Roads & Highways'],
                ['SCI','Science & Technology'], ['SMB','Small Business'],
                ['SPO','Sports & Athletics'], ['TRF','Tariffs'],
                ['TAX','Taxes'], ['TEC','Telecommunications'],
                ['TOB','Tobacco'], ['TOR','Torts'],
                ['TRD','Trade'], ['TRA','Transportation'],
                ['TOU','Travel & Tourism'], ['TRU','Trucking & Shipping'],
                ['UNM','Unemployment'], ['URB','Urban Development'],
                ['UTI','Utilities'], ['VET','Veterans Affairs'],
                ['WEL','Welfare'],
            ]
        });

        TD.LobbyingFilter.registerFilter({
            name: 'lobbyist_ft',
            label: 'Lobbyist',
            help: 'Name of lobbyist.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.LobbyingFilter.registerFilter({
            name: 'lobbyist_is_rep',
            label: 'Member of Congress',
            help: 'Find lobbyists that served as members of Congress',
            field: TD.DataFilter.BooleanField
        });

        TD.LobbyingFilter.registerFilter({
            name: 'registrant_ft',
            label: 'Registrant',
            help: 'The name of the person or organization that filed the lobbying registration.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.LobbyingFilter.registerFilter({
            name: 'transaction_id',
            label: 'Registration ID',
            help: 'The ID of the lobbying registration record.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.LobbyingFilter.registerFilter({
            name: 'year',
            label: 'Year',
            help: 'The year in which the registration was filed.',
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
            TD.HashMonitor.setAnchor('year=2010');
            this.loadHash();
        }
        
    };

});