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

import os, sys, platform
from MySTBase import *
from MySTModule import *
from MySTReply import *

''' Extends MySTModule '''

class MySTModuleCore(MySTModule):

	def __init__(self, config, user_handler):
		self.config = config
		self.user_handler = user_handler

	# Returns core functions
	def getCoreFunctions(self):
		return {'env':['user', 'super'], 'escope':['user', 'super'], 'contacts':['super']}

	# Execute a internal function
	def execute(self, instruct):

		result_code = 0
		result_msg  = 'OK'

		# Get the called command
		command    = instruct.getCommand()
		# Get the parameters from current called command
		parameters = instruct.getParameters()

		# --------------------------------------------------------------------------------------------

		# Help list all commands for escope
		if (command == 'help'):
			# User escope
			escope = self.user_handler.getUserEscope(instruct.getContact()).lower()
			# Module list
			modules = self.config.get('modules')
			# commands for this user
			commands = []
			for module in modules:
				values = self.config.get('modules', module)
				# status of module
				status = values['status'].replace(' ', '')
				if (status == 'disabled'): continue
				# escopes of this module
				escopes = values['escope'].replace(' ', '')
				escopes = escopes.split(',')
				if escope in escopes:
					commands.append(module)
			if (len(commands) > 0):
				result_code = MySTBase.getSucessCode()
				result_msg = 'Commands for you: ' + ', '.join(commands)
			else:
				result_code = MySTBase.getUnavaibleCode()
				result_msg = 'No commands for you. Sorry.'

		# --------------------------------------------------------------------------------------------

		# Information about MyST
		elif (command == 'about'):

			info  = "MyServerTalks! v%s\n" % MySTBase.getVersion()
			info += "Url: www.myservertalks.com\n"
			info += "PID: %s\n" % os.getpid()
			info += "Operational System: %s\n" % ' '.join(platform.uname())
			info += "Local Date/Time: %s\n" % MySTBase.getDateTime()

			result_code = MySTBase.getSucessCode()
			result_msg  = info

		# --------------------------------------------------------------------------------------------

		# User escope
		elif (command == 'escope'):
			escope = ''
			key = ''
			try:
				escope = parameters[0]
				key = parameters[1].strip()
			except Exception:
				pass

			escope = escope.strip()
			escope = escope.lower()

			if (escope == ''):
				result_code = MySTBase.getSucessCode()
				result_msg  = 'Your session escope is ' + self.user_handler.getUserEscope(instruct.getContact()).upper()
			else:
				if (escope == 'super'):
					if (key == ''):
						result_code = MySTBase.getErrorCode()
						result_msg  = 'You must to specify you super key'
					else:
						# Validate the key (secret)
						if not self.user_handler.escopeAuth(instruct.getContact(), key):
							result_code = MySTBase.getErrorCode()
							result_msg  = 'Incorret password for SUPER escope'

				if escope in ('user', 'super'):
					if (result_code == MySTBase.getSucessCode()):
						self.user_handler.setUserEscope(instruct.getContact(), escope)
						result_msg = 'Escope changed to ' + escope.upper()
					else:
						result_msg = 'Error while trying to change your user escope.'
				else:
					result_code = MySTBase.getErrorCode()
					result_msg  = 'Error. You are trying to scale to a invalid escope.'


		# --------------------------------------------------------------------------------------------

		# User environment functions
		elif (command == 'env'):
			cmd = ''
			var = ''
			val = ''
			try:
				cmd = parameters[0]
				var = parameters[1]
				val = parameters[2]
			except Exception:
				pass

			if (cmd == 'set'):
				if (var and val):
					self.user_handler.setUserEnvironment(instruct.getContact(), var, val)
				else:
					result_code = MySTBase.getErrorCode()
					result_msg  = 'Env set must to receive both variable and value'

			elif (cmd == 'get'):
				if var:
					val = self.user_handler.getUserEnvironment(instruct.getContact(), var)
					result_code = MySTBase.getSucessCode()
					result_msg  = val
				else:
					result_code = MySTBase.getErrorCode()
					result_msg  = 'Env get must to specify varname'

			elif (cmd == 'show'):
				env = self.user_handler.getUserEnvironment(instruct.getContact())
				result = ''
				for v in env:
					info = v + ' = "' + env[v] + '"'
					result = result + info + "\n"

				if (result == ''):
					result_code = MySTBase.getUnavaibleCode()
					result_msg  = 'Environment empty'
				else:
					result_code = MySTBase.getSucessCode()
					result_msg  = result

		# --------------------------------------------------------------------------------------------

		# Contact management functions
		# TODO:
		# - more details on contact show
		# - contacts view user (profile view + session information)
		# - contact send [user|all]

		elif (command == 'contacts'):
			cmd     = ''
			contact = ''
			try:
				cmd     = parameters[0]
				contact = parameters[1]
			except Exception:
				pass

			msg_must_especify = 'You must specify the contact to '

			if (cmd == 'show'):
				contacts = self.user_handler.getContactList()
				if (contacts.count == 0):
					result_msg  = 'There are no contacts in this server roster'
					result_code = MySTBase.getErrorCode()
				else:
					result_code = MySTBase.getSucessCode()
					result_msg  = "\n".join(contacts)

			elif (cmd == 'add'):
				if not contact:
					result_code = MySTBase.getErrorCode()
					result_msg  = msg_must_especify + cmd
				else:
					self.user_handler.addContact(contact)
					result_code = MySTBase.getSucessCode()
					result_msg  = 'User added with sucess'

			elif (cmd == 'remove'):
				if not contact:
					result_msg  = msg_must_especify + cmd
					result_code = MySTBase.getErrorCode()
				else:
					self.user_handler.removeContact(contact)
					result_code = MySTBase.getSucessCode()
					result_msg  = 'User removed with sucess'

			else:
				result_code = MySTBase.getErrorCode()
				result_msg  = 'Unknown contacts command'

		# --------------------------------------------------------------------------------------------

		elif (command == 'pwd'):
			result_code = MySTBase.getSucessCode()
			current_path = self.user_handler.getUserEnvironment(instruct.getContact(), 'PWD')
			if (current_path != ''):
				result_msg = current_path
			else:
				result_msg = sys.path[0]

		# --------------------------------------------------------------------------------------------

		elif (command == 'chdir'):
			dir = ''
			try:
				dir = parameters[0]
			except Exception:
				pass
			# Return current directory
			if (dir == ''):
				result_code = MySTBase.getSucessCode()
				result_msg  = self.user_handler.getUserEnvironment(instruct.getContact(), 'PWD')
			else:
				# Merge directory with older directory
				# dir[0] is the first char of 'dir'
				if (dir[0] != '/'):
					dir = self.user_handler.getUserEnvironment(instruct.getContact(), 'PWD') + '/' + dir

				dir = os.path.normpath(dir).replace('\\\\', '\\')

				if os.path.isdir(dir):
					self.user_handler.setUserEnvironment(instruct.getContact(), 'PWD', os.path.normpath(dir))
					result_code = MySTBase.getSucessCode()
					result_msg  = os.path.normpath(dir)
				else:
					result_code = MySTBase.getErrorCode()
					result_msg  = 'No such directory'

		# --------------------------------------------------------------------------------------------

		# List current directory files
		elif (command == 'list'):
			target = ''
			try:
				target = parameters[0]
			except Exception:
				pass
			if (target == ''):
				if (self.user_handler.getUserEnvironment(instruct.getContact(), 'PWD') == ''):
					target = '/'
				else:
					target = self.user_handler.getUserEnvironment(instruct.getContact(), 'PWD')

			if not os.path.exists(target):
				result_msg  = 'No such file or directory'
				result_code = MySTBase.getErrorCode()
			else:
				result_code = MySTBase.getSucessCode()
				if os.path.isdir(target):
					# list of dirs
					dirs = os.listdir(target)
					result = []
					for dir in dirs:
						d = dir
						# full path to dir
						fullpath = os.path.normpath(target + '/' + dir).replace('\\\\', '\\')
						# Change directory apresentation
						if os.path.isdir(fullpath):
							d = "[" + dir + "]"

						result.append(d)

					result.sort()
					result_msg = "\n".join(result)
				else:
					result_msg = target

		return MySTReply(result_code, result_msg)

