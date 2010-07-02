#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#       surfstick/user.py
#       
#       Copyright 2010 Raphael Michel <webmaster@raphaelmichel.de>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import re

import serial

from . import interface

class SurfstickUser(interface.SurfstickInterface):
	
	def __init__(self, port = '/dev/ttyUSB0', waitforechoing = True):
		interface.SurfstickInterface.__init__(self, port, waitforechoing)
	
	def pin_auth(self, pin = False):
		com1 = self.command_onelineanswer('AT+CPIN?')
		if com1.upper().endswith("READY"):
			return (True, "nothing to do")
		elif com1.upper().endswith("SIM PIN") and pin != False:
			com = self.command_onelineanswer('AT+CPIN="%s";' % str(pin))
			if com.upper() == 'OK':
				return (True,)
			else:
				if com.lower() == '+cme error: incorrect password':
					return (False,"incorrect")
				else:
					return (False,com)
		elif com1.upper().endswith("SIM PUK"):
			return (False, "puk")
		else:
			return (False, "unknown")
	
	def pin_needed(self):
		com1 = self.command_onelineanswer('AT+CPIN?')
		if com1.upper().strip().endswith("READY"):
			return (False, "nothing to do")
		elif com1.upper().strip().endswith("SIM PIN"):
			return (True,)
		elif com1.upper().strip().endswith("SIM PUK"):
			return (False, "puk")
		else:
			return (False, "unknown")
	
	def get_manufacturer(self):
		com = self.command_morelineanswer('AT+CGMI') # undocumented, wrong and dirty. but needed.
		com = self.command_morelineanswer('AT+CGMI?')
		return com

	def get_model(self):
		com = self.command_morelineanswer('AT+CGMM') # undocumented, wrong and dirty. but needed.
		com = self.command_morelineanswer('AT+CGMM?')
		return com

	def get_revision(self):
		com = self.command_morelineanswer('AT+CGMR') # undocumented, wrong and dirty. but needed.
		com = self.command_morelineanswer('AT+CGMR?')
		return com

	def get_serial(self):
		com = self.command_morelineanswer('AT+CGSN') # undocumented, wrong and dirty. but needed.
		com = self.command_morelineanswer('AT+CGSN?')
		return com

	def get_imsi(self):
		com = self.command_morelineanswer('AT+CIMI') # undocumented, wrong and dirty. but needed.
		com = self.command_morelineanswer('AT+CIMI?')
		return com

	def get_state(self):
		com = self.command_morelineanswer('AT+CREG')
		com = self.command_morelineanswer('AT+CREG?')
		search = re.search("\\+CREG: [0-9]+,([0-9]+)[^0-9]*", com[1])
		if search:
			return int(search.group(1))
		else:
			return 4
		return com

	def get_signal(self):
		com = self.command_morelineanswer('AT+CSQ')
		com = self.command_morelineanswer('AT+CSQ?')
		search = re.search("\\+CSQ: ([0-9]+),", com[1])
		if search:
			return int(search.group(1))
		else:
			return 99

