#!/usr/bin/env python
# coding: utf-8

# # Repräsentation
# 
# Bis hierhin haben wir nur auf einer sehr abstrakten Ebene besprochen, was für Daten wo liegen und wie diese Datenblöcke gelesen werden können. Womit wir uns noch nicht befasst haben, ist wo bestimmte Tupel und Blöcke liegen. Nach unserer intuitiven Vorstellung hoffen wir, dass alle Tupel einer Relation hintereinander im Speicher zu finden sind, das ist aber oftmals nicht der Fall. Nun muss ein Weg gefunden werden diese Tupel und Blöcke zu lesen ohne bei jeder Anfrage die gesamte Festplatte lesen zu müssen.

# Architektur
# 
# <img src="pictures/5-Schichten-Architektur.png" alt="5-Schichten-Architektur" width="500" style="background-color: white;"/>

# In diesem Kapitel befinden wir uns in der Systempufferschnittstelle. Hier geht es hauptsächlich um Seiten-/ und Blockverwaltung, Puffermanagment, sowie Cashing. Für uns ist die relevante Fragestellung, ob unsere gesuchten Tupel im Hauptspeicher sind oder nicht.

# # Aufbau
# 
# Es gibt folgende Dateneinheiten:
# 
# - **Attributwerte** sind Bytelisten oder auch "Felder" fester oder variabler Länge:
# - **Tupel** sind Feldlisten fester oder variabler Länge, auch genannt „Datensätze“
# - **Physische Blöcke** speichern Datensatzmengen/-listen
# - **Relation** sind Mengen von Blöcken und bilden eine „Datei“, dazu gehören auch Indexstrukturen, wenn z.B ein ```PRIMARY KEY``` vorhanden ist
#         

# # Felder etc.
# 
# Die kleinste Dateneinheit sind Attributwerte, diese werden durch „Felder“ (fields) repräsentiert. Die Fragestellungen die in diesem Themenabschnitt thematisiert werden sind:
# 
# - Wie werden Datentypen als Felder repräsentiert?
# - Wie werden Tupelals Datensätze repräsentiert?
# - Wie werden Mengen von Datensätzen oder Tupelnin Blöcken repräsentiert?
# - Wie werden Relationen als Mengen von Blöcken repräsentiert?
# - Was passiert bei variablen Feld-oder Tupellängen?
# - Was passiert wenn ich einen Block nicht einheitlich in Tupeleinteilen kann?
# - Was passiert wenn sich die Größe eines Datensatzes ändert, insbesondere vergrößert?
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
# Alle Daten werden letzendlich als Bitsequenzen dargestellt bzw. werden alle Daten irgendwann als Bytesequenzen dargestellt. Aus GDBS sollten die folgenden Datentypen bekannt sein:
# 
# - **Integer** belegen im Speicher 2 oder 4 Byte 
# - **Float** belegen im Speicher 4 oder 8 Byte 
# - **Strings fester Länge(CHAR(n))**  sind Felder die feste n Bytes zur Verfügung haben. Die fehlenden Byte-Werte werden mit Nullwerten ($\perp$)ge-padded. Beispiel:‚Katze‘ in CHAR(8) wäre also K a t z e $\perp$$\perp$$\perp$
# - **Strings variabler Länge(VARCHAR(n))** werden mit n+1 Byte reserviert. Die Länge kann maximal 255 BYte sein, daher gibt es oft VARCHAR(255). Hier gibt es einmal die Variante, dass das erste Byte die Länge speichert, die weiteren die Attributwerte speichern und die fehlenden Bytes ignoriert werden. Beispiel: 5 K a t z e. Eine andere Variante ist, dass die ersten Bytes die Attributwerte speichern und hintendran ein null-Wert gespeichert wird. Beispiel: K a t z e $\perp$.

# <img src="pictures/Strings-meme.png" alt="Strings-meme" width="500" style="background-color: white;"/>

