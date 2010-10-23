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

import ConfigParser, string, sys

class MySTConfig:

	def __init__(self):
		self._config = {}
		# Load configuration files
		self._config['modules']  = self.loadConfigFile(sys.path[0]+'/etc/modules.ini')
		self._config['config']   = self.loadConfigFile(sys.path[0]+'/etc/config.ini')
		self._config['contacts'] = self.loadConfigFile(sys.path[0]+'/etc/contacts.ini')

	# Get a information from configuration file
	def get(self, config='', section='', key=''):
		result = None
		try:
			if (config != '' and section == '' and key == ''):
				result = self._config[config]
			elif (config != '' and section != '' and key == ''):
				result = self._config[config][section]
			elif (config != '' and section != '' and key != ''):
				result = self._config[config][section][key]
		except:
			result = None
		return result

	# Load configuration file
	def loadConfigFile(self, file):
		config = {}
		cp = ConfigParser.ConfigParser()
		cp.read(file)
		for sec in cp.sections():
			sec = sec.replace(' ', '')
			sec = sec.lower()
			config[sec] = {}
			for opt in cp.options(sec):
				opt = opt.replace(' ', '')
				opt = opt.lower()
				#config[sec][opt.lower()] = cp.get(sec, opt).replace(' ', '').lower()
				config[sec][opt.lower()] = cp.get(sec, opt)
		return config

	# Save configuration file
	def saveConfigFile(self, filename, config):
		cp = ConfigParser.ConfigParser()
		sections = set([k.split('.')[0] for k in config.keys()])
		map(cp.add_section, sections)
		for k, v in config.items():
			s, o = k.split('.')
			cp.set(s, o, v)
		cp.write(open(filename, 'w'))

