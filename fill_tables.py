# _*_ coding: utf-8 _*_

import sys
from init_db import c, conn

def result_tabs(mainWin):
    ImpStrati = FillTables('rohdaten', 'tabImpStrati', mainWin)
    ImpStrati.fill_table()

class FillTables:
    def __init__(self, db_tab, gui_tab, mainWin):
        self.db_tab = db_tab
        self.gui_tab = gui_tab
        self.mainWin = mainWin
    
    def db_select(self):
        #from aufruf_gui_strati import mainWin  
        sql_bef = 'SELECT * FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        rows = c.fetchall()
        return(rows)

    def ncol_tab(self):
        first_row = self.db_select()
        _ncol = len(first_row[0])
        self.mainWin.tabImpStrati.setColumnCount(_ncol)

    def nrow_tab(self):
        # ermittelt die Anzahl der Zeilen
        sql_bef = 'SELECT COUNT(*) FROM {}'.format(self.db_tab)
        c.execute(sql_bef)
        _nrow = c.fetchone()
        _nrow = _nrow[0]
        self.mainWin.tabImpStrati.setRowCount(_nrow)
    
    def fill_table(self):
        # Anzahl Zeilen und Spalten der Tabelle:
        self.ncol_tab()
        self.nrow_tab()

