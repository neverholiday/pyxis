#!/usr/bin/env python
#
# Copyright (C) 2018  FIBO/KMUTT
#			Written by Nasrun Hayeeyema
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
from widget.step_button import StepButton
from widget.image_widget import ImageWidget

from image_provider.frame_provider import ImageSequence

########################################################
#
#	GLOBALS
#

TEST_IMAGE_PATH = "/home/neverholiday/work/ball_detector/raw_data/data1"

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

class MainWindow( QtGui.QMainWindow ):

    def __init__( self, framePathStr ):
        
        #   call init from super class
        super( MainWindow, self ).__init__()

        #   get menu bar object
        menuBar = self.menuBar()

        #   add file menu to menu bar
        fileMenu = menuBar.addMenu( "File" )

        #   add `New` action
        fileMenu.addAction( "New" )

        #   create `Save` action
        saveAction = QtGui.QAction( "Save", self )
        saveAction.setShortcut( "Ctrl+S" )
        
        #   add `Save` action
        fileMenu.addAction( saveAction )

        #   add `Quit` action
        quitAction = QtGui.QAction( "Quit", self )
        fileMenu.addAction( quitAction )

        #   initial instnce of widget profile
        mainWidget = MainWidget( framePathStr )

        #   add outside widget
        self.setCentralWidget( mainWidget )

        #   set title
        self.setWindowTitle( "Pyxis (beta-version)" )

class MainWidget( QtGui.QWidget ):

    def __init__( self, framePath ):

        #   call super class
        super( MainWidget, self ).__init__()

        #   create image sequence instance
        self.imageSequenceProvider = ImageSequence( framePath )

        #   get widget
        self.imageWidget = ImageWidget( self.imageSequenceProvider )
        #self.buttonWidget = StepButton( self.imageSequenceProvider )

        #   create box layout
        self.boxLayout = QtGui.QVBoxLayout()   

        #   add widget to box
        self.boxLayout.addWidget( self.imageWidget )

      
        #   set layout
        self.setLayout( self.boxLayout )

if __name__ == "__main__":
    
    #	initial app
	app = QtGui.QApplication( sys.argv )

	#	call widget
	mainWindow = MainWindow( TEST_IMAGE_PATH )

	#	show
	mainWindow.show()

	#	execute app
	sys.exit( app.exec_() )





