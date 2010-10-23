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
from MySTBase import *
from MySTModuleCore import *
from MySTModuleExternal import *
from MySTModuleInterface import *
from MySTModuleAutoload import *
from MySTReply import *

class MySTModuleManager:

	def __init__(self, config, user_handler):

		# Module cache
		self._MODULECOMM = {}
		self._MODULECALL = {}
		self._MODULESCOP = {}

		self.user_handler = user_handler
		self.config       = config

		# Get the modules list
		self.modules = self.config.get('modules')

		# Handlers
		self.core      = MySTModuleCore(self.config, self.user_handler)
		self.external  = MySTModuleExternal(self.config)
		self.interface = MySTModuleInterface()

		# mod_core is to cache core reserved functions (that is allways present and cannot be overriden)
		self._MODULECORE = self.core.getCoreFunctions()

		# load config
		self.loadConfigInfo()

	# Get user
	def getUserHandler(self):
		return self.user_handler

	# Get user escope
	def getEscope(self, command):
		try:
			return self._MODULESCOP[command]
		except Exception:
			return ''

	# Get type of command
	def getType(self, command):
		try:
			return self._MODULECOMM[command]
		except Exception:
			return ''

	# Get call to command
	def getCall(self, command):
		try:
			return self._MODULECALL[command]
		except Exception:
			return ''

	def execute(self, instruct):
		commandtype = self.getType(instruct.getCommand())
		escopes     = self.getEscope(instruct.getCommand())

		# User enabled validation
		if not self.user_handler.isUserEnabled(instruct.getContact()):
			return MySTReply(MySTBase.getErrorCode(), 'Error. User not enabled.')

		# Escope validatons
		escope = self.user_handler.getUserEscope(instruct.getContact()).lower()
		if escope in escopes:
			if (commandtype == 'core' or commandtype == 'internal'):
				return self.core.execute(instruct)
			elif (commandtype == 'external'):
				return self.external.execute(instruct)
			elif (commandtype == 'interface'):
				return self.interface.execute(instruct)

		return MySTReply(MySTBase.getErrorCode(), MySTBase.getCommandNotFoundMessage())


	def loadConfigInfo(self):
		# cache core functions
		for module in self._MODULECORE:
			self._MODULECOMM[module] = 'core'
			self._MODULESCOP[module] = self._MODULECORE[module]

		# walk for modules list
		for module in self.modules:
			if not self._MODULECORE.has_key(module):
				# check if module list has status key
				if self.modules[module].has_key('status'):
					# check if module is enabled
					if (self.modules[module]['status'].lower() == 'enabled'):
						# check module type
						if self.modules[module].has_key('type'):
							# check module call
							if self.modules[module].has_key('call'):
								if (self.modules[module]['type'].lower() == 'external'):
									self._MODULECALL[module] = self.modules[module]['call'].lower()
								else:
									self._MODULECALL[module] = ''
								# add module type to module list
								self._MODULECOMM[module] = self.modules[module]['type'].lower()
								# check module escope
								if self.modules[module].has_key('escope'):
									escopenames = self.modules[module]['escope'].replace(' ', '')
									escopelist  = escopenames.split(',')
									self._MODULESCOP[module] = escopelist
