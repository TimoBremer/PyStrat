# _*_ coding: utf-8 _*_

# Möglichkeit zum Kopieren/Download
# Reiter für Fehler etc. erscheinen erst, wenn nötig

import sys
import csv
from tkinter.constants import S
from init_db import c, conn
from PyQt5 import QtWidgets
import os
import tkinter as tk
from tkinter import filedialog

def result_tabs(mainWin):
    impStrati = FillTables('rohdaten', mainWin.tabInStrati, ['left', 'relation', 'right'])
    absData = FillTables('rohdaten_datierung', mainWin.tabInAbs, ['feature', 'date/period'])
    orderAbs = FillTables('reihenf_abs_dat', mainWin.tabInOrderAbs, ['period', 'order'])
    resStrat = StoreabTabs('ergebnis_abs_daten', mainWin.tabResStrat, mainWin.saveResStrat, ['feature', 'from', 'till'])
    impStrati.create_fill()
    absData.create_fill()
    orderAbs.create_fill()
    resStrat.create_fill()

class FillTables:
    def __init__(self, db_tab, gui_tab, head_lab=''):
        self.db_tab = db_tab
        self.head_lab = head_lab
        self.gui_tab = gui_tab
    
    def db_select(self):
        # SQL-Befehl und Result-Set (Objekt) als return:
        sql_bef = 'SELECT * FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        rows = c.fetchall()
        return(rows)

    def ncol_tab(self):
        first_row = self.db_select()
        _ncol = len(first_row[0])
        self.gui_tab.setColumnCount(_ncol)

    def nrow_tab(self):
        # ermittelt die Anzahl der Zeilen
        sql_bef = 'SELECT COUNT(*) FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        _nrow = c.fetchone()
        _nrow = _nrow[0]
        self.gui_tab.setRowCount(_nrow)
    
    def fill_table(self):
        sql_tab = self.db_select()
        _nrow = 0
        for row in sql_tab:
            _ncol = 0
            for value in row:
                value = str(value)
                # "None" muss herausgefiltert werden, sieht sonst doof aus in Tabelle
                if not 'None' in value:
                    self.gui_tab.setItem(_nrow, _ncol, QtWidgets.QTableWidgetItem(value))
                _ncol = _ncol +1
            _nrow = _nrow +1
    
    def tune_table(self):
        # Header und Sortierfunktion:
        self.gui_tab.setSortingEnabled(True)
        self.gui_tab.setHorizontalHeaderLabels(self.head_lab)
    
    def create_fill(self):
        self.ncol_tab()
        self.nrow_tab()
        self.fill_table()
        self.tune_table()

class StoreabTabs(FillTables):
    def __init__(self, db_tab, gui_tab, save_but, head_lab):
        self.save_but = save_but
        FillTables.__init__(self, db_tab, gui_tab, head_lab)
    
        self.save_but.clicked.connect(lambda:self.write_csv())
    
    def file_dialog(self):
        parent = tk.Tk()
        # Ask the user to select a single file name
        path = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        parent.destroy()
        return(path.name)

    def write_csv(self):
        file_name = self.file_dialog()
        sql_tab = self.db_select()
        print(sql_tab)
        with open(file_name, 'w', encoding='UTF8', newline='') as csvfile:
            # "mit with open schließt sich das Fenster automatisch, wenn Befehle abgearbeitet sind"
            writer = csv.writer(csvfile)
            writer.writerow(self.head_lab)
            writer.writerows(sql_tab)