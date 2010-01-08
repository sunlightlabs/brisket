TD = { };

TD.DataFilter = {
    
    fields: { },    // fields added to the filter
    registry: { },  // registry of allowed fields
    
    init: function() {
        
        // populate field selection drop down
        $.each(TD.DataFilter.registry, function(item) {
            var fieldDef = TD.DataFilter.registry[item];
            $('#id_filter').append('<option value="' + item + '">' + fieldDef.config.label + '</option>');
        });
        
        // bind filter form to the submit button
        $('#filterForm').bind('submit', function() {
            return false;
        });
        
        // bind button to add a new field based on field type selection
        $('#filterForm #id_filter').bind('change', function() {
            var fieldType = $('#filterForm #id_filter').val();
            var fieldPrototype = TD.DataFilter.registry[fieldType];
            if (fieldPrototype != undefined) {
                TD.DataFilter.addField(fieldPrototype.instance());
            }
            $('#filterForm #id_filter')[0].selectedIndex = 0;
            return false;
        });
        
        // bind data refresh
        $('#id_refreshdata').bind('click', function() {
            var params = { };
            var values = TD.DataFilter.values();
            for (attr in values) {
                params[attr] = _.reduce(values[attr], '', function(memo, item) {
                    if (item && item != '') {
                        if (memo) memo += '|';
                        memo += item;
                    }
                    return memo;
                });
            }
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
                $('#module_loading').hide();
                $('#module_transactions').show();
            });
            $('#module_directions').hide();
            $('#module_transactions').hide();
            $('#module_loading').show();
            return false;
        });
        
        // download data set
        $('#downloadDataSet').bind('click', function() {
            var qs = '';
            var values = TD.DataFilter.values();
            for (attr in values) {
                if (qs) qs += '&';
                var val = _.reduce(values[attr], '', function(memo, item) {
                    if (item && item != '') {
                        if (memo) memo += '|';
                        memo += item;
                    }
                    return memo;
                });
                qs += attr + '=' + encodeURIComponent(val);
            }
            window.location.replace("/data/contributions/download/?" + qs);
            return false;
        });
        
    },
    
    addField: function(field) {
        var node = field.render();              // create new DOM node
        TD.DataFilter.fields[field.id] = field; // store reference to field
        field.bind(node);                       // bind field object to DOM
        node.appendTo('#filterForm > ul');      // append DOM node to filter list
    },
    
    removeField: function(field) {
        delete TD.DataFilter.fields[field.id];  // remove reference to field
        $('#field_' + field.id).remove();       // remove field from DOM
    },
    
    values: function() {
        return _(TD.DataFilter.fields).chain()
            .map(function(item) { return item.data(); })
            .reduce({ }, function(memo, item) {
                var key = item[0], value = item[1];
                if (memo[key] === undefined) {
                    memo[key] = [];
                }
                memo[key].push(value);
                return memo;
            }).value();
    }
    
};

/* create base Field object
*/
TD.DataFilter.Field = function() { };
TD.DataFilter.Field.prototype.bind = function(node) {
    // bind DOM node to the remove field method
    var me = this;
    node.find('a.minus-button').bind('click', function() {
        TD.DataFilter.removeField(me);
        return false;
    });
};
TD.DataFilter.Field.prototype.instance = function() {
    // create a new instance of this field
    function F() { }
    F.prototype = this;
    var obj = new F();
    obj.id = Math.floor(Math.random() * 90000) + 10000;
    return obj;
};

/* TextField object has a single text input
*/
TD.DataFilter.TextField = function(config) {
    
    var that = new TD.DataFilter.Field();
    that.config = config;
    
    that.render = function() {
        var content = '';
        content += '<li id="field_' + this.id + '" class="textField">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<input id="field_' + this.id + '_' + config.name + '" type="text" name="' + config.name + '"/>';
        content += '</li>';
        return $(content);
    };
    
    that.data = function() {
        return [config.name,
            $("#field_" + this.id + " input").val()];
    };
    
    return that;
    
};

/* DropDownField displays a select box of options.
    - options -- list of [value, text] lists
*/
TD.DataFilter.DropDownField = function(config) {
    
    var that = new TD.DataFilter.Field();
    that.config = config;
    
    that.render = function() {
        var content = '';
        content += '<li id="field_' + this.id + '" class="dropDownField">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<select id="field_' + this.id + '_' + config.name + '" name="' + config.name + '">';
        for (var i = 0; i < config.options.length; i++) {
            content += '<option value="' + config.options[i][0] + '">' + config.options[i][1] + '</option>';
        }
        content += '</select>';
        content += '</li>';
        return $(content);
    };
    
    that.data = function() {
        return [config.name,
            $("#field_" + this.id + " select").val()];
    };
    
    return that;
    
};

