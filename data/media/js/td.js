if (typeof Object.create !== 'function') {
    Object.create = function(o) {
        var F = function() {};
        F.prototype = o;
        return new F();
    };
}

if (typeof window.atob !== 'function') {
    window.atob = function(s) {
        return decodeURIComponent(s);
    };
}

if (typeof window.btoa !== 'function') {
    window.btoa = function(s) {
        return encodeURIComponent(s);
    };
}

var TD = {
    
    HashMonitor: {
        hash: null,
        enabled: true,
        check: function(callback) {
            if (TD.HashMonitor.enabled) {
                if (window.location.hash !== TD.HashMonitor.hash) {
                    callback(window.location.hash);
                    TD.HashMonitor.hash = window.location.hash;
                }
            }
        },
    },
    
    DataFilter: {
        registry: {},
        init: function() {
            
            TD.DataFilter.node = $('#datafilter');
            TD.DataFilter.node.bind('filterchange', function() {
                $('a#downloadData').removeClass('enabled');
                $('a#previewData').addClass('enabled');
            });
            
            $('#datafilter').bind('keypress', function(ev) {
                if (ev.which == 13) {
                    ev.stopPropagation();
                    return false;
                }
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
                    var hash = window.btoa(qs);
                    window.location.replace("/filter/#" + hash);
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
            
        },
        reset: function() {
            for (attr in TD.DataFilter.registry) {
                var filter = TD.DataFilter.registry[attr];
                if (filter.enabled) {
                    filter.disable();
                }
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
        loadHash: function() {
            var params = TD.Utils.parseAnchor();
            if (params) {
                for (attr in params) {
                    var filter = TD.DataFilter.addFilter(attr);
                    var values = filter.config.field.parseValues(params[attr]);
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
            }
        },
        preview: function() {
            if ($('#mainTable').length > 0) {
                var params = TD.DataFilter.values();
                var qs = TD.Utils.toQueryString(params);
                TD.Utils.setAnchor(qs);
                $('a#previewData').removeClass('enabled');
                $('div#tableScroll').hide();
                $('div#loading').show();
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
                    $('div#tableScroll').show();
                    $('div#loading').hide();
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
            var s = window.location.hash;
            if (s.length > 1) {
                s = s.substr(1);
                return window.atob(s);
            }
        },
        parseAnchor: function() {
            var params = {};
            var qs = TD.Utils.getAnchor();
            if (qs) {
                var terms = qs.split('&');
                for (var i = 0; i < terms.length; i++) {
                    var parts = terms[i].split('=');
                    params[parts[0]] = decodeURIComponent(parts[1]);
                }
                return params;
            }
        },
        setAnchor: function(a) {
            var hash = window.btoa(a);
            TD.HashMonitor.enabled = false;
            window.location.hash = hash;
            TD.HashMonitor.hash = window.location.hash;
            TD.HashMonitor.enabled = true;
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

setInterval(function() {
        TD.HashMonitor.check(function(hash) {
            if (hash) {
                TD.DataFilter.reset();
                TD.DataFilter.loadHash();
                TD.DataFilter.preview();
            }
        });
    }, 200);