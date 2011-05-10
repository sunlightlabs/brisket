$().ready(function() {

    TD.ContractorMisconductFilter = new TD.DataFilter();

    TD.ContractorMisconductFilter.path = 'contractor_misconduct';
    TD.ContractorMisconductFilter.ignoreForBulk = ['date_year'];

    TD.ContractorMisconductFilter.row_content = function(row) {
        var content = '<td class="date_year">' + row.date_year + '</td>';
        content += '<td class="penalty_amount">$' + TD.Utils.currencyFormat(row.penalty_amount) + '</td>';
        content += '<td class="contractor">' + row.contractor + '</td>';
        content += '<td class="contracting_party">' + row.contracting_party + '</td>';
        content += '<td class="enforcement_agency">' + row.enforcement_agency + '</td>';
        content += '<td class="misconduct_type">' + row.misconduct_type + '</td>';
        return content;
    }

    TD.ContractorMisconductFilter.init = function() {

        TD.ContractorMisconductFilter.registerFilter({
            name: 'date_year',
            label: 'Year',
            help: 'This is the year in which a date significant to the incident fell.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [ [str(x), str(x)] for x in range(1995, 2011) ]
        });


        TD.ContractorMisconductFilter.registerFilter({
            name: 'penalty_amount',
            label: 'Penalty Amount',
            help: 'This is the dollar amount of the penalty.',
            field: TD.DataFilter.OperatorField
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'contractor_ft',
            label: 'Contractor',
            help: 'Name of the contractor.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'contracting_party_ft',
            label: 'Contracting Party',
            help: 'Name of the contracting party.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'instance_ft',
            label: 'Instance Description',
            help: 'Extended description of misconduct instance.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'enforcment_agency_ft',
            label: 'Enforcment Agency',
            help: 'The agency responsible for enforcing the laws or regulations.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            TD.HashMonitor.setAnchor('date_year=2010');
            this.loadHash();
        }

    };

});
