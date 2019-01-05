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

from widget.frame_with_next_previous_button import ImageWithNextPreviousButton
from widget.color_calibrate_button_widget import ColorButton

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

class ColorCalibrateImageSeqSubapp( QtGui.QWidget ):

    def __init__( self, imageSeqPathStr, configPathStr = None, savePath = '/tmpfs/config.ini' ):

        super( ColorCalibrateImageSeqSubapp, self ).__init__()

        #   get config
        self.configDict = getConfigDict( path = configPathStr )

        #   get save path
        self.savePath = savePath

        #   initialize image with button and color button
        self.colorButton = ColorButton( self.configDict )
        self.imageWithButton = ImageWithNextPreviousButton( imageSeqPathStr, self.colorButton )

        #   create export button
        self.exportButton = QtGui.QPushButton( "Export" )

        #   connect export button with callback function
        self.exportButton.clicked.connect( self.exportButtonFunctionCallback )

        #   create layout
        self.mainLayout = QtGui.QVBoxLayout()

        #   add layout
        self.mainLayout.addWidget( self.imageWithButton )
        self.mainLayout.addWidget( self.colorButton )
        self.mainLayout.addWidget( self.exportButton )

        #   set layout
        self.setLayout( self.mainLayout )

    def exportButtonFunctionCallback( self ):

        print "Save as {}".format( self.savePath )

        saveConfig( self.configDict, savePathStr = self.savePath )


if __name__ == "__main__":


    framePath = "/home/neverholiday/work/ball_detector/raw_data/camera_onbot"

    #	initial app
    app = QtGui.QApplication( sys.argv )

	#	call widget
    widget = ColorCalibrateImageSeqSubapp( framePath )

	#	show
    widget.show()

	#	execute app
    sys.exit( app.exec_() )
