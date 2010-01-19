if (typeof Object.create !== 'function') {
    Object.create = function(o) {
        var F = function() {};
        F.prototype = o;
        return new F();
    };
}

var TD = {
    
    DataFilter: {
        registry: {},
        init: function() {
            
            TD.DataFilter.node = $('#datafilter');
            TD.DataFilter.node.bind('filterchange', function() {
                $('a#downloadData').removeClass('enabled');
                $('a#previewData').addClass('enabled');
            });
            
            $('#datafilter select#filterselect').bind('change', function() {
                var filterName = this.value;
                if (filterName) {
                    TD.DataFilter.addFilter(filterName);
                }
                this.selectedIndex = 0;
                return false;
            });
            
            $('a#previewData').bind('click', function() {
                if ($('#mainTable').length == 0) {
                    // no main table, forward to filter page
                    var qs = TD.Utils.toQueryString(TD.DataFilter.values());
                    window.location.replace("/filter/#" + qs);
                } else {
                    TD.DataFilter.preview();
                }
                return false;
            });
            
            $('a#downloadData').bind('click', function() {
                var qs = TD.Utils.toQueryString(TD.DataFilter.values());
                window.location.replace("/data/contributions/download/?" + qs);
                return false;
            });
            
            var params = TD.Utils.parseAnchor();
            for (attr in params) {
                var filter = TD.DataFilter.addFilter(attr);
                var values = filter.config.field.parseValues(params[attr]);
                //alert(values);
                for (var i = 0; i < values.length; i++) {
                    var field = null;
                    if (filter.fieldCount < i + 1) {
                        field = filter.addField();
                    } else {
                        for (fid in filter.fields) {
                            field = filter.fields[fid];
                            break;
                        }
                    }
                    field.loadValue(values[i]);
                }
            }
            if (params) {
                TD.DataFilter.preview();
            }
            
        },
        registerFilter: function(config) {
            var filter = Object.create(TD.DataFilter.Filter);
            filter.init(config);
            TD.DataFilter.registry[config.name] = filter;
            var option = $('<option value="' + config.name + '">' + config.label + '</option>');
            $('#datafilter select#filterselect').append(option);
        },
        addFilter: function(filterName) {
            var filter = TD.DataFilter.registry[filterName];
            if (filter != undefined) {
                if (filter.enabled) {
                    filter.addField();
                    TD.DataFilter.primaryFilter(filter);
                } else {
                    $('#datafilter ul#filters').prepend(filter.render());
                    filter.enable();
                    filter.addField();
                }
            }
            return filter;
        },
        preview: function() {
            if ($('#mainTable').length > 0) {
                var params = TD.DataFilter.values();
                var qs = TD.Utils.toQueryString(params);
                TD.Utils.setAnchor(qs);
                $('a#previewData').removeClass('enabled');
                $('#mainTable tbody').empty();
                $.getJSON('/data/contributions/', params, function(data) {
                    for (var i = 0; i < data.length; i++) {
                        var contrib = data[i];
                        var className = (i % 2 == 0) ? 'even' : 'odd';
                        var jurisdiction = (contrib.transaction_namespace == 'urn:fec:transaction') ? 'Federal' : 'State';
                        var content = '<tr class="' + className + '">';
                        content += '<td>' + jurisdiction + '</td>';
                        content += '<td>' + (contrib.datestamp || '&nbsp;') + '</td>';
                        content += '<td>$' + contrib.amount + '</td>';
                        content += '<td>' + contrib.contributor_name + '</td>';
                        content += '<td>' + contrib.contributor_city + ', ' + contrib.contributor_state + '</td>';
                        content += '<td>' + contrib.recipient_name + '</td>';
                        content += '</tr>';
                        $('#mainTable tbody').append(content);
                    }
                    $('a#downloadData').addClass('enabled');
                });
            }
        },
        primaryFilter: function(filter) {
            $('#datafilter ul#filters').prepend(filter.node);
        },
        values: function() {
            var params = {};
            for (name in TD.DataFilter.registry) {
                var filter = TD.DataFilter.registry[name];
                if (filter.enabled) {
                    var value = filter.value();
                    if (value) {
                        params[name] = value;
                    }
                }
            }
            return params;
        },
        registerFilter: function(config) {
            var filter = Object.create(TD.DataFilter.Filter);
            filter.init(config);
            TD.DataFilter.registry[config.name] = filter;
            var option = $('<option value="' + config.name + '">' + config.label + '</option>');
            $('#datafilter select#filterselect').append(option);
        }
    },
    
    Utils: {
        getAnchor: function() {
            var a = window.location.hash;
            if (a.indexOf('#') == 0) {
                if (a.length > 1) {
                    a = a.substr(1);
                } else {
                    a = '';
                }
            }
            return decodeURIComponent(a);
        },
        parseAnchor: function() {
            var params = {};
            var qs = TD.Utils.getAnchor();
            if (qs) {
                var terms = qs.split('&');
                for (var i = 0; i < terms.length; i++) {
                    var parts = terms[i].split('=');
                    params[parts[0]] = parts[1];
                }
            }
            return params;
        },
        setAnchor: function(a) {
            window.location.hash = encodeURIComponent(a);
        },
        toQueryString: function(obj) {
            var qs = ''
            for (attr in obj) {
                if (qs) {
                    qs += '&';
                }
                qs += attr + '=' + encodeURIComponent(obj[attr]);
            }
            return qs
        },
        ymdFormat: function(mdy) {
            var mdyParts = mdy.split('/');
            return mdyParts[2] + '-' + mdyParts[0] + '-' + mdyParts[1]
        }
    }
    
};