# # Datum / Bit / Boolean
# 
# **DATE, TIME** werden i.d.R. als String fester Länge repräsentiert. Ein Problem ist jedoch, dass die Zeit mit Bruchteilen von Sekunden gespeichert werden kann (theoretisch beliebig genau). Eine Lösung ist die Speicherung als String fester Länge mit maximaler Genauigkeit eine andere ist die Speicherung als String variabler Länge.
#         
# **BIT(n)** ermöglichen das Arbeiten mit sehr detaillierten Bits, das ist praktisch wenn z.B Hashwerte gespeichert werden sollen. Es gelten 8 Bits pro Byte, falls n nicht durch 8 teilbar ist werden die letzten Bits ignoriert. Beispiel: BIT(12): 010111110011 wird zu 01011111, 00110000.
# 
#     
# **BOOLEAN** setzt sich aus 8 Bits zusammen: Entweder 00000001 und 00000000 oder 11111111 und 00000000.

# # Datensätze
# 
# Mithilfe den thematisierten Datentypen, lassen sich nun Datensätze zusammenstellen.
# 

# ## Datensätze fester Länge
# 
# Jeder Datensatz hat ein Schema bestehend aus Namen und Datentypen der Felder, sowie Offset im Datensatz (Anmerkung: JEDER Datensatz!–Realisiert i.d.R. als Pointer auf das Schema). Betrachten wir das untere Schema für ein Relation Schauspieler, auf relationaler Ebene gibt es vier Attribute, die als Zeichenketten gespeichert werden. Eine sehr einfache Variante um die Größen der Tupel zu berechnen ist immer das Maximum zu wählen.
# <br><br>
# Wir nehmen an alle haben eine feste Länge: 30 Byte + 256 Byte + 1 Byte + 10 Byte = 297 Byte. Somit ist jeder Datensatz gleich groß. Es ist möglich, dass ein Datensatz nicht komplett belegt ist, dann wird dieser Speicher trotzdem besetzt.
#     
# ```
# CREATE TABLE Schauspieler (
#     Name CHAR(30),
#     Adresse VARCHAR(255),
#     Geschlecht CHAR(1),
#     Geburtstag DATE );
# ```
# 
# 

# ## Versatz zur Effizienz
# 
# In der Realität gibt es je nach System noch zusätzliche Anforderungen, wie z.B das Felder am besten bei Hauptspeicheradressen beginnen, die ein Vielfaches von 4 (bzw. 8) sind. Manchmal ist das sogar Pflicht. Dementsprechend müssen die Felder versetzt werden. Für die Festplatte ist das eigentlich egal, aber der eingelesene Datensatz landet auf einem Speicherplatz mit entsprechender Adresse: Vielfaches von 4 oder Vielfaches von 2n. Entsprechend versetzt sind die anderen Felder auch. Im unteren Beispielbild sehen wir zuerst das Feld ohne Versatz und dann mit einem Versatz von zwei.

# <img src="pictures/Versatz-zur-Effizienz.png" alt="Versatz-zur-Effizienz" width="500" style="background-color: white;"/>

# # Speicherung der Metadaten
# 
# Die Metadaten eines Datensatzes,sind z.B. das Schema bzw. Pointer auf ein Schema, Länge des Datensatzes oder Timestamp der letzten Änderung bzw. des letzten Lesens. Diese werden als Header vor dem Datensatz gespeichert. In dem Bild unten reichen 12 Bytes an Speicher für die Metadaten.

# <img src="pictures/Speicherung_Metadaten.png" alt="Speicherung_Metadaten" width="500" style="background-color: white;"/>

# ## Aufteilung in Blöcke
# Um die Datensätze in Blöcke aufzuteilen kann ein Block header benutzt werden, dieser besteht aus:
# - Links auf andere Blocks (z.B. Index)
# - Rolle dieses Blocks (im Index)
# - Relation der Tupel
# - Verzeichnis der offsetsder Datensätze
# - Block ID (gleich)
# - Timestampder letzten Änderung / des letzten Lesens
# 
# Im einfachsten Fall sind alle Datensätze aus der gleichen Relation und haben alle eine feste Länge.
# <br><br>
# Beispiel: Ein Datensatz besteht aus 316 Byte und ein Block aus 4096 Byte,wobei 12 Bytes für je einen Header benötigt werden. Durch Division ergeben sich 12 Datensätze und 292 verlorene Bytes.
# 
# <br><br>
# Dies gilt nur für Datensätze mit fester Länge, die nicht über mehrere Blöcke verteilt sind.

# <img src="pictures/Aufteilung_in_Blöcke.png" alt="Aufteilung_in_Blöcke" width="500" style="background-color: white;"/>

# # Adressierung

