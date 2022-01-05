# läuft unten im Terminal von VS-Code.
# ...Programm-Datei muss im gleichen Pfad sein

# bei Wiederholung müssen die Dateien "dist" und "build" zuvor gelöscht werden
    # geht nur, wenn die gerade nicht ausgeführt werden

# die ui-Dateien müssen mit absoluten Pfaden angegeben werden:
#... in gui_windows.py: mainWin = uic.loadUi(r'C:\Users\timob\OneDrive\Desktop\22_01_05_strati_progr/gui_strati.ui')
#... in fill_tables.py: self.gui_tab = uic.loadUi(r'C:\Users\timob\OneDrive\Desktop\22_01_05_strati_progr/gui_tab.ui')

# Problem mit ui-files:
pyinstaller --noconsole --add-data="C:\Users\timob\OneDrive\Desktop\22_01_05_strati_progr;." --hidden-import=PyQt5 aufruf_gui_strati.py