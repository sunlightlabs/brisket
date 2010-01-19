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
TD.DataFilter.DateRangeField.parseValues = function(v) {
    var values = [];
    var parts = v.split('|');
    for (var i = 0; i < parts.length - 2; i += 3) {
        values.push([parts[i+1], parts[i+2]]);
    }
    return values;
};
TD.DataFilter.DateRangeField.loadValue = function(v) {
    
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

    dstart.bind('change', function() {
        TD.DataFilter.node.trigger('filterchange');
    }).datepicker({
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

    dend.bind('change', function() {
        TD.DataFilter.node.trigger('filterchange');
    }).datepicker({
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
    
    var node = $(content);
    node.find('select').bind('change', function() {
        TD.DataFilter.node.trigger('filterchange');
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
    
    var node = $(content);
    node.find('input').bind('keypress', function() {
        TD.DataFilter.node.trigger('filterchange');
    });
    node.find('select').bind('change', function() {
        TD.DataFilter.node.trigger('filterchange');
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

TD.DataFilter.TextField = Object.create(TD.DataFilter.Field);
TD.DataFilter.TextField.render = function() {    
    var content = '';
    content += '<li id="field_' + this.id + '" class="text_field">';
    content += '<input id="field' + this.id + '" type="text" name="' + this.filter.config.name + '"/>';
    content += '<a href="#" class="remove">-</a>';
    content += '</li>';
    
    var node = $(content);
    node.find('input').bind('keypress', function() {
        TD.DataFilter.node.trigger('filterchange');
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
        TD.DataFilter.node.trigger('filterchange');
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
        TD.DataFilter.node.trigger('filterchange');
    },
    removeField: function(field) {
        delete this.fields[field.id];
        this.fieldCount--;
        field.node.remove();
        if (this.fieldCount === 0) {
            this.disable();
        }
        TD.DataFilter.node.trigger('filterchange');
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