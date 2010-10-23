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

# TODO: get user rights
class MySTUserHandler:
	
	def __init__(self, config):
		self.escope = {}
		self.rights = {}
		self.environment = {}
		# Call method to get user rights
		self.loadUserRights()
		self.contact_handler = None
		self.config = config
	
	def userLoad(self):
		roster_contacts = self.contact_handler.getContacts()
		contacts = self.config.get('contacts')

		# Exclude contacts not enabled in roster
		for rct in roster_contacts:
			if not self.isUserEnabled(rct):
				self.contact_handler.removeContact(rct)

		# Add roster contacts into roster
		for uct in contacts:
			if self.isUserEnabled(uct):
				found = False
				for rct in roster_contacts:
					if (rct == uct):
						found = True
				if not found:
					self.contact_handler.addContact(uct)
	
	def setContactHandler(self, contact_handler):
		self.contact_handler = contact_handler
		self.userLoad()
		# TODO: Compare user configuration agains contacts. Remove contacts not present into contacts.ini and add new ones.

	def getContactHandler(self):
		return self.contact_handler

	def addContact(self,contact):
		self.contact_handler.addContact(contact)
		# TODO: Insert contact into config file
		
	def removeContact(self, contact):
		self.contact_handler.removeContact(contact)
		# TODO: Remove contact from config file
	
	def getContactList(self):
		try:
			return self.contact_handler.getContacts()
		except Exception:
			return []
	
	def isUserEnabled(self, user):
		try:
			status = self.config.get('contacts', user, 'status')
			if (status.lower().strip() == 'enabled'):
				return True
			else:
				return False
		except Exception:
			return False

	def setUserEscope(self, user, escope):
		self.escope[user] = escope
		return escope
	
	def getUserEscope(self, user):
		escope = ''
		try:
			escope = self.escope[user]
		except Exception:
			try:
				status = self.config.get('contacts', user, 'status')
				if (status.lower().strip() == 'enabled'):
					escope = self.setUserEscope(user, 'user')
			except Exception:
				pass
		return escope
	
	def escopeAuth(self, user, secret):
		result = False
		try:
			status       = self.config.get('contacts', user, 'status')
			super_secret = self.config.get('contacts', user, 'super-secret')
			if (status.lower().strip() == 'enabled'):
				if (secret.strip() == super_secret.strip()):
					result = True
		except Exception:
			pass
		return result
	
	def loadUserRights(self):
		return
	
	def getUserRights(self, user):
		return
	
	def userHasRights(self, user, command):
		return True
	
	def setUserEnvironment(self, user, var, val):
		try:
			self.environment[user][var] = val
		except Exception:
			self.environment[user] = {}
			self.environment[user][var] = val
		
	def getUserEnvironment(self, user, var=None):
		if (var == None):
			try:
				return self.environment[user]
			except Exception:
				return {}
		try:
			return self.environment[user][var]
		except Exception:
			return ''
	
	def saveUserEnvironment(self, user):
		pass
	
	def loadUserEnvironment(self, user):
		pass
	
	def cleanUserEnvironment(self, user):
		self.environment[user] = {}

