#!/usr/bin/env python
# coding: utf-8

# # Repräsentation

# Architektur
# 
# <img src="pictures/5-Schichten-Architektur.png" alt="5-Schichten-Architektur" width="500" style="background-color: white;"/>

# # Aufbau
# 
# - Motivation:
#     - Beziehung zwischen Block-Modell des Speichers (Hauptspeicher/Festplatte) und Tupelmodelldes DBMS
# - Dateneinheiten:
#     - Attributwerte -> Bytelisten fester oder variabler Länge: „Felder“
#     - Tupel->Feldlisten fester oder variabler Länge: „Datensätze“
#     - Physische Blöcke speichern Datensatzmengen / -listen
#     - Relation->Mengen von Blöcken: „Datei“
#         - Plus Indexstrukturen
#         

# # Felder etc.
# 
# - Kleinste Dateneinheit: Attributwerte
# - Repräsentiert durch „Felder“ (fields)
# - Fragen für heute:
#     - Wie werden Datentypen als Felder repräsentiert?
#     - Wie werden Tupelals Datensätze repräsentiert?
#     - Wie werden Mengen von Datensätzen oder Tupelnin Blöcken repräsentiert?
#     - Wie werden Relationen als Mengen von Blöcken repräsentiert?
#     - Was passiert bei variablen Feld-oder Tupellängen?
#     - Was passiert wenn ich einen Block nicht einheitlich in Tupeleinteilen kann?
#     - Was passiert wenn sich die Größe eines Datensatzes ändert, insbesondere vergrößert?
#     
# ```
# CREATE TABLE Schauspieler (
#     Name CHAR(30),
#     Adresse VARCHAR(255),
#     Geschlecht CHAR(1),
#     Geburtstag DATE );
# ```

# <img src="pictures/Datenelemente-meme.png" alt="Datenelemente-meme" width="500" style="background-color: white;"/>

# # Datenelemente

# ## Datentypen
# 
# - Irgendwann werden alle Daten als Bitsequenzen dargestellt. 
#     - Bzw.: Irgendwann werden alle Daten als Bytesequenzen dargestellt.
#     - Integer: 2 oder 4 Byte
#     - Float: 4 oder 8 Byte
# - Strings fester Länge: CHAR(n)
#     - Feld hat n Byte
#     - Fehlende Byte-Werte werden mit Nullwerten ($\perp$)ge-padded.
#     - ‚Katze‘ in CHAR(8) wäre also K a t z e $\perp$$\perp$$\perp$

# # Strings variabler Länge
# - VARCHAR(n)
# - Es werden n+1 Byte reserviert.
# - Variante 1
#     - Byte 1 speichert Länge–=> Länge ist maximal 255 Byte–Oft also VARCHAR(255)
#     - Weitere Bytes speichern Attributwert
#     - Fehlende Bytes werden ignoriert
#     - 5 K a t z e
# - Variante 2
#     - Erste Bytes speichern Attributwert
#     - Hintendran ein null-Wert ($\perp$)
#     - K a t z e $\perp$

# <img src="pictures/Strings-meme.png" alt="Strings-meme" width="500" style="background-color: white;"/>

# # Datum / Bit / Boolean
# 
# - DATE, TIME
#     - i.d.R. repräsentiert als String fester Länge
#     - Problem: Zeit kann mit Bruchteilen von Sekunden gespeichert werden (theoretisch beliebig genau)
#         - Lösung 1: Speicherung als String fester Länge mit maximaler Genauigkeit
#         - Lösung 2: Speicherung als String variabler Länge
# - BIT(n)
#     - 8 Bit pro Byte
#     - Letzte Bits ignorieren, falls n nicht durch 8 teilbar ist
#     - BIT(12): 010111110011 wird zu 01011111, 00110000
# - BOOLEAN
#     - 8 Bit: 
#         - 00000001 und 00000000
#         - oder 11111111 und 00000000

# # Datensätze

