# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
import os
import tkinter as tk
from tkinter import filedialog
from eingabe_daten_db import eing_datenb
from gui_windows import mainWin

# muss die Pfade nach dem Ausführen in Datei speichern
def save_previous_paths(file, list_paths):
	txt_file = open(file, "w")
	txt_file.write('# speichert die zuletzt verwendeten Dateipfade\n')
	txt_file.close()
	txt_file = open(file, "a")
	for path in list_paths:
		txt_file.write(path + "\n")
	txt_file.close()

def get_prev_path(file, zeile_txt_file):
	txt_file = open(file, "r")
	pfade = txt_file.readlines()
	txt_file.close()
	if len(pfade) >= zeile_txt_file +1: # +1, weil in der 1. Zeile der Datei nur eine Info steht
		pfad = pfade[zeile_txt_file].strip('\n') # der Linebreak, der für das Schreiben...
		#...in Textdat. notwendig ist, muss wieder entfernt werden
	else:
		pfad = False
	return(pfad)	

def call_prev_path(textfeld, zeile_txt_file):
	txt_file = open("letzte_pfade", "r")
	pfade = txt_file.readlines()
	pfad = get_prev_path("letzte_pfade", zeile_txt_file)
	textfeld.clear()
	textfeld.setText(pfad)

# #// TODO: Funktion kann gelöscht werden, wenn altes Dateipfad-Menü wegkommt
# def aufruf_dateipfad(textfeld, zeile_txt_file):
# 	parent = tk.Tk()
# 	# Ask the user to select a single file name
# 	file_types = [('Textdateien', '*.csv *.txt'), ('All files', '*')]
# 	initialdir = os.path.dirname(get_prev_path("letzte_pfade", zeile_txt_file))
# 	if initialdir == False:
# 		pfad = filedialog.askopenfilename(title='Select a file', filetypes=file_types, parent=parent)
# 	else:
# 		pfad = filedialog.askopenfilename(title='Select a file', initialdir = initialdir, filetypes=file_types, parent=parent)	
# 	parent.destroy()
# 	textfeld.clear()
# 	textfeld.setText(pfad)
	
# def pfade_auslesen():
# 	# Pfad aus GUI nach Eingabe wieder auslesen:
# 	pfad_rohdaten = mainWin.dateipfad_rohdaten.displayText()
# 	pfad_abs_daten = mainWin.dateipfad_abs_daten.displayText()
# 	pfad_reihenf_abs_daten = mainWin.dateipfad_reihenf_abs_daten.displayText()
# 	eing_datenb(pfad_rohdaten, pfad_abs_daten, pfad_reihenf_abs_daten)
# 	# Pfade in Textdatei für zukünftige Durchläufe schreiben
# 	list_paths = [pfad_rohdaten, pfad_abs_daten, pfad_reihenf_abs_daten]
# 	save_previous_paths("letzte_pfade", list_paths)
