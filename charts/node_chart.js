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

div = document.createElement('div');
document.body.appendChild(div);
div.id = 'chart';

Brisket.local_piechart("chart",  {"in-state": 596631.0, "out-of-state": 2390208.0});

Canvas = require('canvas');
CanvasRenderingContext2D = Canvas.Context2d;

require('./rgbcolor.js');
require('./canvg.js');

var canvas = new Canvas(0,0);
canvas.style = {};
canvg(canvas, div.innerHTML, { ignoreMouse: true, ignoreAnimation: true });

canvas.toBuffer(function(err, buffer) {
    process.stdout.write(buffer);
    process.exit();
});