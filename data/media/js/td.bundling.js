$().ready(function() {

    TD.BundlingFilter = new TD.DataFilter();

    TD.BundlingFilter.path = 'contributions/bundled';

    TD.BundlingFilter.row_content = function(row) {
        var content = ''
        content += '<td class="recipient_name">' + TD.Utils.coalesce(new Array(row.recipient_name, row.committee_name)) + '</td>';
        content += '<td class="lobbyist_name">' + TD.Utils.coalesce(new Array(row.lobbyist_name, row.firm_name)) + '</td>';
        content += '<td class="start_date">' + row.start_date + '</td>';
        content += '<td class="end_date">' + row.end_date + '</td>';

        return content;
    }

    TD.BundlingFilter.init = function() {

        TD.BundlingFilter.registerFilter({
            name: 'recipient_name',
            label: 'Recipient',
            help: 'Name of the politician or committee which received the bundled contribution',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.BundlingFilter.registerFilter({
            name: 'lobbyist_name',
            label: 'Lobbyist',
            help: 'Lobbyist or lobbying firm who bundled the contributions',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            this.loadHash();
        }

    };

});
