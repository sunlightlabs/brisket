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
            $('#datafilter select#filterselect').bind('change', function() {
                var filterName = this.value;
                if (filterName) {
                    TD.DataFilter.addFilter(filterName);
                }
                this.selectedIndex = 0;
                return false;
            });
            $('#datafilter a.test').bind('click', function() {
                var values = TD.DataFilter.values();
                var qs = _.reduce(values, '', function(memo, item, name) {
                    if (memo) {
                        memo += '&';
                    }
                    memo += name + '=' + item;
                    return memo;
                });
                alert(qs);
                return false;
            });
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
        ymdFormat: function(mdy) {
            var mdyParts = mdy.split('/');
            return mdyParts[2] + '-' + mdyParts[0] + '-' + mdyParts[1]
        }
    }
    
};

/**********************************************************
 *  fields objects
 */

TD.DataFilter.Field = {
    bind: function(node) {
        var me = this;
        this.node = node;
        if (this.filter.allowMultipleFields) {
            node.find('a.remove').bind('click', function() {
                me.filter.removeField(me);
                return false;
            });
        } else {
            node.find('a.remove').remove();
        }
    }
};

// date range field

TD.DataFilter.DateRangeField = Object.create(TD.DataFilter.Field);
TD.DataFilter.DateRangeField.value = function() {
    var start = $.datepicker.formatDate('yy-mm-dd', 
        this.node.find('input.date_start').datepicker('getDate'));
    var end = $.datepicker.formatDate('yy-mm-dd', 
        this.node.find('input.date_end').datepicker('getDate'));
    if (start && end) {
        return '><|' + start + '|' + end;
    }
};
TD.DataFilter.DateRangeField.render = function() {
    
    var content = '';
    content += '<li class="daterange_field">'
    content += 'between <input type="text" class="date_start" name="' + this.filter.config.name + '_start"/>';
    content += 'and <input type="text" class="date_end" name="' + this.filter.config.name + '_end"/>';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';

    this.node = $(content);
    var dstart = this.node.find('input.date_start');
    var dend = this.node.find('input.date_end');

    dstart.datepicker({
        changeMonth: true,
        changeYear: true,
        duration: '',
        yearRange: '1990:2010',
        onSelect: function(dateText, inst) {
            if (!dend.val()) {
                dend.datepicker('setDate',
                    dstart.datepicker('getDate'));
            }
        }
    });

    dend.datepicker({
        changeMonth: true,
        changeYear: true,
        duration: '',
        yearRange: '1990:2010'
    });

    return this.node;

};

// drop down field
    
TD.DataFilter.DropDownField = Object.create(TD.DataFilter.Field);
TD.DataFilter.DropDownField.render = function() {
    
    var content = '';
    content += '<li class="dropdown_field">';
    content += '<select id="field' + this.id + '" name="' + this.filter.config.name + '">';
    var opts = this.filter.config.options;
    for (var i = 0; i < opts.length; i++) {
        content += '<option value="' + opts[i][0] + '">' + opts[i][1] + '</option>';
    }
    content += '</select>';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';
    return $(content);
    
};
TD.DataFilter.DropDownField.value = function() {
    return this.node.find('select').val();
};

// operator field

TD.DataFilter.OperatorField = Object.create(TD.DataFilter.Field);
TD.DataFilter.OperatorField.render = function() {
    var operators = this.filter.config.operators || [
        ['&gt;', 'greater than'],
        ['&lt;', 'less than']
    ];
    var content = '';
    content += '<li class="operator_field">';
    content += '<select id="field' + this.id + '" name="' + this.filter.config.name + '_operator">';
    for (var i = 0; i < operators.length; i++) {
        var op = operators[i];
        content += '<option value="' + op[0] + '">' + op[1] + '</option>';
    }
    content += '</select>';
    content += '<input id="field' + this.id + '" type="text" name="' + this.filter.config.name + '"/>';
    content += '</li>';
    return $(content);
};
TD.DataFilter.OperatorField.value = function() {
    var value = this.node.find('input').val();
    if (value) {
        var operator = this.node.find('select').val();
        return operator + "|" + value;
    }
};

// basic text field

TD.DataFilter.TextField = Object.create(TD.DataFilter.Field);
TD.DataFilter.TextField.render = function() {    
    var content = '';
    content += '<li id="field_' + this.id + '" class="text_field">';
    content += '<input id="field' + this.id + '" type="text" name="' + this.filter.config.name + '"/>';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';
    return $(content);
};
TD.DataFilter.TextField.value = function() {
    return this.node.find('input').val();
};

/**********************************************************
 *  filter objects
 */

