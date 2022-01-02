# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from progr_strati import programmstart
from fill_tables import init_tabs, result_tabs, impStrati, absData, orderAbs
#from dateipfade import *
from gui_windows import app, mainWin
from tab_create import initial_db

def steuerung_progr():
	#// TODO: hier müssen die to DB-Sachen hin:
	initial_db()
	impStrati.gui_tab_to_db()
	absData.gui_tab_to_db()
	orderAbs.gui_tab_to_db()
	programmstart()
	result_tabs()

mainWin.show()
init_tabs()
# it's a trick because it is impossible to create an empty tabWidget in QtCreator:
mainWin.tabWidget.removeTab(0)
# Eingabe vorherige Dateipfade:
# mainWin.tab_pfad_rohdat_last.clicked.connect(lambda: call_prev_path(mainWin.dateipfad_rohdaten, 1))
# mainWin.tab_pfad_abs_dat_last.clicked.connect(lambda: call_prev_path(mainWin.dateipfad_abs_daten, 2))
# mainWin.tab_pfad_reihenf_last.clicked.connect(lambda: call_prev_path(mainWin.dateipfad_reihenf_abs_daten, 3))

# Eingabe Dateipfade mittels Dialog:
# mainWin.ausw_dateipfad_rohdaten.clicked.connect(lambda: aufruf_dateipfad(mainWin.dateipfad_rohdaten, 1))
# mainWin.ausw_dateipfad_abs_daten.clicked.connect(lambda: aufruf_dateipfad(mainWin.dateipfad_abs_daten, 2))
# mainWin.ausw_dateipfad_reihenf_abs_daten.clicked.connect(lambda: aufruf_dateipfad(mainWin.dateipfad_reihenf_abs_daten, 3))

mainWin.button_start.clicked.connect(lambda: steuerung_progr())

# Wenn abbrechen dann Fenster schließen, wenn O.K. dann Fenster schließen:
mainWin.abbrechen_ok.rejected.connect(mainWin.close) 

sys.exit(app.exec_())