# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

# abs. path for windows pyinstaller:
# path = r'C:\Users\timob\OneDrive\Desktop\22_01_05_strati_progr\'

# else:
path = ''

mainWin = uic.loadUi(path + 'gui_strati.ui')
gui_tab_save = path + 'gui_tab_save.ui'
gui_tab_apply = path + 'gui_tab_apply.ui'