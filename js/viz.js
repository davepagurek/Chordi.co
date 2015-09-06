function swapControls(current, next) {
    var container = $(current);
    var current = container.height();
    container.css("height", current);
    container.animate({height: 0}, 600, "swing");

    var el = $(next),
        autoHeight = el.css('height', 'auto').height();
    el.height(0).animate({height: autoHeight}, 600, "swing", function() {
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

    var viz = "cube";


    var scene = new CSS3D();
    var planeBg = "rgba(255, 255, 255, 0.15)";
    var planeBorder = "0";

    var plane1 = new Shape({
        x: 0, y: 0, z: 0, w: 100, h: 100, rotationX: 90, rotationY: 0,
        bg: planeBg, border: planeBorder
    });
    var plane2 = new Shape({
        x: -50, y: -50, z: 0, w: 100, h: 100, rotationX: 0, rotationY: 90,
        bg: planeBg, border: planeBorder
    });
    var plane3 = new Shape({
        x: 50, y: -50, z: 0, w: 100, h: 100, rotationX: 0, rotationY: 90,
        bg: planeBg, border: planeBorder
    });
    var plane4 = new Shape({
        x: 0, y: -100, z: 0, w: 100, h: 100, rotationX: 90, rotationY: 0,
        bg: planeBg, border: planeBorder
    });
    var plane5 = new Shape({
        x: 0, y: -50, z: -50, w: 100, h: 100, rotationX: 0, rotationY: 0,
        bg: planeBg, border: planeBorder
    });
    var plane6 = new Shape({
        x: 0, y: -50, z: 50, w: 100, h: 100, rotationX: 0, rotationY: 0,
        bg: planeBg, border: planeBorder
    });
    var cube1 = new ShapeGroup({
        x: -100, y: 50, z: 50,
        shapes: [plane1, plane2, plane3, plane4, plane5, plane6]
    });
    var cube2 = cube1.clone();
    cube2.x = 0;
    cube2.update();
    var cube3 = cube1.clone();
    cube3.y = -50;
    cube3.update();
    var cube4 = cube3.clone();
    cube4.x = 0;
    cube4.update();
    var cube5 = cube1.clone();
    cube5.z = -50;
    cube5.update();
    var cube6 = cube2.clone();
    cube6.z = -50;
    cube6.update();
    var cube7 = cube3.clone();
    cube7.z = -50;
    cube7.update();
    var cube8 = cube4.clone();
    cube8.z = -50;
    cube8.update();
    scene.addGroup(cube1);
    scene.addGroup(cube2);
    scene.addGroup(cube3);
    scene.addGroup(cube4);
    scene.addGroup(cube5);
    scene.addGroup(cube6);
    scene.addGroup(cube7);
    scene.addGroup(cube8);
    var cubes = [cube1, cube2, cube3, cube4, cube5, cube6, cube7, cube8];

    var rotationY = Math.random()-0.5;
    var rotationX = Math.random()-0.5;

    function createSvg(parent, height, width) {
        return d3.select(parent).append('svg').attr('height', svgHeight).attr('width', svgWidth).attr('display', "none");
    }

    var graph = document.getElementById('viewport');
    var svgHeight = graph.offsetHeight;
    var svgWidth = graph.offsetWidth;
    var barPadding = 1;
    var svg = createSvg('#viewport', svgHeight, svgWidth);

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
        if (viz == "cube") {
            scene.worldZoom = $(window).width() / 10;
            scene.updateView();
        } else if (viz == "graph") {
            svgHeight = graph.offsetHeight;
            svgWidth = graph.offsetWidth;
            svg.attr('height', svgHeight).attr('width', svgWidth);
        }
    });
    scene.worldZoom = $(window).width() / 100;
    scene.updateView();


    // Continuously loop and update chart with frequency data.
    function renderViz() {

        // Copy frequency data to frequencyData array.
        analyser.getByteFrequencyData(frequencyData);
        //console.log(frequencyData);

        if (viz == "cube") {

            averages = [0, 0, 0, 0, 0, 0, 0, 0];
            total = 0;
            for (var i = 0; i < frequencyData.length; i++) {
                averages[Math.floor(i/frequencyData.length * averages.length)] += frequencyData[i];
                total += frequencyData[i];
            }
            for (var i = 0; i < averages.length; i++) {
                averages[i] /= frequencyData.length/averages.length * 100;
                cubes[i].scale = averages[i] + 0.2;
                cubes[i].update();
            }

            if (total > 256*70) {
                rotationY = (Math.random()-0.5)*2;
                rotationX = (Math.random()-0.5)*2;
            }

            scene.worldRotationY += rotationY;
            scene.worldRotationX += rotationX;
            scene.updateView();

        } else if (viz == "graph") {

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

        }

        requestAnimationFrame(renderViz);

    }

    // Run the loop
    renderViz();

    $("#cube").on("click", function() {
        viz = "cube";
        svg.attr("display", "none");
        document.getElementById("world").style.display = "block";
        document.getElementById("world").classList.remove("fadein");
        graph.classList.add("cube");
        graph.classList.remove("graph");
    });
    $("#graph").on("click", function() {
        viz = "graph";
        svgHeight = graph.offsetHeight;
        svgWidth = graph.offsetWidth;
        svg.attr("display", "block");
        document.getElementById("world").style.display = "none";
        graph.classList.remove("cube");
        graph.classList.add("graph");
    });

});