TD.DataFilter.Filter = {
    init: function(config) {
        this.allowMultipleFields = config.allowMultipleFields || false;
        this.enabled = false;
        this.fields = {};
        this.fieldCount = 0;
        this.config = config;
    },
    addField: function() {
        if (this.fieldCount > 0 && !this.allowMultipleFields) {
            return;
        }
        var field = Object.create(this.config.field);
        field.id = '' + Math.floor(Math.random() * 90000) + 10000;
        field.filter = this;
        var elem = field.render();
        field.bind(elem);
        this.node.find('ul.fields').append(elem);
        this.fields[field.id] = field;
        this.fieldCount++;
    },
    bind: function(node) {
        var me = this;
        me.node = node;
        node.find('a.remove').bind('click', function() {
            me.disable();
            return false;
        });
        node.find('a.add').bind('click', function() {
            me.addField();
            return false;
        });
    },
    enable: function() {
        this.enabled = true;
    },
    disable: function() {
        this.enabled = false;
        for (fieldId in this.fields) {
            this.removeField(this.fields[fieldId]);
        }
        this.node.remove();
    },
    removeField: function(field) {
        delete this.fields[field.id];
        this.fieldCount--;
        field.node.remove();
        if (this.fieldCount === 0) {
            this.disable();
        }
    },
    render: function() {
        var content = '';
        content += '<li id="' + this.config.name + '_filter" class="filter">';
        content += '<label>' + this.config.label + '</label>';
        content += '<a href="#" class="remove">-</a>';
        if (this.allowMultipleFields) {
            content += '<a href="#" class="add">+</a>';
        }
        content += '<p class="help">' + this.config.help + '</p>';
        content += '<ul class="fields"></ul>';
        content += '</li>';
        var node = $(content);
        this.bind(node);
        return node;
    },
    value: function() {
        return _.reduce(this.fields, '', function(memo, item) {
            var value = item.value();
            if (value) {
                if (memo) {
                    memo += '|';
                }
                memo += '' + value;
            }
            return memo;
        });
    }
};

/**********************************************************
 *  declaration of fields
 */
 
$().ready(function() {
    
    TD.DataFilter.init();

    TD.DataFilter.registerFilter({
        name: 'amount',
        label: 'Amount',
        help: 'This is the amount of the contribution',
        field: TD.DataFilter.OperatorField
    });
    
    TD.DataFilter.registerFilter({
        name: 'cycle',
        label: 'Cycle',
        help: 'Election cycles. Odd cycles have only state-level contributions',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['1990','1990'], ['1991','1991'], ['1992','1992'],
            ['1993','1993'], ['1994','1994'], ['1995','1995'],
            ['1996','1996'], ['1997','1997'], ['1998','1998'],
            ['1999','1999'], ['2000','2000'], ['2001','2001'],
            ['2002','2002'], ['2003','2003'], ['2004','2004'],
            ['2005','2005'], ['2006','2006'], ['2007','2007'],
            ['2008','2008'], ['2009','2009'], ['2010','2010']
        ]
    });
    
    TD.DataFilter.registerFilter({
        name: 'contributor_ft',
        label: 'Contributor',
        help: 'Name of individual or PAC that made contribution',
        field: TD.DataFilter.TextField
    });
    
    TD.DataFilter.registerFilter({
        name: 'date',
        label: 'Date',
        help: 'This is the date of the contribution',
        field: TD.DataFilter.DateRangeField
    });
    
    TD.DataFilter.registerFilter({
        name: 'transaction_namespace',
        label: 'Federal/State',
        help: 'State or federal office',
        field: TD.DataFilter.DropDownField,
        options: [
            ['urn:fec:transaction','Federal'],
            ['urn:nimsp:transaction','State']
        ]
    });
    
    TD.DataFilter.registerFilter({
        label: 'Office',
        name: 'seat',
        help: 'Office for which candidate is running',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
        options: [
            ['federal:senate', 'US Senate'],
            ['federal:house', 'US House of Representatives'],
            ['federal:president', 'US President'],
            ['state:upper', 'State Upper Chamber'],
            ['state:lower', 'State Lower Chamber'],
            ['state:governor', 'State Governor']
        ]
    });
    
    TD.DataFilter.registerFilter({
        name: 'organization_ft',
        label: 'Employer',
        help: 'Employer of individual that made contribution',
        field: TD.DataFilter.TextField
    });
    
    TD.DataFilter.registerFilter({
        name: 'recipient_ft',
        label: 'Recipient',
        help: 'Name of candidate or PAC that received contribution',
        field: TD.DataFilter.TextField
    });
    
    TD.DataFilter.registerFilter({
        name: 'state',
        label: 'State',
        help: 'State from which the contribution was made',
        field: TD.DataFilter.DropDownField,
        allowMultipleFields: true,
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
    });
    
    TD.DataFilter.addFilter('date');

});