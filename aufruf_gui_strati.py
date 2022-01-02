# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
#from eingabe_daten_db import eing_datenb
from progr_strati import programmstart #, del_db_tabs
from fill_tables import result_tabs
from dateipfade import *
from gui_windows import app, mainWin

def steuerung_progr():
	# del_db_tabs()
	pfade_auslesen()
	programmstart()
	result_tabs()

mainWin.show()
# Eingabe vorherige Dateipfade:
mainWin.tab_pfad_rohdat_last.clicked.connect(lambda: call_prev_path(mainWin.dateipfad_rohdaten, 1))
mainWin.tab_pfad_abs_dat_last.clicked.connect(lambda: call_prev_path(mainWin.dateipfad_abs_daten, 2))
mainWin.tab_pfad_reihenf_last.clicked.connect(lambda: call_prev_path(mainWin.dateipfad_reihenf_abs_daten, 3))

# Eingabe Dateipfade mittels Dialog:
mainWin.ausw_dateipfad_rohdaten.clicked.connect(lambda: aufruf_dateipfad(mainWin.dateipfad_rohdaten, 1))
mainWin.ausw_dateipfad_abs_daten.clicked.connect(lambda: aufruf_dateipfad(mainWin.dateipfad_abs_daten, 2))
mainWin.ausw_dateipfad_reihenf_abs_daten.clicked.connect(lambda: aufruf_dateipfad(mainWin.dateipfad_reihenf_abs_daten, 3))

mainWin.button_start.clicked.connect(lambda: steuerung_progr())

# Wenn abbrechen dann Fenster schließen, wenn O.K. dann Fenster schließen:
mainWin.abbrechen_ok.rejected.connect(mainWin.close) 

sys.exit(app.exec_())