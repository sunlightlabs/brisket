
var TD = { };

TD.DataFilter = {
    fields: { },
    init: function() {
        $('#filterForm').bind('submit', function() {
            return false;
        });
        $('#filterForm a.plus-button').bind('click', function() {
            //var fieldName = $('#filterForm #id_filter').val();
            if (Math.floor(Math.random() * 2) == 1) {
                TD.DataFilter.addField(
                    TD.DataFilter.TextField({
                        label: 'Amount',
                        name: 'amount',
                        helper: 'Amount of contribution in dollars'
                    }));
                TD.DataFilter.addField(
                    TD.DataFilter.OperatorField({
                        label: 'Amount',
                        name: 'amount',
                        helper: 'Amount of contribution in dollars'
                    }));
            } else {
                TD.DataFilter.addField(
                    TD.DataFilter.DropDownField({
                        label: 'Cycle',
                        name: 'cycle',
                        helper: 'Election cycle',
                        options: [
                            [2004, 2004],
                            [2006, 2006],
                            [2008, 2008]
                        ]
                    }));
            }
            return false;
        });
        $('#downloadDataSet').click(function() {
            var values = TD.DataFilter.values();
            for (attr in values) {
                alert(attr + ' ' + _.reduce(values[attr], '', function(memo, item) {
                    if (memo) {
                        memo += '|';
                    }
                    memo += item;
                    return memo;
                }));
            }
            // for (key in TD.DataFilter.fields) {
            //     var field = TD.DataFilter.fields[key];
            //     var data = field.data();
            //     if (data[1]) {
            //         alert(data[0] + ": " + data[1]);
            //     }
            // }
            return false;
        });
    },
    addField: function(field) {
        var node = field.render();
        node.appendTo('#filterForm ul');
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
        return [
            config.name,
            $(selector + "_operator").val() + '|' + $(selector).val()
        ];
    };
    return that;
};

// TD.DataFilter.EntityField = { }
// TD.DataFilter.DateRangeField = { }

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