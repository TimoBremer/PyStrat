# _*_ coding: utf-8 _*_

# Möglichkeit zum Kopieren/Download
# Reiter für Fehler etc. erscheinen erst, wenn nötig

import sys
import csv
import os
from tkinter.constants import S
from init_db import c, conn
from PyQt5 import QtWidgets
import os
import tkinter as tk
from tkinter import filedialog
from dateipfade import save_previous_paths, get_prev_path

def result_tabs(mainWin):
    #// TODO: Delete Tabs wenn keine Tabellen oder keine Daten in DB
    impStrati = FillTables('rohdaten', mainWin.tabInStrati, ['left', 'relation', 'right'])
    absData = FillTables('rohdaten_datierung', mainWin.tabInAbs, ['feature', 'date/period'])
    orderAbs = FillTables('reihenf_abs_dat', mainWin.tabInOrderAbs, ['period', 'order'])
    resStrat = StoreabTabs('ergebnis_strati_bef', mainWin.tabResStrat, mainWin.saveResStrat, ['feature under', 'feature above'])
    resDates = StoreabTabs('ergebnis_abs_daten', mainWin.tabResDates, mainWin.saveResDates, ['feature', 'from', 'till'])
    
    impStrati.create_fill()
    absData.create_fill()
    orderAbs.create_fill()
    resStrat.create_fill()
    resDates.create_fill()

class FillTables:
    def __init__(self, db_tab, gui_tab, head_lab=''):
        self.db_tab = db_tab
        self.head_lab = head_lab
        self.gui_tab = gui_tab
    
    # def table_has_data(self):
    #     #print('Funktion läuft')
    #     sql_bef = 'SELECT COUNT(*) FROM {}'.format(self.db_tab)
    #     c.execute(sql_bef)
    #     if c.fetchone()[0]==1:
    #         print('Table exists!')

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
        return(_nrow)
    
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
        #self.table_has_data()
        if self.nrow_tab() > 0:
            # create tab eventually
            self.ncol_tab()
            self.fill_table()
            self.tune_table()

class StoreabTabs(FillTables):
    def __init__(self, db_tab, gui_tab, save_but, head_lab):
        self.save_but = save_but
        FillTables.__init__(self, db_tab, gui_tab, head_lab)
    
        self.save_but.clicked.connect(lambda:self.write_csv())
    
    #// FIXME: das doppelt sich stark mit den Funktionen in dateipfade.py, kann man sicher vereinfachen
    def file_dialog(self):
        initialdir = get_prev_path('prev_dir_storage' ,1)
        parent = tk.Tk()
        # Ask the user to select a single file name
        if initialdir == False:
            path = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        else:
            path = filedialog.asksaveasfile(mode='w', initialdir=initialdir, defaultextension=".csv")
        parent.destroy()
        self.save_prev_dir(path.name)
        return(path.name)
    
    def save_prev_dir(self, path):
        path = os.path.dirname(path)
        list_path = []
        list_path.append(path)
        save_previous_paths('prev_dir_storage', list_path)
    
    def write_csv(self):
        file_name = self.file_dialog()
        sql_tab = self.db_select()
        with open(file_name, 'w', encoding='UTF8', newline='') as csvfile:
            # "mit with open schließt sich das Fenster automatisch, wenn Befehle abgearbeitet sind"
            writer = csv.writer(csvfile)
            writer.writerow(self.head_lab)
            writer.writerows(sql_tab)

#// TODO: Subclass zum Bearbeiten der Tabellen
    # gibt es schon für GIS-Datenbankeditor
    # muss allerdings stark angepasst werden