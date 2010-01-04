TD = { };

TD.DataFilter = {
    
    fields: { },    // fields added to the filter
    registry: { },  // registry of allowed fields
    
    init: function() {
        
        // bind filter form to the submit button
        $('#filterForm').bind('submit', function() {
            return false;
        });
        
        // bind button to add a new field based on field type selection
        $('#filterForm a.plus-button').bind('click', function() {
            var fieldType = $('#filterForm #id_filter').val();
            var fieldPrototype = TD.DataFilter.registry[fieldType];
            if (fieldPrototype != undefined) {
                TD.DataFilter.addField(fieldPrototype.instance());
            }
            return false;
        });
        
        /***
         * TEMPORARILY BIND DOWNLOAD DATA SET FOR DEBUGGING
         */
        $('#downloadDataSet').click(function() {
            var values = TD.DataFilter.values();
            for (attr in values) {
                alert(attr + ' ' + _.reduce(values[attr], '', function(memo, item) {
                    if (item && item != '') {
                        if (memo) memo += '|';
                        memo += item;
                    }
                    return memo;
                }));
            }
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

/* DropDownField displays a select box of options.
    - options -- list of [value, text] lists
*/
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

/* OperatorField displays a text input with an operation select box:
   greater than, less than, equal to, not equal to
*/
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
        content += '<option value="!=">not equal to</option>';
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
        content += '<li id="field_' + this.id + '" class="entityField" data-id="' + this.id + '">';
        content += '<label for="field_' + this.id + '_' + config.name + '">' + config.label + '</label>';
        content += '<a class="minus-button" href="#" title="Delete Filter">Delete Filter</a>';
        content += '<span class="helper">' + config.helper + '</span>';
        content += '<ul class="entity_values"></ul>';
        content += '<input id="field_' + this.id + '_' + config.name + '" type="text" name="' + config.name + '"/>';
        content += '</li>';
        
        var elem = $(content);
        
        // temporarily add something to the field, this will be replaced
        // by callback from autocomplete field
        elem.find('input').bind('keypress', function(e) {
            if (e.which == 13) {
                var fieldId = $(this).parent('li').attr('data-id');
                TD.DataFilter.fields[fieldId].addSelection('xxxx_' + Math.floor(Math.random() * 90000), $(this).val());
                return false;
            }
        });
        
        return elem;
        
    };
    
    that.data = function() {
        
        var value = '';
        
        $("#field_" + this.id + " ul.entity_values li").each(function(item) {
            var text = $(this).attr('data-id');
            if (text) {
                if (value) value += '|';
                value += text;
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
    TD.DataFilter.init();
    
    TD.DataFilter.registry = {
        
        amount: TD.DataFilter.OperatorField({
            label: 'Amount',
            name: 'amount',
            helper: 'Amount of contribution in dollars'
        }),
        
        datestamp: TD.DataFilter.DateRangeField({
            label: 'Date',
            name: 'datestamp',
            helper: 'Date of contribution'
        }),
        
        jurisdiction: TD.DataFilter.DropDownField({
            label: 'Jurisdiction',
            name: 'transaction_namespace',
            helper: 'State or federal seat',
            options: [
                ['urn:fec:contribution','Federal'],
                ['urn:nimsp:contribution','State']
            ]
        }),
        
        organization: TD.DataFilter.EntityField({
            label: 'Organization',
            name: 'organization_entity',
            helper: 'Corporation related to contribution'
        })
        
    }
    
});