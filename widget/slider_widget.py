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

class Slider( QtGui.QWidget ):

    def __init__( self, h_max, s_max, v_max, h_min, s_min, v_min ):

        #   SUPAAAA
        super( Slider, self ).__init__()

        #   create HSV slider
        self.hMaxSlider = QtGui.QSlider( QtCore.Qt.Horizontal )
        self.sMaxSlider = QtGui.QSlider( QtCore.Qt.Horizontal )
        self.vMaxSlider = QtGui.QSlider( QtCore.Qt.Horizontal )
        self.hMinSlider = QtGui.QSlider( QtCore.Qt.Horizontal )
        self.sMinSlider = QtGui.QSlider( QtCore.Qt.Horizontal )
        self.vMinSlider = QtGui.QSlider( QtCore.Qt.Horizontal )       

        #   create label
        self.hMaxLabel = QtGui.QLabel( 'H_max' )
        self.hMinLabel = QtGui.QLabel( 'H_min' )
        self.sMaxLabel = QtGui.QLabel( 'S_max' )
        self.sMinLabel = QtGui.QLabel( 'S_min' )
        self.vMaxLabel = QtGui.QLabel( 'V_max' )
        self.vMinLabel = QtGui.QLabel( 'V_min' )

        #   create line edit
        self.hMaxLineEdit = QtGui.QLineEdit( str( h_max ) )
        self.hMinLineEdit = QtGui.QLineEdit( str( h_min ) )
        self.sMaxLineEdit = QtGui.QLineEdit( str( s_max ) )
        self.sMinLineEdit = QtGui.QLineEdit( str( s_min ) )
        self.vMaxLineEdit = QtGui.QLineEdit( str( v_max ) )
        self.vMinLineEdit = QtGui.QLineEdit( str( v_min ) )

        #   initial value of HSV
        self.hMaxValue = h_max
        self.sMaxValue = s_max
        self.vMaxValue = v_max
        self.hMinValue = h_min
        self.sMinValue = s_min
        self.vMinValue = v_min

        #   set H_max range of slider
        self.hMaxSlider.setMinimum( 0 )
        self.hMaxSlider.setMaximum( 179 )
        self.hMaxSlider.setValue( h_max )

        #   set H_min range of slider
        self.hMinSlider.setMinimum( 0 )
        self.hMinSlider.setMaximum( 179 )
        self.hMinSlider.setValue( h_min )

        #   set S_max range of slider
        self.sMaxSlider.setMinimum( 0 )
        self.sMaxSlider.setMaximum( 255 )
        self.sMaxSlider.setValue( s_max )

        #   set S_min range of slider
        self.sMinSlider.setMinimum( 0 )
        self.sMinSlider.setMaximum( 255 )
        self.sMinSlider.setValue( s_min )

        #   set V_max range of slider
        self.vMaxSlider.setMinimum( 0 )
        self.vMaxSlider.setMaximum( 255 )
        self.vMaxSlider.setValue( v_max )

        #   set V_min range of slider
        self.vMinSlider.setMinimum( 0 )
        self.vMinSlider.setMaximum( 255 )
        self.vMinSlider.setValue( v_min )
        
        #   add callback function for slider
        self.hMaxSlider.valueChanged.connect( self.hMaxSliderValueChangeCallback )
        self.hMinSlider.valueChanged.connect( self.hMinSliderValueChangeCallBack )
        self.sMaxSlider.valueChanged.connect( self.sMaxSliderValueChangeCallback )
        self.sMinSlider.valueChanged.connect( self.sMinSliderValueChangeCallBack )
        self.vMaxSlider.valueChanged.connect( self.vMaxSliderValueChangeCallback )
        self.vMinSlider.valueChanged.connect( self.vMinSliderValueChangeCallBack )

        #   add callback function for edit space
        self.hMaxLineEdit.returnPressed.connect( self.hMaxLineEditEnterPressCallBack )
        self.hMinLineEdit.returnPressed.connect( self.hMinLineEditEnterPressCallBack )
        self.sMaxLineEdit.returnPressed.connect( self.sMaxLineEditEnterPressCallBack )
        self.sMinLineEdit.returnPressed.connect( self.sMinLineEditEnterPressCallBack )
        self.vMaxLineEdit.returnPressed.connect( self.vMaxLineEditEnterPressCallBack )
        self.vMinLineEdit.returnPressed.connect( self.vMinLineEditEnterPressCallBack )

        #   create 3 x horizon layout and 1 x vertical box layout
        #   create layout and push sliders to created layout
        self.hueBoxLayout = QtGui.QHBoxLayout()
        self.saturateBoxLayout = QtGui.QHBoxLayout()
        self.valueBoxLayout = QtGui.QHBoxLayout()
        self.verticalBoxLayout = QtGui.QVBoxLayout()

        #   add hue max and min to horizontal box layout
        self.hueBoxLayout.addWidget( self.hMinLabel )
        self.hueBoxLayout.addWidget( self.hMinSlider )
        self.hueBoxLayout.addWidget( self.hMinLineEdit )
        self.hueBoxLayout.addStretch()
        self.hueBoxLayout.addWidget( self.hMaxLabel )
        self.hueBoxLayout.addWidget( self.hMaxSlider )
        self.hueBoxLayout.addWidget( self.hMaxLineEdit )

        #   add saturate max and min to horizontal box layout
        self.saturateBoxLayout.addWidget( self.sMinLabel )
        self.saturateBoxLayout.addWidget( self.sMinSlider )
        self.saturateBoxLayout.addWidget( self.sMinLineEdit )
        self.saturateBoxLayout.addStretch()
        self.saturateBoxLayout.addWidget( self.sMaxLabel )
        self.saturateBoxLayout.addWidget( self.sMaxSlider )
        self.saturateBoxLayout.addWidget( self.sMaxLineEdit )

        #   add value max and min to horizontal box layout
        self.valueBoxLayout.addWidget( self.vMinLabel )
        self.valueBoxLayout.addWidget( self.vMinSlider )
        self.valueBoxLayout.addWidget( self.vMinLineEdit )
        self.valueBoxLayout.addStretch()
        self.valueBoxLayout.addWidget( self.vMaxLabel )
        self.valueBoxLayout.addWidget( self.vMaxSlider )
        self.valueBoxLayout.addWidget( self.vMaxLineEdit )

        #   add three-horizontal box layout to vertical box layout
        self.verticalBoxLayout.addLayout( self.hueBoxLayout )
        self.verticalBoxLayout.addLayout( self.saturateBoxLayout )
        self.verticalBoxLayout.addLayout( self.valueBoxLayout )

        #   set to show
        self.setLayout( self.verticalBoxLayout )

    def hMaxSliderValueChangeCallback( self ):

        self.hMaxValue = self.hMaxSlider.value()
        self.hMaxLineEdit.setText( str( self.hMaxValue ) )

    def hMinSliderValueChangeCallBack( self ):

        self.hMinValue = self.hMinSlider.value()
        self.hMinLineEdit.setText( str( self.hMinValue ) )

    def sMaxSliderValueChangeCallback( self ):

        self.sMaxValue = self.sMaxSlider.value()
        self.sMaxLineEdit.setText( str( self.sMaxValue ) )

    def sMinSliderValueChangeCallBack( self ):

        self.sMinValue = self.sMinSlider.value()
        self.sMinLineEdit.setText( str( self.sMinValue ) )

    def vMaxSliderValueChangeCallback( self ):

        self.vMaxValue = self.vMaxSlider.value() 
        self.vMaxLineEdit.setText( str( self.vMaxValue ) )

    def vMinSliderValueChangeCallBack( self ):

        self.vMinValue = self.vMinSlider.value()
        self.vMinLineEdit.setText( str( self.vMinValue ) )

    def hMaxLineEditEnterPressCallBack( self ):
    
        self.hMaxValue = int( self.hMaxLineEdit.text() )
        self.hMaxSlider.setValue( self.hMaxValue )
    
    def hMinLineEditEnterPressCallBack( self ):
    
        self.hMinValue = int( self.hMinLineEdit.text() )
        self.hMinSlider.setValue( self.hMinValue )
    
    def sMaxLineEditEnterPressCallBack( self ):
    
        self.sMaxValue = int( self.sMaxLineEdit.text() )
        self.sMaxSlider.setValue( self.sMaxValue )
    
    def sMinLineEditEnterPressCallBack( self ):
    
        self.sMinValue = int( self.sMinLineEdit.text() )
        self.sMinSlider.setValue( self.sMinValue )

    def vMaxLineEditEnterPressCallBack( self ):
    
        self.vMaxValue = int( self.vMaxLineEdit.text() )
        self.vMaxSlider.setValue( self.vMaxValue )
    
    def vMinLineEditEnterPressCallBack( self ):
    
        self.vMinValue = int( self.vMinLineEdit.text() )
        self.vMinSlider.setValue( self.vMinValue )
    
    def setValue( self, h_max, s_max, v_max, h_min, s_min, v_min ):

        self.hMaxSlider.setValue( h_max )
        self.hMinSlider.setValue( h_min )
        self.sMaxSlider.setValue( s_max )
        self.sMinSlider.setValue( s_min )
        self.vMaxSlider.setValue( v_max )
        self.vMinSlider.setValue( v_min )

if __name__ == "__main__":
    
    #	initial app
	app = QtGui.QApplication( sys.argv )
	
	#	call widget
	widget = Slider( 255, 255, 255, 0, 0, 0 )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )


