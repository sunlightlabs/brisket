$().ready(function() {
    
    TD.ContributionsDCFilter = new TD.DataFilter();
    
    TD.ContributionsDCFilter.path = 'contributions/dc';
    TD.ContributionsDCFilter.ignoreForBulk = ['cycle', 'transaction_namespace'];
    
    /* TD.ContributionsDCFilter.transaction_type_description = function(transaction_type) {
        if (transaction_type == '29') {
            return "<em>electioneering communication about</em> "
        }
        if (transaction_type == '24a') {
            return "<em>independent expenditure opposing</em> "
        }
        if (transaction_type == '24e') {
            return "<em>independent expenditure supporting</em> "
        }
        if (transaction_type.substring(0,2) == '16') {
            return "<em>loan to</em> "
        }
        return ""
    };*/
    
    TD.ContributionsDCFilter.row_content = function(row) {
        var content = '<td class="jurisdiction">DC</td>';
        content += '<td class="datestamp">' + (row.date || '&nbsp;') + '</td>';
        content += '<td class="amount">$' + TD.Utils.currencyFormat(row.amount) + '</td>';
        content += '<td class="contributor_name">' + row.contributor_name + '</td>';
        content += '<td class="contributor_location">' + TD.Utils.cityStateFormat(row.contributor_city, row.contributor_state) + '</td>';
        content += '<td class="committee_name">' + row.committee_name + '</td>';
        return content;
    };
    

    TD.ContributionsDCFilter.init = function() {

        TD.ContributionsDCFilter.registerFilter({
            name: 'amount',
            label: 'Amount',
            help: 'The dollar amount of the transaction',
            field: TD.DataFilter.OperatorField
        });

        TD.ContributionsDCFilter.registerFilter({
            name: 'contributor_ft',
            label: 'Contributor',
            help: 'Name of individual or organization contributing in the transaction',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContributionsDCFilter.registerFilter({
            name: 'contributor_state',
            label: 'Contributor State',
            help: 'State from which the transaction was made',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
        });
        
        /* TD.ContributionsDCFilter.registerFilter({
            name: 'msa_ft',
            label: 'Contributor Metropolitan Area',
            help: 'Metropolitan Statistical Area of the contributor',
            field: TD.DataFilter.TextField,
            allowMultipleFields: false
        }); */

        TD.ContributionsDCFilter.registerFilter({
            name: 'date',
            label: 'Date',
            help: 'Date of transaction',
            field: TD.DataFilter.DateRangeField
        });

        /* TD.ContributionsDCFilter.registerFilter({
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
                ['state:governor', 'State Governor'],
                ['state:judicial', 'State Judicial']
            ]
        }); */

        /* TD.ContributionsDCFilter.registerFilter({
            name: 'recipient_ft',
            label: 'Recipient',
            help: 'Name of candidate or PAC that received contribution or was targeted by a transaction',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        }); */

        TD.ContributionsDCFilter.registerFilter({
            name: 'committee_ft',
            label: 'Recipient Committee',
            help: 'Name of PAC that received contribution',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            //TD.HashMonitor.setAnchor('');
            this.loadHash();
        }
        
        TD.ContributionsDCFilter.renumberFilters();
        
    };

});
