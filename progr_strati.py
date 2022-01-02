# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

from init_db import c, conn
from fehlerbeh import fehlerkontrolle, fehlersuche, check_initalf_rohdat
from tab_create import create_ergeb
from gui_windows import mainWin

# Wenn kein Fehler Auftritt wird Ergänzung der Werte durchgefuehrt,
# ...bis Anzahl der Zeilen konstant ist:
## ...zuerst Definition der Funktion:
def ergaenzungsschleife(tabelle, anw_fehlerkontrolle):
	nZeilen = 1
	durchlauf = 1
	fehler = False
	if anw_fehlerkontrolle == True: # Fehlerkontrolle muss einmal vor dem Ergänzen durchgefuehrt werden
		fehler = fehlerkontrolle()
	while (nZeilen > 0 and fehler == False):
		c.execute('''INSERT OR IGNORE into
			%s (w1, w2, durchlauf)
			select
				tab1.w1,
				tab2.w2,
				?
			FROM
				%s "tab1",
				%s "tab2"
			where
				tab1.w2 = tab2.w1''' % (tabelle, tabelle, tabelle), (durchlauf,))
		c.execute('SELECT COUNT(*) FROM %s WHERE durchlauf = ?' % (tabelle), (durchlauf,))
			# Fehlerkontrolle muss vor und nach der Schleife durchgeführt werden
		nZeilen = c.fetchone()
		nZeilen = nZeilen[0]
		if anw_fehlerkontrolle == True: #...einmal bei jedem Durchlauf
			fehler = fehlerkontrolle()
		
		('Durchlauf ' + str(durchlauf))
		durchlauf = durchlauf + 1
	if anw_fehlerkontrolle == True and fehler == False: #...und einmal zum Schluss
		fehler = fehlerkontrolle()

def programmkern():
	# in Basistabelle gleich werden "Gegenwerte" eingetragen, z.B. 3=5, 5=3     
	mainWin.anzeige_arbeitsschritt.setText('Programm gestartet')
	c.execute('CREATE TABLE IF NOT EXISTS gleich (w1, w2, durchlauf INTEGER DEFAULT 0, UNIQUE(w1, w2))')
	c.execute('''INSERT OR IGNORE into
			gleich (w1, w2)
		select
			befund1,
			befund2
		FROM
			rohdaten_gef
		where
			ueber_unter = 'gleich'
		union
		select
			befund2,
			befund1
		FROM
			rohdaten_gef
		where
			ueber_unter = "gleich"''')     
	mainWin.anzeige_arbeitsschritt.setText('Gleich-Werte werden ergänzt')	
	mainWin.progressBar.setValue(25)
	print('Gleich-Werte werden ergänzt')
	## ...erster Aufruf der Funktion:
	ergaenzungsschleife('gleich', False)
	mainWin.progressBar.setValue(50)
	
	## die Folgenden SQL-Befehle dienen im Grunde dazu, eine fortlaufende ID zu erstellen, was schwierig ist, da ältere SQlite-Versionen keine row_count Fensterfunktion haben
	# Zuweisung von Ids zu gruppierten Gleich-Werten, wobei alle gleichgesetzten Befunde eine ID bekommen:
	c.execute('CREATE TABLE IF NOT EXISTS ids_gruppen_gleich (id INTEGER PRIMARY KEY, _w2)')
	c.execute('''INSERT OR IGNORE into
		ids_gruppen_gleich (_w2)
		SELECT DISTINCT
			_w2
		FROM
		(
		select
			w1,
			group_concat(w2) "_w2"
		from
			gleich
		GROUP BY
			w1
		)''')     
	# Zuweisung von IDs zu allen Befunden, gleich und ueber_unter:
	c.execute('CREATE TABLE IF NOT EXISTS ids_gesamt (befund, id INTEGER, UNIQUE(befund))')
	c.execute('''INSERT OR IGNORE into
		ids_gesamt (befund, id)
		select
			gleich.w1,
			ids_gruppen_gleich.id
		from
			(
			select
				w1,
				group_concat(w2) "_w2"
			from
				gleich
			GROUP BY
				w1
			) "gleich",
			ids_gruppen_gleich
		WHERE
			gleich._w2 = ids_gruppen_gleich._w2
		UNION ALL
		SELECT
			befund1, 
			0
		FROM
			rohdaten_gef
		where not
			ueber_unter = 'gleich'
		UNION ALL
		SELECT
			befund2, 
			0
		FROM
			rohdaten_gef
		where not
			ueber_unter = "gleich"''')     
	c.execute('UPDATE ids_gesamt SET id = (SELECT coalesce(max(id),1) FROM ids_gruppen_gleich) + rowid WHERE id = 0')
	# Aufbereitung der Rohdaten gleich und Befuellung der Tabelle:
	c.execute('CREATE TABLE IF NOT EXISTS "ueber_unter" (w1, w2, durchlauf INTEGER DEFAULT 0, UNIQUE(w1, w2))')
	c.execute('''INSERT OR IGNORE into
		ueber_unter (w1, w2)
		select
		w1.id "w1", w2.id "w2"
	from
		(
		SELECT 
			befund1, befund2
		from
			rohdaten_gef
		where
			ueber_unter = 'ueber'
		UNION ALL
		SELECT 
			befund2, befund1
		from
			rohdaten_gef
		where
			ueber_unter = 'unter'
		) "rohdaten"
		LEFT join
			ids_gesamt "w1"
		ON
			rohdaten.befund1 = w1.befund
		LEFT join
			ids_gesamt "w2"
		ON
			rohdaten.befund2 = w2.befund''')     
	# test
	mainWin.anzeige_arbeitsschritt.setText('Über-Unter-Werte werden ergänzt')
	mainWin.progressBar.setValue(75)
	# Ergaenzen ueber_unter:
	ergaenzungsschleife('ueber_unter', True)
	mainWin.anzeige_arbeitsschritt.setText('fertig')
	mainWin.progressBar.setValue(100)

def programmstart():
	if check_initalf_rohdat()==True:
		print('Abbruch: Widerspruch in eingegeben Daten derart "Befund 1 über Befund 1" gefunden')	
	else:
		programmkern()
	# Ergebnisse in Tabellen:
	create_ergeb()
	# Datenbank aufräumen:
	#del_tabs()
	conn.commit() 
	
