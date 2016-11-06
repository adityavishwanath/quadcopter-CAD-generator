#!/usr/bin/env python

# The Keyboard Controller Node for the tutorial "Up and flying with the AR.Drone and ROS | Getting Started"
# https://github.com/mikehamer/ardrone_tutorials

# This controller extends the base DroneVideoDisplay class, adding a keypress handler to enable keyboard control of the drone

# Import the ROS libraries, and load the manifest file which through <depend package=... /> will give us access to the project dependencies
import roslib; roslib.load_manifest('ardrone_tutorials')
import rospy

# Load the DroneController class, which handles interactions with the drone, and the DroneVideoDisplay class, which handles video display
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay

# Finally the GUI libraries
from PySide import QtCore, QtGui
from threading import Lock

from ardrone_autonomy.msg import Navdata # for receiving navdata feedback
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy
import cv
import cv2	


# Here we define the keyboard map for our controller (note that python has no enums, so we use a class)
class KeyMapping(object):
	PitchForward     = QtCore.Qt.Key.Key_E
	PitchBackward    = QtCore.Qt.Key.Key_D
	RollLeft         = QtCore.Qt.Key.Key_S
	RollRight        = QtCore.Qt.Key.Key_F
	YawLeft          = QtCore.Qt.Key.Key_W
	YawRight         = QtCore.Qt.Key.Key_R
	IncreaseAltitude = QtCore.Qt.Key.Key_Q
	DecreaseAltitude = QtCore.Qt.Key.Key_A
	Takeoff          = QtCore.Qt.Key.Key_Y
	Land             = QtCore.Qt.Key.Key_H
	Emergency        = QtCore.Qt.Key.Key_Space
	FollowingMode    = QtCore.Qt.Key.Key_T
        VisionMode       = QtCore.Qt.Key.Key_V