# Die Adressierung findet zuerst im Hauptspeicher statt, hier wird die Adresse zuerst angefragt, welche auf die Adresse auf der Festplatte abgebildet wird. Bei einem Block im Hauptspeicher befindet sich die Block-Adresse im virtuellen Adressraum, diese Adresse zeigt auf das erste Byte des Blocks. Wenn ein konkreter Datensatz gesucht wir gibt es zusätzlich es noch eine Datensatz-Adresse, die zeigt auf das erste Byte des Datensatzes.
# Der Block auf der Festplatte ist unser Speicherort. Der genaue Speicherort im ganzen System wird bestimmt wird bestimmt durch die DBMS–Disk ID, Zylinder#(falls HDD vorhanden), Spur#, Sektor, usw.. Unser gefundene Datensatz ist dann der Block und der Offset des ersten Bytes.

# ## Adressraum des Servers
# Es gibt zwei Möglichkeiten um den Adressraum für die Spezifizierung des Blocks zu benutzen:
# 
# - Variante 1: Es werden nur **Physische Adressen** im Hauptspeicher angegeben, bestehend aus folgenden Informationen:
#     - Rechner ID
#     - Disk ID 8-16 Byte
#     - Zylinder# 8-16 Byte
#     - Spur# (bei mehr als einer Oberfläche)
#     - Sektor#
#     - (Offset innerhalb des Blocks)
#   
# - Variante 2: Es werden nur **Logische Adressen** im Hauptspeicher angegeben, welche mit einer Mapping Table in eine physische Adresse übersetzt werden. Eine logische Adresse besteht aus einem beliebigen Byte String. Diese Abstraktion ermöglicht es auch auf Adressen zu verweisen die nicht der physischen Architektur aus Variante 1 entsprechen.
# 
# 
# 

# ## Logische Adressen
# Durch die Indirektion der logischen Adressen, ist die Umorganisation von Daten–Änderungen flexibler, da sie nur auf der Mappingtable stattfindet. Eine logische Adresse bleibt zudem gleich, unabhängig davon ob es sich um eine HDD oder SDD handelt. Eine Hybride Adressierung ist auch möglich, indem es eine physische Adresse für einen Block und eine logische Adresse für einen Datensatz in dem Block, z.B. ein Schlüsselwert gibt.

# <img src="pictures/Logische-Adressen.png" alt="Logische-Adressen" width="500" style="background-color: white;"/>

# ## Hybride Adressierung
# 
# Die Idee bei der hybriden Adressierung ist, dass wir zunächst durch physische Adressen zu einem Block gelangen. Der Block selbst speichert die Offsettable. Das Problem welches hierbei auftreten kann, ist dass Datensätze entfernt und hinzugefügt werden und es zu Fragmentierung kommt. Um dagegen zu wirken, werden Blocksbei Datensätzen variabler Länge von hinten aufgefüllt. Da die Anzahl der Datensätze nicht fix ist, kann die Größe des Headersoffen gelassen werden. Vorteile der Flexibilität (auch ohne Mapping table) sind, dass innerhalb eines Blocks umorganisiert werden kann. Und ein Datensatz sogar Blöke wechseln kann, folglich wird die neue Adresse in der Offsettable gespeichert.

# <img src="pictures/Hybride-Adressierung.png" alt="Hybride-Adressierung" width="500" style="background-color: white;"/>

# ## Columnar Storage
# 
# Bei Columnar Storages ist die Idee, dass die Datensätze Spalten speichern statt Tupel, diese überspannen i.d.R mehrere Blöcke. Die Reihenfolge der Attributwerterte erlaubt die Tupelrekonstruktion alternativ können Tupel-Id's mitgespeichert werden.
# <br><br>
# Beispiel: Es sind 2 Datensätze (4,7,9) und (a,b,c) gegeben. In Columnar Storages würden die Attributwerte hintereinander gespeichert werden, also zuerst 4 dann a usw.
# <br><br>
# Ein Anwendungsfall ist OLAP (Online analyticalprocessing). Hierbei benötigen die meisten Anfragen alle oder viele Werte einer Spalte und die Tupelrekonstruktion ist aufwändig.Was die Komprimierung angeht sind ein Vorteil die geringeren Disk- und I/O-Kosten. Ein Nachteil ist, dass Columnar Storages nur gut auf großen Datenmengen funktionieren, aber effizienter Tupelzugriff erlaubt nur blockweise Komprimierung. Letztlich ist die Indizierung auch schwieriger.

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
