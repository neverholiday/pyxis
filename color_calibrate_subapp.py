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

from PyQt4 import QtCore
from PyQt4 import QtGui

from widget.color_calibrate_button_widget import ColorButton
from widget.frame_widget import FrameWidget
from config_generator import getConfigDict, saveConfig

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

class ColorCalibrateSubapp( QtGui.QWidget ):

    def __init__( self, cameraDevice, configPathStr = None, savePath = '/tmpfs/config.ini' ):

        #   SUPAAAAA
        super( ColorCalibrateSubapp, self ).__init__()

        #   get config dict structure
        self.configDict = getConfigDict( path = configPathStr )
        self.savePathStr = savePath

        #   create color button and slider
        self.colorButton = ColorButton( self.configDict[ "ColorDefinitions" ] )
        self.frameCameraWidget = FrameWidget( cameraDevice, self.colorButton )

        #   create export button
        self.exportButton = QtGui.QPushButton( 'Export' )

        #   connect export to callback function
        self.exportButton.clicked.connect( self.exportButtonCallbackFunction )

        #   create vertical box layout
        self.verticalBoxLayout = QtGui.QVBoxLayout()

        #   add widget 
        self.verticalBoxLayout.addWidget( self.frameCameraWidget )
        self.verticalBoxLayout.addWidget( self.colorButton )
        self.verticalBoxLayout.addWidget( self.exportButton )

        #   set to layout
        self.setLayout( self.verticalBoxLayout )

    def exportButtonCallbackFunction( self ):
        
        print "Save!"

        saveConfig( self.configDict, savePathStr = self.savePathStr )

if __name__ == "__main__":
	
	#	initial app
	app = QtGui.QApplication( sys.argv )

	#	call widget
	widget = ColorCalibrateSubapp( '/dev/video1' )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )