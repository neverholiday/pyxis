#!/usr/bin/env python
#
# Copyright (C) 2018  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

VERSIONNUMBER = 'v1.0'
PROGRAM_DESCRIPTION = "Image processing GUI for hanuman"

########################################################
#
#	STANDARD IMPORTS
#

import sys
import os

import optparse

########################################################
#
#	LOCAL IMPORTS
#

from PyQt4 import QtGui, QtCore
from main_window import MainWindow

########################################################
#
#	Standard globals
#
NUM_REQUIRE_ARGUMENT = 1

########################################################
#
#	Program specific globals
#

########################################################
#
#	Helper functions
#


########################################################
#
#	Class definitions
#

########################################################
#
#	Function bodies
#

########################################################
#
#	main
#	
def main():
	
	#	define usage of programing
	programUsage = "python %prog arg [option] " + str( VERSIONNUMBER ) + ', Copyright (C) 2018 FIBO/KMUTT'

	#	initial parser instance
	parser = optparse.OptionParser( usage = programUsage, description=PROGRAM_DESCRIPTION )

	#	add option of main script
	parser.add_option( "--yamlPath", dest = "yamlPath", type = "string", action = "store",
						help = "Load yaml." )

	#	add option
	( options, args ) = parser.parse_args()

	#	check number of argument from NUM_REQUIRE_ARGUMENT
	if len( args ) != NUM_REQUIRE_ARGUMENT:	
		
		#	raise error from parser
		parser.error( "require {} argument(s)".format( NUM_REQUIRE_ARGUMENT ) )


	#########################################################
	#
	#		get option and argument
	#
	
	print "Start Pyxis Beta Version."

	#	get frame path str
	framePathStr = args[ 0 ]

	#	get yaml path
	yamlPathStr = options.yamlPath

	#	initial app
	app = QtGui.QApplication( sys.argv )

	#	call widget
	mainWindow = MainWindow( framePathStr, yamlPathStr )

	#	show
	mainWindow.show()

	#	execute app
	sys.exit( app.exec_() )
	

########################################################
#
#	call main
#

if __name__=='__main__':
	main()

