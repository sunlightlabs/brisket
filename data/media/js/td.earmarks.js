$().ready(function() {
	
	TD.EarmarksFilter = new TD.DataFilter();
	
	TD.EarmarksFilter.path = 'earmarks';
	TD.EarmarksFilter.ignoreForBulk = ['year'];
	
	TD.EarmarksFilter.row_content = function(row) {
		var content = '<td class="fiscal_year">' + row.fiscal_year + '</td>';
        content += '<td class="final_amount">$' + TD.Utils.currencyFormat(row.final_amount) + '</td>';
        content += '<td class="location">' + row.location + '</td>';
        content += '<td class="description">' + row.description + '</td>';
        content += '<td class="members">' + row.members + '</td>';
        return content;
	};
	
	TD.EarmarksFilter.init = function() {
		
		TD.EarmarksFilter.registerFilter({
            name: 'description',
            label: 'Description',
            help: 'The description of the earmark request.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });
		
        TD.EarmarksFilter.registerFilter({
            name: 'year',
            label: 'Fiscal Year',
            help: 'The fiscal year in which the earmark was requested.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['2008','2008'],
                ['2009','2009'],
                ['2010','2010']
            ]
        });
		
		var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('fiscal_year=2009');
            this.loadHash();
        }
	};
});