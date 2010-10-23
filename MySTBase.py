#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
   This file is part of MyServerTalks.

    MyServerTalks is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    MyServerTalks is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MyServerTalks; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import os
import sys
import time
from MySTConfig import *

class MySTBase(object):
	
	sucess_code    = 0
	error_code     = 1
	unavaible_code = 2
	
	# ---- CODE MSG CONSTANTS -------------
	
	# Sucess Code
	def getSucessCode():
		return MySTBase.sucess_code
	getSucessCode = staticmethod(getSucessCode)

	# Error Code
	def getErrorCode():
		return MySTBase.error_code
	getErrorCode = staticmethod(getErrorCode)
	
	# Unavaible Code
	def getUnavaibleCode():
		return MySTBase.unavaible_code
	getUnavaibleCode = staticmethod(getUnavaibleCode)
	
	# -------------------------------------
	
	# Current Version of MyServerTalks!
	def getVersion():
		config = MySTConfig()
		return config.get('config', 'info', 'version')
	getVersion = staticmethod(getVersion)
	
	# Get the external extensions dir
	def getExternalExtensionDir():
		dir = sys.path[0]+'/extensions/external/'
		if (os.path.exists(dir)):
			return dir
		else:
			print 'Directory for external extensions not found. Create it.'
			sys.exit()
	getExternalExtensionDir = staticmethod(getExternalExtensionDir)
	
	# Get the external extensions dir
	def getAutoloadExtensionDir():
		dir = sys.path[0]+'/extensions/autoload/'
		if (os.path.exists(dir)):
			return dir
		else:
			print 'Directory for autoload extensions not found. Create it.'
			sys.exit()
	getAutoloadExtensionDir = staticmethod(getAutoloadExtensionDir)
	
	# Command not found message
	def getCommandNotFoundMessage():
		return "Ops! Command not found. Try 'help' for a command list."
	getCommandNotFoundMessage = staticmethod(getCommandNotFoundMessage)
	
	# Command not found message
	def getModuleNotFoundMessage():
		return "Module file not exists. Check the file name and try again."
	getModuleNotFoundMessage = staticmethod(getModuleNotFoundMessage)
	
	# Fatal error message
	def getFatalErrorMessage():
		return "Fatal error! MyServerTalks found a problem and need to be restarted, sorry."
	getFatalErrorMessage = staticmethod(getFatalErrorMessage)
	
	# Get current date and time
	def getDateTime():
		# format: Thu Jun 21, 2007 00:02:37 AM
		return time.strftime('%a %b %d, %Y %H:%M:%S %p', time.localtime(time.time()))
	getDateTime = staticmethod(getDateTime)

