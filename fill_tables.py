# _*_ coding: utf-8 _*_

# Möglichkeit zum Kopieren/Download
# Reiter für Fehler etc. erscheinen erst, wenn nötig

import sys
import csv
import os
from tkinter.constants import S
from init_db import c, conn
from PyQt5 import QtWidgets, uic
import os
import tkinter as tk
from tkinter import filedialog
from dateipfade import save_previous_paths, get_prev_path
from gui_windows import mainWin

def result_tabs():
    #// TODO: Delete Tabs wenn keine Tabellen oder keine Daten in DB
    impStrati = FillTables('rohdaten', 'gui_tab_save.ui', 'strat. rel.', ['left', 'relation', 'right'])
    absData = FillTables('rohdaten_datierung', 'gui_tab_save.ui', 'abs. data', ['feature', 'date/period'])
    orderAbs = FillTables('reihenf_abs_dat', 'gui_tab_save.ui', 'periods order', ['period', 'order'])
    resStrat = StoreabTabs('ergebnis_strati_bef', 'gui_tab_save.ui', 'strat. res.', ['feature under', 'feature above'])
    resDates = StoreabTabs('ergebnis_abs_daten', 'gui_tab_save.ui', 'dating', ['feature', 'from', 'till'])
    # // FIXME: Speichern-Button wird noch nicht korrekt angesprochen!
    # //TODO: Tabellen mit Input-Daten brauchen evtl. keinen Speichern-Button?

    impStrati.create_fill()
    absData.create_fill()
    orderAbs.create_fill()
    resStrat.create_fill()
    resDates.create_fill()

class FillTables:
    def __init__(self, db_tab, gui_tab, gui_tab_name, head_lab=''):
        self.db_tab = db_tab
        self.head_lab = head_lab
        self.gui_tab = gui_tab
        self.gui_tab_name = gui_tab_name

        # //TODO: Individuelle Tabs erstellens
        self.gui_tab = uic.loadUi(gui_tab)

    def db_select(self):
        # SQL-Befehl und Result-Set (Objekt) als return:
        sql_bef = 'SELECT * FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        rows = c.fetchall()
        return(rows)

    def ncol_tab(self):
        first_row = self.db_select()
        _ncol = len(first_row[0])
        self.gui_tab.table.setColumnCount(_ncol)

    def nrow_tab(self):
        # ermittelt die Anzahl der Zeilen
        sql_bef = 'SELECT COUNT(*) FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        _nrow = c.fetchone()
        _nrow = _nrow[0]
        self.gui_tab.table.setRowCount(_nrow)
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
                    self.gui_tab.table.setItem(_nrow, _ncol, QtWidgets.QTableWidgetItem(value))
                _ncol = _ncol +1
            _nrow = _nrow +1
    
    def tune_table(self):
        # Header und Sortierfunktion:
        self.gui_tab.table.setSortingEnabled(True)
        self.gui_tab.table.setHorizontalHeaderLabels(self.head_lab)
    
    def add_tab(self):
        #from aufruf_gui_strati import mainWin
        mainWin.tabWidget.addTab(self.gui_tab, self.gui_tab_name)
    
    def create_fill(self):
        #self.table_has_data()
        if self.nrow_tab() > 0:
            self.add_tab()
            self.ncol_tab()
            self.fill_table()
            self.tune_table()

class StoreabTabs(FillTables):
    def __init__(self, db_tab, gui_tab, gui_tab_name, head_lab):
        FillTables.__init__(self, db_tab, gui_tab, gui_tab_name, head_lab)

        self.gui_tab.saveRes.clicked.connect(lambda:self.write_csv())
    
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