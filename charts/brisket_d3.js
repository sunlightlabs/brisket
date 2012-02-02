D3Charts = {
    barchart: function(div, data, opts) {
        var default_opts = {
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
        };
        if (typeof opts === 'undefined') opts = {};
        _.defaults(opts, default_opts);


        totals = _.map(data, function(item) { return d3.sum(item.values); })

        var chart = d3.select('#' + div).append("svg")
            .classed("chart-canvas", true)
            .attr("width", opts.chart_x + opts.chart_width + opts.right_gutter)
            .attr("height", opts.chart_height);

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
                    .attr('fill', parent.node().tagName == 'a' ? opts.link_color : opts.text_color)
                    .text(function(d, i) { return d.key; })
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
    piechart: function(div, data, opts) {
        var default_opts = {
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
        };
        if (typeof opts === 'undefined') opts = {};
        _.defaults(opts, default_opts);

        var twopi = 2 * Math.PI;
        
        var chart = d3.select("#" + div)
            .append("svg")
                .classed('chart-canvas', true)
                .attr("width", opts.chart_width)
                .attr("height", opts.chart_height);
        
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
                .text(function(d, i) { return d.key + " (" + Math.round(100 * d.value / sum) + "%)"; })
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
    timeline_chart: function(div, data, opts) {
        var default_opts = {
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
        };
        if (typeof opts === 'undefined') opts = {};
        _.defaults(opts, default_opts);

        var chart = d3.select('#' + div).append("svg")
            .classed("chart-canvas", true)
            .attr("width", opts.chart_x + opts.chart_width + opts.right_gutter)
            .attr("height", opts.chart_y + opts.chart_height + opts.tick_length + opts.label_padding + opts.row_height);
        
        // scalers
        y = d3.scale.linear().domain([0, d3.max(_.flatten(_.map(data, function(d) { return d.timeline; })))]).range([opts.chart_height, 0]);
        x = d3.scale.linear().domain([0, data[0].timeline.length - 1]).range([opts.chart_x, opts.chart_x + opts.chart_width]);

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
        ], function(day) { return day.day < data[0].timeline.length * 7; });

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
                    .attr('fill', parent.node().tagName == 'a' ? opts.link_color : opts.text_color)
                    .text(function(d, i) { return d.name; })
                    .style('font', '11px arial,sans-serif');
            });
    }
}

Brisket = {
    contribution_single_barchart: function(div, data) {
        if (data.length === 0) return;
        
        graph_data = _.map(data, function(item) {
            return {
                key: item.key,
                href: item.href,
                values: [parseFloat(item.value)]
            };
        });

        D3Charts.barchart(div, graph_data);
    },
    contribution_stacked_barchart: function(div, data) {
        if (data.length === 0) return;

        graph_data = _.map(data, function(item) {
            return {
                key: item.key,
                href: item.href,
                values: [parseFloat(item.value_employee), parseFloat(item.value_pac)]
            };
        });
        D3Charts.barchart(div, graph_data);
    },
    piechart: function(div, data, colors) {
        var in_data = []
        var opts = {colors: []}
        _.each(data, function(value, key) {
            if (value > 0) {
                in_data.push({'key': key, 'value': value})
                opts.colors.push(colors[key]);
            }
        })
        D3Charts.piechart(div, in_data, opts);
    },
    party_piechart: function(div, data) {
        var party_colors = {"Republicans": "#e60002", "Democrats": "#186582", "Other" : "#dcddde"};
        Brisket.piechart(div, data, party_colors);
    },
    indiv_pac_piechart: function(div, data) {
        var indiv_pac_colors = {"Individuals": '#efcc01', "PACs": '#f2e388'};
        Brisket.piechart(div, data, indiv_pac_colors);
    },
    local_piechart: function(div, data) {
        var local_colors = {"in-state": '#efcc01', "out-of-state": '#f2e388', "unknown": '#dcddde'};
        Brisket.piechart(div, data, local_colors);
    },
    level_piechart: function(div, data) {
        var level_colors = {"Federal": '#efcc01', "State": '#f2e388'};
        Brisket.piechart(div, data, level_colors);
    },
    fec_piechart: function(div, data) {
        var fec_colors = {"Individuals": "#efcc01", "PACs": "#f2e388", "Party": "#15576e", "Self-Financing": "#f2f1e4", "Transfers": "#e96d24"};
        Brisket.piechart(div, data, fec_colors);
    }
}
