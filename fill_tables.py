# _*_ coding: utf-8 _*_

# Möglichkeit zum Kopieren/Download
# Reiter für Fehler etc. erscheinen erst, wenn nötig

import sys
import csv
import os
from init_db import c
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QCursor
import os
import tkinter as tk
from tkinter import filedialog
from dateipfade import save_previous_paths, get_prev_path
from gui_windows import mainWin

def result_tabs():
    impStrati = EditTabs('rohdaten', 'gui_tab_apply.ui', 'Strat. Rel.', ['left', 'relation', 'right'])
    absData = EditTabs('rohdaten_datierung', 'gui_tab_apply.ui', 'Abs. Data', ['feature', 'date/period'])
    orderAbs = EditTabs('reihenf_abs_dat', 'gui_tab_apply.ui', 'Periods Order', ['period', 'order'])
    resStrat = StoreabTabs('ergebnis_strati_bef', 'gui_tab_save.ui', 'Strat. Res.', ['feature under', 'feature above'])
    resDates = StoreabTabs('ergebnis_abs_daten', 'gui_tab_save.ui', 'Dating', ['feature', 'from', 'till'])
    Contrad = StoreabTabs('strat_conflicts', 'gui_tab_save.ui', 'Strat. Conflicts', ['feature 1', 'relation', 'feature 2'])

    impStrati.build_tab()
    absData.build_tab()
    orderAbs.build_tab()
    resStrat.create_fill()
    resDates.create_fill()
    Contrad.create_fill()
#// TODO: Tabellen wenn Fehler etc.

class FillTables:
    def __init__(self, db_tab, gui_tab, gui_tab_name, head_lab=''):
        self.db_tab = db_tab
        self.head_lab = head_lab
        self.gui_tab = gui_tab
        self.gui_tab_name = gui_tab_name

        self.gui_tab = uic.loadUi(gui_tab)
        self._nrow = 0
        self._ncol = 0

    def db_select(self):
        # SQL-Befehl und Result-Set (Objekt) als return:
        sql_bef = 'SELECT * FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        rows = c.fetchall()
        return(rows)

    def ncol_tab(self):
        first_row = self.db_select()
        # sets also class variable – not really clean code:
        self._ncol = len(first_row[0])
        self.gui_tab.table.setColumnCount(self._ncol)

    def nrow_tab(self):
        # ermittelt die Anzahl der Zeilen
        sql_bef = 'SELECT COUNT(*) FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        _nrow = c.fetchone()
        self._nrow = _nrow[0]
        self.gui_tab.table.setRowCount(self._nrow)
    
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
        # //TODO: Drop down lists for ueber/unter/gleich and periods
    
    def add_tab(self):
        mainWin.tabWidget.addTab(self.gui_tab, self.gui_tab_name)
    
    def create_fill(self):
        self.nrow_tab()
        if self._nrow > 0:
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

class EditTabs(FillTables):
    def __init__(self, db_tab, gui_tab, gui_tab_name, head_lab):
        FillTables.__init__(self, db_tab, gui_tab, gui_tab_name, head_lab)

        self.upd_rows = []
        self.gui_tab.table.cellChanged.connect(lambda:self.edit_table())
        self.gui_tab.Reset.clicked.connect(lambda:self.reset_changes())
        self.gui_tab.applyChanges.clicked.connect(lambda:self.gui_tab_to_db())

        # right-click event on cells:
        self.gui_tab.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.gui_tab.table.customContextMenuRequested.connect(self.right_click)
        # or right click event on header:
        self.header = self.gui_tab.table.verticalHeader()
        self.header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.header.customContextMenuRequested.connect(self.right_click)

    def build_tab(self):
        self.create_fill()
        self.add_row()
        self.buttons_akt_deakt(False)
    
    def add_row(self):
        self._nrow = self._nrow + 1
        self.gui_tab.table.setRowCount(self._nrow)
    
    def rowids_selec_rows(self):
        #gibt die Spaltennummern des QTableWidgets wieder
        rows = sorted(set(index.row() for index in
            self.gui_tab.table.selectedIndexes()))
        return(rows)
    
    def check_last_row(self):
        # adds another row in when the last row has been edited
        # mir ist nicht ganz klar warum hier Korrektur -1 nötig?
        if self._nrow -1 in self.rowids_selec_rows():
            self.add_row()

    def buttons_akt_deakt(self, status):
        self.gui_tab.saveChanges.setEnabled(status)
        self.gui_tab.applyChanges.setEnabled(status)
        self.gui_tab.Reset.setEnabled(status)
    
    def edit_table(self):
        self.check_last_row()
        #ausgegraute Buttons aktivieren:
        self.buttons_akt_deakt(True)
        #//TODO: format-check for inserts
    
    def reset_changes(self):
            self.ncol_tab()
            self.fill_table()
            self.tune_table()
            self.buttons_akt_deakt(False)
    
    def right_click(self, event):
        menu = QMenu()
        menu.addAction('skip')
        if len(self.rowids_selec_rows()) > 1:
            action_del = menu.addAction('delete selected rows')
        else:
            action_del = menu.addAction('delete selected row')
        action = menu.exec_(self.gui_tab.mapFromParent(QCursor.pos()))
        if action == action_del:
            self.delete_rows()
    
    def delete_rows(self):
        ids = self.rowids_selec_rows()
        # must be in reversed order because the table rearranges the indices afte deleting the first row:
        ids = sorted(ids, reverse=True)
        for id in ids:
            self.gui_tab.table.removeRow(id)
        self.buttons_akt_deakt(True)
    
    def gui_tab_to_db(self):        
        sql_bef = 'DELETE FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        headers = self.db_tab_headers()
        # -1 because the last row is always empty:
        for row in range(self._nrow -1):
            sql_bef = 'INSERT INTO {} ({}) VALUES ({})'.format(self.db_tab, headers, self.get_row(row))
            c.execute(sql_bef)
        self.ncol_tab()
        self.fill_table()
        self.gui_tab.applyChanges.setEnabled(False)
        self.gui_tab.Reset.setEnabled(False)

    def get_row(self, id_zeile):
        zeile = []
        for spalte in range(self._ncol):
            txt_zeile = self.gui_tab.table.item(id_zeile, spalte)
            if txt_zeile is not None and txt_zeile.text() != '':
                wert = "'" + txt_zeile.text() + "'"
            else:
                wert = "''"
            zeile.append(wert)
        zeile = ', '.join(zeile)
        return(zeile)

    def db_tab_headers(self):
        headers = []
        sql_bef = "SELECT name FROM PRAGMA_TABLE_INFO('{}')".format(self.db_tab)
        c.execute(sql_bef)
        rows = c.fetchall()
        for row in rows:
            row = row[0]
            headers.append(row)
        headers = ', '.join(headers)
        return(headers)