/* OperatorField displays a text input with an operation select box:
   greater than, less than, equal to, not equal to
*/
TD.DataFilter.OperatorField = function(config) {
    
    var that = new TD.DataFilter.Field();
    that.config = config;
    
    if (!config.operators) {
        config.operators = [
            ['&gt;', 'greater than'],
            ['&lt;', 'less than'],
            ['=', 'equal to']
        ]
    }
    
    that.render = function() {
        var content = '';
        content += '<li id="field_' + this.id + '" class="operatorField">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<select id="field_' + this.id + '_' + config.name + '_operator" name="' + config.name + '_operator">';
        for (var i = 0; i < config.operators.length; i++) {
            var op = config.operators[i];
            content += '<option value="' + op[0] + '">' + op[1] + '</option>';
        }
        content += '</select>';
        content += '<input id="field_' + this.id + '_' + config.name + '" type="text" name="' + config.name + '"/>';
        content += '</li>';
        return $(content);
    };
    
    that.data = function() {
        var selector = "#field_" + this.id + "_" + config.name;
        return [config.name,
            $(selector + "_operator").val() + '|' + $(selector).val()];
    };
    
    return that;
};

/* DateRangeField displays two text input widgets that specify the dates in the range.
   DateRangeField depends on jquery-ui for the date picker widgets.
*/
TD.DataFilter.DateRangeField = function(config) {
    
    var ymdFormat = function(mdy) {
        var mdyParts = mdy.split('/');
        return mdyParts[2] + '-' + mdyParts[0] + '-' + mdyParts[1]
    };
    
    var that = new TD.DataFilter.Field();
    that.config = config;
    
    that.render = function() {
        
        var content = '';
        content += '<li id="field_' + this.id + '" class="dateRangeField">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<input id="field_' + this.id + '_' + config.name + '_start" type="text" class="date_start" name="' + config.name + '_start"/>';
        content += '<input id="field_' + this.id + '_' + config.name + '_end" type="text" class="date_end" name="' + config.name + '_end"/>';
        content += '</li>';
        
        var elem = $(content);
        
        elem.find('input.date_start').datepicker({
            changeMonth: true,
            changeYear: true,
            duration: '',
            onSelect: function(dateText, inst) {
                var endWidget = elem.find('input.date_end');
                if (!endWidget.val()) {
                    var now = elem.find('input.date_start').datepicker('getDate');
                    endWidget.datepicker('setDate', now);
                }
            },
            yearRange: '1990:2010'
        });
        elem.find('input.date_end').datepicker({
            changeMonth: true,
            changeYear: true,
            duration: '',
            yearRange: '1990:2010'
        });
        
        return elem;
        
    };
    
    that.data = function() {
        var inputs = $("#field_" + this.id + " input");
        var start = ymdFormat(inputs[0].value);
        var end = ymdFormat(inputs[1].value);
        return [config.name, '><|' + start + '|' + end];
    };
    
    return that;
    
};


TD.DataFilter.EntityField = function(config) {
    
    var that = new TD.DataFilter.Field();
    that.config = config;
    
    var parseSuggest = function(res) {
        var params = res.split(',');
        var val = params[1];
        for (var i = 2; i < params.length; i++) {
            val += ',' + params[i];
        }
        return [params[0], val];
    };
    
    that.render = function() {
        
        var content = '';
        content += '<li id="field_' + this.id + '" class="entityField" data-id="' + this.id + '">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<ul class="entity_values"></ul>';
        content += '<input id="field_' + this.id + '_' + config.name + '" type="text" name="' + config.name + '"/>';
        content += '</li>';
        
        var elem = $(content);
        
        var control = elem.find('input');
        
        var ac = control.autocomplete('/data/entities/' + config.name + '/', {
            delay: 600000000,
            max: 20,
            minChars: 2,
            mustMatch: true,
            formatItem: function(row, position, count, terms) {
                var params = parseSuggest(row[0]);
                if (position == count) {
                    control.removeClass('loading');
                }
                return '<span data-id="' + params[0] + '">' + params[1] + '</span>';
            },
            selectFirst: true
        });

        control.bind('result', function(ev) {
            $(this).removeClass('loading');
        });

        control.bind('keydown', function(e) {
            if (e.which == 13 && control.val() != '') {
                $(this).addClass('loading');
                $(this).trigger('suggest');
            }
        });
    
        control.result(function(ev, li) {
            if (li && li[0]) {
                var params = parseSuggest(li[0]);
                var fieldId = elem.attr('data-id');
                TD.DataFilter.fields[fieldId].addSelection(params[0], params[1]);
            }
        });
        
        return elem;
        
    };
    
    that.data = function() {
        
        var value = '';
        
        $("#field_" + this.id + " ul.entity_values li").each(function(i) {
            var item = $(this).attr('data-id');
            if (item) {
                if (value) value += '|';
                value += item;
            }
        });
        
        return [config.name, value];
        
    };
    
    that.addSelection = function(id, name) {
        var s = $('<li data-id="' + id + '">' + name + '</li>');
        s.appendTo("#field_" + this.id + " ul");
        $("#field_" + this.id + " input").val('');
    };
    
    return that;
    
};


