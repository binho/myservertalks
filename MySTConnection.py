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
from idlelib.IOBinding import encoding
import xmpp
import os
import sys
import locale
from MySTParser import *
from MySTContactManager import *
from MySTFormatReply import *
from MySTLog import *
from MySTModuleAutoload import *

class MySTConnection:

	def __init__(self, module_manager):
		self.user = ''
		self.password = ''
		self.server = ''
		self.parser = MySTParser()
		self.module_manager = module_manager
		self.roster = None

	# Connect to jabber
	def connect(self, user, password):
		# set the user and pass for atributes
		self.user     = user
		self.password = password

		self.jid = xmpp.JID(self.user)
		self.user, self.server, self.password = self.jid.getNode(), self.jid.getDomain(), self.password

		# Enable all debug flags
		flags = ['nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth', 'bind', 'socket', 'CONNECTproxy', 'TLS', 'roster', 'browser', 'ibb']
		self.jabber = xmpp.Client(self.server, debug=[]) # to enable debug replace debug=[] with debug=flags

		self.config = MySTConfig()
		# try to get information about different server to connect
		host = self.config.get('config', 'server', 'host')
		port = self.config.get('config', 'server', 'port')

		# info about server (tuple)
		server = ()
		if (host != '' and port != ''): server = (host, int(port))

		# try to get information proxy
		proxy_host = self.config.get('config', 'proxy', 'host')
		proxy_port = self.config.get('config', 'proxy', 'port')
		proxy_user = self.config.get('config', 'proxy', 'user')
		proxy_pass = self.config.get('config', 'proxy', 'pass')

		# info about proxy (dict)
		proxy = {}
		if (proxy_host != ''): proxy['host'] = proxy_host
		if (proxy_port != ''): proxy['port'] = int(proxy_port)
		if (proxy_user != ''): proxy['user'] = proxy_user
		if (proxy_pass != ''): proxy['password'] = proxy_pass

		# try connect
		if (len(server) > 0 or len(proxy) > 0):
			# use a different server or a proxy to connect
			self.conn = self.jabber.connect(server, proxy)
		else:
			self.conn = self.jabber.connect()
	
		# Check the connection
		if not self.conn:
			print 'Unable to connect to server %s' % self.server
			sys.exit(1)

		# Check TLS connection
		if (self.conn != 'tls'):
			print 'Warning: Unable to estabilish secure connection, TLS failed.'

		self.auth = self.jabber.auth(self.user, self.password, 'myservertalks')

		# Check if user is authenticated
		if not self.auth:
			print 'Unable to authorize on %s - check login/password.' % self.server
			sys.exit(1)

		# Check if SASL it's possible
		if (self.auth != 'sasl'):
			print 'Warning: Unable to perform SASL auth os %s. Old authentication method used.' % self.server

		self.jabber.RegisterHandler('message', self.messageHandler)
		self.jabber.RegisterHandler('presence', self.presenceHandler)
		self.jabber.sendInitPresence()

		self.roster = self.jabber.getRoster()

		self.module_manager.getUserHandler().setContactHandler(MySTContactManager(self.roster))
		
		self.user_handler = self.module_manager.getUserHandler()
		
		# Autoload modules
		MySTModuleAutoload(self.config, self.jabber, self.user_handler)

	# Disconnect from jabber
	def disconnect(self):
		self.jabber.disconnect()

	def presenceHandler(self, conn, presence):
		source = presence.getFrom()
		try:
			contact, resource = source.__str__().split('/')
		except Exception:
			contact, resource = source.__str__(), ''

		# When get user status "unavailable" the system cleans user environment
		if (presence.getType() == 'unavailable'):
			self.module_manager.getUserHandler().cleanUserEnvironment(contact.lower())
			return

		if presence.getErrorCode():
			MySTLog.log("Error in presence with exit code: "+presence.getErrorCode())
			return
		
		show   = ''
		status = ''
		escope = self.module_manager.getUserHandler().getUserEscope(contact).lower()
		if (escope == 'user'):
			custom_message = self.config.get('config', 'status', 'dnd')
			show = 'dnd'
			if (custom_message != None and custom_message != ''):
				status = custom_message.strip()
			else:
				status = 'Do not disturb'
		elif (escope == 'super'):
			custom_message = self.config.get('config', 'status', 'avail')
			show = 'avail'
			if (custom_message != None and custom_message != ''):
				status = custom_message.strip()
			else:
				status = 'Available'
		else:
			return

		new_presence = xmpp.Presence(to=source, show=show, priority=5, status=status)
		self.jabber.send(new_presence)


	# Send a message
	def messageSend(self, to, message):
		# try to get the default local language and encoding
		try:
			language, encoding = locale.getdefaultlocale()
		except:
			language, encoding = ['en', 'utf-8']
		# decode the message
		message = message.decode(encoding)
		# send the message
		self.jabber.send(xmpp.Message(to, message))



	# Message handler for received messages
	def messageHandler(self, conn, message):
		print message
		text = message.getBody()
		instruct = MySTParser.parse(text)
		
		print 'message: ', text
		print 'instruct: ', instruct

		if (instruct == None): return False

		# Get the contact sending the message
		from_contact = message.getFrom().__str__()
		if (from_contact.find('/') >= 0):
			contact, resource = message.getFrom().__str__().split('/')
		else:
			contact, resource = from_contact, ''
			
		print 'contact: ', contact, 'resource: ', resource

		# Set contact
		instruct.setContact(contact.lower())

		# User escope
		escope = self.module_manager.getUserHandler().getUserEscope(contact.lower())
		escope = escope.lower()

		# Set the escope
		instruct.setEscope(escope)

		# Reply to contact
		# VERY IMPORTANT
		reply = self.module_manager.execute(instruct)

		# Format to send the reply
		output_format = self.module_manager.getUserHandler().getUserEnvironment('display')

		# Get the output format
		output = MySTFormatReply.getOutput(output_format, reply)
		if (output.strip() != ''):
			presence = xmpp.Presence()
			presence.setFrom(message.getFrom())
			self.presenceHandler(conn, presence)

			# Send the reply
			self.messageSend(message.getFrom(), output)


	# Loop for process and connection status check
	def loop(self):
		while True:
			try:
				# Check if is connected, if not try reconnect
				if not (self.jabber.isConnected()):
					print "Disconnected... Trying to reconnect now...\n"
					self.jabber.reconnectAndReauth()

				self.jabber.Process(1)
			except KeyboardInterrupt:
				break

