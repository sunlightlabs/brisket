$().ready(function() {

    TD.EpaEchoFilter = new TD.DataFilter();

    TD.EpaEchoFilter.path = 'epa_echo';

    TD.EpaEchoFilter.row_content = function(row) {
        var content = ''
        content += '<td class="case_name">' + row.case_name + '</td>';
        content += '<td class="defendants expandable"><p>' + row.defendants + '</p></td>';
        content += '<td class="last_date">' + row.last_date + '</td>';
        content += '<td class="locations expandable"><p>' + row.locations + '</p></td>';
        content += '<td class="penalty">' + TD.Utils.currencyFormatNonZero(row.penalty) + '</td>';

        return content;
    }

    TD.EpaEchoFilter.init = function() {

        TD.EpaEchoFilter.registerFilter({
            name: 'case_name',
            label: 'Case Name',
            help: 'The name of the case.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.EpaEchoFilter.registerFilter({
            name: 'last_date',
            label: 'Date',
            help: 'Most recent date of significance to the case',
            field: TD.DataFilter.DateRangeField,
            allowMultipleFields: false,
            yearRange: '1969:2011'
        });

        TD.EpaEchoFilter.registerFilter({
            name: 'penalty',
            label: 'Penalty',
            help: 'Total penalties',
            field: TD.DataFilter.OperatorField,
            allowMultipleFields: true
        });

        TD.EpaEchoFilter.registerFilter({
            name: 'defendants',
            label: 'Defendants',
            help: 'Defendant names associated with the case',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.EpaEchoFilter.registerFilter({
            name: 'location_addresses',
            label: 'Locations',
            help: 'All locations associated with the case',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            //TD.HashMonitor.setAnchor('date_year=2011');
            this.loadHash();
        }

    };

});
