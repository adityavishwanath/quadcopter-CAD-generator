# hackathon
Modified code for the AE Hackathon 2016

This code is based on: http://robohub.org/up-and-flying-with-the-ar-drone-and-ros-getting-started/ 

*NOTE: Please go through this tutorial as a first, as it will give you an idea of the keyboard controls, how to run it, etc.*

You can download the virtual machine (VirtualBox) from: https://github.com/downloads/mikehamer/ardrone_tutorials_getting_started/ARDroneUbuntu.ova

In order to run our modified code, clone this repository and run:

# NOTE: If you are using the VM, the old ardrone_tutorials is still there, so move it elsewhere first
roscd
mv ardrone_tutorials ardrone_tutorials_orig

# Clone repository
git clone https://github.com/Autonomost/hackathon

mv hackathon ardrone_tutorials 

cd ardrone_tutorials

source setpath.sh

roslaunch ardrone_tutorials keyboard_controller_with_tags.launch

# Safety
1. Please be safe, and put altitude limits in the launch file appropriately
2. If indoors, put the shell on at all times
3. Make sure to note your AR Drone's wifi ID! If there are many you may connect to the wrong one!
4. Familiarize yourself with the keys in the keyboard controller first! Make sure you know how to control, land, and emergency-stop it.

# Q&A
Q. How do I run the keyboard controller?
A. Do not use "python keyboard_controller.py". Use roslaunch command above.

Q. I can run the keyboard contoller but the commands aren't doing anything
A. You have to press the correct keys *on the image window, while it has focus!* 
