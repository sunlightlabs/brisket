// base64 algorithm for IE browsers
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(a){var b="";var c,chr2,chr3,enc1,enc2,enc3,enc4;var i=0;a=Base64._utf8_encode(a);while(i<a.length){c=a.charCodeAt(i++);chr2=a.charCodeAt(i++);chr3=a.charCodeAt(i++);enc1=c>>2;enc2=((c&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64}else if(isNaN(chr3)){enc4=64}b=b+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4)}return b},decode:function(a){var b="";var c,chr2,chr3;var d,enc2,enc3,enc4;var i=0;a=a.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(i<a.length){d=this._keyStr.indexOf(a.charAt(i++));enc2=this._keyStr.indexOf(a.charAt(i++));enc3=this._keyStr.indexOf(a.charAt(i++));enc4=this._keyStr.indexOf(a.charAt(i++));c=(d<<2)|(enc2>>4);chr2=((enc2&15)<<4)|(enc3>>2);chr3=((enc3&3)<<6)|enc4;b=b+String.fromCharCode(c);if(enc3!=64){b=b+String.fromCharCode(chr2)}if(enc4!=64){b=b+String.fromCharCode(chr3)}}b=Base64._utf8_decode(b);return b},_utf8_encode:function(a){a=a.replace(/\r\n/g,"\n");var b="";for(var n=0;n<a.length;n++){var c=a.charCodeAt(n);if(c<128){b+=String.fromCharCode(c)}else if((c>127)&&(c<2048)){b+=String.fromCharCode((c>>6)|192);b+=String.fromCharCode((c&63)|128)}else{b+=String.fromCharCode((c>>12)|224);b+=String.fromCharCode(((c>>6)&63)|128);b+=String.fromCharCode((c&63)|128)}}return b},_utf8_decode:function(a){var b="";var i=0;var c=c1=c2=0;while(i<a.length){c=a.charCodeAt(i);if(c<128){b+=String.fromCharCode(c);i++}else if((c>191)&&(c<224)){c2=a.charCodeAt(i+1);b+=String.fromCharCode(((c&31)<<6)|(c2&63));i+=2}else{c2=a.charCodeAt(i+1);c3=a.charCodeAt(i+2);b+=String.fromCharCode(((c&15)<<12)|((c2&63)<<6)|(c3&63));i+=3}}return b}}
if (typeof window.atob !== 'function') {
    window.atob = function(s) { return Base64.decode(s); };
}
if (typeof window.btoa !== 'function') {
    window.btoa = function(s) { return Base64.encode(s); };
}

// object creation
if (typeof Object.create !== 'function') {
    Object.create = function(o) {
        var F = function() {};
        F.prototype = o;
        return new F();
    };
}

