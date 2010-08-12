function dollar(str) {
  var decimal_split = (str + '').split('.');
  var integer_part = decimal_split[0];
  var rgx = /(\d+)(\d{3})/;
    while (rgx.test(integer_part)) {
        integer_part = integer_part.replace(rgx, '$1' + ',' + '$2');
    }
  return "$"+ integer_part;
}

function piechart(div, data, type) {

    if ( _.keys(data).length === 0) { return; }

    // data is expected as a dict.
    var r = Raphael(div);
    r.g.txtattr.font = "11px 'Fontin Sans', Fontin-Sans, sans-serif";

    var party_colors = {"Republicans": "#E60002", "Democrats": "#186582", "Other" : "#DCDDDE"};
    var other_colors = ["#EFCC01","#F2E388"];

    var slices = [];
    var keys = _.keys(data);
    var total = _(data).chain().values().reduce(0, function(memo, num) {
        return memo + num;
    }).value();

    /* when there's an extra key-value pair, usually it's for an
     * 'unknown' or 'other' category, so make it grey. in a moment
     * of madness i determined why this should work and it apprently
     * does-- it consistently associates the 'uknown' wedge with the
     * additional colour, but now i forget why-- maybe it's because
     * when they keys gets sorted below, 'u' is last in the
     * alphabetical sort...? */
    if (keys.length > 2 ) {
      other_colors = ["#DCDDDE"].concat(other_colors);
    }

    for (var i = 0; i < keys.length; i++) {

        var key = keys[i];
        var value = Math.min(data[key], total);
        var color = (type && type == "party") ? party_colors[key] : other_colors[i];

        var percent = Math.round((value / total) * 100);
        var label = (key || ' ') + ' (' + percent + '%)';

        if (value > 0) {
            slices.push({
                value: value,
                label: label,
                color: color
            });
        }

    }

    slices.sort(function(a, b) {
        return b.value - a.value;
    });

    var labels = _.map(slices, function(s){ return s.label; });
    var values = _.map(slices, function(s){ return s.value; });
    var colors = _.map(slices, function(s){ return s.color; });

    pie = r.g.piechart(70, 70, 60, values, {
        legend: labels,
        legendpos: "east",
        colors: colors,
        strokewidth: 0
    });

    for (var i=0; i < pie.labels.length; i++) {
    /* each label has two elements-- a circle for the slice colour
     * (the 0th element), and some text (the 1st element). we only
     * want to set the colour of the latter-- hence setting the
     * 1st element of each label. */
    pie.labels[i][1].attr('fill', '#666666');
    }

    var lbl = undefined;

    pie.hover(function () {
        this.sector.stop();
        // first two args to scale() are the scaled size.
        this.sector.scale(1.04, 1.04, this.cx, this.cy);
        if (this.label) {
            this.label[0].stop();
            this.label[0].scale(1.5);
            this.label[1].attr({"font-weight": 800, 'fill': '#666666'});
            lbl = r.text(70, 70, dollar(this.value.value));
            lbl.attr({"font-weight": 800, "font-size": "12px"});
            lbl.show();
        }
    }, function () {
        this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
        if (this.label) {
            this.label[0].animate({scale: 1}, 500, "bounce");
            this.label[1].attr({"font-weight": 400});
            lbl.hide();
        }
    });

}



