//Aditya Vishwanath

var arDrone = require('ar-drone');
var client  = arDrone.createClient();

client.takeoff();
console.log("we took off!");

client
  .after(5000, function() {
    this.stop();
  })

  .after(10000, function() {
    this.right(0.1);
  })
  .after(5000, function() {
    this.stop();
  })
  .after(8000, function() {
    this.counterClockwise(0.03214285714); //need to test!
  })
  .after(10000, function() {
    this.right(0.1);
  })
  .after(5000, function() {
    this.stop();
  })
  .after(8000, function() {
    this.counterClockwise(0.03214285714); //need to test!
  })
  .after(10000, function() {
    this.right(0.1);
  })
  .after(5000, function() {
    this.stop();
  })
  .after(8000, function() {
    this.counterClockwise(0.03214285714); //need to test!
  })
  .after(10000, function() {
    this.right(0.1);
  })
  .after(5000, function() {
    this.stop();
  })
  .after(8000, function() {
    this.counterClockwise(0.03214285714); //need to test!
  })
  .after(5000, function() {
    this.stop();
  })
  .after(5000, function() {
    this.land();
  })




/*
FOR TURNING 90 DEGREES AT A CORNER

 .after(8000, function() {
    this.counterClockwise(0.03214285714); //need to test!
  })
*/

/*
ONE SIDE OF THE BOX

.after(10000, function() {
    this.right(0.1);
  })

*/


/*

client
  .after(4000, function() {
    this.up(0.2);
  })
  //first side
  .after(4000, function() {
    this.right(0.1);
  })
  .after(8000, function() {
    this.counterClockwise(0.03214285714); //need to test!
  })
  //second side
  .after(4000, function() {
    this.right(0.1);
  })
  .after(4000, function() {
    this.counterClockwise(0.1); //need to test!
  })
  //third side
  .after(4000, function() {
    this.right(0.1);
  })
  .after(4000, function() {
    this.counterClockwise(0.1); //need to test!
  })
  //fourth side
  .after(4000, function() {
    this.right(0.1);
  })
  .after(4000, function() {
    this.counterClockwise(0.1); //need to test!
  })
  //come down now!!!!
  .after(4000, function() {
    this.stop();
    this.down(0.1);
    this.land();
  });

*/

console.log("We landed and we should be done!");