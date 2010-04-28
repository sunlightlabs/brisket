TD.Field = {
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

// boolean field

TD.DataFilter.BooleanField = Object.create(TD.Field);
TD.DataFilter.BooleanField.value = function() {
    return "true"
};
TD.DataFilter.BooleanField.parseValues = function(v) { return true; }
TD.DataFilter.BooleanField.loadValues = function(v) { }
TD.DataFilter.BooleanField.render = function() {    
    var content = '';
    content += '<li id="field_' + this.id + '" class="boolean_field">';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';
    return $(content);
};

// date range field

TD.DataFilter.DateRangeField = Object.create(TD.Field);
TD.DataFilter.DateRangeField.value = function() {
    var start = $.datepicker.formatDate('yy-mm-dd', 
        this.node.find('input.date_start').datepicker('getDate'));
    var end = $.datepicker.formatDate('yy-mm-dd', 
        this.node.find('input.date_end').datepicker('getDate'));
    if (start && end) {
        return '><|' + start + '|' + end;
    }
};
TD.DataFilter.DateRangeField.parseValues = function(v) {
    var values = [];
    var parts = v.split('|');
    for (var i = 0; i < parts.length - 2; i += 3) {
        values.push([parts[i+1], parts[i+2]]);
    }
    return values;
};
TD.DataFilter.DateRangeField.loadValue = function(v) {
    var start = $.datepicker.parseDate('yy-mm-dd', v[0]);
    var end = $.datepicker.parseDate('yy-mm-dd', v[1]);
    this.node.find('input.date_start').datepicker('setDate', start);
    this.node.find('input.date_end').datepicker('setDate', end);
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

    var today = new Date();
    
    dstart.bind('change', function() {
        TD.activeFilter.node.trigger('filterchange');
    }).val('01/01/2009').datepicker({
        changeMonth: true,
        changeYear: true,
        defaultDate: new Date(2009, 0, 1),
        duration: '',
        yearRange: '1990:2010',
        onSelect: function(dateText, inst) {
            if (!dend.val()) {
                dend.datepicker('setDate',
                    dstart.datepicker('getDate'));
            }
        }
    });

    dend.bind('change', function() {
        TD.activeFilter.node.trigger('filterchange');
    }).val($.datepicker.formatDate('mm/dd/yy', today)).datepicker({
        changeMonth: true,
        changeYear: true,
        defaultDate: null,
        duration: '',
        yearRange: '1990:2010'
    });

    return this.node;

};

// drop down field
    
TD.DataFilter.DropDownField = Object.create(TD.Field);
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
    
    var node = $(content);
    node.find('select').bind('change', function() {
        TD.activeFilter.node.trigger('filterchange');
    });
    
    return node;
    
};
TD.DataFilter.DropDownField.value = function() {
    return this.node.find('select').val();
};
TD.DataFilter.DropDownField.parseValues = function(v) {
    return v.split('|');
};
TD.DataFilter.DropDownField.loadValue = function(v) {
    this.node.find('select').val(v);
};

// dual drop down field

TD.DataFilter.DualDropDownField = Object.create(TD.Field);
TD.DataFilter.DualDropDownField.render = function() {
    
    var content = '';
    content += '<li class="dualdropdown_field">';
    content += '<select id="field' + this.id + '_first" name="' + this.filter.config.name + '_first" class="first">';
    var opts = this.filter.config.options;
    for (var i = 0; i < opts.length; i++) {
        content += '<option value="' + opts[i][0] + '">' + opts[i][1] + '</option>';
    }
    content += '</select>';
    content += '<select id="field' + this.id + '_second" name="' + this.filter.config.name + '_second" class="second"></select>';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';
    
    var node = $(content);
    node.find('select').bind('change', function() {
        TD.activeFilter.node.trigger('filterchange');
    });
    node.find('select.first').bind('change', function() {
        for (var i = 0; i < opts.length; i++) {
            if (opts[i][0] == node.find('select.first').val()) {
                var content = '<option value="">All</option>';
                var opts2 = opts[i][2];
                for (var j = 0; j < opts2.length; j++) {
                    content += '<option value="' + opts2[j][0] + '">' + opts2[j][1] + '</option>';
                }
                node.find('select.second').empty().append($(content))[0].selectedIndex = 0;
                if (opts2.length == 1) {
                    node.find('select.second').hide();
                } else {
                    node.find('select.second').show();
                }
                break;
            }
        }
    }).trigger('change');
    
    return node;
    
};
TD.DataFilter.DualDropDownField.value = function() {
    return this.node.find('select.first').val() + ',' + this.node.find('select.second').val(); 
};
TD.DataFilter.DualDropDownField.parseValues = function(v) {
    return v.split('|');
};
TD.DataFilter.DualDropDownField.loadValue = function(v) {
    var values = v.split(',');
    this.node.find('select.first').val(values[0]);
    this.node.find('select.second').val(values[1]);
};

// operator field

TD.DataFilter.OperatorField = Object.create(TD.Field);
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
    
    var node = $(content);
    node.find('input').bind('keypress', function() {
        TD.activeFilter.node.trigger('filterchange');
    });
    node.find('select').bind('change', function() {
        TD.activeFilter.node.trigger('filterchange');
    });
    
    return node;
};
TD.DataFilter.OperatorField.value = function() {
    var value = this.node.find('input').val();
    if (value) {
        var operator = this.node.find('select').val();
        return operator + "|" + value;
    }
};
TD.DataFilter.OperatorField.parseValues = function(v) {
    var values = [];
    var parts = v.split('|');
    for (var i = 0; i < parts.length - 1; i += 2) {
        values.push([parts[i], parts[i+1]]);
    }
    return values;
};
TD.DataFilter.OperatorField.loadValue = function(v) {
    this.node.find('select').val(v[0]);
    this.node.find('input').val(v[1]);
};

// basic text field

TD.DataFilter.TextField = Object.create(TD.Field);
TD.DataFilter.TextField.render = function() {    
    var content = '';
    content += '<li id="field_' + this.id + '" class="text_field">';
    content += '<input id="field' + this.id + '" type="text" name="' + this.filter.config.name + '"/>';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';
    
    var node = $(content);
    node.find('input').bind('keypress', function() {
        TD.activeFilter.node.trigger('filterchange');
    });
    
    return node;
};
TD.DataFilter.TextField.value = function() {
    return this.node.find('input').val();
};
TD.DataFilter.TextField.parseValues = function(v) {
    return v.split('|')
};
TD.DataFilter.TextField.loadValue = function(v) {
    this.node.find('input').val(v);
};

/**********************************************************
 *  filter objects
 */

TD.Filter = {
    init: function(config) {
        this.allowMultipleFields = config.allowMultipleFields || false;
        this.required = config.required || false;
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
        if (TD.activeFilter) {
            TD.activeFilter.node.trigger('filterchange');
        }
        return field;
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
        TD.activeFilter.node.trigger('filterchange');
    },
    removeField: function(field) {
        delete this.fields[field.id];
        this.fieldCount--;
        field.node.remove();
        if (this.fieldCount === 0) {
            this.disable();
        }
        TD.activeFilter.node.trigger('filterchange');
    },
    render: function() {
        var content = '';
        content += '<li id="' + this.config.name + '_filter" class="filter">';
        content += '<label>' + this.config.label + '</label>';
        if (!this.required) {
            content += '<a href="#" class="remove">-</a>';
        }
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