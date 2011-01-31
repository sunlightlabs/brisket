$().ready(function() {
    
    TD.ContractsFilter = new TD.DataFilter();
    
    TD.ContractsFilter.path = 'contracts';
    TD.ContractsFilter.ignoreForBulk = ['fiscal_year'];
    
    TD.ContractsFilter.row_content = function(row) {
        var content = '<td class="fiscal_year">' + row.fiscal_year + '</td>';
        content += '<td class="current_amount">$' + TD.Utils.currencyFormat(row.baseandexercisedoptionsvalue) + '</td>';
        content += '<td class="vendor_name">' + row.vendorname + '</td>';
        content += '<td class="contract_description">' + row.descriptionofcontractrequirement + '</td>';
        return content;
    };
    
    TD.ContractsFilter.init = function() {

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
            name: 'place_state',
            label: 'Place of Performance State',
            help: 'The state in which the contract action will be performed.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
        });

		TD.ContractsFilter.registerFilter({
            name: 'vendor_name',
            label: 'Vendor',
            help: 'The name of the organization that received the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

		TD.ContractsFilter.registerFilter({
            name: 'vendor_duns',
            label: 'Vendor DUNs',
            help: 'The Dun and Bradstreet identifier of the organization that received the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

		TD.ContractsFilter.registerFilter({
            name: 'vendor_parent_duns',
            label: 'Vendor DUNs (parent)',
            help: 'The Dun and Bradstreet identifier of the parent of the organization that received the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

		TD.ContractsFilter.registerFilter({
            name: 'vendor_city',
            label: 'Vendor City',
            help: 'The city of the organization that received the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractsFilter.registerFilter({
            name: 'vendor_state',
            label: 'Vendor State',
            help: 'The state of the organization that received the contract.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: TD.STATES
        });

		TD.ContractsFilter.registerFilter({
            name: 'vendor_zipcode',
            label: 'Vendor Zipcode',
            help: 'The zipcode of the organization that received the contract.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('fiscal_year=2009');
            this.loadHash();
        }
        
    };

});