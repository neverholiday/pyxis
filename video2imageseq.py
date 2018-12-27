#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

VERSIONNUMBER = 'v1.0'
PROGRAM_DESCRIPTION = "Change video to image seqeuence"

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

import cv2
import numpy as np

########################################################
#
#	Standard globals
#
NUM_REQUIRE_ARGUMENT = 2

########################################################
#
#	Program specific globals
#

########################################################
#
#	Helper functions
#

def generateFrameNumber( numIdx ):

	#   get index name
	idxNameStr = str( numIdx )
	if len( idxNameStr ) == 1:
		idxNameStr = '000' + idxNameStr
	elif len( idxNameStr ) == 2:
		idxNameStr = '00' + idxNameStr
	elif len( idxNameStr ) == 3:
		idxNameStr = '0' + idxNameStr

	return idxNameStr

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
	parser.add_option( "--prefixName", dest = "prefixName", type = "string", action = "store",
						help = "Specify prefix name.", default = "frame" )

	parser.add_option( "--formatFile", dest = "formatFile", type = "string", action = "store",
						help = "Specify image format file.", default = "jpg" )

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
	videoPathStr = args[ 0 ]
	saveDirPathStr = os.path.abspath( args[ 1 ] )

	#	get filename and format from this option 
	prefixNameStr = options.prefixName
	formatName = options.formatFile

	#	create directory
	#	if not have, mkdir it
	if not os.path.exists( saveDirPathStr ):
		os.mkdir( saveDirPathStr )

	#	initial capture instance
	capture = cv2.VideoCapture( videoPathStr )

	#	TODO : อย่างแรง
	#	ให้ savefile เท่าไหร่ก็ได้
	#	แก้ขัดไปก่อน
	if capture.get( cv2.CAP_PROP_FRAME_COUNT ) > 9999:
		raise TypeError( "HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA, Exceed 9999 frames" )

	#	initial frame index
	frameIndex = 0

	while True:

		#	get image 
		ret, frame = capture.read()

		#	break when frame is empty
		if not ret:
			break

		#
		#	save process
		#

		#	get frame number for save
		frameIndexStr = generateFrameNumber( frameIndex )

		#	combine prefix, frame number and format file
		fileNameStr = prefixNameStr + frameIndexStr + '.' + formatName

		if saveDirPathStr[ -1 ] != '/':
			savePathStr = saveDirPathStr + '/' + fileNameStr

		else:
			savePathStr = saveDirPathStr + fileNameStr
		
		save = cv2.imwrite( savePathStr, frame )

		if not save:
			raise IOError( "{} can't save hahahaha".format( savePathStr ) )

		#
		#	Show Information 
		#
		print "Save as {}".format( savePathStr )
		print "Remaining {} / {} ".format( frameIndex + 1, int( capture.get( cv2.CAP_PROP_FRAME_COUNT ) ) ) 

		#	increment index of frame number
		frameIndex += 1	

	print "finish!!!"
	capture.release()

########################################################
#
#	call main
#

if __name__=='__main__':
	main()

