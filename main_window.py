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
#from widget.step_button import StepButton
#from widget.image_widget import ImageWidget

from image_provider.frame_provider import ImageSequence

from widget.frame_with_roi import FrameWithROI

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

    def __init__( self, framePathStr, saveYAMLPath = None ):
        
        #   call init from super class
        super( MainWindow, self ).__init__()

        #   get menu bar object
        menuBar = self.menuBar()

        #   add file menu to menu bar
        self.fileMenu = menuBar.addMenu( "File" )

        #   add `New` action
        self.loadAction = QtGui.QAction( "Load", self )
        self.fileMenu.addAction( self.loadAction )

        #   create `Save` action
        self.saveAction = QtGui.QAction( "Save", self )
        self.saveAction.setShortcut( "Ctrl+S" )
        self.saveAction.triggered.connect( self.saveActionFunctionCallback )
        
        #   add `Save` action
        self.fileMenu.addAction( self.saveAction )

        #   add `Quit` action
        self.quitAction = QtGui.QAction( "Quit", self )
        self.fileMenu.addAction( self.quitAction )

        #   initial instnce of widget profile
        self.mainWidget = MainWidget( framePathStr, saveYAMLPath )

        #   add outside widget
        self.setCentralWidget( self.mainWidget )

        #   set title
        self.setWindowTitle( "Pyxis (beta-version)" )

    def saveActionFunctionCallback( self ):
        
        #   get file path
        filePathStr = str( QtGui.QFileDialog.getSaveFileName( self, "Save yaml", os.path.expanduser( "~" ), '(*.yaml)' ) )

        #   check format if not have put it
        if filePathStr.split( '.' )[ -1 ] != 'yaml':
            filePathStr += ".yaml"

        print "Save as {}".format( filePathStr )

        #   save yaml
        self.mainWidget.frameWithROI.roiProvider.saveDataDict( filePathStr )


class MainWidget( QtGui.QWidget ):

    def __init__( self, framePath, saveYAMLPath ):

        #   call super class
        super( MainWidget, self ).__init__()

        #   create image sequence instance
        # self.imageSequenceProvider = ImageSequence( framePath )

        #   get widget
        #self.imageWidget = ImageWidget( self.imageSequenceProvider )
        #self.buttonWidget = StepButton( self.imageSequenceProvider )

        self.frameWithROI = FrameWithROI( framePath, saveYAMLPath )

        #   create box layout
        self.boxLayout = QtGui.QVBoxLayout()   

        #   add widget to box
        self.boxLayout.addWidget( self.frameWithROI )
      
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





