$().ready(function() {
    
    TD.ContributionsDCFilter = new TD.DataFilter();
    
    TD.ContributionsDCFilter.path = 'contributions/dc';
    TD.ContributionsDCFilter.ignoreForBulk = ['cycle', 'transaction_namespace'];
    
    TD.ContributionsDCFilter.row_content = function(row) {
        var content = '<td class="jurisdiction">DC</td>';
        content += '<td class="datestamp">' + (row.date || '&nbsp;') + '</td>';
        content += '<td class="amount">$' + TD.Utils.currencyFormat(row.amount) + '</td>';
        content += '<td class="contributor_name">' + row.contributor_name + '</td>';
        content += '<td class="contributor_location">' + TD.Utils.cityStateFormat(row.contributor_city, row.contributor_state) + '</td>';
        content += '<td class="committee_name">' + row.committee_name + '</td>';
        content += '<td class="recipient_name">' + row.recipient_name + '</td>';
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
        
        TD.ContributionsDCFilter.registerFilter({
            name: 'date',
            label: 'Date',
            help: 'Date of transaction',
            field: TD.DataFilter.DateRangeField,
            yearRange: '2011:2013'
        });

         TD.ContributionsDCFilter.registerFilter({
            name: 'office_ft',
            label: 'Office',
            help: 'Office for which candidate is running',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true,
        });

         TD.ContributionsDCFilter.registerFilter({
            name: 'payment_type_ft',
            label: 'Payment Type',
            help: 'Type of payment, e.g. cash/check. Also used to indicate audit adjustments.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true,
        });

        TD.ContributionsDCFilter.registerFilter({
            name: 'recipient_ft',
            label: 'Recipient',
            help: 'Name of candidate that received contribution',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

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
