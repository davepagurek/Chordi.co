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

        $.ajax({method:"GET", url:"music/"+instrument+"/"+mode}).done(function(msg){
            $("#audioElement").attr("src",msg);
            swapControls("#loading", "#controls");
        });
    });
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


    var scene = new CSS3D();
    var planeBg = "rgba(255, 255, 255, 0.2)";
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
    var cube = new ShapeGroup({
        x: -50, y: 0, z: 0,
        shapes: [plane1, plane2, plane3, plane4, plane5, plane6]
    })
    scene.addGroup(cube);


    // Continuously loop and update chart with frequency data.
    function renderViz() {

        // Copy frequency data to frequencyData array.
        analyser.getByteFrequencyData(frequencyData);
        //console.log(frequencyData);

        scene.worldRotationY += 0.5;
        scene.updateView();

        requestAnimationFrame(renderViz);

    }

    // Run the loop
    renderViz();

});
