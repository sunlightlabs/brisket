var testvar;

(function($) {
    $.fn.ellipsis = function()
    {
        return this.each(function()
        {
            var el = $(this);

            if(el.css("overflow") == "hidden")
            {
                var text = el.html();
                var multiline = el.hasClass('multiline');
                var t = $(this.cloneNode(true))
                        .hide()
                        .css('position', 'absolute')
                        .css('overflow', 'visible')
                        .width(multiline ? el.width() : 'auto')
                        .height(multiline ? 'auto' : el.height())
                        ;

                el.after(t);

                function height() { return t.height() > el.height(); };
                function width() { return t.width() > el.width(); };

                var func = multiline ? height : width;

                while (text.length > 0 && func())
                {
                        text = text.substr(0, text.length - 1);
                        t.html(text + "...");
                }

                el.html(t.html());
                t.remove();
            }
        });
    };
})(jQuery);

D3Charts = {
    BARCHART_DEFAULTS: {
        chart_height: 195,
        chart_width: 235,
        chart_x: 215,
        chart_y: 10,
        bar_gutter: 5,
        right_gutter: 70,
        left_gutter: 15,
        row_height: 18,
        bar_height: 14,
        chart_padding: 4,
        colors : ["#efcc01", "#f27e01"],
        axis_color: "#827d7d",
        text_color: "#666666",
        link_color: "#0a6e92"
    },
    _get_barchart_size: function(opts) {
        return {
            'width': opts.chart_x + opts.chart_width + opts.right_gutter,
            'height': opts.chart_height
        }
    },
    barchart: function(div, data, opts) {
        if (typeof opts === 'undefined') opts = {};
        _.defaults(opts, D3Charts.BARCHART_DEFAULTS);

        totals = _.map(data, function(item) { return d3.sum(item.values); })

        var size = D3Charts._get_barchart_size(opts);
        var chart = d3.select('#' + div).append("svg")
            .classed("chart-canvas", true)
            .attr("width", size.width)
            .attr("height", size.height);

        var width = d3.scale.linear()
            .domain([0, d3.max(totals)])
            .range([0, opts.chart_width]);

        var yPos = d3.scale.ordinal()
            .domain(d3.range(totals.length))
            .rangeBands([opts.chart_y + opts.chart_padding, opts.chart_y + (opts.row_height * data.length) + opts.chart_padding]);


        // bars
        chart.selectAll("g")
            .data(data)
        .enter().append("g")
            .attr("transform", function(d, i) {
                return "translate(" + opts.chart_x + "," + yPos(i) + ")";
            })
        .selectAll("path")
            .data(function(d) { return _.map(_.range(d.values.length), function(j) { return d3.sum(d.values.slice(0, j + 1))}).reverse(); })
        .enter().append("path")
            .attr("d", function(d, i) {
                var x = 0;
                var y = 0;
                var h = opts.bar_height;

                var r = 4;

                var w = width(d, i);

                var array = [].concat(
                    ["M", x, y],
                    ["L", d3.max([x + w - r, 0]), y, "Q", x + w, y, x + w, y + r],
                    ["L", x + w, d3.max([y + h - r, 0]), "Q", x + w, y + h, d3.max([x + w - r, 0]), y + h],
                    ["L", x, y + h, "Z"]
                );

                return array.join(" ");
            })
            .attr("fill", function(d, i) { return opts.colors[data[0].values.length - i - 1] });

        // numbers
        var format = d3.format(',.0f');
        chart.selectAll("text.chart-number")
            .data(totals)
        .enter().append("text")
            .classed('chart-number', true)
            .attr("x", function(d, i) { return opts.chart_x + width(d, i) + opts.bar_gutter; })
            .attr("y", function(d, i) { return yPos(i) + yPos.rangeBand() / 2; })
            .attr("dy", ".15em") // vertical-align: middle
            .attr('fill', opts.text_color)
            .text(function(d, i) { return '$' + format(d); })
            .style('font', '11px arial,sans-serif');

        // labels
        chart.selectAll("g.chart-label")
            .data(data)
        .enter().append("g")
            .classed('chart-label', true)
            .attr("transform", function(d, i) { return "translate(" + opts.left_gutter + "," + (yPos(i) + yPos.rangeBand() / 2) + ")"; })
            .each(function(d, i) {
                var parent = d3.select(this);
                if (d.href) {
                    parent = parent.append("a")
                    parent.attr('xlink:href', d.href);
                }
                parent.append("text")
                    .attr("y", ".15em") // vertical-align: middle
                    .attr('fill', parent.node().tagName.toLowerCase() == 'a' ? opts.link_color : opts.text_color)
                    .text(function(d, i) { return d.name; })
                    .style('font', '11px arial,sans-serif');
            })

        // axes
        chart.append("line")
            .attr("x1", opts.chart_x - .5)
            .attr("x2", opts.chart_x - .5)
            .attr("y1", opts.chart_y)
            .attr("y2", opts.chart_y + (data.length * opts.row_height) + opts.chart_padding)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");

        chart.append("line")
            .attr("x1", opts.chart_x)
            .attr("x2", opts.chart_x + opts.chart_width + opts.right_gutter)
            .attr("y1", opts.chart_y + (data.length * opts.row_height) + opts.chart_padding - .5)
            .attr("y2", opts.chart_y + (data.length * opts.row_height) + opts.chart_padding - .5)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");
    },

    PIECHART_DEFAULTS: {
        chart_height: 116,
        chart_width: 240,
        chart_r: 54,
        chart_cx: 58,
        chart_cy: 58,
        colors : ["#efcc01", "#f2e388"],
        text_color: "#666666",
        amount_color: '#000000',
        row_height: 14,
        legend_padding: 15,
        legend_r: 5
    },
    _get_piechart_size: function(opts) {
        return {
            'width': opts.chart_width,
            'height': opts.chart_height
        }
    },
    piechart: function(div, data, opts) {
        if (typeof opts === 'undefined') opts = {};
        _.defaults(opts, D3Charts.PIECHART_DEFAULTS);

        var twopi = 2 * Math.PI;

        var size = D3Charts._get_piechart_size(opts);
        var chart = d3.select("#" + div)
            .append("svg")
                .classed('chart-canvas', true)
                .attr("width", size.width)
                .attr("height", size.height);

        // pie
        _.each(data, function(d, i) { d.color = opts.colors[i]; });
        data = _.sortBy(data, function(d) { return d.value; }).reverse();
        var values = _.map(data, function(d) { return d.value; })

        var aScale = d3.scale.linear()
            .domain([0, d3.sum(values)])
            .range([0, twopi]);

        var marker = -1 * aScale(values[0]) / 2;
        var sectors = []
        for (var i = 0; i < values.length; i++) {
            var sector = {
                'startAngle': marker,
                'innerRadius': 0,
                'outerRadius': opts.chart_r
            }
            marker += aScale(values[i]);
            sector['endAngle'] = marker;
            sectors.push(sector);
        }

        var circle = chart.append("g")
                .attr("transform", "translate(" + opts.chart_cx + "," + opts.chart_cy + ")")

        var arc = d3.svg.arc();

        var arcs = circle.selectAll("g.slice")
            .data(sectors)
            .enter()
                .append("g")
                .classed("slice", true)
                .attr("data-slice", function(d, i) { return i; });

            arcs.append("path")
                .attr("fill", function(d, i) { return data[i].color; } )
                .attr("d", arc)
                .on("mouseover", function(d, i) {
                    chart.selectAll('g[data-slice="' + i + '"] path')
                        .attr('transform', 'scale(1.05)');
                    chart.selectAll('g[data-slice="' + i + '"] circle')
                        .attr('transform', 'scale(1.5)');
                    chart.selectAll('text[data-slice="' + i + '"]')
                        .style('display', null);
                    chart.selectAll('g[data-slice="' + i + '"] text')
                        .style('font-weight', 'bold');
                })
                .on("mouseout", function(d, i) {
                    chart.selectAll('g[data-slice="' + i + '"] path, g[data-slice="' + i + '"] circle')
                        .transition()
                            .duration(200)
                            .attr('transform', 'scale(1)');
                    chart.selectAll('text[data-slice="' + i + '"]')
                        .style('display', 'none');
                    chart.selectAll('g[data-slice="' + i + '"] text')
                        .style('font-weight', null);
                });


            /* arcs.append("text")
                .attr("transform", function(d) {
                    //we have to make sure to set these before calling arc.centroid
                    d.innerRadius = 0;
                    d.outerRadius = opts.chart_r;
                    return "translate(" + arc.centroid(d) + ")";
                })
                .attr("text-anchor", "middle")
                .text(function(d, i) { return data[i].key; })
                .attr('fill', opts.text_color)
                .style('font', '11px arial,sans-serif'); */

        // legend
        var legend_x = opts.chart_cx + opts.chart_r + opts.legend_padding;
        var legend_y = opts.chart_cy - (data.length * opts.row_height / 2);
        var legend = chart.append("g")
            .attr("transform", "translate(" + legend_x + "," + legend_y + ")");

        var sum = d3.sum(values);
        var legendItems = legend.selectAll("g.legend-item")
            .data(data)
            .enter()
                .append("g")
                .classed("legend-item", true)
                .attr("data-slice", function(d, i) { return i; })
                .attr("transform", function(d, i) { return "translate(0," + ((i + .5) * opts.row_height) + ")"; })

            legendItems.append("circle")
                .attr("fill", function(d, i) { return d.color; })
                .attr("cx", 0)
                .attr("cy", 0)
                .attr("r", opts.legend_r);

            legendItems.append("text")
                .attr("y", ".45em") // vertical-align: middle
                .attr("x", opts.legend_padding)
                .attr('fill', opts.text_color)
                .text(function(d, i) { return d.key? d.key + " (" + Math.round(100 * d.value / sum) + "%)" : ""; })
                .style('font', '11px arial,sans-serif');

        // amounts
        var format = d3.format(',.0f');
        var amounts = chart.selectAll("text.amount")
            .data(data)
            .enter()
                .append("text")
                .classed("amount", true)
                .attr("x", opts.chart_cx)
                .attr("y", opts.chart_cy)
                .attr("dy", ".5em") // vertical-align: middle
                .attr('fill', opts.amount_color)
                .attr('data-slice', function(d, i) { return i; })
                .text(function(d, i) { return '$' + format(d.value); })
                .style('font', 'bold 12px arial,sans-serif')
                .style('text-anchor', 'middle')
                .style('display', 'none');
    },
    TIMELINE_DEFAULTS: {
        chart_height: 195,
        chart_width: 300,
        chart_x: 85,
        chart_y: 10,
        right_gutter: 135,
        label_padding: 10,
        legend_padding: 15,
        legend_r: 5,
        dot_r: 5,
        row_height: 14,
        colors : ["#e96d24", "#15576e", "#f2e388", "#f2f1e4", "#efcc01"],
        axis_color: "#827d7d",
        tick_color: '#dcddde',
        text_color: "#666666",
        link_color: "#0a6e92",
        tick_length: 5
    },
    _get_timeline_size: function(opts) {
        return {
            'width': opts.chart_x + opts.chart_width + opts.right_gutter,
            'height': opts.chart_y + opts.chart_height + opts.tick_length + opts.label_padding + opts.row_height
        }
    },
    timeline_chart: function(div, data, opts) {
        if (typeof opts === 'undefined') opts = {};
        _.defaults(opts, D3Charts.TIMELINE_DEFAULTS);

        var size = D3Charts._get_timeline_size(opts);
        var chart = d3.select('#' + div).append("svg")
            .classed("chart-canvas", true)
            .attr("width", size.width)
            .attr("height", size.height);

        // scalers
        y = d3.scale.linear().domain([0, d3.max(_.flatten(_.map(data, function(d) { return d.timeline; })))]).range([opts.chart_height, 0]);

        var max_weeks = d3.max(_.map(data, function(item) { return item.timeline.length; }));
        x = d3.scale.linear().domain([0, max_weeks - 1]).range([opts.chart_x, opts.chart_x + opts.chart_width]);

        // y-ticks
        var ticks = chart.append('g')
            .classed('ticks', true)
            .attr('transform', 'translate(0,' + (opts.chart_y) + ')')
            .selectAll('line.graph-tick')
            .data(y.ticks(5))
            .enter();
                ticks.append('line')
                    .classed('graph-tick', true)
                    .attr("x1", opts.chart_x - opts.tick_length)
                    .attr("x2", opts.chart_x + opts.chart_width)
                    .attr("y1", y)
                    .attr("y2", y)
                    .style("stroke", function(d, i) { return i == 0 ? opts.axis_color : opts.tick_color })
                    .style("stroke-width", "1")
                var format = d3.format(',.0f');
                ticks.append('text')
                    .classed('chart-number', true)
                    .attr("x", opts.chart_x - opts.label_padding)
                    .attr("y", y)
                    .attr("dy", ".45em") // vertical-align: middle
                    .attr('fill', opts.text_color)
                    .text(function(d, i) { return '$' + format(d); })
                    .style('font', '11px arial,sans-serif')
                    .style('text-anchor', 'end');

        // x-ticks
        var dayToPx = function(d) { return x(d.day / 7) - .5; };
        // 0-indexed quarter starts
        var quarters = _.filter([
            {'label': 'Jan. 1', 'day': 0}, // jan 1
            {'label': 'Apr. 1', 'day': 90}, // apr 1
            {'label': 'Jul. 1', 'day': 181}, // jul 1
            {'label': 'Oct. 1', 'day': 273}, // oct 1
            {'label': 'Jan. 1', 'day': 365}, // jan 1
            {'label': 'Apr. 1', 'day': 455}, // apr 1
            {'label': 'Jul. 1', 'day': 546}, // jul 1
            {'label': 'Oct. 1', 'day': 638} // oct 1
        ], function(day) { return day.day < max_weeks * 7; });

        var ticks = chart.append('g')
            .classed('ticks', true)
            .selectAll('line.graph-tick')
            .data(quarters)
            .enter();
                ticks.append('line')
                    .classed('graph-tick', true)
                    .attr("x1", dayToPx)
                    .attr("x2", dayToPx)
                    .attr("y1", opts.chart_y + opts.chart_height)
                    .attr("y2", opts.chart_y + opts.chart_height + opts.tick_length)
                    .style("stroke", opts.axis_color)
                    .style("stroke-width", "1")
                ticks.append('text')
                    .classed('chart-number', true)
                    .attr("x", dayToPx)
                    .attr("y", opts.chart_y + opts.chart_height + opts.tick_length + opts.label_padding)
                    .attr("dy", ".45em") // vertical-align: middle
                    .attr('fill', opts.text_color)
                    .text(function(d, i) { return String(d.label); })
                    .style('font', '11px arial,sans-serif')
                    .style('text-anchor', 'middle');

        // lines
        var line = d3.svg.line()
            .x(function(d,i) { return x(i); })
            .y(y);

        chart.append('g')
            .classed('lines', true)
            .attr('transform', 'translate(0,' + (opts.chart_y) + ')')
            .selectAll('path.graph-line')
            .data(data)
                .enter()
                .append('path')
                .classed('graph-line', true)
                .attr('d', function(d, i) { return line(d.timeline); })
                .style('stroke-width', '3')
                .style('stroke', function(d, i) { return opts.colors[i]; })
                .style('fill', 'none');

        // floating box
        var make_box = function(x, y, color, text) {
            var box = chart.append('g')
                .classed('graph-float', true);

            var rect = box.append('rect');

            var label = box.append("text")
                .classed('chart-number', true)
                .attr("x", x - (2 * opts.label_padding))
                .attr("y", y)
                .attr("dy", ".5em") // vertical-align: middle
                .attr('fill', opts.text_color)
                .text(text)
                .style('font', '11px arial,sans-serif')
                .style('text-anchor', 'end');

            var width = label.node().getComputedTextLength();
            rect.attr('width', width + (2 * opts.label_padding))
                .attr('height', opts.row_height + opts.label_padding)
                .attr('x', x - width - (3 * opts.label_padding))
                .attr('y', y - opts.label_padding)
                .style('fill', '#fff')
                .style('stroke', color)
                .style('stroke-width', 1);

            return box;
        };

        // dots
        chart.append('g')
            .classed('graph-dots', true)
            .attr('transform', 'translate(0,' + (opts.chart_y) + ')')
            .selectAll('g.series-dots')
            .data(data)
                .enter()
                .append('g')
                .attr('data-series', function(d, i) { return i; })
                .classed('series-dots', true)
                .selectAll('circle')
                .data(function(d, i) { return d.timeline; })
                .enter()
                    .append('circle')
                    .attr("fill", 'rgba(0,0,0,0)')
                    .attr("cx", function(d,i) { return x(i); })
                    .attr("cy", y)
                    .attr("r", opts.dot_r)
                    .style('stroke', 'rgba(0,0,0,0)')
                    .style('stroke-width', 8)
                    .on('mouseover', function(d, i) {
                        var series = d3.select(this.parentNode).attr('data-series');
                        var color = opts.colors[parseInt(series)];
                        var dthis = d3.select(this).attr('fill', color);
                        this.floatingBox = make_box(dthis.attr('cx'), parseFloat(dthis.attr('cy')) + opts.chart_y, color, '$' + format(d));

                        var circle = chart.selectAll('g.legend-item[data-series="' + series + '"] circle')
                            .attr('transform', 'scale(1.5)');
                        clearTimeout(circle.node().timeout);
                        chart.selectAll('g.legend-item[data-series="' + series + '"] text')
                            .style('font-weight', 'bold');
                    })
                    .on('mouseout', function(d, i) {
                        var series = d3.select(this.parentNode).attr('data-series');
                        d3.select(this).attr("fill", 'rgba(0,0,0,0)');
                        this.floatingBox.remove();

                        var circle = chart.selectAll('g.legend-item[data-series="' + series + '"] circle');
                        circle.node().timeout = setTimeout(function() {
                            circle.transition()
                                .duration(200)
                                .attr('transform', 'scale(1)');
                            chart.selectAll('g.legend-item[data-series="' + series + '"] text')
                                .style('font-weight', null);
                        }, 100)
                    });

        // axes
        chart.append("line")
            .attr("x1", opts.chart_x - .5)
            .attr("x2", opts.chart_x - .5)
            .attr("y1", opts.chart_y)
            .attr("y2", opts.chart_y + opts.chart_height + opts.tick_length)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");

        // legend
        var legend_x = opts.chart_x + opts.chart_width + opts.legend_padding;
        var legend_y = opts.chart_y + (opts.chart_height / 2) - (data.length * opts.row_height / 2);
        var legend = chart.append("g")
            .attr("transform", "translate(" + legend_x + "," + legend_y + ")");

        var legendItems = legend.selectAll("g.legend-item")
            .data(data)
            .enter()
                .append("g")
                .classed("legend-item", true)
                .attr("data-series", function(d, i) { return i; })
                .attr("transform", function(d, i) { return "translate(0," + ((i + .5) * opts.row_height) + ")"; })

            legendItems.append("circle")
                .attr("fill", function(d, i) { return opts.colors[i]; })
                .attr("cx", 0)
                .attr("cy", 0)
                .attr("r", opts.legend_r)
                .each(function() {
                    this.timeout = null;
                })

            legendItems.each(function(d, i) {
                var parent = d3.select(this);
                if (d.href) {
                    parent = parent.append("a")
                    parent.attr('xlink:href', d.href);
                }

                parent.append("text")
                    .attr("y", ".45em") // vertical-align: middle
                    .attr("x", opts.legend_padding)
                    .attr('fill', parent.node().tagName.toLowerCase() == 'a' ? opts.link_color : opts.text_color)
                    .text(function(d, i) { return d.name; })
                    .style('font', '11px arial,sans-serif');
            });
    },
    THREEPANE_BAR_DEFAULTS: {
        chart_height: 260,
        chart_width: 800,
        row_height: 16,
        bar_height:10,
        bar_gutter: 5,
        colors : ["#efcc01", "#f2e388"],
        text_color: "#666666",
        amount_color: "#000000",
        link_color: "#0a6e92",
        axis_color: "#827d7d",
    },
    threepane_bar: function(div, data, opts) {
        if (typeof opts == 'undefined') opts = {};
        _.defaults(opts, D3Charts.THREEPANE_BAR_DEFAULTS);

        var leftFullWidth = opts.chart_width / 5,
            leftFullHeight = opts.chart_height,
            centerFullHeight = opts.chart_height * 0.65,
            rightFullHeight = opts.chart_height * 0.35;

        var barMargin = {top: 5, right: 100, bottom: 10, left: 200},
            centerFullWidth = opts.chart_width - leftFullWidth,
            barChartWidth = centerFullWidth - barMargin.left - barMargin.right,
            barChartHeight = centerFullHeight - barMargin.top - barMargin.bottom;

        var rightFullWidth = opts.chart_width - leftFullWidth;

        var formatMoney = function (e) {
            var currencyString;
            if (e < 1000) {
                currencyString = e;
            } else if (e > 999           && e < 1000000) {
                currencyString = e/1000+"K";
            } else if (e > 999999        && e < 1000000000){
                currencyString = e/1000000+"M"
            } else if (e > 999999999     && e < 1000000000000){
                currencyString = e/1000000000+"B"
            } else {
                // cry(forever);
                currencyString = e/1000000000000 + "T"
            }
            return "$" + currencyString;
        };

        var formatTickLabel = function(d) { return "";};

        // Set up panes
        mainDiv = d3.select("#"+div)
          .style("display", "block")
          .style("width", leftFullWidth + rightFullWidth + "px")
          .style("height", leftFullHeight + "px");

        var leftPane = mainDiv.select(".leftPane")
          .style("width", leftFullWidth + "px")
          .style("height", leftFullHeight + "px");

        var centerPane = mainDiv.select(".rightTopPane")
          .style("width", centerFullWidth + "px")
          .style("height", centerFullHeight + "px")
          .select("svg")
          .attr("width", centerFullWidth + "px")
          .attr("height", centerFullHeight + "px");

        var rightPane = mainDiv.select(".rightBottomPane")
          .style("width", centerFullWidth + "px")
          .style("height", rightFullHeight + "px");

        var categoryTitle = rightPane.select(".categoryTitle");

        var categorySubtitle = rightPane.select(".categorySubtitle");

        var categoryDescription = rightPane.select(".categoryDescription");

        var categories = data.slice(0,10);
        testvar = categories;
        console.log(categories);

        var allData = [];
        var mostChildren = 0;
        categories.forEach(function(d){
          d.identifier = d.name;
          mostChildren = d3.max([d.children.length, mostChildren]);
          d.children.forEach(function(f){
            f.categoryName = d.name;
            newf = f;
            newf['categoryName'] = d.name;
            newf['all_key'] = f.name+'_'+d.identifier;
            allData.push(newf);
            })
        });
        var top10 = allData.sort(function(a,b){ return b.amount - a.amount }).slice(0,10)

        var yScale = d3.scale.ordinal()
        .domain(d3.range(mostChildren))
        .rangeBands([0, barChartHeight]);
        //.rangeBands([0, mostChildren * opts.row_height]);

        var xScale = d3.scale.linear()
        .range([0, barChartWidth]);
        
        xScale.domain([0, d3.max(allData, function(d) {return d.amount;})]);

        var barChart = centerPane.append("svg:g")
              .attr("transform","translate(" + barMargin.left + "," + barMargin.top + ")");

        barChart.append("line")
            .attr("x1", -.5)
            .attr("x2", -.5)
            .attr("y1", 0)
            .attr("y2", barChartHeight)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");

        barChart.append("line")
            .attr("x1", -.5)
            .attr("x2", barChartWidth)
            .attr("y1", barChartHeight)
            .attr("y2", barChartHeight)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");

        function allTopTen(){
          drawRight(top10);
        }

        function category_selector_label(d) {
            return d.name;
        }


        leftPane.selectAll("div")
            .data(categories)
            .enter()
            .append("div")
            .style("width",leftFullWidth+"px")
            .style("height",opts.chart_height / 10 + "px")
            .classed("selector","true")
            .on("mouseover", function() { darken(d3.select(this)); } )
            .on("mouseout", function() { undarken(d3.select(this)); })
            .on("click", function (d) {
                d3.select(this.parentNode).select('.focused').classed("focused",false);
                d3.select(this).classed("focused",true);
                drawCenter(d);
                drawRight(d);
            })
            .append("div").html(function(d) { return category_selector_label(d) }).style("pointer-events","none").style("line-height",opts.chart_height / 10 + "px");

        var darken = function(selection) {
                selection.classed("darkened",true);
        }

        var undarken = function(selection) {
                selection.classed("darkened",false);
        }

        var drawCenter = function(parentCategory) {
          //console.log(parentCategory);
          if (parentCategory.hasOwnProperty('name')) {
            var parentIdentifier = parentCategory.identifier;
            var parentTotal = parentCategory.amount;
            var childData = parentCategory.children;
          } else {
            var parentIdentifier = false;
            var childData = parentCategory;
          }

          childData.forEach(function(d) {
              if (parentIdentifier) {
                d.all_key = d.name+'_'+parentIdentifier;
              }
          });

          barChart.selectAll(".axis").remove();

          yScale.domain(childData.map(function(d) {return d.all_key;}));

            labels = centerPane.selectAll("g.chart-label")
                  .data(childData,function(d){ return d.all_key;});

            labels.enter().append("g")
                .classed('chart-label', true)
                .attr("transform", function(d, i) { return "translate(5," + ((yScale(d.all_key) + yScale.rangeBand() / 2) + barMargin.top) + ")"; })
                .each(function(d, i) {
                    var parent = d3.select(this);
                    if (d.href) {
                        parent = parent.append("a")
                        parent.attr('xlink:href', d.href);
                    }
                    parent.append("text")
                        .attr("y", ".15em") // vertical-align: middle
                        .attr('fill', parent.node().tagName.toLowerCase() == 'a' ? opts.link_color : opts.text_color)
                        .text(function(d, i) { return d.name; })
                        .style('font', '11px arial,sans-serif');
                });
                /*.style("fill-opacity",1e-6)
                .transition()
                .duration(500)
                .style("fill-opacity",1)
                .delay(200);*/

            labels.exit()
                /*.transition()
                .duration(500)
                .style("fill-opacity", 1e-6)
                .delay(200)*/
                .remove();

            bars = barChart.selectAll(".bar")
              .data(childData,function(d){ return d.all_key;});

            var barLeftMargin = 0;

            bars.enter().append("g")
                .attr("class", "bar")
                .attr("transform", function(d) {
                    return "translate("+barLeftMargin+","+yScale(d.all_key)+")"
                })
                .append("path")
                .attr("d", function(d) {
                        var x = 0;
                        var y = 0;
                        //var h = yScale.rangeBand(d);
                        var h = opts.bar_height;

                        var r = 4;

                        var w = xScale(d.amount);

                        var array = [].concat(
                            ["M", x, y],
                            ["L", d3.max([x + w - r, 0]), y, "Q", x + w, y, x + w, y + r],
                            ["L", x + w, d3.max([y + h - r, 0]), "Q", x + w, y + h, d3.max([x + w - r, 0]), y + h],
                            ["L", x, y + h, "Z"]
                    );

                    return array.join(" ");
                })
                .style("fill",opts.colors[0]);
                /*.style("fill-opacity",1e-6);
                .transition()
                .duration(500)
                .style("fill-opacity",1)
                .delay(200);*/
      
            bars.exit()
              /*.transition()
              .duration(500)
              .style("fill-opacity", 1e-6)
              .delay(200)*/
              .remove();
        
            var format = d3.format(',.0f');
            var numbers = barChart.selectAll("text.chart-number")
              .data(childData,function(d){ return d.all_key;});    
            
            numbers.enter().append("text")
                .classed('chart-number', true)
                .attr("x", function(d, i) { return xScale(d.amount) + opts.bar_gutter; })
                .attr("y", function(d, i) { return yScale(d.all_key) + yScale.rangeBand() / 2; })
                .attr("dy", ".15em") // vertical-align: middle
                .attr('fill', opts.text_color)
                .text(function(d, i) { return '$' + format(d.amount); })
                .style('font', '11px arial,sans-serif');

            numbers.exit()
              .remove();

          };

        var drawRight = function(parentCategory) {
          if (parentCategory.hasOwnProperty('name')) {
            var parentIdentifier = parentCategory.identifier;
            var parentTotal = parentCategory.amount;
          } else {
            var parentIdentifier = 'All Bills';
            var parentTotal = parentCategory.amount;
          }

          var display_metadata = opts.metadata_display_fct(parentCategory);
          categoryTitle.html(display_metadata.title);
          categorySubtitle.html(display_metadata.subtitle);
          categoryDescription.html(display_metadata.description);
          $('.ellipsis').ellipsis();
        };

        function initCenter() {
            $('.leftPane .selector').first().click();
        }

        initCenter();
    },
    TWOPANE_PIE_DEFAULTS: {
        chart_height: 200,
        chart_width: 750,
        row_height: 16,
        bar_height:10,
        bar_gutter: 5,
        donut_outer_r: 70,
        colors : ["#efcc01", "#f2e388"],
        text_color: "#666666",
        amount_color: "#000000",
        link_color: "#0a6e92",
        axis_color: "#827d7d",
    },
    twopane_pie: function(div, data, opts) {

        if (typeof opts == 'undefined') opts = {};
        _.defaults(opts, D3Charts.TWOPANE_PIE_DEFAULTS);

        var pieMargin = {top: 25, right: 15, bottom: 20, left: 90},
            //(opts.chart_height - (opts.donut_outer_r*2)) / 2,
            rad = opts.donut_outer_r,
            innerRad = opts.donut_outer_r / 3,
            svgtransbase = "translate(" + (rad + pieMargin.left) + "," + (rad + pieMargin.top) + ")",
            leftFullWidth = (rad*2) + pieMargin.left + pieMargin.right,
            leftFullHeight = (rad*2) + pieMargin.top + pieMargin.bottom;

        var barMargin = {top: 20, right: 80, bottom: 20, left: 220},
            rightFullWidth = opts.chart_width - leftFullWidth;
            barChartWidth = rightFullWidth - barMargin.left - barMargin.right,
            barChartHeight = leftFullHeight - barMargin.top - barMargin.bottom;
            
        var decFormat = d3.format(',.2f');

        var formatMoney = function (e) {
            var currencyString;
            if (e < 1000) {
                currencyString = decFormat(e);
            } else if (e > 999           && e < 1000000) {
                currencyString = decFormat(e/1000)+"K";
            } else if (e > 999999        && e < 1000000000){
                currencyString = decFormat(e/1000000)+"M"
            } else if (e > 999999999     && e < 1000000000000){
                currencyString = decFormat(e/1000000000)+"B"
            } else {
                // cry(forever);
                currencyString = decFormat(e/1000000000000) + "T"
            }
            return "$" + currencyString;
        };

        var formatTickLabel = function(d) { return "";};
                                                    //d.split("_")[0];};
        var titleFormatMoney = d3.format(',.0f');

        //Set up panes
        mainDiv = d3.select("#"+div)
          .append("div") // http://code.google.com/p/chromium/issues/detail?id=98951
          .style("display", "inline-block")
          .style("width", leftFullWidth + rightFullWidth + "px")
          .style("height", leftFullHeight + "px");

        var leftPane = mainDiv.append("div")
          .style("display", "inline-block")
          .attr("width", leftFullWidth)
          .attr("height", leftFullHeight)
          .append("svg:svg")
          .attr("width",leftFullWidth)
          .attr("height",leftFullHeight);

        var rightPane = mainDiv.append("div")
          .style("display", "inline-block")
          .attr("width", rightFullWidth)
          .attr("height", leftFullHeight)
          .append("svg:svg")
          .attr("width", rightFullWidth)
          .attr("height", leftFullHeight);

        var barChart = rightPane.append("svg:g")
              .attr("transform","translate(" + barMargin.left + "," + barMargin.top + ")");

        var categories = data;

        var allData = [];
        var overallSum = 0;
        var mostChildren = 0;
        categories.forEach(function(d){
          overallSum += d.amount;
          mostChildren = d3.max([d.children.length, mostChildren]);
          d.children.forEach(function(f){
            f.categoryName = d.name;
            newf = f;
            newf['categoryName'] = d.name;
            newf['all_key'] = f.name+'_'+d.name;
            allData.push(newf); 
          })
        });
        var top10 = allData.sort(function(a,b){ return b.amount - a.amount }).slice(0,10)
        
        var yScale = d3.scale.ordinal()
        .domain(d3.range(mostChildren))
        .rangeBands([0, barChartHeight]);

        var xScale = d3.scale.linear()
        .range([0, barChartWidth]);
        
        barChart.append("line")
            .attr("x1", -.5)
            .attr("x2", -.5)
            .attr("y1", 0)
            .attr("y2", barChartHeight)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");

        barChart.append("line")
            .attr("x1", -.5)
            .attr("x2", barChartWidth)
            .attr("y1", barChartHeight)
            .attr("y2", barChartHeight)
            .style("stroke", opts.axis_color)
            .style("stroke-width", "1");

        /*
        var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .tickFormat(formatTickLabel);

        var xAxis = d3.svg.axis()
        .scale(x)
        .orient("top")
        .ticks(5)
        .tickFormat(formatMoney);
        */

        xScale.domain([0, d3.max(allData, function(d) {return d.amount;})]);
        
        var pieChart = leftPane.append("svg:g")
            .attr("transform", svgtransbase);

        var pie = d3.layout.pie()
            .value(function(d) { return d.amount; })
            .sort(function(a, b) { return b.amount - a.amount; });

        categories = pie(categories);

        var arc = d3.svg.arc()
            .innerRadius(innerRad)
            .outerRadius(rad);

        function resetRotation() {
          pieChart.transition().duration(500).attr("transform",svgtransbase);
        }

        function resetAllSlices() {
          pieChart.selectAll("g path")
                .classed("focusedSlice",false)
                .attr("transform","scale(1)");
        }

        function allTopTen(){
          drawRight(top10);
        }

        var center = leftPane.append("svg:g")
            .attr("transform", svgtransbase);


        var g = pieChart.selectAll("g")
            .data(categories)
            .enter().append("svg:g")
            .attr("data-slice", function(d,i) { return i; });

        //testfunc2 = pie;

        g.append("svg:path")
            .attr("d", arc)
            .style("fill", function(d) { return opts.colors[d.data.name]; })
            .on("click",(function(d,i) {
                    resetAllSlices();
                    pieChart.selectAll('g[data-slice="'+i+'"] path')
                      .classed('focusedSlice',true)
                      .attr('transform', 'scale(1.2)');
                    newtrans = svgtransbase + "rotate(" + (-1 * angle(d)) + ")";
                    pieChart.transition().duration(500).attr("transform",newtrans);
                    drawRight(d);
                    }))
            .on("mouseover",function(d,i){
                pieChart.selectAll('g[data-slice="'+i+'"] path')
                  .attr('transform', 'scale(1.05)');
                  })
            .on("mouseout",function(d,i){
                pieChart.selectAll('g[data-slice="'+i+'"] path')
                  .each(function(d) { 
                        var slice = d3.select(this);
                        if (slice.classed('focusedSlice')){
                                slice.attr('transform','scale(1.2)');
                        } else {
                                slice.attr('transform','scale(1)');
                        }})
                })
          .append("svg:title")
          .text(function(d) { return d.data.name + ": " + formatMoney(d.data.amount); });

        center.append("svg:circle")
            .attr("cx",0)
            .attr("cy",0)
            .attr("r",(innerRad * 1.2))
            .attr("fill","#dcddde")
            .on("click",function(d){
                resetRotation();
                resetAllSlices();
                allTopTen();});

        center.append("svg:text")
            .attr("dy", ".35em")
            .attr("text-anchor", "middle")
            .classed("allLabel",true)
            .text("All")
            .style("pointer-events","none");

         /* fade in pie chart
         g.style("fill-opacity",1e-6)
                .transition()
                .duration(1000)
                .style("fill-opacity",1); */

        /* scale in pie chart */
         g.attr("transform","scale(0.1)")
                .transition()
                .duration(1000)
                .attr("transform","scale(1)");


        function angle(d) {
          var rot;
          var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
          rot = a;
          return rot;
        }

        var drawRight = function(parentCategory) {
          if (parentCategory.hasOwnProperty('data')) {
            var parentName = parentCategory.data.name;
            var parentTotal = parentCategory.data.amount;
            var childData = parentCategory.data.children;
          } else {
            var parentName = false;
            var childData = parentCategory;
          }

          childData.forEach(function(d) {
              if (parentName) {
                d.all_key = d.name+'_'+parentName;
              }
          });

          barChart.selectAll(".axis").remove();

          yScale.domain(childData.map(function(d) {return d.all_key;}));

          //barChart.append("g")
          //    .attr("class", "x axis")
          //    .attr("transform", "translate(10,0)") // now just placing it at the top
          //    .call(xAxis);

          var yaxis = barChart.append("g")
            .attr("class", "y axis");

          var barTransition = rightPane.transition().duration(1000).delay(1000);

          //barTransition.select(".y.axis")
            //  .call(yAxis)
            //.selectAll("g");

            // labels
            labels = rightPane.selectAll("g.chart-label")
                  .data(childData,function(d){ return d.all_key;});

            labels.enter().append("g")
                .classed('chart-label', true)
                .attr("transform", function(d, i) { return "translate(20," + ((yScale(d.all_key) + yScale.rangeBand() / 2) + barMargin.top) + ")"; })
                .each(function(d, i) {
                    var parent = d3.select(this);
                    if (d.href) {
                        parent = parent.append("a")
                        parent.attr('xlink:href', d.href);
                    }
                    parent.append("text")
                        .attr("y", ".15em") // vertical-align: middle
                        .attr('fill', parent.node().tagName.toLowerCase() == 'a' ? opts.link_color : opts.text_color)
                        .text(function(d, i) { return d.name; })
                        .style('font', '11px arial,sans-serif');
                })
                .style("fill-opacity",1e-6)
                .transition()
                .duration(1000)
                .style("fill-opacity",1)
                .delay(800);

            barTransition.selectAll("g.chart-label")
                .attr("transform", function(d, i) { return "translate(20," + ((yScale(d.all_key) + yScale.rangeBand() / 2) + barMargin.top) + ")"; })

            labels.exit()
                .transition()
                .duration(1000)
                .style("fill-opacity", 1e-6)
                .remove()
        

          yaxis.append("text")
              .classed("ytitle",true)
              .attr("transform", "translate(-"+barMargin.left+",-"+ barMargin.top +")")
              .attr("dy", ".85em")
              .style("text-anchor", "left")
              .style("fill", function(d) { if (parentName) { return opts.colors[parentName] } else { return 'All';} })
              .text(function (d) { if (parentName) {return parentName +": $"+ titleFormatMoney(parentTotal)} else {return "Top Ten Overall";}});

            /*
            bars.enter().append("rect")
                .attr("class", "bar")
                .style("fill", function(d) { if (parentName) { return opts.colors[parentName] } else { return opts.colors[d.categoryName];} })
                .attr("width", function(d) { return xScale(d.amount);})
                .attr("height", yScale.rangeBand)
                .attr("x", 10)
                .attr("y", function(d) {
                    return yScale(d.all_key); })
                .style("fill-opacity",1e-6)
                .transition()
                .duration(1000)
                .style("fill-opacity",1)
                .delay(800);
                */
            
            bars = barChart.selectAll(".bar")
              .data(childData,function(d){ return d.all_key;});

            var barLeftMargin = 0;
            
            bars.enter().append("g")
                .attr("class", "bar")
                .attr("transform", function(d) {
                    return "translate("+barLeftMargin+","+yScale(d.all_key)+")"
                })
                .append("path")
                .attr("d", function(d) {
                        var x = 0;
                        var y = 0;
                        //var h = yScale.rangeBand(d);
                        var h = opts.bar_height;

                        var r = 4;

                        var w = xScale(d.amount);

                        var array = [].concat(
                            ["M", x, y],
                            ["L", d3.max([x + w - r, 0]), y, "Q", x + w, y, x + w, y + r],
                            ["L", x + w, d3.max([y + h - r, 0]), "Q", x + w, y + h, d3.max([x + w - r, 0]), y + h],
                            ["L", x, y + h, "Z"]
                    );

                    return array.join(" ");
                })
                .style("fill", function(d) { if (parentName) { return opts.colors[parentName] } else { return opts.colors[d.categoryName];} })
                .style("fill-opacity",1e-6)
                .transition()
                .duration(1000)
                .style("fill-opacity",1)
                .delay(800);

            //barTransition.selectAll(".bar")
              //.attr("y", function(d) {return yScale(d.all_key);});
           
            barTransition.selectAll(".bar") 
                .attr("transform", function(d) {
                    return "translate("+barLeftMargin+","+yScale(d.all_key)+")"
                });
            
            bars.exit()
              .transition()
              .duration(1000)
              .style("fill-opacity", 1e-6)
              .remove(); 
            
            var format = d3.format(',.0f');
            var numbers = barChart.selectAll("g.chart-number-group")
              .data(childData,function(d){ return d.all_key;});    
            
            numbers.exit()
              .remove();

            numbers.attr("transform", function(d){
                    return "translate(0,"+yScale(d.all_key)+ yScale.rangeBand() / 2+")";
                });
                
            
            numbers.enter().append("g")
                .classed('chart-number-group', true)
                .append("text")
                .attr("x", function(d, i) { return xScale(d.amount) + opts.bar_gutter; })
                .attr("y", function(d, i) { return yScale(d.all_key) + yScale.rangeBand() / 2; })
                .classed('chart-number', true)
                .attr("dy", ".15em") // vertical-align: middle
                .text(function(d, i) { return '$' + format(d.amount); })
                .style('font', '11px arial,sans-serif')
                .style('fill', opts.text_color)
                .style("fill-opacity",1e-6)
                .transition()
                .duration(1000)
                .style("fill-opacity",1)
                .delay(800);
            
            /*barTransition.selectAll(".chart-number")
                .each(function(d){
                    d3.select(this)
                        .attr("transform", function(d){
                                            return "translate(0,"+yScale(d.all_key)+ yScale.rangeBand() / 2+")";
                        })
                });
            */


          };
        resetRotation();
        allTopTen();
        }

}

