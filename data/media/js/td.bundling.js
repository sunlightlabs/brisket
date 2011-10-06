$().ready(function() {

    TD.BundlingFilter = new TD.DataFilter();

    TD.BundlingFilter.path = 'contributions/bundled';

    TD.BundlingFilter.row_content = function(row) {
        var content = ''
        content += '<td class="committee_name">' + row.committee_name + '</td>';
        content += '<td class="recipient_name">' + row.recipient_name + '</td>';
        content += '<td class="lobbyist_name">' + row.lobbyist_name + '</td>';
        content += '<td class="firm_name">' + row.firm_name + '</td>';
        content += '<td class="start_date">' + row.start_date + '</td>';
        content += '<td class="end_date">' + row.end_date + '</td>';

        return content;
    }

    TD.BundlingFilter.init = function() {

        TD.BundlingFilter.registerFilter({
            name: 'committee_name',
            label: 'Committee Name',
            help: 'The name of the committee receiving the bundled contributions.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.BundlingFilter.registerFilter({
            name: 'recipient_name',
            label: 'Recipient',
            help: 'Name of the politician (if any) associated with the committee which received the bundle',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.BundlingFilter.registerFilter({
            name: 'lobbyist_name',
            label: 'Lobbyist',
            help: 'Lobbyist who bundled the contributions',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.BundlingFilter.registerFilter({
            name: 'firm_name',
            label: 'Lobbying Firm',
            help: 'The name of the lobbying firm associated with the bundled contributions',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            this.loadHash();
        }

    };

});
