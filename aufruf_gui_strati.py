# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from progr_strati import programmstart
from fill_tables import init_tabs, result_tabs, impStrati, absData, orderAbs
#from dateipfade import *
from gui_windows import app, mainWin
from tab_create import initial_db

def steuerung_progr():
	# Create tables:
	initial_db()
	# Create gui-tables:
	impStrati.gui_tab_to_db()
	absData.gui_tab_to_db()
	orderAbs.gui_tab_to_db()
	programmstart()
	result_tabs()

mainWin.show()
init_tabs()
# it's a trick because it is impossible to create an empty tabWidget in QtCreator:
mainWin.tabWidget.removeTab(0)

mainWin.button_start.clicked.connect(lambda: steuerung_progr())

# Wenn abbrechen dann Fenster schließen, wenn O.K. dann Fenster schließen:
mainWin.abbrechen_ok.rejected.connect(mainWin.close) 

sys.exit(app.exec_())