BrisketModern = {
    contribution_barchart: function(div, data) {
        D3Charts.barchart(div, data);
    },
    contribution_single_barchart: function(div, data) {
        if (data.length === 0) return;

        graph_data = _.map(data, function(item) {
            return {
                name: item.key,
                href: item.href,
                values: [parseFloat(item.value)]
            };
        });

        Brisket.contribution_barchart(div, graph_data);
    },
    contribution_stacked_barchart: function(div, data) {
        if (data.length === 0) return;

        graph_data = _.map(data, function(item) {
            return {
                name: item.key,
                href: item.href,
                values: [parseFloat(item.value_employee), parseFloat(item.value_pac)]
            };
        });
        Brisket.contribution_barchart(div, graph_data);
    },
    piechart: function(div, data, colors) {
        var in_data = []
        var opts = {colors: []}
        _.each(data, function(value, key) {
            if (value > 0) {
                in_data.push({'key': key, 'value': value});
                opts.colors.push(colors[key]);
            }
        })
        D3Charts.piechart(div, in_data, opts);
    },
    threepane_bar : function(div, data, display_metadata) {
        var opts = {'metadata_display_fct': display_metadata};
        D3Charts.threepane_bar(div, data, opts);
    },
    twopane_pie : function(div, data, colors) {
        var opts = {'colors': colors};
        D3Charts.twopane_pie(div, data, opts);
    },
    party_piechart: function(div, data) {
        var party_colors = {"Republicans": "#e60002", "Democrats": "#186582", "Other" : "#dcddde"};
        Brisket.piechart(div, data, party_colors);
    },
    indiv_pac_piechart: function(div, data) {
        var indiv_pac_colors = {"Individuals": '#efcc01', "PACs": '#f2e388', "Unknown": '#dcddde'};
        Brisket.piechart(div, data, indiv_pac_colors);
    },
    local_piechart: function(div, data) {
        var local_colors = {"In-State": '#efcc01', "Out-of-State": '#f2e388', "Unknown": '#dcddde'};
        Brisket.piechart(div, data, local_colors);
    },
    level_piechart: function(div, data) {
        var level_colors = {"Federal": '#efcc01', "State": '#f2e388'};
        Brisket.piechart(div, data, level_colors);
    },
    fec_piechart: function(div, data) {
        var fec_colors = {"Individuals": "#efcc01", "PACs": "#f2e388", "Party": "#15576e", "Self-Financing": "#f2f1e4", "Transfers": "#e96d24"};
        Brisket.piechart(div, data, fec_colors);
    },
    timeline_chart: function(div, data) {
        D3Charts.timeline_chart(div, data);
    },
    bills_threepane_bar : function(div, data) {
        //console.log('bills function received: '+div);
        function display_bills_metadata(node) {
            var md_html = {'title':'', 'subtitle': '', 'description': ''};

            summary = node.metadata.display_summary

            md_html['title'] = '<a href="'+node.metadata.url+'">';
            md_html['title'] += '<h3 class="ellipsis">' + node.metadata.display_title + '</h3></a>';
            //md_html['subtitle'] = '<h3>' + node.metadata.display_subtitle +'</h3>';
            md_html['description']  = '<dl class="ellipsis multiline">';
            if (node.metadata.display_nicknames) {
                md_html['description'] += '<dt>Nicknames</dt>';
                md_html['description'] += '<dd>' + node.metadata.display_nicknames + '</dd>';
            }
            md_html['description'] += '<dt>Issue</dt>';
            md_html['description'] += '<dd>' + node.metadata.bill_issue + '</dd>';
            md_html['description'] += '<dt>Last Action</dt>';
            if (node.metadata.last_action) {
                md_html['description'] += '<dd>' + node.metadata.last_action.type.toUpperCase() + ': ' + node.metadata.last_action.text + '</dd>';
            } else {
                md_html['description'] += '<dd>No information available</dd>';
            }
            md_html['description'] += '<dt>Summary</dt>';
            md_html['description'] += '<dd>' + summary + '</dd>'
            md_html['description'] += '</dl>';
            return md_html;
        }

        Brisket.threepane_bar(div, data, display_bills_metadata);

    },
    issues_threepane_bar : function(div, data) {
        //console.log('issues function received: '+div);

        function display_issues_metadata(node) {
            //console.log(node);
            var md_html = {'title':'', 'subtitle': '', 'description': ''};

            md_html['title'] = '<h3>' + node.metadata.general_issue + '</h3>';
            md_html['subtitle'] = '<h3></h3>';
            // + node.metadata.general_issue_code + '</h3>';
            md_html['description']  = '<ul>';
            /* Not populated yet
            for (i in node.metadata.top_bills) {
                md_html['description']  += '<li>' + node.metadata.top_bills[i];
            }
            */
            md_html['description'] += '</ul>';

            return md_html;
        }

        Brisket.threepane_bar(div, data, display_issues_metadata);
    },
    party_twopane_pie : function(div,data) {
        var party_colors = {"Republicans": "#e60002", "Democrats": "#186582", "Other" : "gray"};
        Brisket.twopane_pie(div, data, party_colors);
    },
    pol_group_twopane_pie : function(div,data) {
        var pol_group_colors = {"Direct": "#f27e01", "Associated Individuals": "#efcc01"};
        Brisket.twopane_pie(div, data, pol_group_colors);
    },
    state_fed_twopane_pie : function(div,data) {
        var level_colors = {"Federal": '#efcc01', "State": '#f2e388'};
        Brisket.twopane_pie(div, data, level_colors);
    },
}

