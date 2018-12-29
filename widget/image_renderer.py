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

from PyQt4 import QtGui, QtCore

########################################################
#
#	GLOBALS
#

########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

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

	def setImageLabel( self, image ):
		
		#   get property of image 
		height, width, channel = image.shape
		bytePerRow = image.strides[ 0 ]

		#   create qImage from opencv
		#   convert image numpy format to QImage format
		self.qImage = QtGui.QImage( image.data, width, height, bytePerRow, QtGui.QImage.Format_RGB888 )

		#   create pixmap by QImage object
		self.pixmap = QtGui.QPixmap( self.qImage )

		#	set pixmap to image label
		self.setPixmap( self.pixmap ) 