// main TransparencyData namespace
var TD = {
    
    // stores the active filter
    activeFilter: null,
    
    init: function() {
        
        // create popup dialogs
        $('#downloading').dialog({
            autoOpen: false,
            buttons: { "OK": function() { $(this).dialog("close"); } },
            draggable: false,
            modal: true,
            resizable: false,
            title: 'Downloading...'
        });
        $('#suggestbulk').dialog({
            autoOpen: false,
            buttons: { "OK": function() { $(this).dialog("close"); } },
            draggable: false,
            modal: true,
            resizable: false,
            title: 'Bulk Downloads'
        });

        // run hashmonitor
        TD.HashMonitor.init();
        
    },
    
    // monitors the URL hash for changes
    // provides methods for working with setting the hash/anchor
    HashMonitor: {
        hash: null,
        enabled: false,
        interval: null,
        init: function() {
            this.enabled = true;
            this.interval = setInterval(function() {
                TD.HashMonitor.check(function(hash) {
                    if (hash) {
                        TD.activeFilter.reset();
                        TD.activeFilter.loadHash();
                        TD.activeFilter.preview();
                    }
                });
            }, 200);
        },
        check: function(callback) {
            if (TD.HashMonitor.enabled) {
                if (window.location.hash !== TD.HashMonitor.hash) {
                    callback(window.location.hash);
                    TD.HashMonitor.hash = window.location.hash;
                }
            }
        },
        getAnchor: function() {
            var s = window.location.hash;
            if (s.length > 1) {
                s = s.substr(1);
                return window.atob(s);
            }
        },
        setAnchor: function(a) {
            var hash = window.btoa(a);
            this.enabled = false;
            window.location.hash = hash;
            this.hash = window.location.hash;
            this.enabled = true;
        },
        parseAnchor: function() {
            var params = {};
            var qs = this.getAnchor();
            if (qs) {
                var terms = qs.split('&');
                for (var i = 0; i < terms.length; i++) {
                    var parts = terms[i].split('=');
                    params[parts[0]] = decodeURIComponent(parts[1]);
                }
                return params;
            }
        }
    },
    
    Utils: {
        cityStateFormat: function(city, state) {
            if (state != undefined && state != '') {
                var fmt = state;
                if (city != undefined && city != '') {
                    fmt = city + ', ' + fmt;
                }
                return fmt;
            }
            return '';
        },
        currencyFormat: function(s) {
            return $.currency(parseFloat(s));
        },
        toQueryString: function(obj) {
            var qs = ''
            for (attr in obj) {
                if (qs) qs += '&';
                qs += attr + '=' + encodeURIComponent(obj[attr]);
            }
            return qs
        },
        ymdFormat: function(mdy) {
            var mdyParts = mdy.split('/');
            return mdyParts[2] + '-' + mdyParts[0] + '-' + mdyParts[1]
        }
    },
    
    STATES: [
             ['AL', 'Alabama'],          ['AK', 'Alaska'],       ['AZ', 'Arizona'],      ['AR', 'Arkansas'],
             ['CA', 'California'],       ['CO', 'Colorado'],     ['CT', 'Connecticut'],  ['DE', 'Delaware'],
             ['DC', 'District of Columbia'],
             ['FL', 'Florida'],          ['GA', 'Georgia'],      ['HI', 'Hawaii'],       ['ID', 'Idaho'],
             ['IL', 'Illinois'],         ['IN', 'Indiana'],      ['IA', 'Iowa'],         ['KS', 'Kansas'],
             ['KY', 'Kentucky'],         ['LA', 'Louisiana'],    ['ME', 'Maine'],        ['MD', 'Maryland'],
             ['MA', 'Massachusetts'],    ['MI', 'Michigan'],     ['MN', 'Minnesota'],    ['MS', 'Mississippi'],
             ['MO', 'Missouri'],         ['MT', 'Montana'],      ['NE', 'Nebraska'],     ['NV', 'Nevada'],
             ['NH', 'New Hampshire'],    ['NJ', 'New Jersey'],   ['NM', 'New Mexico'],   ['NY', 'New York'],
             ['NC', 'North Carolina'],   ['ND', 'North Dakota'], ['OH', 'Ohio'],         ['OK', 'Oklahoma'],
             ['OR', 'Oregon'],           ['PA', 'Pennsylvania'], ['RI', 'Rhode Island'], ['SC', 'South Carolina'],
             ['SD', 'South Dakota'],     ['TN', 'Tennessee'],    ['TX', 'Texas'],        ['UT', 'Utah'],
             ['VT', 'Vermont'],          ['VA', 'Virginia'],     ['WA', 'Washington'],   ['WV', 'West Virginia'],
             ['WI', 'Wisconsin'],        ['WY', 'Wyoming']
         ]
}

