array = ['A', 'B', 'C', 'A', 'B', 'C', 'B', 'C', 'A', 'B', 'C']

setInterval(function(){ 

// highlight corresponding chord
switch (array[0]) {
		case 'A':
			myFunction(1);
			break;
		case 'B':
			myFunction(2);
			break;
		case 'C':
			myFunction(3);
			break;
		case 'D':
			myFunction(4);
			break;
		case 'E':
			myFunction(5);
			break;
		case 'F':
			myFunction(6);
			break;
	}
array.shift();

 }, 1000);



function myFunction(numb) {
  var elements = document.getElementsByClassName('selected');
  elements[0].classList.remove("selected");
  var element = document.getElementById("string" + String(numb));
  element.classList.add("selected");
}