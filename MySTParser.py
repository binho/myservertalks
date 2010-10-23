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
from MySTInstruct import *

class MySTParser:

	def __init__(self):
		pass

	def parse(text):
		# text to parse
		if not text or text == None:
			return None
		text = text.strip()

		# pointer
		idx = 0

		# result
		command = ''
		parameters = []

		# flags
		gotCommand   = False
		gotLineBreak = False
		gotEndOfLine = False
		BeginOfWord  = True
		QuoteOpenned = ''

		# buffer
		buffer = ''

		for c in text:
			if (c == "\n"):
				gotLineBreak = True
				if not gotCommand:
					command = buffer
				else:
					parameters.append(buffer)
				buffer = ''
				continue

			if (c == " "):
				if not BeginOfWord:
					if not QuoteOpenned:
						if not gotCommand:
							command = buffer
							gotCommand = True
						else:
							parameters.append(buffer)
						BeginOfWord = True
						buffer = ''
					else:
						buffer = buffer + c
				continue

			if (c == "'" or c == '"'):
				if (BeginOfWord and not QuoteOpenned):
					QuoteOpenned = c
				else:
					if (QuoteOpenned == c):
						QuoteOpenned = ''
						parameters.append(buffer)
						buffer = ''
						BeginOfWord = True
					else:
						buffer = buffer + c
				continue
			buffer = buffer + c
			BeginOfWord = False

		if buffer:
			if not gotCommand:
				command = buffer
			else:
				parameters.append(buffer)
				idx = idx + 1

		# return the instruct
		return MySTInstruct(command,parameters)
	parse = staticmethod(parse)
