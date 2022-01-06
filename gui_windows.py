# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from pathlib import Path

app = QApplication(sys.argv)

# abs. path to current working directory for all operating sys.:
def get_pass(_dir):
    _cur_dir = Path.cwd()
    path = Path(_cur_dir, _dir)
    print(path)
    return(path)

mainWin = uic.loadUi(get_pass('gui_strati.ui'))
gui_tab_save = get_pass('gui_tab_save.ui')
gui_tab_apply = get_pass('gui_tab_apply.ui')