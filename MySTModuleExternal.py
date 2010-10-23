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
#import sys
import os
import subprocess
from MySTBase import *
from MySTLog import *
from MySTReply import *

class MySTModuleExternal:
	
	def __init__(self, config):
		self.config = config
	
	def execute(self, instruct):
		# get the command
		extension = instruct.getCommand().lower()
		try:
			# File to call
			file = self.config.get('modules', extension, 'call')

			# normalize path separators
			fullpath = os.path.normpath( MySTBase.getExternalExtensionDir() + file )

			# Verify if file exists
			if (file == '' or not os.path.exists(fullpath)):
				raise Exception('Path not exists, please check and try again.')

			cmd  = [fullpath]
			args = instruct.__str__().split(' ')

			# merge command and arguments
			cmd_with_args = list( cmd + args )

			# execute command and get output
			o = subprocess.Popen(cmd_with_args, bufsize=-1, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, universal_newlines=True)

			(stdout, stdin, stderr) = (o.stdout, o.stdin, o.stderr)

			# get output to send to contact
			output = stdout.read()

			MySTLog.log('Running external module: '+extension+' ('+file+')')

			stdout.close()
			stdin.close()
			stderr.close()

		except:
			output = MySTBase.getCommandNotFoundMessage()
			MySTLog.log('Ops! tried to execute non existing module')

		# call the reply object
		return MySTReply(MySTBase.getSucessCode(), output)