BrisketServer = {
    contribution_barchart: function(div, data) {
        var in_data = [];
        _.each(data, function(item) {
            in_data.push({
                'name': '',
                'href': '',
                'values': item
            })
        });
        D3Charts.barchart(div, in_data);
    },
    piechart: function(div, data) {
        var in_data = []
        var opts = {colors: []}
        _.each(data, function(value) {
            in_data.push({'key': '', 'value': value[1]});
            opts.colors.push(value[2]);
        })
        D3Charts.piechart(div, in_data, opts);
    },
    timeline_chart: function(div, data) {
        var in_data = [];
        _.each(data, function(item) {
            in_data.push({
                'name': '',
                'href': '',
                'timeline': item
            });
        })
        D3Charts.timeline_chart(div, in_data);
    }
}
_.defaults(BrisketServer, BrisketModern);

// base64 function for external links
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(a){var b="";var c,chr2,chr3,enc1,enc2,enc3,enc4;var i=0;a=Base64._utf8_encode(a);while(i<a.length){c=a.charCodeAt(i++);chr2=a.charCodeAt(i++);chr3=a.charCodeAt(i++);enc1=c>>2;enc2=((c&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64}else if(isNaN(chr3)){enc4=64}b=b+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4)}return b},decode:function(a){var b="";var c,chr2,chr3;var d,enc2,enc3,enc4;var i=0;a=a.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(i<a.length){d=this._keyStr.indexOf(a.charAt(i++));enc2=this._keyStr.indexOf(a.charAt(i++));enc3=this._keyStr.indexOf(a.charAt(i++));enc4=this._keyStr.indexOf(a.charAt(i++));c=(d<<2)|(enc2>>4);chr2=((enc2&15)<<4)|(enc3>>2);chr3=((enc3&3)<<6)|enc4;b=b+String.fromCharCode(c);if(enc3!=64){b=b+String.fromCharCode(chr2)}if(enc4!=64){b=b+String.fromCharCode(chr3)}}b=Base64._utf8_decode(b);return b},_utf8_encode:function(a){a=a.replace(/\r\n/g,"\n");var b="";for(var n=0;n<a.length;n++){var c=a.charCodeAt(n);if(c<128){b+=String.fromCharCode(c)}else if((c>127)&&(c<2048)){b+=String.fromCharCode((c>>6)|192);b+=String.fromCharCode((c&63)|128)}else{b+=String.fromCharCode((c>>12)|224);b+=String.fromCharCode(((c>>6)&63)|128);b+=String.fromCharCode((c&63)|128)}}return b},_utf8_decode:function(a){var b="";var i=0;var c=c1=c2=0;while(i<a.length){c=a.charCodeAt(i);if(c<128){b+=String.fromCharCode(c);i++}else if((c>191)&&(c<224)){c2=a.charCodeAt(i+1);b+=String.fromCharCode(((c&31)<<6)|(c2&63));i+=2}else{c2=a.charCodeAt(i+1);c3=a.charCodeAt(i+2);b+=String.fromCharCode(((c&15)<<12)|((c2&63)<<6)|(c3&63));i+=3}}return b}};

