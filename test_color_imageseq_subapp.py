#!/usr/bin/env python
#
# Copyright (C) 2018  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

VERSIONNUMBER = 'v1.0'
PROGRAM_DESCRIPTION = "one of pyxis, color calibrator"

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

from PyQt4 import QtCore
from PyQt4 import QtGui
from color_calibrate_imageseq_subapp import ColorCalibrateImageSeqSubapp

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

	parser.add_option( "-i", "--importConfigPathStr", dest = "importConfigPathStr", type = "string", action = "store",
						help = "Import config path." )
	
	parser.add_option( "-o", "--exportConfigPathStr", dest = "exportConfigPathStr", type = "string", action = "store",
						help = "Export config path.", default = "/tmpfs/config.ini" )
	

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
	framePathStr = args[ 0 ]
	
	importConfigPathStr = options.importConfigPathStr
	exportConfigPathStr = options.exportConfigPathStr

	#	initial app
	app = QtGui.QApplication( sys.argv )

	#	call widget
	widget = ColorCalibrateImageSeqSubapp( framePathStr, configPathStr = importConfigPathStr, savePath = exportConfigPathStr )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )
	

########################################################
#
#	call main
#

if __name__=='__main__':
	main()

