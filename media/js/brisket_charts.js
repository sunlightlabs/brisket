
function piechart(div, data, type) {

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

    for (var i = 0; i < keys.length; i++) {

        var key = keys[i];
        var value = data[key];
        var color = (type && type == "party") ? party_colors[key] : other_colors[i];

        var percent = Math.round((value / total) * 100);
        var label = (key || ' ') + ' (' + percent + '%)';
        if (label.length > 1) {
            label = label[0].toUpperCase() + label.substr(1, label.length);
        }

        slices.push({
            value: value,
            label: label,
            color: color,
        });

    }

    slices.sort(function(a, b) {
        return b.value - a.value;
    });

    var labels = _.map(slices, function(s){ return s.label });
    var values = _.map(slices, function(s){ return s.value });
    var colors = _.map(slices, function(s){ return s.color });

    pie = r.g.piechart(70, 70, 60, values, {
        legend: labels,
        legendpos: "east",
        colors: colors,
        strokewidth: 0,
    });

    var lbl = undefined;

    pie.hover(function () {
        this.sector.stop();
        // first two args to scale() are the scaled size.
        this.sector.scale(1.04, 1.04, this.cx, this.cy);
        if (this.label) {
            this.label[0].stop();
            this.label[0].scale(1.5);
            this.label[1].attr({"font-weight": 800});
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

function dollar(str) {
  str += '';
  x = str.split('.');
  x1 = x[0];
  x2 = x.length > 1 ? '.' + x[1] : '';
  var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
      x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
  return "$"+ x1 + x2;
}


function barchart(div, data, limit) {
    // expects data to be a list of dicts each with keys called key,
    // value, and href.
    b = Raphael(div);
    b.g.txtattr.font = "11px 'Fontin Sans', Fontin-Sans, sans-serif";

    if (limit && limit < data.length) {
        data = data.slice(0, limit);
    }

    /* if the data has less than 10 records, pad it so that
    * the chart doesn't look like crap. */
    var original_len = data.length;

  /* commenting this out while we demo
    if (data.length < 10) {
        for (var i=data.length; i<10; i++) {
            data[i] = {'key':' ', 'value': 0, 'href':'#'};
        }
    }
  */
    var data_values = [];
    for (var i = 0; i < data.length; i++) {
	    data_values.push(data[i]['value']);
    }

    var data_labels = [];
    for (var i = 0; i < data.length; i++) {
	    data_labels.push(data[i]['key']);
    }

    var data_hrefs = [];
    for (var i = 0; i < data.length; i++) {
	    data_hrefs.push(data[i]['href']);
    }

    opts = {
        "type": "soft",
        "gutter": 30, //space between bars, as fn of bar width/height
        "stacked": false,
        "colors" : ["#EFCC01"]
    };

    /* data array must be passed inside another array-- barchart fn
       supports multiple data series so expects an array of arrays,
       even for just one data series. Else it will treat each data
       point as one series. */
    var barchart = b.g.hbarchart(10,10, 330, 150, [data_values], opts);

    // pass in labels array inside another array
    barchart.label([data_labels], false);

    // add links to the labels
    for (var i = 0; i < barchart.labels.length; i++) {
        barchart.labels[i].attr({'href': data_hrefs[i] });
    }

    // this is the desired link colour, but it also seems to make
    //the font bold, which is undesireable :/
    barchart.labels.hover(
        function() {
            this.attr({fill: "#0A6E92"});
        },
        function() {
            this.attr({fill: "#000000"});
        }
    );


    /* figure out the longest label text and move the chart over by
     that amount, so that the labels are beside and not on top of the
     chart. */
    var far_right = 0;
    for (var i = 0; i < data_labels.length; i++) {
        var bb = barchart.labels[i].getBBox();
        if (bb.x + bb.width > far_right) {
            far_right = bb.x + bb.width;
        }
    }
    far_right = 165; // FAKE IT HERE!!
    barchart.translate(far_right);

    /* add text markers for the amounts (which unfortunately uses a
     method called 'label' just to confuse you) */
    s = b.set();
    for (var i=0; i< original_len; i++) {
        x = barchart.bars[0][i].x;
	y = barchart.bars[0][i].y + 1;
	text = '$'+barchart.bars[0][i].value;
	marker = b.g.text(x,y,text);
	s.push(marker);
    };
    var spacing = 10; // spacing between bars and text markers
    s.attr({translation: far_right+spacing, 'text-anchor': 'start'});

    var yAxis = b.path("M 175 10 L 175 154");
    yAxis.attr({"stroke": "#827D7D", "stroke-width": 1});
    yAxis.show();

    var xAxis = b.path("M 175 154 L 560 154");

    xAxis.attr({"stroke": "#827D7D", "stroke-width": 1});
    xAxis.show();

}

function sparkline(div, data) {
  r = Raphael(div, 100, 30);
  var x = [], y = [];
  for (var i=0; i<data.length; i++) {
    x[i] = data[i]['step'];
    y[i] = data[i]['amount'];
  }
  r.g.linechart(0, 10, 100, 30, x, y);

}
