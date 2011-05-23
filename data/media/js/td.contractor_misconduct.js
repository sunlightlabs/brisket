$().ready(function() {

    TD.ContractorMisconductFilter = new TD.DataFilter();

    TD.ContractorMisconductFilter.path = 'contractor_misconduct';

    TD.ContractorMisconductFilter.row_content = function(row) {
        var content = '<td class="date_year">' + row.date_year + '</td>';
        content += '<td class="contractor">' + row.contractor.name + '</td>';
        content += '<td class="instance">' + row.instance + '</td>';
        content += '<td class="penalty_amount">' + TD.Utils.currencyFormatNonZero(row.penalty_amount, true) + '</td>';
        return content;
    }

    TD.ContractorMisconductFilter.init = function() {

        TD.ContractorMisconductFilter.registerFilter({
            name: 'date_year',
            label: 'Year',
            help: 'This is the year in which a date significant to the incident fell.',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: [ ['1995', '1995'],
                       ['1996', '1996'],
                       ['1997', '1997'],
                       ['1998', '1998'],
                       ['1999', '1999'],
                       ['2000', '2000'],
                       ['2001', '2001'],
                       ['2002', '2002'],
                       ['2003', '2003'],
                       ['2004', '2004'],
                       ['2005', '2005'],
                       ['2006', '2006'],
                       ['2007', '2007'],
                       ['2008', '2008'],
                       ['2009', '2009'],
                       ['2010', '2010']]
        });


        TD.ContractorMisconductFilter.registerFilter({
            name: 'contractor',
            label: 'Contractor',
            help: 'Name of the contractor.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'contracting_party',
            label: 'Contracting Party',
            help: 'Name of the contracting party.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'instance',
            label: 'Instance Description',
            help: 'Extended description of misconduct instance.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.ContractorMisconductFilter.registerFilter({
            name: 'enforcement_agency',
            label: 'Enforcement Agency',
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