# Our controller definition, note that we extend the DroneVideoDisplay class
class KeyboardController(DroneVideoDisplay):
	def __init__(self):
		super(KeyboardController,self).__init__()
		
		self.pitch = 0
		self.roll = 0
		self.yaw_velocity = 0 
		self.z_velocity = 0
		self.following_mode = 0

		self.tags = []
		self.tagLock = Lock()

		#Subscribe to the /ardrone/navdata topic, of message type navdata, and call self.ReceiveNavdata when a message is received
		self.subNavdata = rospy.Subscriber('/ardrone/navdata',Navdata,self.ReceiveNavdata)     
		self.bridge = CvBridge()
		self.image_sub = None
		cv2.namedWindow("Image window")
		cv2.startWindowThread()

	def ReceiveImageData(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
		except CvBridgeError as e:
			print(e)
		
		rospy.logwarn("Received image size {} x {}".format(cv_image.width, cv_image.height))
   
               	# Note: This is broken for some reason. It just hangs after displaying one image.
               	cv2_image = array = numpy.array( cv_image )
		cv2.imshow("Image window", cv2_image)
		cv2.waitKey(1)
		cv.ShowImage("Image window", cv_image)

	def ReceiveNavdata(self,navdata):
		# Indicate that new data has been received (thus we are connected)
		self.communicationSinceTimer = True

		# Update the message to be displayed
		msg = self.StatusMessages[navdata.state] if navdata.state in self.StatusMessages else self.UnknownMessage
		self.statusMessage = '{} (Battery: {}%)'.format(msg,int(navdata.batteryPercent))

		self.tagLock.acquire()
		try:
			if navdata.tags_count > 0:
				self.tags = [(navdata.tags_xc[i],navdata.tags_yc[i],navdata.tags_distance[i]) for i in range(0,navdata.tags_count)]
			else:
				self.tags = []
		finally:
			self.tagLock.release()

		if self.following_mode == 1:
			# Get tags
			offsetFromCenter = 0
			if len(self.tags) > 0:
				self.tagLock.acquire()
				try:
					for (x,y,d) in self.tags:
						offsetFromCenter = (900/2) - x
					
				finally:
					self.tagLock.release()

				# Set roll/pitch/yaw
				if offsetFromCenter > 200:
					self.roll = 1
					#self.roll = 0
				elif offsetFromCenter < -200:
					self.roll = -1
					#self.roll = 0
				elif d > 350 :
					self.pitch = 1
				elif d < 200 :
					self.pitch = -1
				elif y > 500 :
					self.z_velocity = -1
				elif y < 300 :
					self.z_velocity = 1
				else:
					self.roll = 0
					self.pitch = 0
					self.z_velocity = 0
				rospy.logwarn("offset: {} roll: {} x: {} y:{} d:{}".format(offsetFromCenter, self.roll,x,y,d))
			else:
				self.roll = 0
				self.pitch = 0
				self.z_velocity = 0

			# finally we set the command to be sent. The controller handles sending this at regular intervals
			controller.SetCommand(self.roll, self.pitch, self.yaw_velocity, self.z_velocity)

# We add a keyboard handler to the DroneVideoDisplay to react to keypresses
	def keyPressEvent(self, event):
		key = event.key()

		# If we have constructed the drone controller and the key is not generated from an auto-repeating key
		if controller is not None and not event.isAutoRepeat():
			# Handle the important cases first!
			if key == KeyMapping.Emergency:
				controller.SendEmergency()
			elif key == KeyMapping.Takeoff:
				controller.SendTakeoff()
			elif key == KeyMapping.Land:
				controller.SendLand()
			

			else:
				# Now we handle moving, notice that this section is the opposite (+=) of the keyrelease section
				if key == KeyMapping.YawLeft:
					self.yaw_velocity += 1
				elif key == KeyMapping.YawRight:
					self.yaw_velocity += -1

				elif key == KeyMapping.PitchForward:
					self.pitch += 1
				elif key == KeyMapping.PitchBackward:
					self.pitch += -1

				elif key == KeyMapping.RollLeft:
					self.roll += 1
				elif key == KeyMapping.RollRight:
					self.roll += -1

				elif key == KeyMapping.IncreaseAltitude:
					self.z_velocity += 1
				elif key == KeyMapping.DecreaseAltitude:
					self.z_velocity += -1

				elif key == KeyMapping.FollowingMode:
					self.following_mode = 1

				elif key == KeyMapping.VisionMode:
					if self.image_sub is None:
						rospy.logwarn("Subscribing")
	                			self.image_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.ReceiveImageData)
						cv2.startWindowThread()
						self.vision_mode = 1

			# finally we set the command to be sent. The controller handles sending this at regular intervals
			controller.SetCommand(self.roll, self.pitch, self.yaw_velocity, self.z_velocity)


	def keyReleaseEvent(self,event):
		key = event.key()

		# If we have constructed the drone controller and the key is not generated from an auto-repeating key
		if controller is not None and not event.isAutoRepeat():
			# Note that we don't handle the release of emergency/takeoff/landing keys here, there is no need.
			# Now we handle moving, notice that this section is the opposite (-=) of the keypress section
			if key == KeyMapping.YawLeft:
				self.yaw_velocity -= 1
			elif key == KeyMapping.YawRight:
				self.yaw_velocity -= -1

			elif key == KeyMapping.PitchForward:
				self.pitch -= 1
			elif key == KeyMapping.PitchBackward:
				self.pitch -= -1

			elif key == KeyMapping.RollLeft:
				self.roll -= 1
			elif key == KeyMapping.RollRight:
				self.roll -= -1

			elif key == KeyMapping.IncreaseAltitude:
				self.z_velocity -= 1
			elif key == KeyMapping.DecreaseAltitude:
				self.z_velocity -= -1
			elif key == KeyMapping.FollowingMode:
				self.following_mode = 0
				self.roll = 0
				self.pitch = 0
				self.z_velocity = 0
			elif key == KeyMapping.VisionMode:
				rospy.logwarn("Unsubscribing")
 				self.image_sub.unregister()
				self.vision_mode = 0

			# finally we set the command to be sent. The controller handles sending this at regular intervals
			controller.SetCommand(self.roll, self.pitch, self.yaw_velocity, self.z_velocity)



# Setup the application
if __name__=='__main__':
	import sys
	# Firstly we setup a ros node, so that we can communicate with the other packages
	rospy.init_node('ardrone_keyboard_controller')

	# Now we construct our Qt Application and associated controllers and windows
	app = QtGui.QApplication(sys.argv)
	controller = BasicDroneController()
	display = KeyboardController()
	display.show()

	# executes the QT application
	status = app.exec_()

	# and only progresses to here once the application has been shutdown
	rospy.signal_shutdown('Great Flying!')
	sys.exit(status)
