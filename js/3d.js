function Shape(options) {
    options = options || {};
    var shapeDiv = document.createElement("div");
    this.x = options.x || 0;
    this.y = options.y || 0;
    this.z = options.z || 0;
    this.w = options.w || 10;
    this.h = options.h || 10;
    this.rotationX = options.rotationX || 0;
    this.rotationY = options.rotationY || 0;
    this.scale = options.scale || 1;
    this.bg = options.bg || "#000";
    this.border = options.border || "0";

    this.clone = function() {
        return new Shape(options);
    };

    this.update = function() {
        var t = "translateX(" + this.x + "px) translateY(" + this.y + "px) translateZ(" + this.z + "px) rotateX(" + this.rotationX + "deg) rotateY(" + this.rotationY + "deg) scale3d(" + this.scale + ", " + this.scale + ", " + this.scale + ")";
        shapeDiv.style.webkitTransform = t;
        shapeDiv.style.MozTransform = t;
        shapeDiv.style.oTransform = t;
        shapeDiv.style.transform = t;
        shapeDiv.style.width = this.w + "px";
        shapeDiv.style.height = this.h + "px";
        shapeDiv.style.background = this.bg;
        shapeDiv.style.border = this.border;
    };

    this.shapeElement = function() {
        return shapeDiv;
    };

    this.update();
}
window.Shape = Shape;

function ShapeGroup(options) {
    options = options || {};
    var groupDiv = document.createElement("div");
    this.x = options.x || 0;
    this.y = options.y || 0;
    this.z = options.z || 0;
    this.rotationX = options.rotationX || 0;
    this.rotationY = options.rotationY || 0;
    this.scale = options.scale || 1;
    var shapes = [];
    if (options.shapes) {
        shapes = options.shapes;
        for (var i=0; i<shapes.length; i++) {
            groupDiv.appendChild(shapes[i].shapeElement());
        }
    }

    this.clone = function() {
        return new ShapeGroup({
            x: this.x,
            y: this.y,
            z: this.z,
            rotationX: this.rotationX,
            rotationY: this.rotationY,
            shapes: shapes.map(function(shape) {
                return shape.clone();
            })
        });
    };

    this.addShape = function(shape) {
        shapes.push(shape);
        groupDiv.appendChild(shape.shapeElement());
    };

    this.groupElement = function() {
        return groupDiv;
    };

    this.getShapes = function() {
        return shapes;
    };

    this.update = function() {
        var t = "translateX(" + this.x + "px) translateY(" + this.y + "px) translateZ(" + this.z + "px) rotateX(" + this.rotationX + "deg) rotateY(" + this.rotationY + "deg) scale3d(" + this.scale + ", " + this.scale + ", " + this.scale + ")";
        groupDiv.style.webkitTransform = t;
        groupDiv.style.MozTransform = t;
        groupDiv.style.oTransform = t;
        groupDiv.style.transform = t;
        groupDiv.style.width = this.w;
        groupDiv.style.height = this.h;
    };

    this.update();
}
window.ShapeGroup = ShapeGroup;

function CSS3D() {
    var world = document.getElementById("world");
    var viewport = document.getElementById("viewport");
    var groups = [];
    this.worldRotationX = 0;
    this.worldRotationY = 0;
    this.worldZoom = 0;

    this.updateView = function() {
        var t = "translateZ(" + this.worldZoom + "px) rotateX(" + this.worldRotationX + "deg) rotateY(" + this.worldRotationY + "deg)";
        world.style.webkitTransform = t;
        world.style.MozTransform = t;
        world.style.oTransform = t;
        world.style.transform = t;
    };

    this.addGroup = function(group) {
        groups.push(group);
        world.appendChild(group.groupElement());
    };
}
window.CSS3D = CSS3D;