# ## Datensätze fester Länge
# 
# - Jeder Datensatz hat ein Schema.
#     - Namen und Datentypen der Felder 
#     - Offset im Datensatz
#     - Anmerkung: JEDER Datensatz!–Realisiert i.d.R. als Pointer auf das Schema
#     
# ```
# CREATE TABLE Schauspieler (
#     Name CHAR(30),
#     Adresse VARCHAR(255),
#     Geschlecht CHAR(1),
#     Geburtstag DATE );
# ```
# 
# - Alle haben feste Länge
#     - 30 Byte + 256 Byte + 1 Byte + 10 Byte = 297 Byte

# ## Versatz zur Effizienz
# 
# - Felder beginnen am besten bei Hauptspeicheradressen, die ein Vielfaches von 4 (bzw. 8) sind.
#     - Manchmal sogar Pflicht
# - Für Festplatte eigentlich egal
#     - Aber eingelesener Datensatz landet auf einem Speicherplatz mit entsprechender Adresse
#         - Vielfaches von 4
#         - Vielfaches von 2n
#     - Entsprechend versetzt sind die anderen Felder

# <img src="pictures/Versatz-zur-Effizienz.png" alt="Versatz-zur-Effizienz" width="500" style="background-color: white;"/>

# # Speicherung der Metadaten
# 
# - Metadaten eines Datensatzes, z.B.
#     - Schema bzw. Pointer auf ein Schema□Länge des Datensatzes
#     - Timestampder letzten Änderung bzw. des letzten Lesens
# - Lösung: Header vor den Datensatz

# <img src="pictures/Speicherung_Metadaten.png" alt="Speicherung_Metadaten" width="500" style="background-color: white;"/>

# ## Aufteilung in Blöcke
# 
# - Block header(optional)
#     - Links auf andere Blocks (z.B. Index)
#     - Rolle dieses Blocks (im Index)
#     - Relation der Tupel
#     - Verzeichnis der offsetsder Datensätze
#     - Block ID (gleich)□Timestampder letzten Änderung / des letzten Lesens
# - Einfachster Fall: Alle Datensätze aus gleicher Relation, aller fester Länge
# - Beispiel
#     - Datensatz 316 Byte
#     - Block 4096 Byte, 12 davon als Header
#     - => 12 Datensätze und 292 verlorene Byte

# <img src="pictures/Aufteilung_in_Blöcke.png" alt="Aufteilung_in_Blöcke" width="500" style="background-color: white;"/>

# # Adressierung

# ## Virtueller Speicher vs. Festplatte
# 
# - Block im Hauptspeicher
#      - Block-Adresse ist im virtuellen Adressraum
#      - Zeigt auf erstes Byte des Blocks
#      - Datensatz-Adresse zeigt auf erstes Byte des Datensatzes
# - Block auf Festplatte□Speicherort im gesamten System des DBMS–Disk ID, Zylinder#, Spur#, Sektor, ...
#     - Datensatz: Block + offsetdes ersten Bytes

# ## Adressraum des Servers
# 
# - Blocks und Offsets innerhalb von Blocks
# - Variante 1: Physische Adressen
#     - Rechner ID
#     - Disk ID 8-16 Byte
#     - Zylinder# 8-16 Byte
#     - Spur# (bei mehr als einer Oberfläche)
#     - Sektor#
#     - (Offset innerhalb des Blocks)
# - Variante 2: Logische Adressen
#     - Beliebiger Byte String
#     - Mapping tableübersetzt diese Adresse in eine physische Adresse.

# ## Logische Adressen
# 
# - Warum die Indirektion?
#     - Flexibilität bei der Umorganisation von Daten–Änderungen nur auf der mappingtable
# - Hybride Adressierung
#     - Physische Adresse für einen Block□Logische Adresse für einen Datensatz in dem Block–Z.B. Schlüsselwert

# <img src="pictures/Logische-Adressen.png" alt="Logische-Adressen" width="500" style="background-color: white;"/>

