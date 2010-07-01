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
import gtk

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
		
class MainWindow(gtk.Window):
	
	def ev_leave(self, this):
		gtk.main_quit()
	
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
		
		self.set_geometry_hints(self, 650, 400, 1024, 600, 650, 400, 1, 1)
		self.connect('destroy', self.ev_leave)
		
		main_notebook = gtk.Notebook()
		main_notebook.show()
		
		main_notebook.append_page(gtk.Label("Test"), gtk.Label("Informationen"))
		main_notebook.append_page(gtk.Label("Test"), gtk.Label("SMS"))
		main_notebook.append_page(gtk.Label("Test"), gtk.Label("Prepaid-Tarife"))
		
		
		self.mainmenu = gtk.MenuBar()
		
		menuitem_program = gtk.MenuItem("Programm")
		submenu_program = gtk.Menu()
		submenuitem_exit = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
		submenuitem_exit.connect('activate', self.ev_leave)
		submenu_program.add(submenuitem_exit)
		menuitem_program.set_submenu(submenu_program)
		
		menuitem_help = gtk.MenuItem("Hilfe")
		submenu_help = gtk.Menu()
		submenuitem_about = gtk.ImageMenuItem(stock_id=gtk.STOCK_ABOUT)
		submenuitem_about.connect('activate', self.about_dialog)
		submenu_help.add(submenuitem_about)
		menuitem_help.set_submenu(submenu_help)
		
		self.mainmenu.add(menuitem_program)
		self.mainmenu.add(menuitem_help)
		self.mainmenu.show()
		
		main_vbox = gtk.VBox()
		main_vbox.pack_end(main_notebook)
		main_vbox.pack_end(self.mainmenu, False, False)
		main_vbox.show()
		
		self.add(main_vbox)
		
class SurfstickGUI:
	def __init__(self):
		main_win = MainWindow()
		main_win.show_all()
		#main_win.set_icon_from_file("img/logo.png")
		main_win.set_title("Surfstick GUI")

if __name__ == '__main__':
	gui = SurfstickGUI()
	try:
		gtk.main()
	except KeyboardInterrupt:
		try:
			gui.exit()
		finally:
			sys.exit(0)
