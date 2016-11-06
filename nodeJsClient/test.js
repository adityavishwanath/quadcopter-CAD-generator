var arDrone = require('ar-drone');
var client  = arDrone.createClient();


client.takeoff();
client.land();

client
  .after(5000, function() {
    this.stop();
  })
  .after(8000, function() {
    this.clockwise(0.03214285714); //need to test!
  })