# ## Hybride Adressierung
# 
# - Idee: Physische Adressen zu einem Block. Block selbst speichert offsettable.
# - Auffüllen des Blocks von hinten bei Datensätzen variabler Länge
#     - Anzahl der Datensätze nicht fix=> Größe des headerskann offen gelassen werden
# - Vorteile der Flexibilität (auch ohne Mapping table)
#     - Innerhalb eines Blocks kann umorganisiert werden
#     - Datensatz kann sogar Blöcke wechseln–Speicherung der neuen Adresse in der offsettable

# <img src="pictures/Hybride-Adressierung.png" alt="Hybride-Adressierung" width="500" style="background-color: white;"/>

# ## Columnar Storage
# 
# - Idee: Datensätze speichern Spalten statt Tupel
# - Überspannen idRmehrere Blöcke
# - Reihenfolge der Werte erlaubt Rekonstruktion
#     - Alternativ: Tupel-Idsmitspeichern
# - Beispiel: 2 Datensätze: (4,7,9) und (a,b,c)
#     - Alternativ: ((2,7),(1,4),(3,9)) und ((3,c),(1,a),(2,b))
#     - Vorteil: Umsortierung möglich->Komprimierung
# - Anwendungsfall: OLAP (Online analyticalprocessing)
#     - Die meisten Anfragen benötigen alle oder viele Werte einer Spalte
#     - Tupelrekonstruktionaufwändig
# - Diskussion Komprimierung
#     - Vorteil: Weniger Diskkosten; weniger I/O
#     - Nachteile: Funktioniert nur gut auf großen Datenmengen, aber effizienter Tupelzugrifferlaubt nur blockweise Komprimierung; Indizierung schwierig

# # Daten variabler Länge

# ## Variable Länge
# 
# - Bisher: Alles hat feste Länge.
# - Aber es gibt:
#     - Felder variabler Länge
#         - Adresse VARCHAR(255) wird selten voll ausgeschöpft
#     - Datensätze variabler Länge
#         - Ergänzung von Datensätzen um Felder
#         - Schauspieler, die auch Regie führen
#      - Riesige Felder
#         - GIF, MPEG–Passen nicht mehr auf einen Block

# ## Finden von Feldern
# 
# - Datensatz muss Informationen speichern, um jedes Feld aufzufinden.
# - Idee: Felder fester Länge an den Anfang des Datensatzes
# - Header speichert
#     - Länge des Datensatzes
#     - Pointer (offsets) zu den Anfängen aller Felder variabler Länge
#         - Pointer zum ersten kann sogar gespart werden.

# <img src="pictures/Finden-von-Fehlern.png" alt="Finden-von-Fehlern" width="500" style="background-color: white;"/>

# ## Datensätze variabler Länge
# 
# - Anwendungsfall: Es ist unbekannt welche undwie viele Felder der Datensatz haben wird.
# - Taggedfields(getaggteFelder)
#     - Feldname (Attributname)
#     - Feldtyp
#     - Feldlänge
#     - Feldwert
# - Nützlich bei
#     - Informationsintegration: Es ist noch unbekannt welche Felder von Quellen hinzukommen.
#     - Dünn besetzte Datensätze: Tausende Attribute, nur wenige haben Werte

# <img src="pictures/Datensätze-variabler-Länge.png" alt="Datensätze-variabler-Länge" width="500" style="background-color: white;"/>

# ## Anwendungsfalls SparseDataBeispiel: LinkedOpen Data

# <img src="pictures/Linked-open-data.png" alt="Linked-open-data" width="500" style="background-color: white;"/>

# ## Microsoft SQL Server: SPARSE columns
# 
# ```
# CREATE TABLE DocumentStore(
#     DocIDintPRIMARY KEY,
#     Title varchar(200) NOT NULL,
#     ProdSpecvarchar(20) SPARSE NULL,
#     ProdLocsmallintSPARSE NULL)
# ```
# 
# - Betrifft nur physische Ebene (wie Indizes)
# - Benötigt für nicht-NULL Werte mehr Platz

# <img src="pictures/SPARSE-columns.png" alt="SPARSE-columns" width="500" style="background-color: white;"/>

