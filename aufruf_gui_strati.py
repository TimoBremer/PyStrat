# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtWidgets import QApplication, QDialog
from eingabe_daten_db import eing_datenb
from progr_strati import programmstart
from dateipfade import *

def steuerung_progr(hauptfenster):
	pfade_auslesen(hauptfenster)
	programmstart(hauptfenster)
	
app = QApplication(sys.argv)
window = QDialog()
hauptfenster = uic.loadUi('gui_strati.ui')
hauptfenster.show()

# Eingabe vorherige Dateipfade:
hauptfenster.tab_pfad_rohdat_last.clicked.connect(lambda: call_prev_path(hauptfenster.dateipfad_rohdaten, 1))
hauptfenster.tab_pfad_abs_dat_last.clicked.connect(lambda: call_prev_path(hauptfenster.dateipfad_abs_daten, 2))
hauptfenster.tab_pfad_reihenf_last.clicked.connect(lambda: call_prev_path(hauptfenster.dateipfad_reihenf_abs_daten, 3))

# Eingabe Dateipfade mittels Dialog:
hauptfenster.ausw_dateipfad_rohdaten.clicked.connect(lambda: aufruf_dateipfad(hauptfenster.dateipfad_rohdaten, 1))
hauptfenster.ausw_dateipfad_abs_daten.clicked.connect(lambda: aufruf_dateipfad(hauptfenster.dateipfad_abs_daten, 2))
hauptfenster.ausw_dateipfad_reihenf_abs_daten.clicked.connect(lambda: aufruf_dateipfad(hauptfenster.dateipfad_reihenf_abs_daten, 3))

hauptfenster.button_start.clicked.connect(lambda: steuerung_progr(hauptfenster))

# Wenn abbrechen dann Fenster schließen, wenn O.K. dann Fenster schließen:
hauptfenster.abbrechen_ok.rejected.connect(hauptfenster.reject) 

sys.exit(app.exec_())
