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

from image_renderer import ImageLabel

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
class ImageWithBoundingBox( ImageLabel ):
	""" FOR Renderer only! """

	def __init__( self, currentImage ):
		
		#   call super class of label
		super( ImageWithBoundingBox, self ).__init__( currentImage )

		#   initial position top left
		#   initial position bottom right
		#self.topLeftPosition = QtCore.QPoint( 0, 0 )
		#self.bottomRightPosition = QtCore.QPoint( 0, 0 )
		self.topLeftPosition = None
		self.bottomRightPosition = None

		#	initial list of position that contain tuple of coordinate
		#	ex. [ ( topRight, bottomLeft ), ( ... ) ]
		self.submitPositivePosition = list()
		self.submitNegativePosition = list()

		#	bounding box rectangle object
		self.boundingBoxRect = None

	def mousePressEvent( self, event ):

		#   get event
		print "mouse press event " + str( event.pos().x() ) + " | " + str( event.pos().y() )
		
		#   get top left position
		self.topLeftPosition = event.pos()
		self.bottomRightPosition = event.pos()

 		#   update 
		#self.update()

	def mouseMoveEvent( self, event ):

		#   get event
		#print "mouse move event " + str( event.pos() )

		#   get bottom right position while moving
		self.bottomRightPosition = event.pos()

		#   update 
		#self.update()

	def mouseReleaseEvent( self, event ):

		#   get event
		print "mouse release event " + str( event.pos().x() ) + " | " + str( event.pos().y() )

		#   get bottom right position
		self.bottomRightPosition = event.pos()

		#   update 
		#self.update()

	def paintEvent( self, event ):
		
		#   create painter object
		self.painter = QtGui.QPainter(  )

		#   begin
		self.painter.begin( self )

		#   set painter to draw pixmap
		self.painter.drawPixmap( self.rect(), self.pixmap )

		#
		#	re-draw image submit roi	
		#
		for roiTuple in self.submitPositivePosition:

			#	get top left and bottom right
			topLeftPos = QtCore.QPoint( roiTuple[ 0 ][ 1 ], roiTuple[ 0 ][ 0 ] )  
			bottomRightPos = QtCore.QPoint( roiTuple[ 1 ][ 1 ], roiTuple[ 1 ][ 0 ] )

			#	setup pen
			self.painter.setPen( QtGui.QColor( QtCore.Qt.blue ) )

			#	create temporary bounding box
			boundingBoxRect = QtCore.QRect( topLeftPos, bottomRightPos )

			#	draw each of box
			self.painter.drawRect( boundingBoxRect )

		for roiTuple in self.submitNegativePosition:

			#	get top left and bottom right
			topLeftPos = QtCore.QPoint( roiTuple[ 0 ][ 1 ], roiTuple[ 0 ][ 0 ] )  
			bottomRightPos = QtCore.QPoint( roiTuple[ 1 ][ 1 ], roiTuple[ 1 ][ 0 ] )

			#	setup pen
			self.painter.setPen( QtGui.QColor( QtCore.Qt.red ) )

			#	create temporary bounding box
			boundingBoxRect = QtCore.QRect( topLeftPos, bottomRightPos )

			#	draw each of box
			self.painter.drawRect( boundingBoxRect )

		#	create not submit bounding box
		if self.bottomRightPosition is not None and self.topLeftPosition is not None:
			
			#   setup pen
			self.painter.setPen( QtGui.QColor( QtCore.Qt.yellow ) )

			#	create bounding box
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
				#print "[ERROR] {} : No rectangle object before".format( self ) 
				pass
		#   end
		self.painter.end()

class ImageWidget( QtGui.QWidget ):
	
	def __init__( self, imageSequenceProvider ):

		#   call super class
		super( ImageWidget, self ).__init__()

		#   create image label
		self.imageLabel = ImageWithBoundingBox( imageSequenceProvider.currentFrameImage )

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
