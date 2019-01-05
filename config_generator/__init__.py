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

import configobj

########################################################
#
#	GLOBALS
#

CONFIG_DEFAULT_PATH = __path__[ 0 ] + '/config.ini'

COLOR_CONFIG_SUPPORT_LIST = [
            'OrangeColorParameter',
            'FieldGreenColorParameter',
            'BlueColorParameter',
            'YellowColorParameter',
            'WhiteColorParameter',
            'BlackColorParameter',
            'MagentaColorParameter',
            'CyanColorParameter'
]

########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

def getConfigDict( path = None ):
    """
    Get dictionary of config
    """

    if path is None:
        config = configobj.ConfigObj( CONFIG_DEFAULT_PATH )
    else:
        config = configobj.ConfigObj( path )

    return config

def getConfigDictAsPath( path ):
    """
    Get config by to this path
    """
    config = configobj.ConfigObj( path )

    return config

def saveConfig( config, savePathStr = None ):
    """
    Save new config to same file or new file if path is not none
    """

    if savePathStr is None:
        config.write()

    else:
        with open( savePathStr, 'w' ) as outputFile:
            config.write( outfile = outputFile )

def setNewValueToConfigColor( config, colorKey, H_max = None, H_min = None, S_max = None, S_min = None, V_max = None, V_min = None ):
    """
    Set new value to config depend on colorkey
    Example of color key which is valid :

        'OrangeColorParameter',
        'FieldGreenColorParameter',
        'BlueColorParameter',
        'YellowColorParameter',
        'WhiteColorParameter',
        'BlackColorParameter',
        'MagentaColorParameter',
        'CyanColorParameter'
    
    """
    
    try:
        if H_max is not None:
            config[ colorKey ][ 'H_max' ] = H_max
        if H_min is not None:
            config[ colorKey ][ 'H_min' ] = H_min
        if S_max is not None:
            config[ colorKey ][ 'S_max' ] = S_max
        if S_min is not None:
            config[ colorKey ][ 'S_min' ] = S_min
        if V_max is not None:
            config[ colorKey ][ 'V_max' ] = V_max
        if V_min is not None:
            config[ colorKey ][ 'V_min' ] = V_min

        return True

    except KeyError:

        print "[ERROR] {} is not valid".format( colorKey )

        return False

def getConfigValue( config, colorKey ):

    #   get hsv value
    hMax = int( config[ colorKey ][ 'H_max' ] )    
    sMax = int( config[ colorKey ][ 'S_max' ] )
    vMax = int( config[ colorKey ][ 'V_max' ] )
    hMin = int( config[ colorKey ][ 'H_min' ] )
    sMin = int( config[ colorKey ][ 'S_min' ] )
    vMin = int( config[ colorKey ][ 'V_min' ] )
 
    return ( hMax, sMax, vMax, hMin, sMin, vMin )