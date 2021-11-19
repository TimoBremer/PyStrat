# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
import os
import tkinter as tk
from tkinter import filedialog
from eingabe_daten_db import eing_datenb

# muss die Pfade nach dem Ausführen in Datei speichern
def save_previous_paths(list_paths):
	txt_file = open("letzte_pfade", "w")
	txt_file.write('# speichert die zuletzt verwendeten Dateipfade\n')
	txt_file.close()
	txt_file = open("letzte_pfade", "a")
	for path in list_paths:
		txt_file.write(path + "\n")
	txt_file.close()

def get_prev_path(zeile_txt_file):
	txt_file = open("letzte_pfade", "r")
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
	pfad = get_prev_path(zeile_txt_file)
	textfeld.clear()
	textfeld.setText(pfad)

def aufruf_dateipfad(textfeld, zeile_txt_file):
	# This is executed when the button is pressed
	parent = tk.Tk()
	# Ask the user to select a single file name
	file_types = [('Textdateien', '*.csv *.txt'), ('All files', '*')]
	initialdir = os.path.dirname(get_prev_path(zeile_txt_file))
	if get_prev_path(zeile_txt_file) == False:
		pfad = filedialog.askopenfilename(title='Select a file', filetypes=file_types, parent=parent)
	else:
		pfad = filedialog.askopenfilename(title='Select a file', initialdir = initialdir, filetypes=file_types, parent=parent)	
	parent.destroy()
	textfeld.clear()
	textfeld.setText(pfad)
	
def pfade_auslesen(hauptfenster):
	##from aufruf_gui_strati import hauptfenster
	# Pfad aus GUI nach Eingabe wieder auslesen:
	pfad_rohdaten = hauptfenster.dateipfad_rohdaten.displayText()
	pfad_abs_daten = hauptfenster.dateipfad_abs_daten.displayText()
	pfad_reihenf_abs_daten = hauptfenster.dateipfad_reihenf_abs_daten.displayText()
	eing_datenb(pfad_rohdaten, pfad_abs_daten, pfad_reihenf_abs_daten)
	# Pfade in Textdatei für zukünftige Durchläufe schreiben
	list_paths = [pfad_rohdaten, pfad_abs_daten, pfad_reihenf_abs_daten]
	save_previous_paths(list_paths)