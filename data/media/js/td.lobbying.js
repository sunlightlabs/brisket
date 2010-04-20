TD.Lobbying = {
    downloadPath: "/lobbying/download/",
    previewPath: "/lobbying/",
    shouldUseBulk: function() {
        var useBulk = false;
        var values = _.keys(TD.DataFilter.values());
        values = _.without(values, 'year');
        if (values.length == 0) {
            $('#suggestbulk').dialog('open');    
        }
        return values.length == 0;
    },
    preview: function() {
        if ($('#mainTable').length > 0) {
            if (!TD.DataSet.shouldUseBulk()) {
                var params = TD.DataFilter.values();
                var qs = TD.Utils.toQueryString(params);
                TD.Utils.setAnchor(qs);
                $('a#previewData').removeClass('enabled');
                $('div#tableScroll').hide();
                $('div#nodata').hide();
                $('div#loading').show();
                $('#mainTable tbody').empty();
                $('span#previewCount').html('...');
                $('span#recordCount').html('...');
                $.getJSON('/data/lobbying/', params, function(data) {
                    if (data.length === 0) {
                        $('div#nodata').show();
                    } else {
                        for (var i = 0; i < data.length; i++) {
                            var lob = data[i];
                            var className = (i % 2 == 0) ? 'even' : 'odd';
                            // var jurisdiction = (contrib.transaction_namespace == 'urn:fec:transaction') ? 'Federal' : 'State';
                            var content = '<tr class="' + className + '">';
                            content += '<td class="year">' + lob.year + '</td>';
                            content += '<td class="amount">$' + TD.Utils.currencyFormat(lob.amount) + '</td>';
                            content += '<td class="registrant_name">' + lob.registrant_name + '</td>';
                            content += '<td class="client_name">' + lob.client_name + '</td>';
                            content += '<td class="client_parent_name">' + (lob.client_parent_name || '&nbsp;') + '</td>';
                            content += '<td class="lobbyists">';
                            for (var j = 0; j < lob.lobbyists.length; j++) {
                                var lobbyist = lob.lobbyists[j];
                                content += '<p>' + lobbyist.lobbyist_name + '</p>';
                            }
                            content += '</td>';
                            content += '</tr>';
                            $('#mainTable tbody').append(content);
                        }
                        $('span#previewCount').html(data.length);
                        $('a#downloadData').addClass('enabled');
                        $('div#nodata').hide();
                        $('div#tableScroll').show();
                    }    
                    $('div#loading').hide();
                    if (data.length < 30) {
                        $('span#recordCount').html(data.length);
                    } else {
                        $.get('/data/lobbying/count/', params, function(data) {
                            $('span#recordCount').html(data);
                        });
                    }
                });
            }
        }
    }
}

$().ready(function() {

    if ($('#datafilter').length > 0) {

        TD.DataFilter.registerFilter({
            name: 'amount',
            label: 'Amount',
            help: 'This is the amount of the contribution',
            field: TD.DataFilter.OperatorField
        });

        TD.DataFilter.registerFilter({
            name: 'client_ft',
            label: 'Client',
            help: 'Name of organization that hired or employed the lobbyist.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.DataFilter.registerFilter({
            name: 'client_parent_ft',
            label: 'Client Parent',
            help: 'Name of organization that owns the client.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.DataFilter.registerFilter({
            name: 'lobbyist_ft',
            label: 'Lobbyist',
            help: 'Name of lobbyist.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.DataFilter.registerFilter({
            name: 'registrant_ft',
            label: 'Registrant',
            help: 'The name of the person or organization that filed the lobbying registration.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.DataFilter.registerFilter({
            name: 'transaction_id',
            label: 'Registration ID',
            help: 'The ID of the lobbying registration record.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.DataFilter.registerFilter({
            name: 'year',
            label: 'Year',
            help: 'The year in which the registration was filed.',
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
        
        TD.DataFilter.init(TD.Lobbying, function() {
            var anchor = TD.Utils.getAnchor();
            if (anchor === undefined) {
                TD.Utils.setAnchor('year=2010');
                TD.DataFilter.loadHash();
            }
        });
            
    }

});