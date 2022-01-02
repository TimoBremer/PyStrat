# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import os 
import csv
from init_db import c
from tab_create import initial_db

# def eing_datenb(pfad_rohdaten, pfad_abs_daten, pfad_reihenf_abs_daten):
# 	initial_db()
# 	# in Datenbank einfügen:
# 	csv_to_gui(pfad_rohdaten, "rohdaten", 3)
# 	csv_to_gui(pfad_abs_daten, "rohdaten_datierung", 2)
# 	csv_to_gui(pfad_reihenf_abs_daten, "reihenf_abs_dat", 2)

# def type_con(csv_str):
# 	csv_str = csv_str.strip(' ')
# 	if not csv_str.isnumeric():
# 		csv_str = "'{}'".format(csv_str)
# 	return(csv_str)

# #// TODO: csv_to_gui anpassen
# def csv_to_gui(pfad, tabelle, anz_spalten):
# 	# Kontrolle, ob es Datei gibt:
# 	isFile = os.path.isfile(pfad)
# 	if isFile==True:
# 		#Einfügen Daten:
# 		with open(pfad) as csvfile:
# 			reader = csv.reader(csvfile, delimiter=',') # no header information with delimiter
# 			for row in reader:
# 				# hier muss noch was mit der Codierung des Zeichensatzes geschehen:
# 				r0 = type_con(row[0])
# 				r1 = type_con(row[1])
# 				if anz_spalten==3:
# 					r2 = type_con(row[2])
# 					sql_bef = 'INSERT INTO {} VALUES ({},{},{})'.format(tabelle, r0, r1, r2)
# 				else:
# 					sql_bef = 'INSERT INTO {} VALUES ({},{})'.format(tabelle, r0, r1)
# 				c.execute(sql_bef)


# def fill_table(self):
# 	sql_tab = self.db_select()
# 	_nrow = 0
# 	for row in sql_tab:
# 		_ncol = 0
# 		for value in row:
# 			value = str(value)
# 			# "None" muss herausgefiltert werden, sieht sonst doof aus in Tabelle
# 			if not 'None' in value:
# 				self.gui_tab.table.setItem(_nrow, _ncol, QtWidgets.QTableWidgetItem(value))
# 			_ncol = _ncol +1
# 		_nrow = _nrow +1