/* main search box functionality
*/ 
TD.SearchBox = {
    
    isValid: false,
    
    init: function() {
        
        // on focus, clear text if equal to title
        // on blur, set value to title if no value is specified
        // trigger blur to set value to title
        $('#searchBtn').bind('focus', function() {
            if (this.value === this.title) {
                this.value = '';
                TD.SearchBox.isValid = true;
            }
        }).bind('blur', function() {
            if (!this.value) {
                this.value = this.title;
                TD.SearchBox.isValid = false;
            }
        }).trigger('blur');
        
        // do search
        $('button.searchBtn').bind('click', function() {
            var entityId = $('#searchEntityID').val();
            if (TD.SearchBox.isValid && entityId) {
                alert('ok!');
            } else {
                alert('not good');
            }
            return false;
        });
        
    }
    
};

/* UI modifiers
*/ 
TD.UI = {
    fluid: function() {
        $('body').addClass('filteredSearch');
    },
    fixed: function() {
        $('body').removeClass('filteredSearch');
    }
};

/* main ready function
*/
$().ready(function() {
    
    TD.SearchBox.init();
    
    TD.DataFilter.registry = {
        
        amount: TD.DataFilter.OperatorField({
            label: 'Amount',
            name: 'amount',
            helper: 'Amount of contribution in dollars',
            operators: [
                ['&gt;', 'greater than'],
                ['&lt;', 'less than'],
                ['&gt;&lt;', 'between']
            ]
        }),

        cycle: TD.DataFilter.DropDownField({
            label: 'Cycle',
            name: 'cycle',
            helper: 'Federal election cycle',
            options: [
                ['1990','1990'], ['1992','1992'], ['1994','1994'], ['1996','1996'],
                ['1998','1998'], ['2000','2000'], ['2002','2002'], ['2004','2004'],
                ['2006','2006'], ['2008','2008'], ['2010','2010']
            ]
        }),

        datestamp: TD.DataFilter.DateRangeField({
            label: 'Date',
            name: 'date',
            helper: 'Date of contribution'
        }),
        
        state: TD.DataFilter.DropDownField({
            label: 'State',
            name: 'state',
            helper: 'State from which the contribution was made',
            options: [
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
        }),

        jurisdiction: TD.DataFilter.DropDownField({
            label: 'Jurisdiction',
            name: 'transaction_namespace',
            helper: 'State or federal seat',
            options: [
                ['urn:fec:transaction','Federal'],
                ['urn:nimsp:transaction','State']
            ]
        }),
        
        seat: TD.DataFilter.DropDownField({
            label: 'Seat',
            name: 'seat',
            helper: 'Type of seat for which candidate is running',
            options: [
                ['federal:senate', 'US Senate'],
                ['federal:house', 'US House of Representatives'],
                ['federal:president', 'US President'],
                ['state:upper', 'State Upper Chamber'],
                ['state:lower', 'State Lower Chamber'],
                ['state:governor', 'State Governor']
            ]
        }),
        
        // entity fields
        
        contributor: TD.DataFilter.EntityField({
            label: 'Contributor',
            name: 'contributor',
            helper: 'Name of individual or PAC that made contribution'
        }),
                
        recipient: TD.DataFilter.EntityField({
            label: 'Recipient',
            name: 'recipient',
            helper: 'Name of candidate or PAC that received contribution'
        }),

        organization: TD.DataFilter.EntityField({
            label: 'Organization',
            name: 'organization',
            helper: 'Corporation related to contribution'
        })
        
    }
    
    TD.DataFilter.init();
    
});