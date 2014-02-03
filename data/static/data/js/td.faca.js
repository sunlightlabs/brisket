$().ready(function() {

    TD.FacaFilter = new TD.DataFilter();

    TD.FacaFilter.path = 'faca';

    TD.FacaFilter.row_content = function(row) {
        var content = ''
        content += '<td class="committee_name">' + row.committee_name + '</td>';
        content += '<td class="agency_abbr">' + row.agency_abbr + '</td>';
        content += '<td class="member_name">' + row.member_name + '</td>';
        content += '<td class="affiliation">' + row.affiliation + '</td>';
        content += '<td class="start_date">' + row.start_date + '</td>';
        content += '<td class="end_date">' + row.end_date + '</td>';

        return content;
    }

    TD.FacaFilter.init = function() {

        TD.FacaFilter.registerFilter({
            name: 'affiliation',
            label: 'Organization',
            help: 'The name of the affiliated organization.',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var years = [];
        for (var i=2012; i>1970; i--) {
            years.push([i,i]);
        }
        TD.FacaFilter.registerFilter({
            name: 'year',
            label: 'Year',
            help: 'Years the member served on the committee',
            field: TD.DataFilter.DropDownField,
            allowMultipleFields: true,
            options: years
        });


        TD.FacaFilter.registerFilter({
            name: 'member_name',
            label: 'Member',
            help: 'Name of the committee member',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.FacaFilter.registerFilter({
            name: 'agency_name',
            label: 'Agency',
            help: 'Agency associated with the committee',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        TD.FacaFilter.registerFilter({
            name: 'committee_name',
            label: 'Committee',
            help: 'The name of the committee',
            field: TD.DataFilter.TextField,
            allowMultipleFields: true
        });

        var anchor = TD.HashMonitor.getAnchor();
        if (anchor === undefined) {
            this.loadHash();
        }
        
        TD.FacaFilter.renumberFilters();

    };

});
