$().ready(function() {

    TD.EpaEchoFilter = new TD.DataFilter();

    TD.EpaEchoFilter.path = 'epa_echo';

    TD.EpaEchoFilter.row_content = function(row) {
        var content = ''
        content += '<td class="case_num">' + row.case_num + '</td>';
        content += '<td class="case_name">' + row.case_name + '</td>';
        content += '<td class="first_date">' + row.first_date + '</td>';
        content += '<td class="first_date_significance">' + row.first_date_significance + '</td>';
        content += '<td class="last_date">' + row.last_date + '</td>';
        content += '<td class="last_date_significance">' + row.last_date_significance + '</td>';
        content += '<td class="penalty">' + TD.Utils.currencyFormatNonZero(row.penalty) + '</td>';
        content += '<td class="penalty_enfops">' +  TD.Utils.currencyFormatNonZero(row.penalty_enfops) + '</td>';
        content += '<td class="penalty_enfccaa">' + TD.Utils.currencyFormatNonZero(row.penalty_enfccaa) + '</td>';
        content += '<td class="penalty_enfcraa">' + TD.Utils.currencyFormatNonZero(row.penalty_enfcraa) + '</td>';
        content += '<td class="penalty_enfotpa">' + TD.Utils.currencyFormatNonZero(row.penalty_enfotpa) + '</td>';
        content += '<td class="penalty_enfotsa">' + TD.Utils.currencyFormatNonZero(row.penalty_enfotsa) + '</td>';
        content += '<td class="num_defendants">' + row.num_defendants + '</td>';
        content += '<td class="defendants">' + row.defendants + '</td>';
        content += '<td class="locations">' + row.locations + '</td>';
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
            name: 'first_date',
            label: 'First Date of Significance',
            help: 'First date of significance to the case',
            field: TD.DataFilter.DateRangeField,
            allowMultipleFields: false,
            yearRange: '1969:2011'
        });

        TD.EpaEchoFilter.registerFilter({
            name: 'last_date',
            label: 'Last Date of Significance',
            help: 'Last date of significance to the case',
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
            name: 'locations',
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
