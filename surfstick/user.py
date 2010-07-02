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
import serial
from . import interface

class SurfstickUser(interface.SurfstickInterface):
	
	def __init__(self, port = '/dev/ttyUSB0', waitforechoing = True):
		interface.SurfstickInterface.__init__(self, port, waitforechoing)
	
	def pin_auth(self, pin):
		com = self.command_onelineanswer('AT+CPIN="%s";' % str(pin))
		if com.upper() == 'OK':
			return (True,)
		else:
			if com.lower() == '+cme error: incorrect password':
				return (False,"incorrect")
			else:
				return (False,"other")
		
