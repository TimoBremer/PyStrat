# läuft unten im Terminal von VS-Code.
# ...Programm-Datei muss im gleichen Pfad sein

# bei Wiederholung müssen die Dateien "dist" und "build" zuvor gelöscht werden
    # geht nur, wenn die gerade nicht ausgeführt werden

pyinstaller --noconsole --add-data 'C:\Users\timob\OneDrive\Desktop\strati\gui_strati.ui;.' --add-data 'C:\Users\timob\OneDrive\Desktop\strati\gui_tab_apply.ui;.' --add-data 'C:\Users\timob\OneDrive\Desktop\strati\gui_tab_save.ui;.' aufruf_gui_strati.py