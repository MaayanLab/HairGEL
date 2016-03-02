// for barplot
var screenWidth = $(window).width();
var margin = {top: 40, right: 20, bottom: 50, left: 50};
if (screenWidth > 500) {
	var width = 500 - margin.left - margin.right,
	height = 300 - margin.top - margin.bottom;
} else{
	var width = 0.9*(screenWidth - margin.left - margin.right),
	height = 0.9*0.6*(screenWidth - margin.top - margin.bottom);
};

var x = d3.scale.ordinal()
.rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
.range([height, 0]);

var xAxis = d3.svg.axis()
.scale(x)
.orient("bottom")
.tickSize(5,5);

var yAxis = d3.svg.axis()
.scale(y)
.orient("left")

var svg = d3.select("#barplot-container").append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.attr("id", "fpkm-barplot")
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// table
function fpkmTable(json) {
	d3.select("#fpkm-table-gene").remove()
	var table = d3.select("#fpkm-table").append("table")
	.attr('id', 'fpkm-table-gene')
	.attr('class', 'table table-bordered table-condensed');
	data = json['data'];
	for (var i = 0; i < data.length; i++) {
		data[i]['sampleName'] = sampleNames[data[i].name];
	};
	var theads = table.append("thead").append("tr")
	.selectAll("th").data(data)
	.enter().append("th")
	.text(function(d) { return d.sampleName; } )
	var trs = table.append("tbody").append("tr")
	.selectAll("td").data(data)
	.enter().append("td")
	.text(function(d){ return parseFloat(d.avg).toFixed(1); })
}

function barPlot(json) {
	d3.select("#title").remove();
	d3.select("#x-axis").remove();
	d3.select("#y-axis").remove();
	d3.selectAll(".mouseover-title").remove()
	data = json['data'];
	for (var i = 0; i < data.length; i++) {
		data[i]['sampleName'] = sampleNames[data[i].name];
	};
	x.domain(data.map(function(d) { return d.sampleName; }));
	y.domain([0, 1.25*d3.max(data, function(d) { return parseFloat(d.avg); })]);
	// set up xAxis
	svg.append("g")
	.attr("class", "x axis")
	.attr("id", "x-axis")
	.attr("transform", "translate(0," + height + ")")
	.call(xAxis)
	.selectAll("text")
	.style("text-anchor", "end")
	.attr("dx", "-.8em")
	.attr("dy", ".0em")
	.attr("transform", function(d) {
		return "rotate(-45)" 
	});

	// set up yAxis
	svg.append("g")
	.attr("class", "y axis")
	.attr("id", "y-axis")
	.call(yAxis)
	.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", ".71em")
	.style("text-anchor", "middle")
	.style("font-size", "16px")
	.text("FPKM");

	// plot bars
	var rects = svg.selectAll("rect").data(data);
	rects.enter().append("rect")
	.attr("class", function(d) {return d.name; })
	.attr("x", function(d) { return x(d.sampleName); })
	.attr("width", x.rangeBand())
	.attr("y", function(d) { return y(d.avg); })
	.attr("height", function(d) { return height - y(d.avg); })

	rects.transition()
	.duration(1000)
	.attr("y", function(d) { return y(d.avg); })
	.attr("height", function(d) { return height - y(d.avg); });

	rects.append('title')
	.attr("class", "mouseover-title")
	.text(function(d){ return 'FPKM: ' + parseFloat(d.avg).toFixed(1); });

	rects.exit().remove();

	// add error bars
	var errorBars = svg.selectAll(".errorBar").data(data);
	errorBars.enter().append("path")
	.attr("class", 'errorBar')
	.attr("d", function(d){
		var barWidth = 0.5*x.rangeBand();
		var xVal = x(d.sampleName)+barWidth;
		var upper = parseFloat(d.avg) + parseFloat(d.sd),
		lower = parseFloat(d.avg) - parseFloat(d.sd);
		return "M"+xVal+","+y(lower)+ "L"+xVal+","+y(d.avg) +"L"+xVal+','+y(upper);
	});

	errorBars.transition().duration(1000)
	.attr("d", function(d){
		var barWidth = 0.5*x.rangeBand();
		var xVal = x(d.sampleName)+barWidth;
		var upper = parseFloat(d.avg) + parseFloat(d.sd),
		lower = parseFloat(d.avg) - parseFloat(d.sd);
		return "M"+xVal+","+y(lower)+ "L"+xVal+","+y(d.avg) +"L"+xVal+','+y(upper);
	});

	errorBars.exit().remove();

	// add title
	var title = svg.append("text")
	.attr("x", width / 2 )
	.attr("y", 0)
	.attr('id', 'title')
	.style("text-anchor", "middle")
	.style("font-size", "20px")
	.text(function(){
		if (json['signature']) {
			return json['gene'] + '*';
		}else {
			return json['gene'];
		}
	});
}

$(document).ready(function(){ // preload a bargraph
	$.getJSON('genes.php', {gene: exampleGene, table: tableName}, function(json){
		barPlot(json);
		fpkmTable(json);
	})
})

$('#gene').bind("enterKey",function(e){
	var geneInput = $(this).val();
	$.getJSON('genes.php', {gene: geneInput, table: tableName}, function(json){
		barPlot(json);
		fpkmTable(json);
	})
});

$('#go-button').click(function(){
	var geneInput = $('#gene').val();
	$.getJSON('genes.php', {gene: geneInput, table: tableName}, function(json){
		barPlot(json);
		fpkmTable(json);
	})
})

$('#gene').keyup(function(e){
	if(e.keyCode == 13) {
		$(this).trigger("enterKey");
	}
});

$('.example').click(function(){ // to show example when clicked
	var geneInput = $(this).text();
	$.getJSON('genes.php', {gene: geneInput, table: tableName}, function(json){
		barPlot(json);
		fpkmTable(json);
	})
})

// autocomplete
$.getJSON("geneNames.json",function(data){
	$(function() {
		$( "#gene" ).autocomplete({
			minLength: 3,
			source: data,
		});
	});
});

d3.select("#save-button").on("click", function(){
	saveSvgAsPng(document.getElementById("fpkm-barplot"), "fpkm-barplot.png"); 
});
