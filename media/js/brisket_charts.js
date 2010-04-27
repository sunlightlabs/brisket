function piechart(div, data, chart_title) {
    // data is expected as a dict.

    var r = Raphael(div);
    r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
    r.g.text(150, 10, chart_title).attr({"font-size": 15});

    var data_values = [];
    for (k in data) {
	data_values.push(data[k]);
    }

  var values_total = 0;
  for (v in data_values) {
    values_total += data_values[v];
  }

    var data_labels = [];
    for (k in data) {
      var percent = Math.round((data[k]/values_total)*100);
      data_labels.push(k+' ('+percent+'%)');
    }

    pie = r.g.piechart(150, 100, 60, data_values, { legend: data_labels, legendpos: "east",
						    colors: ["#FFCC33","#FF9900"] });

    pie.hover(function () {
    this.sector.stop();
    // first two args to scale() are the scaled size.
    this.sector.scale(1.04, 1.04, this.cx, this.cy);
    if (this.label) {
    this.label[0].stop();
    this.label[0].scale(1.5);
    this.label[1].attr({"font-weight": 800});
//    this.sector.flag
//    this.tag = this.tag || r.g.tag(this.x, this.y, this.value, 0, this.r + 2).insertBefore(this);
//   this.tag.show();

    }
    }, function () {
    this.sector.animate({scale: [1, 1, this.cx,
    this.cy]}, 500, "bounce");
    if (this.label) {
    this.label[0].animate({scale: 1}, 500,
    "bounce");
    this.label[1].attr({"font-weight": 400});
//    this.tag && this.tag.hide();
    }
    });
}

function barchart(div, data, chart_title, limit) {
    // expects data to be a list of dicts each with keys called key,
    // value, and link.
    b = Raphael(div);
    b.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
    b.g.text(150, 10, chart_title).attr({"font-size": 15});

  /*
    var fin = function () {
    this.flag = b.g.label(this.bar.x, this.bar.y,this.bar.value || "0").insertBefore(this);
    };

    var fout = function () {
    this.flag.animate({opacity: 0}, 300, function () { this.remove();});
    };

*/

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
    "colors" : ["#FF9900"]
    };

    /* data array must be passed inside another array-- barchart fn
       supports multiple data series so expects an array of arrays,
       even for just one data series. Else it will treat each data
       point as one series. */
  var barchart = b.g.hbarchart(10,20, 250, 150, [data_values], opts);

    // pass in labels array inside another array
    barchart.label([data_labels], false);

    // add links to the labels
    for (var i=0; i< barchart.labels.length; i++) {
      barchart.labels[i].attr({'href': data_hrefs[i] })
    }
    barchart.labels.attr({stroke: "#666", 'font-weight': 1000});

    /* add text markers (which unfortunately uses a method called
       'label' just to confuse you) */
    b.g.txtattr.font = "10px 'Fontin Sans', Fontin-Sans, sans-serif";
    s = b.set();
    for (var i=0; i< barchart.bars[0].length; i++) {
	x = barchart.bars[0][i].x;
	y = barchart.bars[0][i].y;
	text = '$'+barchart.bars[0][i].value;
	marker = b.g.text(x,y,text);
	s.push(marker);
    };
    s.attr({stroke: "#333", translation: "140,0"});


    /* figure out the longest label text and move the chart over by
    that amount. so the labels are beside and not on top of the
    chart. */
    var far_right = 0;
    for (var i = 0; i < data_labels.length; i++) {
	bb = barchart.labels[i].getBBox();
        if (bb.x + bb.width > far_right) {
            far_right = bb.x + bb.width;
        }
    }
    barchart.translate(far_right);
}