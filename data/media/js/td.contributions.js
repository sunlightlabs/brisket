$().ready(function() {
    
    TD.ContributionFilter = new TD.DataFilter();
    
    TD.ContributionFilter.path = 'contributions';
    TD.ContributionFilter.ignoreForBulk = ['for_against', 'cycle', 'transaction_namespace'];
    
    TD.ContributionFilter.transaction_type_description = function(transaction_type) {
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
    };
    
    TD.ContributionFilter.row_content = function(row) {
        var jurisdiction = (row.transaction_namespace == 'urn:fec:transaction') ? 'Federal' : 'State';
        var content = '<td class="jurisdiction">' + jurisdiction + '</td>';
        content += '<td class="datestamp">' + (row.date || '&nbsp;') + '</td>';
        content += '<td class="amount">$' + TD.Utils.currencyFormat(row.amount) + '</td>';
        content += '<td class="contributor_name">' + row.contributor_name + '</td>';
        content += '<td class="contributor_location">' + TD.Utils.cityStateFormat(row.contributor_city, row.contributor_state) + '</td>';
        content += '<td class="organization_name">' + (row.organization_name || '&nbsp;') + '</td>';
        content += '<td class="recipient_name">' + this.transaction_type_description(row.transaction_type) + row.recipient_name + '</td>';
        return content;
    };
    

    TD.ContributionFilter.init = function() {

        TD.ContributionFilter.registerFilter({
            name: 'amount',
            label: 'Amount',
            help: 'The dollar amount of the transaction',
            field: TD.DataFilter.OperatorField
        });

        TD.ContributionFilter.registerFilter({
            name: 'cycle',
            label: 'Cycle',
            help: 'The two-year span in which the transaction was reported',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [
                ['1990','1989-1990'], ['1992','1991-1992'], ['1994','1993-1994'],
                ['1996','1995-1996'], ['1998','1997-1998'], ['2000','1999-2000'],
                ['2002','2001-2002'], ['2004','2003-2004'], ['2006','2005-2006'],
                ['2008','2007-2008'], ['2010','2009-2010'], ['2012','2011-2012']
            ]
        });

        TD.ContributionFilter.registerFilter({
            name: 'contributor_ft',
            label: 'Contributor',
            help: 'Name of individual, employer, or organization in transaction',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContributionFilter.registerFilter({
            name: 'contributor_industry',
            label: 'Contributor Industry',
            help: 'The industry in which the person or organization making the transaction is involved',
            field: TD.DataFilter.DualDropDownField,
            allowMultipleFields: true,
            options: TD.INDUSTRIES
        });

        TD.ContributionFilter.registerFilter({
            name: 'contributor_state',
            label: 'Contributor State',
            help: 'State from which the transaction was made',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
        });
        
        TD.ContributionFilter.registerFilter({
            name: 'msa_ft',
            label: 'Contributor Metropolitan Area',
            help: 'Metropolitan Statistical Area of the contributor',
            field: TD.DataFilter.TextField,
            allowMultipleFields: false
        });

        TD.ContributionFilter.registerFilter({
            name: 'date',
            label: 'Date',
            help: 'Date of transaction',
            field: TD.DataFilter.DateRangeField
        });

        TD.ContributionFilter.registerFilter({
            name: 'transaction_namespace',
            label: 'Federal/State',
            help: 'transaction at state or federal level',
            field: TD.DataFilter.DropDownField,
            options: [
                ['urn:fec:transaction','Federal'],
                ['urn:nimsp:transaction','State']
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
            help: 'Name of employer or pass-through organization associated with transaction',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContributionFilter.registerFilter({
            name: 'recipient_ft',
            label: 'Recipient',
            help: 'Name of candidate or PAC that received contribution or was targed by transaction',
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
            name: 'general_transaction_type',
            help: 'Transactions can be contributions, independent expenditures or a variety of more esoteric types',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            required: true,
            options: [
                ['all', 'All (includes types below and other types)'],
                ['standard', 'Standard Contributions'],
                ['ie_supporting', 'Independent Expenditures Supporting Candidate'],
                ['ie_opposing', 'Independent Expenditures Opposing Candidate'],
                ['electioneering', 'Electioneering (Issue Ads)']
            ]
        });
        
        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('general_transaction_type=standard&cycle=2012');
            this.loadHash();
        }
        
        TD.ContributionFilter.renumberFilters();
        
    };

});