function barchart(div, data) {
    /* expects data to be a list of dicts each with keys called key,
       value, and href. */

    if (data.length === 0) return;

    var sizes = {
        chart_height: 195,
        chart_width: 285,
        chart_x: 215,
        chart_y: 10,
        bar_gutter: 30,
        right_gutter: 65,
        row_height: 18
    };

    opts = {
        "type": "soft",
        "gutter": sizes.bar_gutter, //space between bars, as fn of bar width/height
        "stacked": data[0]['value_employee'] ? true : false,
        "colors" : ["#EFCC01", "#f27e01"]
    };

    real_rows = data.length;

    // Note: ideally we'd just make the chart itself smaller when there are fewer rows.
    // But Raphael sizing is unpredictable, so we have to keep the height and number of
    // rows constant in order to be able to match Raphael's row positions.
    if (data.length < 10) {
        for (var i=data.length; i < 10; i++) {
          data[i] = {'key':' ', 'value': 0};
        }
    }

    if (opts['stacked']) {
        data_series = [_.pluck(data, 'value_employee'), _.pluck(data, 'value_pac')];
        data_labels = [_.pluck(data, 'key'), _.map(data, function(x){ return " "; })];
    } else {
        data_series = [_.pluck(data, 'value')]
        data_labels = [_.pluck(data, 'key')];
    }

    b = Raphael(div);
    b.setSize(sizes.chart_x + sizes.chart_width + sizes.right_gutter, sizes.chart_y + sizes.chart_height);
    b.g.txtattr.font = "11px 'Fontin Sans', Fontin-Sans, sans-serif";

    var barchart_obj = b.g.hbarchart(sizes.chart_x, sizes.chart_y, sizes.chart_width, sizes.chart_height, data_series, opts);
    barchart_obj.label(data_labels, false);

    var num_datasets = barchart_obj.bars.length;

    var graphElem = jQuery('#' + div);
    var graphElemPosition = graphElem.offset();
    labelCount = 0;
    for (var i = 0; i < barchart_obj.labels.length; i++) {
        var text = barchart_obj.labels[i].attr('text');
        if (text != ' ') {
            var e = document.createElement(data[labelCount].href ? 'a' : 'span');
            e.appendChild(document.createTextNode(text));
            e.style.position = 'absolute';
            e.style.top = (sizes.chart_y + labelCount * sizes.row_height) + 'px';
            e.style.left = '15px';
            e.style.fontSize = '11px';
            e.style.textDecoration = 'none';
            e.style.zIndex = 100 + labelCount * sizes.row_height;
            if (data[labelCount].href) {
                e.href = data[labelCount].href;
            }
            graphElem.prepend(e);
            labelCount += 1;
        }
    }

    barchart_obj.labels.translate((sizes.chart_x - 10) * -1, -1000000);

    /* add text markers for the amounts (which unfortunately uses a
       method called 'label' just to confuse you) */
    var s = b.set();
    for (var i=0; i< data.length; i++) {
        if (data[i].value > 0) {
            var x = barchart_obj.bars[num_datasets-1][i].x;
            var y = barchart_obj.bars[num_datasets-1][i].y;
            text = dollar(data[i]['value']);
            marker = b.g.text(x,y,text);
            marker.attr("fill", "#666666");
            s.push(marker);
        }
    }

    var spacing = 10; // spacing between bars and text markers
    s.attr({translation: spacing + ',0', 'text-anchor': 'start'});

    bottomY = 5 + sizes.chart_y + sizes.row_height * real_rows

    var yAxis = b.path("M " + sizes.chart_x + " " + sizes.chart_y + " L " + sizes.chart_x + " " + bottomY);
    yAxis.attr({"stroke": "#827D7D", "stroke-width": 1});
    yAxis.show();

    var xAxisLength = sizes.chart_width + sizes.chart_x + sizes.right_gutter;
    var xAxis = b.path("M " + sizes.chart_x + " " + bottomY + " L " + xAxisLength + " " + bottomY);

    xAxis.attr({"stroke": "#827D7D", "stroke-width": 1});
    xAxis.show();
}


function sparkline(div, data) {
    if (data.length === 0) {
        return;
    }

    r = Raphael(div, 100, 30);
    var x = [], y = [];
    for (var i=0; i<data.length; i++) {
        x[i] = data[i]['step'];
        y[i] = data[i]['amount'];
    }
    r.g.linechart(0, 1, 100, 30, x, y, { width: 1, gutter: 1 });
}

function sparkline_by_party(div, data, cut_off_point) {
    if (data.length === 0) {
        return;
    }

    // data => { 'R': [{'step': 1, 'amount': 100}, {...}], 'D': [{...},], 'O': [{...},] }

    var party_colors = ["#186582", "#E60002"];

    r = Raphael(div, 100, 30);
    var x = [], y = [];
    var keys = ['D', 'R']

    // for (thus far) unknown reasons, raphael refuses to show any charts if all of the
    // amounts are zero, even though the data structure is otherwise complete, so we need
    // to track whether we have any non-zero values to show in the chart
    var saw_non_zero_value = false

    for (var i=0; i<keys.length; i++) {
        var key = keys[i];
        y[key] = [];

        stop_at = data[key].length

        if (cut_off_point < stop_at) {
            stop_at = cut_off_point
        }

        for (var j=0; j<stop_at; j++) {
            x[j] = j+1;
            y[key][j] = data[key][j]['amount'];

            if (y[key][j] > 0) {
                saw_non_zero_value = true
            }
        }
    }

    // bail if we don't have a real chart to show (and to avoid having raphael break the whole page)
    if (!saw_non_zero_value) {
        return []
    }

    r.g.linechart(0, 1, 100, 30, x, [y['D'], y['R']], { colors: party_colors, width: 1, gutter: 1 });

    // the legend is hidden by default, in case we had the aforementioned all-zero situation
    // so show it now
    jQuery("#sparklines_legend").show();
}
