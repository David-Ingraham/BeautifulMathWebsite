let x, y;
let px, py;
let step = 1;
let stepSize = 20;
let numSteps = 1;
let state = 0;
let turnCounter = 1;
let totalSteps;

function isPrime(value) {
  if (value == 1) return false;
  for (let i = 2; i <= sqrt(value); i++) {
    if (value % i == 0) {
      return false;
    }
  }
  return true;
}

function setup() {
  createCanvas(1100, 500);
  textFont("Courier");

  const cols = width / stepSize;
  const rows = height / stepSize;
  totalSteps = cols * rows;

  x = width / 2;
  y = height / 2;
  px = x;
  py = y;
  background(0);
}

function draw() {
  // textSize(stepSize);
  // textAlign(CENTER, CENTER);
  //text(step, x, y);
  noStroke();
  
  if (!isPrime(step)) {
    fill(45, 197, 244);
    rectMode(CENTER);
    push();
    translate(x,y);
    rotate(frameCount * 0.01);
    rect(0, 0, stepSize * 0.5);
    pop();
  } else {
    let r = stepSize * 0.5;
    fill(240, 99, 164);
    push();
    translate(x,y);
    rotate(-PI/4);
    triangle(-r,+r,0,-r,+r,+r);
    pop();
  }
  px = x;
  py = y;

  switch (state) {
    case 0:
      x += stepSize;
      break;
    case 1:
      y -= stepSize;
      break;
    case 2:
      x -= stepSize;
      break;
    case 3:
      y += stepSize;
      break;
  }

  if (step % numSteps == 0) {
    state = (state + 1) % 4;
    turnCounter++;
    if (turnCounter % 2 == 0) {
      numSteps++;
    }
  }
  step++;

  if (step > totalSteps) {
    noLoop();
  }

  //frameRate(1);
}
