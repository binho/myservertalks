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
class MySTInstruct:

	def __init__(self, command, parameters=[], contact='', escope=''):
		self.command    = command
		self.parameters = parameters
		self.contact    = contact
		self.escope     = escope

	'''
		result format send to script
	'''
	def __str__(self):
		#return (" '" + self.contact + "' '" + self.escope + "' " + self.command + " '" + ";".join(self.parameters) + "'").strip()
		return ( self.contact + ' ' + self.escope + ' ' + self.command + ' ' + ';'.join(self.parameters) )

	def setContact(self, contact):
		self.contact = contact

	def setEscope(self, escope):
		self.escope = escope

	def getCommand(self):
		return self.command

	def getParameters(self):
		return self.parameters

	def getContact(self):
		return self.contact

	def getEscope(self):
		return self.escope
