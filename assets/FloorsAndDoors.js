function setup() {
  // put setup code here
	createCanvas(1300, 660);
}

function draw() {
  // put drawing code here

	stroke(0,255, 0);
	for (i =2; i < 1000; i+=5){
		line (i, i*2, i*3, length);
		length++;
		if (i%2!=0){
			let c = color(255, 204, 0, 0.5);
			fill(c);
			rect(i, i*2, i*3, length);
		//	rect.color() = "red";		


		}
	}


	for (i=939; i > 0; i-=2){
		length ++;
		line(i, i*2, i*3, length)
	}

	for (i=1400; i > 0; i-=3){
		length ++;
		line(i, i*2, i*3, length)
	}


	let x1 = 40, y1 = 40, x2 = 80, y2 = 80;
	
	for (i =0; i < 500; i+=2){

		line(x1,y1,x2,y2);
		x1+=5;
		x2+=5;
		y1+=1;
		y2-=5;
//	if ((x1 + y1 + x2 + y2) % 2 == 0 ){
//		line ((x1/2),(x2/2),(y1/2),(y2/2));
//
//	}	

	}
	

	let numsqs = 0
	let x =1;
	let y =1;
	let h =10;
	let w =10;
	let c1 = color(253,89,7,0.7)
	fill(c1)
	while (numsqs < 250){
		numsq++;
		fill(c1);	
		rect(x, y, h, w);
		x += random(1,100);

		y += random(1,100);

		h += random(1,100);

		w += random(1,100);

	}	

	fill(c1); 
}
