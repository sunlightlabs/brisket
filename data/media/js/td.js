var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(a){var b="";var c,chr2,chr3,enc1,enc2,enc3,enc4;var i=0;a=Base64._utf8_encode(a);while(i<a.length){c=a.charCodeAt(i++);chr2=a.charCodeAt(i++);chr3=a.charCodeAt(i++);enc1=c>>2;enc2=((c&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64}else if(isNaN(chr3)){enc4=64}b=b+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4)}return b},decode:function(a){var b="";var c,chr2,chr3;var d,enc2,enc3,enc4;var i=0;a=a.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(i<a.length){d=this._keyStr.indexOf(a.charAt(i++));enc2=this._keyStr.indexOf(a.charAt(i++));enc3=this._keyStr.indexOf(a.charAt(i++));enc4=this._keyStr.indexOf(a.charAt(i++));c=(d<<2)|(enc2>>4);chr2=((enc2&15)<<4)|(enc3>>2);chr3=((enc3&3)<<6)|enc4;b=b+String.fromCharCode(c);if(enc3!=64){b=b+String.fromCharCode(chr2)}if(enc4!=64){b=b+String.fromCharCode(chr3)}}b=Base64._utf8_decode(b);return b},_utf8_encode:function(a){a=a.replace(/\r\n/g,"\n");var b="";for(var n=0;n<a.length;n++){var c=a.charCodeAt(n);if(c<128){b+=String.fromCharCode(c)}else if((c>127)&&(c<2048)){b+=String.fromCharCode((c>>6)|192);b+=String.fromCharCode((c&63)|128)}else{b+=String.fromCharCode((c>>12)|224);b+=String.fromCharCode(((c>>6)&63)|128);b+=String.fromCharCode((c&63)|128)}}return b},_utf8_decode:function(a){var b="";var i=0;var c=c1=c2=0;while(i<a.length){c=a.charCodeAt(i);if(c<128){b+=String.fromCharCode(c);i++}else if((c>191)&&(c<224)){c2=a.charCodeAt(i+1);b+=String.fromCharCode(((c&31)<<6)|(c2&63));i+=2}else{c2=a.charCodeAt(i+1);c3=a.charCodeAt(i+2);b+=String.fromCharCode(((c&15)<<12)|((c2&63)<<6)|(c3&63));i+=3}}return b}}

if (typeof Object.create !== 'function') {
    Object.create = function(o) {
        var F = function() {};
        F.prototype = o;
        return new F();
    };
}

if (typeof window.atob !== 'function') {
    window.atob = function(s) {
        return Base64.decode(s);
    };
}

if (typeof window.btoa !== 'function') {
    window.btoa = function(s) {
        return Base64.encode(s);
    };
}


var TD = {
    activeFilter: null,
    init: function() {
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

        TD.HashMonitor.enabled = true;

        TD.HashMonitor.interval = setInterval(function() {
            TD.HashMonitor.check(function(hash) {
                if (hash) {
                    TD.activeFilter.reset();
                    TD.activeFilter.loadHash();
                    TD.activeFilter.preview();
                }
            });
        }, 200);
    },
    HashMonitor: {
        hash: null,
        enabled: false,
        interval: null,
        check: function(callback) {
            if (TD.HashMonitor.enabled) {
                if (window.location.hash !== TD.HashMonitor.hash) {
                    callback(window.location.hash);
                    TD.HashMonitor.hash = window.location.hash;
                }
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
                if (qs) qs += '&';
                qs += attr + '=' + encodeURIComponent(obj[attr]);
            }
            return qs
        },
        ymdFormat: function(mdy) {
            var mdyParts = mdy.split('/');
            return mdyParts[2] + '-' + mdyParts[0] + '-' + mdyParts[1]
        }
    }
}

TD.DataFilter = function() {
    var that = this;
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
            window.location.replace(that.previewPath + "#" + hash);
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
                window.location.replace(that.downloadPath + "?" + qs);
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
    var params = TD.Utils.parseAnchor();
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
