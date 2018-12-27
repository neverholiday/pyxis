#!/usr/bin/env python
#
# Copyright (C) 2018  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

########################################################
#
#	STANDARD IMPORTS
#

import sys
import os

########################################################
#
#	LOCAL IMPORTS
#

from PyQt4 import QtGui
from PyQt4 import QtCore

import cv2
import numpy as np

########################################################
#
#	GLOBALS
#

TEST_IMAGE_PATH = "/home/neverholiday/work/ball_detector/raw_data/data1/frame0020.jpg"
TEST_FRAME_PATH = "/home/neverholiday/work/ball_detector/raw_data/data1"
########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

def loadImage():
	"""Load image from cv2"""

	#   load image
	image = cv2.imread( TEST_IMAGE_PATH )

	#   convert bgr to rgb
	testImage = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )

	return testImage

########################################################
#
#	CLASS DEFINITIONS
#
class ImageLabel( QtGui.QLabel ):
	""" FOR Renderer only! """

	def __init__( self, currentImage ):
		
		#   call super class of label
		super( ImageLabel, self ).__init__()

		#   load image
		self.image = currentImage

		#   set image label
		self.setImageLabel( self.image )

		#   add image to label
		self.setPixmap( self.pixmap ) 

		#   initial position top left
		#   initial position bottom right
		#self.topLeftPosition = QtCore.QPoint( 0, 0 )
		#self.bottomRightPosition = QtCore.QPoint( 0, 0 )
		self.topLeftPosition = None
		self.bottomRightPosition = None

		#	bounding box rectangle object
		self.boundingBoxRect = None

	def mousePressEvent( self, event ):

		#   get event
		print "mouse press event " + str( event.pos().x() ) + " | " + str( event.pos().y() )
		
		#   get top left position
		self.topLeftPosition = event.pos()
		self.bottomRightPosition = event.pos()

		#   update 
		self.update()

	def mouseMoveEvent( self, event ):

		#   get event
		#print "mouse move event " + str( event.pos() )

		#   get bottom right position while moving
		self.bottomRightPosition = event.pos()

		#   update 
		self.update()

	def mouseReleaseEvent( self, event ):

		#   get event
		print "mouse release event " + str( event.pos().x() ) + " | " + str( event.pos().y() )

		#   get bottom right position
		self.bottomRightPosition = event.pos()

		#   update 
		self.update()

	def paintEvent( self, event ):
		
		#   create painter object
		self.painter = QtGui.QPainter(  )

		#   begin
		self.painter.begin( self )

		#   set painter to draw pixmap
		self.painter.drawPixmap( self.rect(), self.pixmap )

		if self.bottomRightPosition is not None and self.topLeftPosition is not None:
			
			#   setup pen
			self.painter.setPen( QtGui.QColor( QtCore.Qt.red ) )

			self.boundingBoxRect = QtCore.QRect( self.topLeftPosition, self.bottomRightPosition )

			#   draw !!!
			self.painter.drawRect( self.boundingBoxRect )
		
		else:
			
			try:
				#	Erase rectangle object
				self.painter.eraseRect( self.boundingBoxRect )

				#	NOTE:
				#		When remove rectangle, painter will remove inside too.
				#		So I fill pixmap after remove it.
				self.painter.drawPixmap( self.rect(), self.pixmap )
			
			except TypeError:
				print "[ERROR] {} : No rectangle object before".format( self ) 
 
		#   end
		self.painter.end()

	def setImageLabel( self, image ):
		
		#   get property of image 
		height, width, channel = image.shape
		bytePerRow = image.strides[ 0 ]

		#   create qImage from opencv
		#   convert image numpy format to QImage format
		self.qImage = QtGui.QImage( image.data, width, height, bytePerRow, QtGui.QImage.Format_RGB888 )

		#   create pixmap by QImage object
		self.pixmap = QtGui.QPixmap( self.qImage )



class ImageWidget( QtGui.QWidget ):
	
	def __init__( self, imageSequenceProvider ):

		#   call super class
		super( ImageWidget, self ).__init__()

		#   create image label
		self.imageLabel = ImageLabel( imageSequenceProvider.currentFrameImage )

		#   create layout
		self.boxLayout = QtGui.QVBoxLayout()

		#   add image label to layout
		self.boxLayout.addWidget( self.imageLabel )
		self.boxLayout.addStretch()

		#   set layout
		self.setLayout( self.boxLayout )


if __name__ == "__main__":
	
	from image_provider.frame_provider import ImageSequence

	#	initial app
	app = QtGui.QApplication( sys.argv )

	frameProvider = ImageSequence( TEST_FRAME_PATH )
	
	#	call widget
	widget = ImageWidget( frameProvider )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )
