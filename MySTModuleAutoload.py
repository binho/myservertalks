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
import thread
import xmpp
import locale
import subprocess
from MySTBase import *
from MySTLog import *
from MySTReply import *
from MySTContactManager import *

class MySTModuleAutoload:

	# ----------------------------------------------------------------------------------------

	def __init__(self, config, jabber, user_handler):
		self.config       = config
		self.jabber       = jabber
		self.user_handler = user_handler

		# load modules
		modules = self.config.get('modules')
		for module in modules:
			# get module type
			type = self.config.get('modules', module, 'type')
			# get status module
			status = self.config.get('modules', module, 'status')

			# check module type and start thread
			if (type == 'autoload' and status == 'enabled'):
				# get sleep time to check process
				sleeptime = self.config.get('config', 'autoload', 'check_interval')
				if (sleeptime == None or sleeptime == 0 or sleeptime == ''):
					sleeptime = 20 # default sleep time

				# start listening module messages
				thread.start_new_thread(self.startModule, (module, sleeptime))
				time.sleep(10)

	# ----------------------------------------------------------------------------------------

	'''
		thread to control module
	'''
	def startModule(self, module, sleeptime):
		while 1:
			try:
				# info about module
				info = self.config.get('modules', module)

				# normalize path separators
				fullpath = os.path.normpath( MySTBase.getAutoloadExtensionDir() + info['call'] )

				# verify if file exists
				if (fullpath == '' or not os.path.exists(fullpath)):
					raise Exception('Path not exists, please check and try again.')

				# command to execute
				cmd = [fullpath]

				# call user command
				o = subprocess.Popen(cmd,
									bufsize=-1,
									stdout=subprocess.PIPE,
									stdin=subprocess.PIPE,
									stderr=subprocess.PIPE,
									close_fds=True,
									universal_newlines=True)

				(stdout, stdin, stderr) = (o.stdout, o.stdin, o.stderr)

				# read the output
				output = stdout.read()

				stdout.close()
				stdin.close()
				stderr.close()

				MySTLog.log('Running autoload module: '+info['call'])
				
			except:
				output = MySTBase.getCommandNotFoundMessage()
				MySTLog.log('Ops! tried to execute non existing autoload module')

			# has message to send? broadcast now! (send to all online contacts)
			if (output != '' and output != None):
				self.broadcast(output)

			time.sleep( int(sleeptime) )

	# ----------------------------------------------------------------------------------------

	# Send message to all contacts
	def broadcast(self, message):
		# get the default local language and encoding
		try:
			language, encoding = locale.getdefaultlocale()
		except:
			language, encoding = ['en', 'utf-8']

		# decode the message
		message = message.decode(encoding)

		# get contacts
		contacts = self.user_handler.getContactList()
		# remove yourself from broadcast list
		contacts.remove(self.config.get('config', 'account', 'user'))
		
		if (len(contacts) > 0):
			for contact in contacts:
				self.jabber.send(xmpp.Message(contact, message))


	# ----------------------------------------------------------------------------------------
	