# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

#//TODO: Die Sicherung der Dateipfade ist zurzeit sinnlos, muss noch zur Erstellung von Projektdateien umgebaut werden

import sys
import os
import tkinter as tk
from tkinter import filedialog
from gui_windows import mainWin

# muss die Pfade nach dem Ausführen in Datei speichern
def save_previous_paths(file, list_paths):
	txt_file = open(file, "w")
	txt_file.write('# speichert die zuletzt verwendeten Dateipfade\n')
	txt_file.close()
	txt_file = open(file, "a+")
	for path in list_paths:
		txt_file.write(path + "\n")
	txt_file.close()

def get_prev_path(file, zeile_txt_file):
	txt_file = open(file, "a+")
	pfade = txt_file.readlines()
	txt_file.close()
	if len(pfade) >= zeile_txt_file +1: # +1, weil in der 1. Zeile der Datei nur eine Info steht
		pfad = pfade[zeile_txt_file].strip('\n') # der Linebreak, der für das Schreiben...
		#...in Textdat. notwendig ist, muss wieder entfernt werden
	else:
		pfad = False
	return(pfad)	

def call_prev_path(textfeld, zeile_txt_file):
	txt_file = open("letzte_pfade", "a+")
	pfade = txt_file.readlines()
	pfad = get_prev_path("letzte_pfade", zeile_txt_file)
	textfeld.clear()
	textfeld.setText(pfad)