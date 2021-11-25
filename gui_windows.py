# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
mainWin = uic.loadUi('gui_strati.ui')