BrisketFallback = {
    PATH: 'http://localhost:3000/chart/',
    draw_graph: function(div, data, remote_name, size) {
        var url = BrisketFallback.PATH + remote_name + '/' + Base64.encode($.toJSON(data));
        var graph = document.getElementById(div);
        if (!graph) return;
        graph.style.width = size.width + 'px';
        graph.style.height = size.height + 'px';
        graph.style.background = 'url(' + url + ') no-repeat top left';
    },
    draw_legend: function(chart, legend_x, legend_y, row_height, items) {
        chart.css('position', 'relative');
        _.each(items, function(item, index) {
            var listing = $('<div>')
                .html(
                    typeof item.href !== 'undefined' && item.href ?
                    '<a href="' + item.href + '">' + item.name + '</a>' :
                    item.name
                )
                .css({
                    'position': 'absolute',
                    'left': legend_x + 'px',
                    'top': (legend_y + (row_height * index) + 2) + 'px',
                    'font': '11px arial,sans-serif'
                });
            chart.append(listing);
        })
    },
    contribution_barchart: function(div, data) {
        var legend_data = [];
        var in_data = [];
        _.each(data, function(item) {
            legend_data.push({
                'name': item.name,
                'href': item.href,
                'values': item.values
            })
            in_data.push(item.values);
        });

        BrisketFallback.draw_graph(div, in_data, 'contribution_barchart', D3Charts._get_barchart_size(D3Charts.BARCHART_DEFAULTS));

        var chart = $('#' + div);
        var opts = D3Charts.BARCHART_DEFAULTS;
        var legend_x = opts.left_gutter;
        var legend_y = opts.chart_y + 3;
        BrisketFallback.draw_legend(chart, legend_x, legend_y, opts.row_height, legend_data);
    },
    piechart: function(div, data, colors) {
        var in_data = [];
        var legend_data = [];
        var sum = d3.sum(_.map(data, function(item) { return item; }));;
        _.each(data, function(value, key) {
            if (value > 0) {
                in_data.push([key, value, colors[key]]);
                legend_data.push({'name': key + " (" + Math.round(100 * value / sum) + "%)", 'value': value});
            }
        })
        BrisketFallback.draw_graph(div, in_data, 'piechart', D3Charts._get_piechart_size(D3Charts.PIECHART_DEFAULTS));

        /* emulate legend locally */
        var legend_data = _.sortBy(legend_data, function(d) { return d.value; }).reverse();
        var opts = D3Charts.PIECHART_DEFAULTS;
        var legend_x = opts.chart_cx + opts.chart_r + (2 * opts.legend_padding);
        var legend_y = opts.chart_cy - (legend_data.length * opts.row_height / 2);
        var chart = $('#' + div);
        BrisketFallback.draw_legend(chart, legend_x, legend_y, opts.row_height, legend_data);
    },
    timeline_chart: function(div, data) {
        if (data.length === 0) return;

        var in_data = _.map(data, function(item) {
            return item.timeline;
        })
        BrisketFallback.draw_graph(div, in_data, 'timeline_chart', D3Charts._get_timeline_size(D3Charts.TIMELINE_DEFAULTS));

        /* emulate legend locally */
        var opts = D3Charts.TIMELINE_DEFAULTS;
        var legend_x = opts.chart_x + opts.chart_width + (2 * opts.legend_padding);
        var legend_y = opts.chart_y + (opts.chart_height / 2) - (data.length * opts.row_height / 2);
        var chart = $('#' + div);
        BrisketFallback.draw_legend(chart, legend_x, legend_y, opts.row_height, data);
    }
}
_.defaults(BrisketFallback, BrisketModern);

if (!(document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure", "1.1")) || (document.location.search && document.location.search.search(/fallback/) >= 0)) {
    Brisket = BrisketFallback;
} else {
    Brisket = BrisketModern;
}
