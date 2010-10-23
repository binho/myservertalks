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
class MySTReply:

	def __init__(self, code=0, message=''):
		self.code = 0
		self.message = message
		pass
	
	def getCode(self):
		return self.code
	
	def getMessage(self):
		return self.message
	
	def setCode(self, code):
		self.code = code
	
	def setMessage(self, message):
		self.message = message
	
	def __str__(self):
		return ("%d-" % self.code) + self.message
	
