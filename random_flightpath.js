//Aditya Vishwanath

var arDrone = require('ar-drone');
var client  = arDrone.createClient();

client.takeoff();

client
  .after(4000, function() {
    this.up(0.2);
  })
  //first side
  .after(4000, function() {
    this.right(0.1);
  })
  .after(4000, function() {
    this.counterClockwise(0.1); //need to test!
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
    this.down(0.1);
  })
  .after(2000, function() {
    this.land();
  });