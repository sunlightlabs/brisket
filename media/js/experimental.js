function network_graph(div, network) {
  if (network['edges'].length == 0) {
    return;
  }

  var r = Raphael(div, 600, 200);
  var nodes = network['nodes'];
  var edges = network['edges'];
  var x = 0, y = 50, radius = 15, spacing=7;
  var drawn = {};
  for (var i in edges) {

    /* only increase spacing for the next iteration if one of the
     * start or end nodes is new
     */
    var new_start = false, new_end = false;
    var start_node = edges[i][0];
    if (!drawn[start_node]) { // not yet drawn
      x = x + spacing*radius;
      var x_start = x;
      var y_start = y;
      r.circle(x_start, y_start, radius).attr({"fill": "#ff9900"});
      r.text(x_start,y_start, start_node);
      drawn[start_node] = [x_start, y_start];
      new_start = true;
    }
    else {
      var x_start = drawn[start_node][0];
      var y_start = drawn[start_node][1];
    }

    var end_node = edges[i][1];
    if (!drawn[end_node]) {
      x = x + spacing*radius;
      var x_end = x;
      var y_end = y;
      r.circle(x_end, y_end, radius).attr({"fill": "#ff9900"});
      r.text(x_end, y_end, end_node);
      drawn[end_node] = [x_end, y_end];
      new_end = true;
    }
    else {
      var x_end = drawn[end_node][0];
      var y_end = drawn[end_node][1];
    }

    x_control = (x_end+x_start)/2;
    y_control = y+60;
    r.path("M"+x_start+','+y_start+' S'+x_control+','+y_control+' '+x_end+','+y_end);

    // update x position
//    if (new_start && new_end) {
//      alert ("increasing spacing");
//      x = x_end + spacing*radius;
//    }

  }
}