TD.DataFilter = function() {
    this.registry = {};
    this.node = $();
    this.downloadNode = $();
    this.previewNode = $();
};
TD.DataFilter.prototype.bindDataFilter = function(sel) {
    var that = this;
    this.node = $(sel);
    this.node.bind('keypress', function(ev) {
        if (ev.which == 13) {
            ev.stopPropagation();
            that.previewNode.trigger('click');
            return false;
        }
    }).bind('filterchange', function() {
        that.downloadNode.removeClass('enabled');
        that.previewNode.addClass('enabled');
    }).find('select#filterselect').bind('change', function() {
        that.addFilter(this.value);
        this.selectedIndex = 0;
        return false;
    });
};
TD.DataFilter.prototype.bindPreview = function(sel) {
    var that = this;
    this.previewNode = $(sel);
    this.previewNode.bind('click', function() {
        if ($('#mainTable').length == 0) {
            // no main table, forward to filter page
            var qs = TD.Utils.toQueryString(that.values());
            var hash = window.btoa(qs);
            window.location.replace("/" + that.path + "/#" + hash);
        } else if ($(this).hasClass('enabled')) {
            that.preview();
        }
        return false;
    });
};
TD.DataFilter.prototype.bindDownload = function(sel) {
    var that = this;
    this.downloadNode = $(sel);
    this.downloadNode.bind('click', function() {
        var node = $(this);
        if (node.hasClass('enabled')) {
            node.removeClass('enabled');
            if (!that.shouldUseBulk()) {
                $('#downloading').dialog('open');
                var qs = TD.Utils.toQueryString(that.values());
                window.location.replace("/" + that.path + "/download/?" + qs);
            }
        }
        return false;
    });
};
TD.DataFilter.prototype.reset = function() {
    for (attr in this.registry) {
        var filter = this.registry[attr];
        if (filter.enabled) {
            filter.disable();
        }
    }
};
TD.DataFilter.prototype.registerFilter = function(config) {
    var filter = Object.create(TD.Filter);
    filter.init(config);
    this.registry[config.name] = filter;
    var option = $('<option value="' + config.name + '">' + config.label + '</option>');
    this.node.find('select#filterselect').append(option);
};
TD.DataFilter.prototype.addFilter = function(filterName) {
    var filter = this.registry[filterName];
    if (filter != undefined) {
        if (filter.enabled) {
            filter.addField();
            this.primaryFilter(filter);
        } else {
            this.node.find('ul#filters').prepend(filter.render());
            filter.enable();
            filter.addField();
        }
    }
    return filter;
};
TD.DataFilter.prototype.filterCount = function() {
    var count = 0;
    for (attr in this.registry) {
        if (this.registry[attr].enabled) {
            count++;
        }
    }
    return count;
};
TD.DataFilter.prototype.primaryFilter = function(filter) {
    this.node.find('ul#filters').prepend(filter.node);
};
TD.DataFilter.prototype.values = function() {
    var params = {};
    for (name in this.registry) {
        var filter = this.registry[name];
        if (filter.enabled) {
            var value = filter.value();
            if (value) {
                params[name] = value;
            }
        }
    }
    return params;
};
TD.DataFilter.prototype.loadHash = function() {
    var params = TD.HashMonitor.parseAnchor();
    if (params) {
        for (attr in params) {
            var filter = this.addFilter(attr);
            if (filter) {
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
    }
};
TD.DataFilter.prototype.preview = function() {
    if ($('#mainTable').length > 0) {
        if (!this.shouldUseBulk()) {
            var that = this;
            var params = this.values();
            var qs = TD.Utils.toQueryString(params);
            TD.HashMonitor.setAnchor(qs);
            this.previewNode.removeClass('enabled');
            $('div#tableScroll').hide();
            $('div#nodata').hide();
            $('div#loading').show();
            $('#mainTable tbody').empty();
            $('span#previewCount').html('...');
            $('span#recordCount').html('...');
            $.getJSON('/data/' + this.path, params, function(data) {
                if (data.length === 0) {
                    $('div#nodata').show();
                } else {
                    for (var i = 0; i < data.length; i++) {
                        var className = (i % 2 == 0) ? 'even' : 'odd';
                        var content = '<tr class="' + className + '">';
                        content += that.row_content(data[i]);
                        content += '</tr>';
                        $('#mainTable tbody').append(content);
                    }
                    $('span#previewCount').html(data.length);
                    that.downloadNode.addClass('enabled');
                    $('div#nodata').hide();
                    $('div#tableScroll').show();
                }    
                $('div#loading').hide();
                if (data.length < 30) {
                    $('span#recordCount').html(data.length);
                } else {
                    $.get("/data/" + that.path + "/count/", params, function(data) {
                        $('span#recordCount').html(data);
                    });
                }
            });
        }
    }
};
TD.DataFilter.prototype.shouldUseBulk = function() {
    var values = _.keys(this.values());
    values = _.without.apply(_, [values].concat(this.ignoreForBulk));

    var useBulk = values.length == 0;
    if (useBulk) {
        $('#suggestbulk').dialog('open');    
    }
    return useBulk;
};