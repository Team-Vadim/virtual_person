(function() {
  var Photo, addListeners, canvas, createGrid, ctx, gridItem, grids, height, img, imgInfo, imgSrc, imgs, init, magnet, mouse, populateCanvas, render, resizeCanvas, rotateAndPaintImage, updateMouse, useGrid, width;

  canvas = document.getElementById('canvas');

  ctx = canvas.getContext('2d');

  width = canvas.width = window.innerWidth;

  height = canvas.height = window.innerHeight*2;

  imgSrc = canvas.dataset.image;

  img = new Image();

  useGrid = true;

  imgInfo = {};

  imgs = [];

  grids = [];

  magnet = 2000;

  mouse = {
    x: 1,
    y: 0
  };

  init = function() {
    addListeners();
    img.onload = function(e) {
      var numberToShow;
      imgInfo.width = e.path ? e.path[0].width : e.target.width;
      imgInfo.height = e.path ? e.path[0].height : e.target.height;
      numberToShow = (Math.ceil(window.innerWidth / imgInfo.width)) * (Math.ceil(window.innerHeight / imgInfo.height));
      //if (useGrid) {
      //  createGrid();
      //}
      populateCanvas(numberToShow * 20);
      canvas.classList.add('ready');
      return render();
    };
    return img.src = imgSrc;
  };

  addListeners = function() {
    window.addEventListener('resize', resizeCanvas);
    window.addEventListener('mousemove', updateMouse);
    return window.addEventListener('touchmove', updateMouse);
  };

  updateMouse = function(e) {
    mouse.x = e.clientX;
    return mouse.y = e.clientY;
  };

  resizeCanvas = function() {
    width = canvas.width = window.innerWidth;
    return height = canvas.height = window.innerHeight;
  };

 populateCanvas = function(nb) {
    var i, p, _results;
    i = 0;
    _results = [];
    while (i <= nb) {
      p = new Photo();
      imgs.push(p);
      _results.push(i++);
    }
    return _results;
  };

  createGrid = function() {
    var c, grid, i, imgScale, item, r, x, y, _i, _j, _k, _ref, _ref1, _ref2, _results;
    imgScale = 0.5;
    grid = {
      row: Math.ceil(window.innerWidth / (imgInfo.width * imgScale)),
      cols: Math.ceil(window.innerHeight / (imgInfo.height * imgScale)),
      rowWidth: imgInfo.width * imgScale,
      colHeight: imgInfo.height * imgScale
    };
    for (r = _i = 0, _ref = grid.row; 0 <= _ref ? _i < _ref : _i > _ref; r = 0 <= _ref ? ++_i : --_i) {
      x = r * grid.rowWidth;
      for (c = _j = 0, _ref1 = grid.cols; 0 <= _ref1 ? _j < _ref1 : _j > _ref1; c = 0 <= _ref1 ? ++_j : --_j) {
        y = c * grid.colHeight;
        item = new gridItem(x, y, grid.rowWidth, grid.colHeight);
        grids.push(item);
      }
    }
    _results = [];
    for (i = _k = 0, _ref2 = grids.length; 0 <= _ref2 ? _k < _ref2 : _k > _ref2; i = 0 <= _ref2 ? ++_k : --_k) {
      _results.push(grids[i].draw());
    }
    return _results;
  };

  gridItem = function(x, y, w, h) {
    if (x == null) {
      x = 0;
    }
    if (y == null) {
      y = 0;
    }
    this.draw = function() {
      ctx.drawImage(img, x, y, w, h);
    };
  };

  Photo = function() {
    var TO_RADIANS, finalX, finalY, forceX, forceY, h, r, seed, w, x, y;
    seed = Math.random() * (15 - 10) + 10;
    w = imgInfo.width / seed;
    h = imgInfo.height / seed;
    x = window.innerWidth * Math.random();
    finalX = x;
    y = window.innerHeight * Math.random();
    finalY = y;
    console.log("INIT Y :: " + finalY + " || INIT X :: " + finalX);
    r = Math.random() * (180 - (-180)) + (-180);
    forceX = 0;
    forceY = 0;
    TO_RADIANS = Math.PI / 180;
    this.update = function() {
      var distance, dx, dy, powerX, powerY, x0, x1, y0, y1;
      x0 = x;
      y0 = y;
      x1 = mouse.x;
      y1 = mouse.y;
      dx = x1 - x0;
      dy = y1 - y0;
      distance = Math.sqrt((dx * dx) + (dy * dy));
      powerX = x0 - (dx / distance) * magnet / distance;
      powerY = y0 - (dy / distance) * magnet / distance;
      forceX = (forceX + (finalX - x0) / 2) / 2.1;
      forceY = (forceY + (finalY - y0) / 2) / 2.2;
      x = powerX + forceX;
      y = powerY + forceY;
    };
    this.draw = function() {
      return rotateAndPaintImage(ctx, img, r * TO_RADIANS, x, y, w / 2, h / 2, w, h);
    };
  };

  rotateAndPaintImage = function(context, image, angle, positionX, positionY, axisX, axisY, widthX, widthY) {
    context.translate(positionX, positionY);
    context.rotate(angle);
    context.drawImage(image, -axisX, -axisY, widthX, widthY);
    context.rotate(-angle);
    return context.translate(-positionX, -positionY);
  };

  render = function() {
    var x, y;
    x = 0;
    y = 0;
    ctx.clearRect(0, 0, width, height);
    while (y < grids.length) {
      grids[y].draw();
      y++;
    }
    while (x < imgs.length) {
      imgs[x].update();
      imgs[x].draw();
      x++;
    }
    return requestAnimationFrame(render);
  };

  init();

}).call(this);