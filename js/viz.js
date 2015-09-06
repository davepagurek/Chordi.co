function swapControls(current, next) {
    var container = $(current);
    var current = container.height();
    container.css("height", current);
    container.animate({height: 0}, 300, "swing");

    var el = $(next),
        autoHeight = el.css('height', 'auto').height();
    el.height(0).animate({height: autoHeight}, 300, "swing", function() {
        el.css('height', 'auto');
    });
}

$(document).ready(function () {
    $("#generate").on("click", function() {
        var instrument = $("#instrument").val();
        var mode = $("#mode").val();

        swapControls("#settings", "#loading");
        refreshSong(instrument, mode);
     });
    function refreshSong(instrument, mode){
        $.ajax({method:"GET", url:"music/"+instrument+"/"+mode}).done(function(msg){
            $("#audioElement").attr("src",msg);
            $("#downloadButton").attr("download", msg);
            $("#downloadButton").attr("href", msg);
            swapControls("#loading", "#controls");
        });
    }
    $("#shuffleButton").on("click",function(){
      swapControls("#controls","#loading");
      shuffleSong();
    });
    function shuffleSong(){
      refreshSong(Math.round(Math.random()) * 128, (Math.random() > .5)?"major" : "minor");
    }
    $("#scroll").on("click", function() {
        swapControls("#try", "#settings");
    });
    $("#back").on("click", function() {
        document.getElementById('audioElement').pause()
        swapControls("#controls", "#settings");
    });
    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    var audioElement = document.getElementById('audioElement');
    var audioSrc = audioCtx.createMediaElementSource(audioElement);
    var analyser = audioCtx.createAnalyser();

    // Bind our analyser to the media element source.
    audioSrc.connect(analyser);
    audioSrc.connect(audioCtx.destination);

    //var frequencyData = new Uint8Array(analyser.frequencyBinCount);
    var frequencyData = new Uint8Array(200);

    function createSvg(parent, height, width) {
        return d3.select(parent).append('svg').attr('height', svgHeight).attr('width', svgWidth);
    }

    var graph = document.getElementById('graph');
    var svgHeight = graph.offsetHeight;
    var svgWidth = graph.offsetWidth;
    var barPadding = 1;
    var svg = createSvg('#graph', svgHeight, svgWidth);

    // Create our initial D3 chart.
    svg.selectAll('rect')
    .data(frequencyData)
    .enter()
    .append('rect')
    .attr('fill', 'rgba(255,255,255,0.6)')
    .attr('x', function (d, i) {
        return i * (svgWidth / frequencyData.length);
    })
    .attr('height', svgHeight).attr('width', svgWidth);

    $(window).on("resize", function() {
        svgHeight = graph.offsetHeight;
        svgWidth = graph.offsetWidth;
        svg.attr('height', svgHeight).attr('width', svgWidth);
    });

    // Continuously loop and update chart with frequency data.
    function renderChart() {

        // Copy frequency data to frequencyData array.
        analyser.getByteFrequencyData(frequencyData);
        //console.log(frequencyData);

        // Update d3 chart with new data.
        svg.selectAll('rect')
        .data(frequencyData)
        .attr('y', function(d) {
            return svgHeight - d/280 * svgHeight;
        })
        .attr('x', function (d, i) {
            return i * (svgWidth / frequencyData.length);
        })
        .attr('height', function(d) {
            return d/280 * svgHeight;
        })
        .attr('width', svgWidth / frequencyData.length - barPadding);

        requestAnimationFrame(renderChart);

    }

    // Run the loop
    renderChart();

});
