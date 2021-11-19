# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

import sqlite3
import os ## kann entfernt werden, wenn DB im RAM läuft!

if os.path.exists('stratigrafie.sqlite'):## kann entfernt werden, wenn DB im RAM läuft!
	os.remove('stratigrafie.sqlite') 

conn = sqlite3.connect('stratigrafie.sqlite')
#conn = sqlite3.connect(':memory:')
c = conn.cursor()
