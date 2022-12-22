let r;
let factor = 2;

function setup() {
  createCanvas(windowWidth, windowHeight);
  r = height / 2 - 16;
}

function getVector(index, total) {
  const angle = map(index % total, 0, total, 0, TWO_PI);
  const v = p5.Vector.fromAngle(angle + PI);
  v.mult(r);
  return v;
}

function draw() {
  background(0);
  const total = 200; //int(map(mouseX, 0, width, 0, 200));
  factor += 0.015;

  translate(width / 2, height / 2);
  stroke(255, 150);
  strokeWeight(2);
  noFill();
  ellipse(0, 0, r * 2);

  strokeWeight(2);
  for (let i = 0; i < total - 1; i++) {
    const a = getVector(i, total);
    const b = getVector(i + 16, total);
    const c = getVector((i + 8) * factor, total);
    const d = getVector((i + 1) * factor, total);
    bezier(a.x, a.y, b.x, b.y, c.x, c.y, d.x, d.y);
  }
}