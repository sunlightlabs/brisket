$().ready(function() {
    
    TD.ContributionFilter = new TD.DataFilter();
    
    TD.ContributionFilter.path = 'contributions';
    TD.ContributionFilter.ignoreForBulk = ['for_against', 'cycle', 'transaction_namespace'];
    
    TD.ContributionFilter.row_content = function(row) {
        var jurisdiction = (row.transaction_namespace == 'urn:fec:transaction') ? 'Federal' : 'State';
        var content = '<td class="jurisdiction">' + jurisdiction + '</td>';
        content += '<td class="datestamp">' + (row.date || '&nbsp;') + '</td>';
        content += '<td class="amount">$' + TD.Utils.currencyFormat(row.amount) + '</td>';
        content += '<td class="contributor_name">' + row.contributor_name + '</td>';
        content += '<td class="contributor_location">' + TD.Utils.cityStateFormat(row.contributor_city, row.contributor_state) + '</td>';
        content += '<td class="organization_name">' + (row.organization_name || '&nbsp;') + '</td>';
        content += '<td class="recipient_name">' + row.recipient_name + '</td>';   
        return content;
    };
    

    TD.ContributionFilter.init = function() {

        TD.ContributionFilter.registerFilter({
            name: 'amount',
            label: 'Amount',
            help: 'This is the amount of the contribution',
            field: TD.DataFilter.OperatorField
        });

        TD.ContributionFilter.registerFilter({
            name: 'cycle',
            label: 'Cycle',
            help: 'The two-year span in which the contributions were reported',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['1990','1989-1990'], ['1992','1991-1992'], ['1994','1993-1994'],
                ['1996','1995-1996'], ['1998','1997-1998'], ['2000','1999-2000'],
                ['2002','2001-2002'], ['2004','2003-2004'], ['2006','2005-2006'],
                ['2008','2007-2008'], ['2010','2009-2010']
            ]
        });

        TD.ContributionFilter.registerFilter({
            name: 'contributor_ft',
            label: 'Contributor',
            help: 'Name of individual, employer, or organization that made contribution',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContributionFilter.registerFilter({
            name: 'contributor_industry',
            label: 'Contributor Industry',
            help: 'The industry in which the person or organization making the contribution is involved',
            field: TD.DataFilter.DualDropDownField,
            allowMultipleFields: true,
            options: TD.INDUSTRIES
        });

        TD.ContributionFilter.registerFilter({
            name: 'contributor_state',
            label: 'Contributor State',
            help: 'State from which the contribution was made',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
        });

        TD.ContributionFilter.registerFilter({
            name: 'date',
            label: 'Date',
            help: 'This is the date of the contribution',
            field: TD.DataFilter.DateRangeField
        });

        TD.ContributionFilter.registerFilter({
            name: 'transaction_namespace',
            label: 'Federal/State',
            help: 'State or federal office',
            field: TD.DataFilter.DropDownField,
            options: [
                ['urn:fec:transaction','Federal'],
                ['urn:nimsp:transaction','State']
            ]
        });

        TD.ContributionFilter.registerFilter({
            name: 'for_against',
            label: 'For/against candidate',
            help: 'Contributions can be made in support of or against a candidate',
            field: TD.DataFilter.DropDownField,
            //required: true,
            options: [
                ['for','In support of the candidate'],
                ['against','Against the candidate']
            ]
        });
    
        TD.ContributionFilter.registerFilter({
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
        });

        TD.ContributionFilter.registerFilter({
            name: 'organization_ft',
            label: 'Organization',
            help: 'Name of employer or pass-through organization associated with contribution',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContributionFilter.registerFilter({
            name: 'recipient_ft',
            label: 'Recipient',
            help: 'Name of candidate or PAC that received contribution',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContributionFilter.registerFilter({
            name: 'recipient_state',
            label: 'Recipient State',
            help: 'The state in which the recipient is running or is located',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
        });

        TD.ContributionFilter.registerFilter({
            label: 'Transaction Type',
            name: 'transaction_type',
            help: 'The FEC transaction type of the contribution. You must remove the for/against filter for this filter to work properly.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['15', 'Contribution (15)'],
                ['15e', 'Earmarked contribution (15e)'],
                ['15j', 'Joint fundraising committee contribution (15j)'],
                ['22y', 'Refund (22y)'],
                ['22z', 'Contribution refund to a candidate or committee (22z)'],
                ['24a', 'Independent expenditure against candidate (24a)'],
                ['24c', 'Coordinated expenditure (24c)'],
                ['24e', 'Independent expenditure for candidate (24e)'],
                ['24f', 'Communication cost for candidate (24f)'],
                ['24g', 'Transfer to affiliated committee (24g)'],
                ['24k', 'Direct contribution (24k)'],
                ['24n', 'Communication cost against candidate (24n)'],
                ['24r', 'Election recount disbursement (24r)'],
                ['24z', 'In kind contribution (24z)'],
                ['10', '"Soft" money or Levin fund (10)'],
                ['11', 'Tribal contribution (11)']
            ]
        });
        
        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('for_against=for&cycle=2010');
            this.loadHash();
        }
        
    };

});