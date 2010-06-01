function piechart(div, data, type) {
  // data is expected as a dict.
  var r = Raphael(div);
  r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";

  party_colors = {"Republicans": "#E60002", "Democrats": "#186581", "Other" : "#666666"};
  other_colors = ["#EFCC01","#F2E388"];

  var values_total = 0;
  for (k in data) {
    values_total += data[k];
  }

  var data_values = [];
  var use_colors = [];
  var data_labels = [];
  //for (k in data) {
  for (var k in data) {
    //capitalize the labels (making sure the label is at least length 1).
    if (k) { kk = k[0].toUpperCase()+k.substring(1,k.length);}
    else { kk = k; }
    var percent = Math.round((data[k]/values_total)*100);
    data_labels.push(kk+' ('+percent+'%)');
    data_values.push(data[k]);
    //console.log(k+':'+data[k]);
    if (type && type == "party") {
      use_colors.push(party_colors[k]);
      //console.log('pushing '+ party_colors[k]);
    }
  }
  if (!type || type != "party") {
    use_colors = other_colors;
  }

  var data_values_fixed = [];
  for (var i=0; i<data_values.length; i++) {
    data_values_fixed[i] = data_values[i];
  }
  /*
  console.log(use_colors);
  console.log(data_labels);
  console.log(data_values);
  console.log(data_values_fixed);
   */
  pie = r.g.piechart(70, 70, 60, data_values, { legend: data_labels, legendpos: "east",
						  colors: use_colors });

    pie.hover(function () {
    this.sector.stop();
    // first two args to scale() are the scaled size.
    this.sector.scale(1.04, 1.04, this.cx, this.cy);
    if (this.label) {
    this.label[0].stop();
    this.label[0].scale(1.5);
    this.label[1].attr({"font-weight": 800});
    lbl = r.text(70, 70, dollar(this.value.value));
    lbl.attr({"font-weight": 800, "font-size": "13px"});
    lbl.show();
    }}, function () {
    this.sector.animate({scale: [1, 1, this.cx,
    this.cy]}, 500, "bounce");
    if (this.label) {
    this.label[0].animate({scale: 1}, 500,
    "bounce");
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
    // value, and link.
    b = Raphael(div);
    b.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";

  if (limit && limit < data.length) {
    data= data.slice(0,limit);
  }

    data_values = [];
    for (i in data) {
	data_values.push(data[i]['value']);
    }

    data_labels = [];
    for (i in data) {
	data_labels.push(data[i]['key']);
    }

    data_hrefs = [];
    for (i in data) {
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
  var barchart = b.g.hbarchart(10,10, 350, 150, [data_values], opts);

    // pass in labels array inside another array
    barchart.label([data_labels], false);

    // add links to the labels
    for (var i=0; i< barchart.labels.length; i++) {
      barchart.labels[i].attr({'href': data_hrefs[i] })
    }

    // this is the desired link colour, but it also seems to make
    //the font bold, which is undesireable :/
    barchart.labels.hover(function() {this.attr({stroke: "#0A6E92"})},
			  function() {this.attr({stroke: ""})});


    /* figure out the longest label text and move the chart over by
     that amount, so that the labels are beside and not on top of the
     chart. */
    var far_right = 0;
    for (var i = 0; i < data_labels.length; i++) {
	bb = barchart.labels[i].getBBox();
        if (bb.x + bb.width > far_right) {
            far_right = bb.x + bb.width;
        }
    }
    barchart.translate(far_right);

    /* add text markers for the amounts (which unfortunately uses a
     method called 'label' just to confuse you) */
    s = b.set();
    for (var i=0; i< barchart.bars[0].length; i++) {
        x = barchart.bars[0][i].x;
	y = barchart.bars[0][i].y;
	text = '$'+barchart.bars[0][i].value;
	marker = b.g.text(x,y,text);
	s.push(marker);
    };
    var spacing = 10; // spacing between bars and text markers
    s.attr({translation: far_right+spacing, 'text-anchor': 'start'});

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
