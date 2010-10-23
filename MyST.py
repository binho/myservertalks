#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
	MyServerTalks! Project Beta | myservertalks.com / myservertalks.net

	Andrei de Oliveira Mosman
	mosman [at] myservertalks.net

	Cleber Willian dos Santos
	binho [at] myservertalks.net

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

#import os
import sys
from MySTBase import *
from MySTLog import *
from MySTConfig import *
from MySTUserHandler import *
from MySTConnection import *
from MySTModuleManager import *

class MyST:

	def __init__(self):
		self.config = MySTConfig()

		if not self.config.get('config', 'account', 'user'):
			print 'MyServerTalks is not configured. Try to setup config.ini'
			sys.exit(1)

		# Get user and pass from MyST jabber user
		self.user     = self.config.get('config', 'account', 'user')
		self.password = self.config.get('config', 'account', 'pass')
		
		self.user_handler = MySTUserHandler(self.config)
		
		print 'MyServerTalks! '+MySTBase.getVersion()+' running...\n'
		MySTLog.log('MyServerTalks! '+MySTBase.getVersion()+' running...')

	# Connect MyST
	def connect(self):
		self.conn = MySTConnection(MySTModuleManager(self.config, self.user_handler))
		self.conn.connect(self.user, self.password)

	# Process informations and check connection state
	def looping(self):
		self.conn.loop()


if __name__ == '__main__':
	myst = MyST()
	myst.connect()
	myst.looping()
