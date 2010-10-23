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

class MySTFormatReply:

	'''
		TODO:
		Implements other response formats as: XML, JSON, CSV
	'''
	def getOutput(format, reply):
		output = ''
		format = 'human'
		if (reply == None):
			return ''
		
		# Human Readable Format Reply
		if (format == 'human-readable' or format == 'human'):
			if (reply.getCode() != 0):
				output = 'Error: '
			output = reply.getMessage()
		
		return output
	getOutput = staticmethod(getOutput)

