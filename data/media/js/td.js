
var TD = { };

TD.DataFilter = {
    fields: { },
    init: function() {
        $('#filterForm').bind('submit', function() {
            return false;
        });
        $('#filterForm a.plus-button').bind('click', function() {
            //var fieldName = $('#filterForm #id_filter').val();
            TD.DataFilter.addField(
                TD.DataFilter.DateRangeField({
                    label: 'Amount',
                    name: 'amount',
                    helper: 'Amount of contribution in dollars'
                }));
            return false;
        });
        $('#downloadDataSet').click(function() {
            var values = TD.DataFilter.values();
            for (attr in values) {
                alert(attr + ' ' + _.reduce(values[attr], '', function(memo, item) {
                    if (memo) memo += '|';
                    memo += item;
                    return memo;
                }));
            }
            return false;
        });
    },
    addField: function(field) {
        var node = field.render();
        node.appendTo('#filterForm > ul');
        field.bind(node);
        TD.DataFilter.fields[field.id] = field;
    },
    removeField: function(field) {
        $('#field_' + field.id).remove();
        delete TD.DataFilter.fields[field.id];
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

TD.DataFilter.Field = function() {
    this.id = Math.floor(Math.random() * 90000) + 10000;
};
TD.DataFilter.Field.prototype.bind = function(node) {
    var me = this;
    node.find('a.minus-button').bind('click', function() {
        TD.DataFilter.removeField(me);
        return false;
    });
};


TD.DataFilter.TextField = function(config) {
    
    var that = new TD.DataFilter.Field();
    
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
        return [config.name, $("#field_" + this.id + " input").val()];
    };
    
    return that;
    
};


TD.DataFilter.DropDownField = function(config) {
    
    var that = new TD.DataFilter.Field();
    
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
        return [config.name, $("#field_" + this.id + " select").val()];
    };
    
    return that;
    
};


TD.DataFilter.OperatorField = function(config) {
    
    var that = new TD.DataFilter.Field();
    
    that.render = function() {
        var content = '';
        content += '<li id="field_' + this.id + '" class="operatorField">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<select id="field_' + this.id + '_' + config.name + '_operator" name="' + config.name + '_operator">';
        content += '<option value="&gt;">greater than</option>';
        content += '<option value="&lt;">less than</option>';
        content += '<option value="=">equal to</option>';
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


TD.DataFilter.DateRangeField = function(config) {
    
    var that = new TD.DataFilter.Field();
    
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
        
        var options = {
            changeMonth: true,
            changeYear: true,
            duration: ''
        }        
        elem.find('input.date_start').datepicker(options);
        elem.find('input.date_end').datepicker(options);
        
        return elem;
        
    };
    
    that.data = function() {
        var inputs = $("#field_" + this.id + " input");
        return [config.name, inputs[0].value + '-' + inputs[1].value];
    };
    
    return that;
    
};


TD.DataFilter.EntityField = function(config) {
    
    var that = new TD.DataFilter.Field();
    
    that.render = function() {
        
        var content = '';
        content += '<li id="field_' + this.id + '" class="entityField">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<ul></ul>';
        content += '<input id="field_' + this.id + '_' + config.name + '" type="text" name="' + config.name + '"/>';
        content += '</li>';
        
        var elem = $(content);
        
        // temporarily add something to the field, this will be replaced
        // by callback from autocomplete field
        elem.find('input').bind('keypress', function(e) {
            if (e.which == 13) {
                that.addSelection('xxxx', $(this).val());
                return false;
            }
        });
        
        return elem;
        
    };
    
    that.data = function() {
        
        var value = _.reduce(
            $("#field_" + this.id + " ul li"),
            '',
            function(memo, item) {
                var text = item.innerHTML;
                if (text) {
                    if (memo) memo += '|';
                    memo += text;
                }
                return memo;
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


/*
 * main search box functionality
 */
 
TD.SearchBox = {
    isValid: false,
    init: function() {
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

/*
 * UI modifiers
 */
 
TD.UI = {
    fluid: function() {
        $('body').addClass('filteredSearch');
    },
    fixed: function() {
        $('body').removeClass('filteredSearch');
    }
}

$().ready(function() {
    TD.SearchBox.init();
    TD.DataFilter.init();
});