# ## Zu große Datensätze
# 
# - Idee: Spannedrecordsüberspannen mehr als einen Block.
# - Für übergroße Felder
#     - „Riesige“ Felder (Mega-oder Gigabyte) gleich
# - Für Datensatzgrößen, die viel Platz verschwenden
#     - Z.B. 51% eines Blocks => 49% verschwendet
# - Datensatzfragment
#     - Falls zu einem Datensatz mehr als ein Fragment gehört, ist er spanned.
# - Zusätzliche Informationen im Header
#     - Bit sagt ob Fragment oder nicht
#     - Bits sagen ob erstes oder letztes Fragment
#     - Zeiger zum nächsten und/oder vorigen Fragment–Doppelt verkettet Liste

# ## BLOBs
# 
# - BLOB = Binary Large Object
# - Bilder/Grafiken: JPEG, GIF
# - Audio: mp3, ..
# - Filme: MPEG, ...
# - Probleme
#     - Speicherung: Mehr als ein Block nötig–Sequenz von Blöcken/Zylindern
#     - Realtime: Lesegeschwindigkeit einer Disk nicht ausreichend => Verteilung auf mehrere Disks
# - Lesen 
#     - Anweisung, einen (ganzen) Datensatz zu lesen, ist nicht mehr gültig
#     - Stattdessen: Kleiner Teil eines Datensatzes lesen
#     - Navigation innerhalb des BLOBs (z.B. „Sprung zur 45ten Minute“) => spezielle Indexstrukturen
# - CLOB = CharacterLarge Object

# # Datensatzänderungen

# ## Einfügen mit Platz
# 
# - Einfacher Fall: Keine Ordnung verlangt
#      - Suche freien Platz auf einem Block (oder suche freien Block).
#      - Füge Datensatz ein.
# - Schwierigerer Fall: Ordnung (z.B. nach Primärschlüssel) ist verlangt.
#      - Suche entsprechenden Block
#      - Falls Platz frei ist, bewege Datensätze auf Block, so dass neuer Datensatz an entsprechende Stelle eingefügt werden kann.

# <img src="pictures/Einfügen-mit-Platz.png" alt="Einfügen-mit-Platz" width="500" style="background-color: white;"/>

# ## Einfügen ohne Platz
# 
# - Variante 1: Suche Block in der Nähe
#     - Voriger oder nächste Block 
#     - Bewege ersten oder letzen Datensatz zu jeweils neuem Block
#         - Weiterleitungsadresse in altem Block („Nachsendeauftrag“)
#         - Bewege gegebenenfalls Datensätze in beiden Blöcken hin und her.
#     - Füge neuen Datensatz ein.
# - Variante 2: Erzeuge Overflow Block
#     - Designierter Overflow Block
#     - Adresse im headerdes ursprünglichen Blocks
#     - Overflow Block kann selbst wiederum einen Overflow Block haben.

# ## Löschen
# 
# - Nach Löschen 
#     - Datensätze im Block verschieben um freien Platz zu konsolidieren
#     - Oder: Im headereine Liste mit freien Plätzen verwalten
#     - Oder: Verkette Liste der freien Plätze
# - Reorganisation der Overflow Blocks möglich.
# - Grabsteine (tombstones)
#     - Es könnte noch Pointerauf den zu löschenden Datensatz geben.
#     - Grabstein hinterlassen (3 Varianten)
#         - Null-Pointer im header
#         - Null-Pointer in mappingtable
#         - Grabstein am Anfang der Datensätze
#     - Müssen (im Allgemeinen) ewig erhalten bleiben
#         - Bis Re-Organisation der Datenbank

# <img src="pictures/Löschen-meme.png" alt="Löschen-meme" width="500" style="background-color: white;"/>

# ## Update
# 
# - Bei fester Länge kein Problem
# - Bei variabler Länge
#     - Gleiche Probleme wie beim Einfügen

# <img src="pictures/update.png" alt="update" width="500" style="background-color: white;"/>
