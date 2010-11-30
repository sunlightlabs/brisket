$().ready(function() {
    
    TD.LobbyingFilter = new TD.DataFilter();
    
    TD.LobbyingFilter.path = 'lobbying';
    TD.LobbyingFilter.ignoreForBulk = ['year'];
    
    TD.LobbyingFilter.row_content = function(row) {
        var content = '<td class="year">' + row.year + '</td>';
        content += '<td class="amount">$' + TD.Utils.currencyFormat(row.amount) + '</td>';
        content += '<td class="registrant_name">' + row.registrant_name + '</td>';
        content += '<td class="client_name">' + row.client_name + '</td>';
        content += '<td class="client_parent_name">' + (row.client_parent_name || '&nbsp;') + '</td>';
        content += '<td class="lobbyists">';
        for (var j = 0; j < row.lobbyists.length; j++) {
            var lobbyist = row.lobbyists[j];
            content += '<p>' + lobbyist.lobbyist_name + '</p>';
        }
        content += '</td>';
        return content;
    }

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
            name: 'industry',
            label: 'Client Industry',
            help: 'The industry in which the lobbying client is involved',
            field: TD.DataFilter.DualDropDownField,
            allowMultipleFields: true,
            options: TD.INDUSTRIES
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
            name: 'transaction_type',
            label: 'Registration Type',
            help: 'The type of registration filed with SOPR.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['q1n','First Quarter (No Activity)'],
                ['q1a','First Quarter Amendment'],
                ['q1an','First Quarter Amendment (No Activity)'],
                ['q1','First Quarter Report'],
                ['q1t','First Quarter Termination'],
                ['q1ta','First Quarter Termination Amendment'],
                ['q2n','Second Quarter (No Activity)'],
                ['q2a','Second Quarter Amendment'],
                ['q2qn','Second Quarter Amendment (No Activity)'],
                ['q2','Second Quarter Report'],
                ['q2t','Second Quarter Termination'],
                ['q2tn','Second Quarter Termination (No Activity)'],
                ['q2ta','Second Quarter Termination Amendment'],
                ['q2an','Second Quarter Termination Amendment (No Activity)'],
                ['q3n','Third Quarter (No Activity)'],
                ['q3a','Third Quarter Amendment'],
                ['q3an','Third Quarter Amendment (No Activity)'],
                ['q3','Third Quarter Report'],
                ['q3t','Third Quarter Termination'],
                ['q3tn','Third Quarter Termination (No Activity)'],
                ['q3ta','Third Quarter Termination Amendment'],
                ['q4n','Fourth Quarter (No Activity)'],
                ['q4a','Fourth Quarter Amendment'],
                ['q4','Fourth Quarter Report'],
                ['q4t','Fourth Quarter Termination'],
                ['q4tn','Fourth Quarter Termination (No Activity)'],
                ['q4ta','Fourth Quarter Termination Amendment'],
                ['q4an','Fourth Quarter Termination Amendment (No Activity)'],
                ['mn','Mid-Year (No Activity)'],
                ['ma','Mid-Year Amendment'],
                ['man','Mid-Year Amendment (No Activity)'],
                ['m','Mid-Year Report'],
                ['mt','Mid-Year Termination'],
                ['mtn','Mid-Year Termination (No Activity)'],
                ['mta','Mid-Year Termination Amendment'],
                ['mtan','Mid-Year Termination Amendment (No Activity)'],
                ['MTL','Mid-Year Termination Letter'],
                ['en','Year-End (No Activity)'],
                ['ea','Year-End Amendment'],
                ['ean','Year-End Amendment (No Activity)'],
                ['er','Year-End Report'],
                ['et','Year-End Termination'],
                ['etn','Year-End Termination (No Activity)'],
                ['eta','Year-End Termination Amendment'],
                ['eran','Year-End Termination Amendment (No Activity)'],
                ['ETL','Year-End Termination Letter'],
                ['RA','Registration Amendment']
            ]
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
            TD.HashMonitor.setAnchor('year=2008');
            this.loadHash();
        }
        
    };

});