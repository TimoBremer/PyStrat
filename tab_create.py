# _*_ coding: utf-8 _*_
#!/usr/bin/env python3

from init_db import c, conn

def initial_db():
	# Erstellen der Tabellen:
	c.execute('CREATE TABLE rohdaten (befund1, ueber_unter TEXT, befund2)')
	c.execute('CREATE TABLE rohdaten_datierung (befund, datierung)')
	c.execute('CREATE TABLE reihenf_abs_dat (datierung TEXT UNIQUE, reihenfolge INTEGER UNIQUE)')
	c.execute('CREATE TABLE ausschluss_rohdaten (befund1, ueber_unter TEXT, befund2)')   
	#// FIXME: Subphasen stimmt wahrscheinlich irgendetwas nicht mit!
	c.execute('CREATE TABLE vorschl_subphasen(befund, datierung, schichten_darueber, schichten_darunter, subphase)')   
	# bindet im ersten Schritt, die Reihenfolge an die absoluten Daten:
	c.execute('''CREATE VIEW "dat_reihenf" AS 
	SELECT 
		dat.befund "bef",
		--es geht nur Reihenfolge oder Sortierung anhand der Phasenbenennungen, aber nicht beides:
		CASE WHEN EXISTS(SELECT * FROM reihenf_abs_dat) = 1 THEN reihenf.reihenfolge ELSE dat.datierung END "reihenf"
	FROM 
		rohdaten_datierung "dat"
		LEFT JOIN
			reihenf_abs_dat "reihenf"
		ON
			dat.datierung = reihenf.datierung
	WHERE
		reihenf IS NOT NULL''')
	# ~ c.execute('''CREATE VIEW abs_daten_gleich AS
	# ~ SELECT
		# ~ dat_reihenf.bef "befund",
		# ~ dat_reihenf.reihenf "reihenfolge"
	# ~ FROM
		# ~ dat_reihenf
		# ~ LEFT JOIN
			# ~ abs_daten_ueber_unter
		# ~ ON
			# ~ dat_reihenf.bef = abs_daten_ueber_unter.befund
	# ~ WHERE
		# ~ --schließt Daten aus, bei denen die absolute Datierung im Widersrpruch zur Stratigrafie steht
		# ~ --wegen dem "Vetorecht" der Stratigrafie
		# ~ --muss später noch in eigene Abfragen zur Fehlerkontrolle
		# ~ (
			# ~ --muss jeweils geprüft werden, ob es überhaupt einen Wert bei der Reihenfolge gibt
			# ~ abs_daten_ueber_unter.reihenfolge_gleich_od_nach IS NULL
		# ~ OR
			# ~ abs_daten_ueber_unter.reihenfolge_gleich_od_nach > dat_reihenf.reihenf
		# ~ )
	# ~ OR	
			# ~ abs_daten_ueber_unter.reihenfolge_gleich_od_vor IS NULL
		# ~ OR
			# ~ abs_daten_ueber_unter.reihenfolge_gleich_od_vor < dat_reihenf.reihenf''')
	# sucht jeweils die höchste und niedrigste Datierung, um daraus von- und bis-Werte zu bilden:
	# ist Grundlage der Analyse absoluter Daten und Widersprüche
	c.execute('''CREATE VIEW abs_daten_ueber_unter_inkl_widerspr AS
		SELECT 
			befund,
			max(reihenfolge_gleich_od_nach) "reihenfolge_gleich_od_nach",
			min(reihenfolge_gleich_od_vor) "reihenfolge_gleich_od_vor"
		FROM
			(
			select
				ueber_unter_befunde.befund2 "befund",
				-- Reihenfolge ist immer dann wichtig, wenn diese nicht aus dem Namen der Phasen hervorgeht (z.B. HA 1 und LT 2)
				-- ...also in der Folge immer mit der Reihenfolge arbeiten, anstatt mit der tatsächlichen Datierung
				dat_reihenf.reihenf "reihenfolge_gleich_od_vor",
				NULL "reihenfolge_gleich_od_nach"
			from 
				ueber_unter_befunde,
				dat_reihenf
			where
				ueber_unter_befunde.befund1 = dat_reihenf.bef

			UNION ALL

			--union unter-Beziehungen (gleich od. vor Datierung)
			select
				ueber_unter_befunde.befund1,
				NULL,
				dat_reihenf.reihenf
			from 
				ueber_unter_befunde,
				dat_reihenf
			where
				ueber_unter_befunde.befund2 = dat_reihenf.bef
			)
		GROUP BY
			befund''')
	# filtert Widersprüche aus Datierungsspannen heraus:
	c.execute('''CREATE VIEW abs_daten_ueber_unter AS
	SELECT * FROM
		abs_daten_ueber_unter_inkl_widerspr
		WHERE 
			(
				--diese Zeile schliesst Widersprueche in der Datierung der Art "gleich/unter 3 und gleich/ueber 5" ausschluss_rohdaten
				--muss später in eigene Abfrage zur Widerspruchsanalyse
				reihenfolge_gleich_od_vor > reihenfolge_gleich_od_nach
			OR
				--...damit der Vergleich funktioniert, darf aber keiner der Werte Null sein
				reihenfolge_gleich_od_vor || reihenfolge_gleich_od_nach IS NULL
			)
		AND NOT
			--hiermit werden alle Datierungen ausgeschlossen, die sich über die gesamte mögliche Spannweite erstrecken (z.B. von Phase 1 bis 6)
			(
				reihenfolge_gleich_od_nach = (SELECT min_reihenfolge FROM min_max_datierungen)
			AND
				reihenfolge_gleich_od_vor = (SELECT max_reihenfolge FROM min_max_datierungen)
			)''')
	# hier werden die Datierungsspannen und die exakten Datierungen zusammengeführt:
	# die Reihenfolge wird wieder durch die Benennung der Datierungen ersetzt
	c.execute('''CREATE VIEW ergebnis_abs_daten AS
	SELECT
		abs_dat.befund,
		coalesce(dat_links.datierung, abs_dat.reihenfolge_gleich_od_nach) "dat_gleich_od_nach",
		coalesce(dat_rechts.datierung, abs_dat.reihenfolge_gleich_od_vor) "dat_gleich_od_vor"
	FROM
		(
		SELECT 
			*
		FROM
			abs_daten_ueber_unter
		WHERE 
			befund NOT IN (SELECT bef FROM dat_reihenf)

		UNION ALL

		SELECT
			bef,
			reihenf,
			reihenf
		FROM
			 dat_reihenf
		) "abs_dat"
		LEFT JOIN
			reihenf_abs_dat "dat_links"
		ON
			abs_dat.reihenfolge_gleich_od_nach = dat_links.reihenfolge
		LEFT JOIN
			reihenf_abs_dat "dat_rechts"
		ON
			abs_dat.reihenfolge_gleich_od_vor = dat_rechts.reihenfolge''')
	c.execute('''CREATE VIEW min_max_datierungen AS
	SELECT
		min(rohdaten_datierung.datierung) "min_dat",
		max(rohdaten_datierung.datierung) "max_dat",
		min(coalesce(reihenf_abs_dat.reihenfolge, rohdaten_datierung.datierung)) "min_reihenfolge",
		max(coalesce(reihenf_abs_dat.reihenfolge, rohdaten_datierung.datierung)) "max_reihenfolge"
	FROM
		rohdaten_datierung
		LEFT JOIN
			reihenf_abs_dat
		ON
			reihenf_abs_dat.datierung = reihenf_abs_dat.datierung''')
	c.execute('''CREATE VIEW rohdaten_gef as
	select * from 
		rohdaten
	where not ROWID in
		(
		select 
			rohdaten.ROWID
		from 
			rohdaten,
			ausschluss_rohdaten
		WHERE 
			rohdaten.befund1 = ausschluss_rohdaten.befund1
		AND
			rohdaten.ueber_unter = ausschluss_rohdaten.ueber_unter
		AND
			rohdaten.befund2 = ausschluss_rohdaten.befund2
		)''')
	c.execute('''CREATE VIEW rohdaten_geordnet AS
	select
		befund1,
		ueber_unter,
		befund2
	from
		rohdaten_gef
	where
		ueber_unter in('ueber', 'gleich')
	union all
	select
		befund2,
		'ueber',
		befund1
	from
		rohdaten_gef
	where
		ueber_unter = 'unter'
	union all
	select
		befund2,
		ueber_unter,
		befund1
	from
		rohdaten_gef
	where
		(ueber_unter = 'gleich')''')
	c.execute('''CREATE VIEW ueber_unter_befunde AS
	SELECT 
		id_links.befund "befund1",
		id_rechts.befund "befund2"
	FROM
		ueber_unter,
		ids_gesamt "id_links",
		ids_gesamt "id_rechts"
	WHERE
		ueber_unter.w1 = id_links.id
	AND
		ueber_unter.w2 = id_rechts.id''')
	# zeigt Widersprüche an...
		# 1. wenn älterer Befund über jüngerem liegt
		# 2. wenn sich absolute Datierung und Spanne widersprechen
	# ~ c.execute('''CREATE VIEW widerspr_strati_abs_daten AS
	# ~ SELECT
		# ~ bef "befund",
		# ~ coalesce(dat_exakt.datierung, reihenf) "dat_exakt",
		# ~ coalesce(dat_links.datierung, reihenfolge_gleich_od_nach) "von",
		# ~ coalesce(dat_rechts.datierung, reihenfolge_gleich_od_vor) "bis",
		# ~ fehler
	# ~ FROM
		# ~ (
		# ~ SELECT
			# ~ dat_reihenf.bef,
			# ~ dat_reihenf.reihenf,
			# ~ abs_daten_ueber_unter.reihenfolge_gleich_od_nach,
			# ~ abs_daten_ueber_unter.reihenfolge_gleich_od_vor,
			# ~ 'exakte Datierung und Datierungsspanne widersprechen sich' "fehler"
		# ~ FROM 
			# ~ abs_daten_ueber_unter,
			# ~ dat_reihenf
		# ~ WHERE
			# ~ abs_daten_ueber_unter.befund = dat_reihenf.bef
		# ~ AND NOT 
			# ~ reihenfolge_gleich_od_nach || reihenfolge_gleich_od_vor IS NULL
		# ~ AND NOT
			# ~ dat_reihenf.reihenf BETWEEN reihenfolge_gleich_od_nach AND reihenfolge_gleich_od_vor
		# ~ UNION ALL
		# ~ SELECT 
			# ~ befund,
			# ~ '' "exakte_dat",
			# ~ reihenfolge_gleich_od_nach, --an Reihenfolge müssen noch Datierungen angehängt werden!
			# ~ reihenfolge_gleich_od_vor,
			# ~ 'jüngere Dat. unter älterer'
		# ~ FROM
			# ~ abs_daten_ueber_unter_inkl_widerspr
			# ~ WHERE 
				# ~ reihenfolge_gleich_od_vor < reihenfolge_gleich_od_nach
		# ~ ) "fehler"
		# ~ LEFT JOIN
				# ~ reihenf_abs_dat "dat_exakt"
			# ~ ON
				# ~ fehler.reihenf = dat_exakt.reihenfolge
		# ~ LEFT JOIN
				# ~ reihenf_abs_dat "dat_links"
			# ~ ON
				# ~ fehler.reihenfolge_gleich_od_nach = dat_links.reihenfolge
		# ~ LEFT JOIN
				# ~ reihenf_abs_dat "dat_rechts"
			# ~ ON
				# ~ fehler.reihenfolge_gleich_od_vor = dat_rechts.reihenfolge''')
	c.execute('''CREATE VIEW widerspr_strati_abs_daten AS
		WITH fehler AS
		(
		SELECT
			dat_reihenf.bef,
			dat_reihenf.reihenf "reihenf1",
			CASE WHEN dat_reihenf.reihenf < abs_daten_ueber_unter.reihenfolge_gleich_od_nach THEN 'über' ELSE 'unter' END "bez",
			CASE WHEN dat_reihenf.reihenf < abs_daten_ueber_unter.reihenfolge_gleich_od_nach THEN abs_daten_ueber_unter.reihenfolge_gleich_od_nach ELSE abs_daten_ueber_unter.reihenfolge_gleich_od_vor END "reihenf2"
		FROM 
			abs_daten_ueber_unter,
			dat_reihenf
		WHERE
			abs_daten_ueber_unter.befund = dat_reihenf.bef
		AND 
			(
				dat_reihenf.reihenf < abs_daten_ueber_unter.reihenfolge_gleich_od_nach
			OR
				dat_reihenf.reihenf > abs_daten_ueber_unter.reihenfolge_gleich_od_vor
			)
		)
		SELECT 
			fehler1.bef "bef_1",
			dat_1.datierung "dat_bef_1",
			fehler1.bez,
			fehler2.bef "bef_2",
			dat_2.datierung "dat_bef_2"
		FROM
			fehler "fehler1",
			fehler "fehler2"
		LEFT JOIN
				rohdaten_datierung "dat_1"
			ON
				fehler1.bef = dat_1.befund
		LEFT JOIN
				rohdaten_datierung "dat_2"
			ON
				fehler2.bef = dat_2.befund
		WHERE
			fehler1.reihenf1 = fehler2.reihenf2''')
	c.execute('''CREATE VIEW fehlerk_anf AS
	SELECT
		fehlerkette1.*
	from
		(
		SELECT 
			* 
		FROM 
			fehlerkette
		where
			durchlauf = 0
		) fehlerkette1,
		(
		SELECT 
			* 
		FROM 
			fehlerkette
		where 
			durchlauf = (select max(durchlauf) from fehlerkette)
		) "fehlerkette2"
	where 
		fehlerkette1.id_bez = fehlerkette2.id_bez
	AND
		fehlerkette1.befund1 = fehlerkette2.befund2''')
	c.execute('''CREATE VIEW fehlerk_ende AS
	SELECT
		fehlerkette2.*
	from
		(
		SELECT 
			* 
		FROM 
			fehlerkette
		where
			durchlauf = 0
		) fehlerkette1,
		(
		SELECT 
			* 
		FROM 
			fehlerkette
		where 
			durchlauf = (select max(durchlauf) from fehlerkette)
		) "fehlerkette2"
	where 
		fehlerkette1.id_bez = fehlerkette2.id_bez
	AND
		fehlerkette1.befund1 = fehlerkette2.befund2''')
	c.execute('''CREATE VIEW fehlerkontrolle_1 AS
	select
		ueber_unter1.w1,
		ueber_unter1.w2
	from 
		ueber_unter "ueber_unter1", 
		ueber_unter "ueber_unter2" 
	where 
		ueber_unter1.w1 = ueber_unter2.w2 
	and 
		ueber_unter1.w2 = ueber_unter2.w1
	and NOT
		(
			ueber_unter1.w1 = ueber_unter1.w2
		OR
			ueber_unter2.w1 = ueber_unter2.w2
		)''')
	c.execute('''CREATE VIEW initalf_rohdat AS
	select distinct
		roh1.*
	from 
		rohdaten_geordnet roh1
		left join
			rohdaten_geordnet roh2
			on roh1.befund1 = roh2.befund2
			AND roh1.befund2 = roh2.befund1
	WHERE
		(
			roh1.befund1 = roh2.befund2
		AND
			roh1.befund2 = roh2.befund1
		)
	AND
		(
			roh1.ueber_unter = 'ueber'
		or
			roh2.ueber_unter = 'ueber'
		)''')

def create_ergeb():
	c.execute('''CREATE VIEW ergebnis_strati_bef AS
	SELECT 
		id_links.befund "befund1",
		id_rechts.befund "befund2"
	FROM
		ueber_unter,
		ids_gesamt "id_links",
		ids_gesamt "id_rechts"
	WHERE
		ueber_unter.w1 = id_links.id
	AND
		ueber_unter.w2 = id_rechts.id''')
	c.execute('''CREATE TABLE abs_daten_exakt_mit_vorschl_subphasen AS
	SELECT befund, datierung || subphase AS "vorschl_datierung" FROM vorschl_subphasen where subphase is not null
	UNION ALL
	SELECT * FROM rohdaten_datierung where befund not in (SELECT befund FROM vorschl_subphasen where subphase is not null)''')

