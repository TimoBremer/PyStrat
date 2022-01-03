# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

from init_db import c, conn

def check_initalf_rohdat():
	c.execute('SELECT COUNT(*) FROM initalf_rohdat')
	anz_fehler = c.fetchone()
	anz_fehler = anz_fehler [0]
	if anz_fehler > 0:
		# //FIXME: hier ist der Wurm in der Fehlerkette drin:
		c.execute('INSERT into fehlerkette (befund1, ueber_unter, befund2) select * from initalf_rohdat')
		return True
	else:
		return False
	
def fehlerkontrolle():
	c.execute('SELECT COUNT(*) FROM fehlerkontrolle_1')
	anz_fehler = c.fetchone()
	anz_fehler = anz_fehler[0]
	if anz_fehler > 0:
		print('Abbruch: Widerspruch gefunden, suche Fehler')
		fehlersuche()
		return True
	else: 
		return False
	
def fehlersuche():
	# Fehlerkette wird vom Anfang zum Ende aufgebaut und dann rückwaerts abgearbeitet
	durchlauf = 0
	# die initiale Beziehung wird aus allen am Fehler beteiligten Befunden ausgesucht
	# in die erste Spalte kommt im nächsten Befehl eine ID für jede Beziehung
	c.execute('''INSERT into fehlerkette
		select NULL, *, 0
		from
			rohdaten_geordnet
		where
			befund1 in(
			select
				befund1.befund "befund1"
			from
				fehlerkontrolle_1,
				ids_gesamt "befund1"
			where
				fehlerkontrolle_1.w1 = befund1.id
			union
			select
				befund2.befund "befund2"
			from
				fehlerkontrolle_1,
				ids_gesamt "befund2"
			where
				fehlerkontrolle_1.w2 = befund2.id
			)
		AND not
			rohdaten_geordnet.ueber_unter = 'gleich'
		AND NOT
			(
				befund1 = befund2
			and
				ueber_unter = 'gleich'
			)''')
	# nun die Vergabe der ID für die initialen Fehlerbeziehungen:
	c.execute('UPDATE fehlerkette set id_bez = ROWID')
	# Ergaenzung der Fehlerkette hin:
	anz_zeilen = 1
	#// FIXME: Widersprüche, die vor dem 1. Durchlauf bestehen, werden erst viel später erfasst:
	#while (anz_zeilen == 0 or durchlauf < 1): 
	while (anz_zeilen > 0):
		print(anz_zeilen, ' ', durchlauf)
		durchlauf = durchlauf + 1
		# die letzte Bedingung in Klammern verhindert Fehler derart 3=2 | 2=3:
		c.execute('''INSERT into fehlerkette
			select distinct
				fehlerkette.id_bez,
				rohdaten_geordnet.befund1,
				rohdaten_geordnet.ueber_unter,
				rohdaten_geordnet.befund2,
				?
			from 
				rohdaten_geordnet,
				fehlerkette
			where
				CAST(fehlerkette.befund2 AS INTEGER) = CAST(rohdaten_geordnet.befund1 AS INTEGER)
			and not
				(
					CAST(fehlerkette.befund1 AS INTEGER) = CAST(rohdaten_geordnet.befund2 AS INTEGER)
				and
					(
						fehlerkette.ueber_unter = 'gleich'
					and
						rohdaten_geordnet.ueber_unter = 'gleich'
					)
				)''', (durchlauf,))
		# Prüfung ob erster Wert in Kette und letzter Wert gleich, Kreis also geschlossen:
		c.execute('SELECT COUNT(*) from fehlerk_ende')
		anz_zeilen = c.fetchone()
		anz_zeilen = anz_zeilen[0]
	fehlerkette_rueck(durchlauf)
	conn.commit
	
def fehlerkette_rueck(durchlauf):
	# erstmal den Beginn der Fehlerkette löschen und alle Beziehungen, die nicht zu Fehlerkette gehören:
	c.execute('''DELETE FROM 
			fehlerkette
		WHERE
			id_bez NOT in (select id_bez from fehlerk_ende)''')
	# Anfang und Ende der Fehlerkette werden überarbeitet:
	c.execute('''delete from fehlerkette 
		WHERE 
			durchlauf IN (0, ?)
		AND NOT
			ROWID IN
			(
			select fehlerkette.ROWID
			from 
				fehlerkette,
				(
				select * from fehlerk_anf
				UNION ALL
				select * from fehlerk_ende
				) anf_ende
			WHERE
				fehlerkette.id_bez = anf_ende.id_bez
				AND
				fehlerkette.befund1 = anf_ende.befund1
				AND
				fehlerkette.ueber_unter = anf_ende.ueber_unter
				AND
				fehlerkette.befund2 = anf_ende.befund2
				AND
				fehlerkette.durchlauf = anf_ende.durchlauf
			)''', (durchlauf,))
	# Schleife Rücklauf:
	for i in range(durchlauf, 1, -1):
		print('Rücklauf: ' + str(i)) 
		c.execute('''delete from fehlerkette 
			WHERE 
				durchlauf = ?-1
			AND NOT
				ROWID IN
				(
				select 
					fehlerkette.ROWID
				from 
					fehlerkette,
					(
					SELECT
						durchl0.*
					FROM
						(
						select 
							* 
						from 
							fehlerkette 
						where 
							durchlauf = ?-1
						) durchl0,
						(
						select 
							* 
						from 
							fehlerkette 
						where 
							durchlauf = ?
						) durchl1
					WHERE
						durchl0.id_bez = durchl1.id_bez
					AND
						durchl0.befund2 = durchl1.befund1
					) fehlerkette2
				WHERE
					fehlerkette.id_bez = fehlerkette2.id_bez
					AND
					fehlerkette.befund1 = fehlerkette2.befund1
					AND
					fehlerkette.ueber_unter = fehlerkette2.ueber_unter
					AND
					fehlerkette.befund2 = fehlerkette2.befund2
					AND
					fehlerkette.durchlauf = fehlerkette2.durchlauf
				)''', (i, i, i,))