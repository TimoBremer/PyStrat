# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from progr_strati import programmstart
from fill_tables import init_tabs, result_tabs, fill_gui
from gui_windows import app, mainWin
from tab_create import initial_db

#// TODO: Start ausgrauen, so lange noch nichts in Input Strat. Rel.

init_tabs()
first_run = True

def steuerung_progr():
	# Create tables:
	initial_db()
	# Create gui-tables:
	fill_gui()
	programmstart()
	# cuts the 4th tab 5 times to make sure, no result tab is left:
	# ...a bit complicated, because I found no way to remove the tabs by their name
	if first_run == False:
		for i in range(4):
			mainWin.tabWidget.removeTab(3)
	result_tabs()
	_run()

def _run():
	global first_run
	first_run = False

mainWin.show()
# it's a trick because it is impossible to create an empty tabWidget in QtCreator:
mainWin.tabWidget.removeTab(0)
mainWin.button_start.clicked.connect(lambda: steuerung_progr())
# Wenn abbrechen dann Fenster schließen, wenn O.K. dann Fenster schließen:
mainWin.abbrechen_ok.rejected.connect(mainWin.close) 

sys.exit(app.exec_())