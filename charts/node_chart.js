/* set up all the dom stuff */

DOMParser = require('xmldom').DOMParser;

var jsdom = require("jsdom");
jsdom.jsdom("<html><head></head><body></body></html>");
document = jsdom.jsdom("<html><head></head><body></body></html>");
window = document.createWindow();
navigator = window.navigator;
CSSStyleDeclaration = window.CSSStyleDeclaration;
window.DOMParser = DOMParser;

Sizzle = require("sizzle");
window.Sizzle = Sizzle;

process.env.TZ = "America/Los_Angeles";

document.createRange = function() {
  return {
    selectNode: function() {},
    createContextualFragment: function(html) { return jsdom.jsdom(html); }
  };
};


_ = require('underscore');

require('./d3.min.js');

require('./d3.geom.min.js');
require('./brisket_d3.js');

Canvas = require('canvas');
CanvasRenderingContext2D = Canvas.Context2d;

require('./rgbcolor.js');
require('./canvg.js');

/* set up express */
var express = require('express');
var app = express();

app.get(/^\/chart\/([a-zA-Z_]+)\/(.+)/, function(req, res) {
    var chart = req.params[0], in_data = req.params[1];
    if (typeof BrisketServer[chart] == 'undefined') {
        res.send(404);
        return;
    }
    /* decode the data */
    var data = JSON.parse(new Buffer(in_data, 'base64').toString('ascii'));

    /* draw the chart */
    var div = document.createElement('div');
    document.body.appendChild(div);
    div.id = String((new Date().getTime()) + Math.random()).replace('.','-');

    var canvas = new Canvas(0,0);
    canvas.style = {};

    BrisketServer[chart](div.id, data);

    canvg(canvas, div.innerHTML, { ignoreMouse: true, ignoreAnimation: true });

    canvas.toBuffer(function(err, buffer) {
        res.header('Content-Type', 'image/png');
        res.send(buffer);
        res.end();

        div.parentNode.removeChild(div);
    });
});

var http = require("http");
module.exports = http.createServer(app);