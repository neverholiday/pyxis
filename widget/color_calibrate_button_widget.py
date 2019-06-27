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

from slider_widget import Slider
from config_generator import COLOR_CONFIG_SUPPORT_LIST
from config_generator import setNewValueToConfigColor, getConfigValue

import numpy as np

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

class ColorButton( QtGui.QWidget ):
	
	def __init__( self, configDict ):

		#   SUPAAAAAAAAAAAAAAAAAA
		super( ColorButton, self ).__init__( )
		
		#   get configdict
		self.configDict = configDict

		#   create button
		self.submitButton = QtGui.QPushButton( "Submit" )

		#   create combobox
		self.colorParameterComboBox = QtGui.QComboBox()
		self.colorParameterComboBox.addItems( COLOR_CONFIG_SUPPORT_LIST )

		#   initial slider
		self.sliderWidget = Slider( *getConfigValue( self.configDict, str( self.colorParameterComboBox.currentText() ) ) )

		#	Create reset button
		self.resetButton = QtGui.QPushButton( "Reset" )
 
		#   connect callback function
		self.submitButton.clicked.connect( self.submitButtonCallbackFunction )
		self.colorParameterComboBox.currentIndexChanged.connect( self.colorParameterComboBoxCallbackFunction )
		self.resetButton.clicked.connect( self.resetButtonCallbackFunction )

		#   create layout
		self.verticalBoxLayout = QtGui.QVBoxLayout()

		#   add slider to layout
		self.verticalBoxLayout.addWidget( self.colorParameterComboBox )
		self.verticalBoxLayout.addWidget( self.sliderWidget )
		self.verticalBoxLayout.addWidget( self.resetButton )
		self.verticalBoxLayout.addWidget( self.submitButton )

		#   set layout
		self.setLayout( self.verticalBoxLayout )

	def submitButtonCallbackFunction( self ):

		#   get hsv value from tracking bar
		upperValueArray, lowerValueArray = self.getColorRangeValueList()

		#   get every h, s, v max and min
		hMax = int( upperValueArray[ 0 ] )
		sMax = int( upperValueArray[ 1 ] )
		vMax = int( upperValueArray[ 2 ] )
		hMin = int( lowerValueArray[ 0 ] )
		sMin = int( lowerValueArray[ 1 ] )
		vMin = int( lowerValueArray[ 2 ] )

		#   get color key
		colorKeyStr = str( self.colorParameterComboBox.currentText() )

		#   set new color
		setNewValueToConfigColor( self.configDict, colorKeyStr, H_max=hMax, H_min=hMin, S_max=sMax, S_min=sMin, V_max=vMax, V_min=vMin )

	def colorParameterComboBoxCallbackFunction( self ):

		#   get color key
		colorKeyStr = str( self.colorParameterComboBox.currentText() )

		#	get hsv value
		hMax, sMax, vMax, hMin, sMin, vMin = getConfigValue( self.configDict, colorKeyStr )

		#	change slider value
		# self.sliderWidget.hMaxSlider.setValue( hMax )
		# self.sliderWidget.sMaxSlider.setValue( sMax )
		# self.sliderWidget.vMaxSlider.setValue( vMax )
		# self.sliderWidget.hMinSlider.setValue( hMin )
		# self.sliderWidget.sMinSlider.setValue( sMin )
		# self.sliderWidget.vMinSlider.setValue( vMin )
		self.sliderWidget.setValue( hMax, sMax, vMax, hMin, sMin, vMin )


	def resetButtonCallbackFunction( self ):

		#	Reset value from config
		self.sliderWidget.setValue( *getConfigValue( self.configDict, str( self.colorParameterComboBox.currentText() ) ) )
		 

	def getColorRangeValueList( self ):

		upperValueList = [ self.sliderWidget.hMaxValue, self.sliderWidget.sMaxValue, self.sliderWidget.vMaxValue ]
		lowerValueList = [ self.sliderWidget.hMinValue, self.sliderWidget.sMinValue, self.sliderWidget.vMinValue ]

		#   convert to numpy array
		upperValueArray = np.array( upperValueList )
		lowerValueArray = np.array( lowerValueList )
 
		return upperValueArray, lowerValueArray

if __name__ == "__main__":

	import configobj
	from config_generator import CONFIG_DEFAULT_PATH
	
	#	initial app
	app = QtGui.QApplication( sys.argv )

	#	get dummy config
	config = configobj.ConfigObj( CONFIG_DEFAULT_PATH )[ "ColorDefinitions" ]
	
	#	call widget
	widget = ColorButton( config )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )
