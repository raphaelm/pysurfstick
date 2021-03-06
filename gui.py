#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       gui.py
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

# Imports
import sys
from optparse import OptionParser

import gtk

import surfstick.user

# Easy-to-use GTK dialogs
def err(text, sectext = None):
	if sectext is None:
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR
					, message_format=text
					, buttons=gtk.BUTTONS_OK)
	else:
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR
					, message_format=text
					, buttons=gtk.BUTTONS_OK)
		error_dlg.format_secondary_text(sectext)
	error_dlg.run()
	error_dlg.destroy()

def warning(text, sectext = None):
	if sectext is None:
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_WARNING
					, message_format=text
					, buttons=gtk.BUTTONS_OK)
	else:
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_WARNING
					, message_format=text
					, buttons=gtk.BUTTONS_OK)
		error_dlg.format_secondary_text(sectext)
	error_dlg.run()
	error_dlg.destroy()

def info(text, sectext = None):
	if sectext is None:
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO
					, message_format=text
					, buttons=gtk.BUTTONS_OK)
	else:
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO
					, message_format=text
					, buttons=gtk.BUTTONS_OK)
		error_dlg.format_secondary_text(sectext)
	error_dlg.run()
	error_dlg.destroy()
	
def confirm(text, sectext = None):
	if sectext is None:
		dlg = gtk.MessageDialog(message_format=text,
					flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					type=gtk.MESSAGE_QUESTION)
	else:
		dlg = gtk.MessageDialog(message_format=text,
					flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					type=gtk.MESSAGE_QUESTION)
		dlg.format_secondary_text(sectext)
	dlg.add_button(gtk.STOCK_NO, 1)
	dlg.add_button(gtk.STOCK_YES, 3)
	run = dlg.run()
	if run == 3:
		ret = True
	else:
		ret = False
	dlg.destroy()
	return ret
	
# A ListBox widget for PyGTK
class ListBox(gtk.TreeView):
	"""s = gtk.ListStore(str)
	ls.append(["a"])
	self.history_listbox = ListBox("Datum", ls)
	self.history_listbox.fix_width(200)
	self.history_listbox.show()"""
		
	def __init__(self, title, ls):
		gtk.TreeView.__init__(self, ls)
		
		self.col = gtk.TreeViewColumn(title)
		self.cell = gtk.CellRendererText()
		self.col.pack_start(self.cell)
		self.col.add_attribute(self.cell, 'text', 0)
		self.col.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		self.append_column(self.col)
	
	def fix_width(self, width):
		self.col.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		self.col.set_fixed_width(width)
		
# Our MainWindow
class MainWindow(gtk.Window):
	
	def ev_leave(self, this):
		self.destroy()
	
	def about_dialog(self, this):
		d = gtk.AboutDialog()
		d.set_authors(['Raphael Michel <webmaster@raphaelmichel.de>'])
		d.set_comments("""o2 Surfstick und verwandte Geräte auch unter Linux benutzen""")
		d.set_copyright('Copyright 2010 Raphael Michel')
		try:
			d.set_license(open('/usr/share/common-licenses/GPL-2', 'r').read())
		except:
			pass
		#d.logo = 
		d.set_name('Surfstick GUI')
		d.set_version('0.0.0-dev')
		d.set_website('http://github.com/raphaelm/pysurfstick')
		d.set_website_label('pySurfstick auf github')
		res = d.run()
		d.destroy()
	
	def __init__(self):
		gtk.Window.__init__(self)
		
		# Main Window
		self.set_geometry_hints(self, 650, 400, 1024, 600, 650, 400, 1, 1)
		
		# Big tab environment area as main element
		self.main_notebook = gtk.Notebook()
		self.main_notebook.show()
		
		self.main_notebook.append_page(gtk.Label("Test"), gtk.Label("Informationen"))
		self.main_notebook.append_page(gtk.Label("Test"), gtk.Label("SMS"))
		self.main_notebook.append_page(gtk.Label("Test"), gtk.Label("Prepaid-Tarife"))
		self.main_notebook.append_page(gtk.Label("Test"), gtk.Label("SIM-Telefonbuch"))
		
		# menubar top
		self.mainmenu = gtk.MenuBar()
		
		# menubar item program
		menuitem_program = gtk.MenuItem("Programm")
		submenu_program = gtk.Menu()
		submenuitem_exit = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
		submenuitem_exit.connect('activate', self.ev_leave)
		submenu_program.add(submenuitem_exit)
		menuitem_program.set_submenu(submenu_program)
		
		# menubar item help
		menuitem_help = gtk.MenuItem("Hilfe")
		submenu_help = gtk.Menu()
		submenuitem_about = gtk.ImageMenuItem(stock_id=gtk.STOCK_ABOUT)
		submenuitem_about.connect('activate', self.about_dialog)
		submenu_help.add(submenuitem_about)
		menuitem_help.set_submenu(submenu_help)
		
		# menubar items
		self.mainmenu.add(menuitem_program)
		self.mainmenu.add(menuitem_help)
		self.mainmenu.show()
		
		# statusbar
		self.statusbar = gtk.Statusbar()
		self.statusbar.push(0, 'Hallo!')
		
		# vbox to combine menubar and notebook
		main_vbox = gtk.VBox()
		main_vbox.pack_end(self.statusbar, False, False)
		main_vbox.pack_end(self.main_notebook)
		main_vbox.pack_end(self.mainmenu, False, False)
		main_vbox.show()
		
		self.add(main_vbox)
		
# Main class
class SurfstickGUI:
	def startconnection(self):
		try:
			self.s = surfstick.user.SurfstickUser('/dev/ttyUSB0')
			return (self.s.command_onelineanswer("AT").upper() == 'OK')
		except surfstick.interface.SurfstickInterfaceError:
			return False
			
	def pinauth(self):
		dlg = gtk.Dialog("PIN-Eingabe", None,
					gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
					gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		entry = gtk.Entry()
		entry.set_visibility(False)
		hbox = gtk.HBox()
		hbox.pack_start(gtk.Label("PIN-Code:"), False, 5, 5)
		hbox.pack_end(entry)
		dlg.vbox.pack_end(hbox, True, True, 0)
		dlg.show_all()
		
		ret = dlg.run()
		if ret == -2 or ret == -4:
			sys.exit(0)
		elif ret == -3:
			try:
				pin = entry.get_text().strip()[0:4]
				test = int(pin)
			except:
				dlg.destroy()
				err("Es wird ein vierstelliger Zahlencode erwartet!")
				self.pinauth()
			else:
				if len(pin) == 4:
					if self.s.pin_auth(pin):
						return True
					else:
						dlg.destroy()
						err("Die PIN wurde von der Karte nicht akzeptiert", "Entweder war die PIN falsch oder die Karte ist gesperrt. In letzterem Fall kann dir diese Software leider nicht weiterhelfen. Du musst dann die SIM-Karte beispielsweise in ein Handy einlegen und deine PUK eingeben.)")
						self.pinauth()
				else:
					dlg.destroy()
					err("Es wird ein vierstelliger Zahlencode erwartet!")
					self.pinauth()
	
	def ev_leave(self, this):
		gtk.main_quit()
		
	def __init__(self, port = '/dev/ttyUSB0'):
		# Class variables
		self.port = port
		
		# test connection
		if not self.startconnection():
			err('Verbindung zum Gerät auf %s fehlgeschlagen!' % port, """Bitte überprüfe, ob dein UMTS-Modem korrekt angeschlossen ist. Wenn du das Programm mit diesem Modem zum ersten Mal nutzt, prüfe weiterhin, ob das Modem als mit dieser Software kompatibel bekannt ist oder nicht.
Ein anderer Port kann über den Kommandozeilenparameter -p spezifiert werden.""")
			sys.exit(0)
		
		self.pinauth()
			
		
		# main window
		self.main_win = MainWindow()
		self.main_win.show_all()
		#self.main_win.set_icon_from_file("img/logo.png")
		self.main_win.set_title("Surfstick GUI")
		self.main_win.connect('destroy', self.ev_leave)
	
	def __del__(self):
		try:
			self.s.close()
		except:
			pass

# parameters, initialization
if __name__ == '__main__':
	
	parser = OptionParser(usage="Usage: %prog [options]")
	parser.add_option("-p", "--port", dest="port", default="/dev/ttyUSB0",
					  help="serial port to use (default: /dev/ttyUSB0)", metavar="PORT")
	(options, args) = parser.parse_args()
	
	gui = SurfstickGUI(options.port)
	try:
		gtk.main()
	except KeyboardInterrupt:
		try:
			gui.exit()
		finally:
			sys.exit(0)
