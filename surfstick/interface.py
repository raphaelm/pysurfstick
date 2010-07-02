#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#       surfstick/interface.py
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

class SurfstickInterfaceError(Exception):
	pass

class SurfstickInterface:
	def __init__(self, port = '/dev/ttyUSB0', waitforechoing = True):
		self.crlf = "\r\n"
		try:
			self.serial = serial.Serial(port)
			self.serial.open()
		except serial.serialutil.SerialException:
			self.connected = False
		else:
			self.connected = True
		self.waitforechoing = waitforechoing
		
	def close(self):
		if not self.connected:
			raise SurfstickInterfaceError("Not connected")
			return False
		self.serial.close()
	
	def command_onelineanswer(self, cmd):
		if not self.connected:
			raise SurfstickInterfaceError("Not connected")
			return False
		cmd = cmd.strip()
		self.serial.write(cmd+self.crlf)
		
		incoming = []
		echoed = False
		while True:
			new = self.serial.read(1)
			incoming.append(new)
			if incoming[-2:len(incoming)] == list(self.crlf) and self.waitforechoing and not echoed:
				incoming = []
				echoed = True
			elif incoming[-2:len(incoming)] == list(self.crlf):
				result = "".join(incoming).strip()
				return result
				break
	
	def command_morelineanswer(self, cmd):
		if not self.connected:
			raise SurfstickInterfaceError("Not connected")
			return False
		cmd = cmd.strip()
		self.serial.write(cmd+self.crlf)
		
		incoming = []
		echoed = False
		while True:
			new = self.serial.read(1)
			incoming.append(new)
			if incoming[-2:len(incoming)] == list(self.crlf) and self.waitforechoing and not echoed:
				incoming = []
				echoed = True
			else incoming[-2:len(incoming)] == list(self.crlf):
				result = "".join(incoming).strip()
				if result.endswith("OK"):
					return (True, result[0:len(result)-2].strip())
					break
				else:
					if result.endswith("ERROR") or result.strip().startswith("+CME ERROR"):
						return (False, result)
						break
