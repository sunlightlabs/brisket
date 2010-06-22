
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
    /* expects data to be a list of dicts each with keys called key,
       value, and href. */

    b = Raphael(div);
    b.g.txtattr.font = "11px 'Fontin Sans', Fontin-Sans, sans-serif";

    thedata = data;
    if (limit && limit < data.length) {
        data = data.slice(0, limit);
    }

    /* if the data has less than 10 records, pad it so that
    * the chart doesn't look like crap. */
    var original_len = data.length;

    if (data.length < 10) {
        for (var i=data.length; i<10; i++) {
          data[i] = {'key':' ', 'value': 0, 'href': -1};
        }
    }

    var data_values = [];
    for (var i = 0; i < data.length; i++) {
	    data_values.push(data[i]['value']);
    }

    /* make the hrefs a map so that we can use the key to ensure the
     * right url is assigned to the right entity. */
    data_hrefs = {};
    for (var i = 0; i < data.length; i++) {	
	if (data[i]['href'] != -1) {
	    data_hrefs[data[i]['key']] = data[i]['href'];
	}
    }

    var data_labels = [];
    for (var i = 0; i < data.length; i++) {
	ind = data_labels.push(data[i]['key']);
    }

    opts = {
        "type": "soft",
        "gutter": 30, //space between bars, as fn of bar width/height
        "stacked": false,
	"colors" : ["#EFCC01", "#f27e01"]
    };

    /* check if this is a stacked barchart. data sets must be passed
       inside another array-- barchart fn supports multiple data
       series so expects an array of arrays, even for just one data
       series. Else it will treat each data point as one series. */
    if (data[0]['value_employee']) {
      var values_employee = [];
      var values_pac = [];
      for (var i=0; i<data.length; i++) {
	values_employee.push(data[i]['value_employee']);
	values_pac.push(data[i]['value_pac']);
      }
      all_data = [values_employee, values_pac];
      opts['stacked'] = true;
    } else {
      all_data = [data_values];
    }

    var barchart = b.g.hbarchart(175,10, 330, 150, all_data, opts);
    var num_datasets = barchart.bars.length;

    /* pass in labels array inside another array. if this is a stacked
     * barchart, raphael defaults to including the data value as a
     * label when no label is passed in, so trick it by sending in
     * blank (but non-empty!) strings.  */
    if (barchart.bars.length > 1) {
     the_labels = [data_labels, 
		   ["   ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   "]];
    }
    else {
      the_labels = [data_labels];
    }
    barchart.label(the_labels, false);

    /* add links to the labels */
    for (var i = 0; i < barchart.labels.length; i++) {
      var key = barchart.labels[i].attr('text');
      if (data_hrefs[key]) {
	  barchart.labels[i].attr({'href': data_hrefs[key], 'fill': "#666666" });
      }
      else {
	  barchart.labels[i].attr({'fill': "#666666" });
      }
    }

    /* change the labels to the link colour on hover */
    barchart.labels.hover(function() {
	    if (this.attr("href")) {
		this.attr({fill: "#0A6E92"});
	    }
        }, function() {
            this.attr({fill: "#666666"});
        }
	);

    barchart.labels.translate(-165);

    /* add text markers for the amounts (which unfortunately uses a
       method called 'label' just to confuse you) */
    s = b.set();
    for (var i=0; i< original_len; i++) {
      x = barchart.bars[num_datasets-1][i].x;
      y = barchart.bars[num_datasets-1][i].y;
      text = 0;
      for (var n=0; n< num_datasets; n++) {
	text = text + barchart.bars[n][i].value;
      }
      text = "$"+text;

      marker = b.g.text(x,y,text);
      marker.attr("fill", "#666666");
      s.push(marker);
    };

    var spacing = 10; // spacing between bars and text markers
    s.attr({translation: spacing, 'text-anchor': 'start'});

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
