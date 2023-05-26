#!/usr/bin/env python
# coding: utf-8

# # Speicherung

# Physische Speicherstrukturen

# Zoom in die interne Ebene: Die 5-Schichten Architektur
# <img src="pictures/5-Schichten-Architektur.png" alt="5-Schichten-Architektur" width="500" style="background-color: white;"/>

# Übersicht
# 1. Speicherhierarchie
# 2. Disks
# 3. Effiziente Diskoperationen
#     - TPMMS
# 4. Zugriffsbeschleunigung
# 5. Diskausfälle
# 
# <img src="pictures/Speicherhierachie.png" alt="Speicherhierachie" width="500" style="background-color: white;"/>

# Speicherhierachie - Kosten
# 
# <img src="pictures/Speicherhierachie-Kosten.png" alt="Speicherhierachie-Kosten" width="500" style="background-color: white;"/>

# Speicherhierarchie – Zugriffszeiten
# 
# <img src="pictures/Speicherhierachie-Zugriffszeiten.png" alt="Speicherhierachie-Zugriffszeiten" width="500" style="background-color: white;"/>
# Zahlen aus dem Foliensatz von Viktor Leis 2019

# Speicherhierarchie – Kapazitäten
# 
# <img src="pictures/Speicherhierachie-Kapazitäten.png" alt="Speicherhierachie-Kapazitäten" width="500" style="background-color: white;"/>
# Zahlen aus dem Foliensatz von Viktor Leis 2019

# Pat Helland, DEBS 2022
# 
# <img src="pictures/PatHelland-DEBS2022.png" alt="PatHelland-DEBS2022" width="500" style="background-color: white;"/>
# <img src="pictures/PatHelland-DEBS2022_2.png" alt="PatHelland-DEBS2022" width="500" style="background-color: white;"/>

# ## Virtueller Speicher
# Jede Anwendung verwaltet einen virtuellen Adressraum
# - Kann größer als tatsächlich verfügbarer Hauptspeicher sein
# - 32-bit Adressraum -> 2^32 unterschiedliche Adressen darstellbar
#   - Jedes Byte hat eigene Adresse = max. Hauptspeichergröße 4GB
# - 64-bit Adressraum -> max. 16 Exabyte
# - Aber: meist weniger Hauptspeicher vorhanden
# - Abhilfe: Daten werden auf Disk ausgelagert
#   - Lesen und Schreiben von ganzen Blöcken zwischen Hauptspeicher und Festplatte (Blockgröße 4 – 56 KB) -> Seiten des virtuellen Speichers
#   - Verwaltet durch Betriebssystem
# - Datenbanken verwalten oft Positionen der Daten auf Festplatte selbst (O_DIRECT).
# - Eigene Bufferpoolmanager

# ## Sekundärspeicher: Festplatten
# - Nicht nur (magnetische) Festplatten; auch optische (read-only) Speicher
# - Im Wesentlichen wahlfreier Zugriff (random access)
#   - Zugriff auf jedes Datum kostet gleich viel
#   - Aber: Erst einmal hinkommen!
# - HDDs halten Daten aus Cache / Seiten des virtuellen Speichers von Anwendungsprogrammen
# - HDDs halten Daten aus Dateisystem
# - Operationen
#   - Disk-read (Kopieren eines Blocks in Hauptspeicher)
#   - Disk-write (Kopieren eines Blocks aus dem Hauptspeicher)
#   - Beides: Disk-I/O

# ## Festplatten - Puffer
# - Bufferpool Manager puffert Teile von Dateien
#   - In Blockgröße (z.B. 4 KB)
#   <img src="pictures/Festplatten-Puffer.png" alt="Festplatten-Puffer" width="500" style="background-color: white;"/>
# - DBMS verwaltet Positionen der Blöcke innerhalb der Datei selbst!
# - Dauer für Schreiben oder Lesen eines Blocks: 10 - 30 ms
#   - In dieser Zeit viele Millionen Prozessoranweisungen ausführbar
#   - I/O-Zeit dominiert Gesamtkosten
#   - Deshalb am besten: Block sollte bereits im Hauptspeicher sein!

# ## Tertiärspeicher: Magnetbänder
# 
# - Viele Terabyte (10^12 Bytes) Verkaufsdaten
# - Viele Petabyte (10^15 Bytes) Satellitenbeobachtungsdaten
# - Festplatten ungeeignet
#     - Zu teuer (Wartung, Strom)
# - Vergleich Tertiärspeicher – Sekundärspeicher
#     - I/O-Zeiten wesentlich höher
#     - Kapazitäten wesentlich höher
#     - Kosten pro Byte geringer
# - Kein wahlfreier Zugriff (random access)
#     - Zugriffszeiten hängen stark von der Position des jeweiligen Datensatzes ab (in Bezug auf die aktuelle Position des Schreib-/Lesekopfes)
# 
# <img src="pictures/Magnetband.png" alt="Magnetband" width="500" style="background-color: white;"/>

# ## Tertiärspeicher
# 
# - Ad-hoc Speicherung auf Magnetbändern
#   - Magnetbandspulen
#   - Kassetten
#   - Von Menschenhand ins Regal
#   - Gut beschriften!
# - Magnetbandroboter (Silo)
#   - Roboter bedient Magnetbänder (Kassetten)
#   - 10 mal schneller als Mensch
# - CD / DVD - Juke-Boxes
#   - Roboterarm extrahiert jeweiliges Medium (CD oder DVD)
#   - Hohe Lebensdauer (30 Jahre)
#   - Wahrscheinlicher, dass kein Lesegerät mehr existiert
#   
#    <img src="pictures/Tertiärspeicher.png" alt="Tertiärspeicher" width="500" style="background-color: white;"/>

# ## Moore's Law (Gordon Moore, 1965)
# - Exponentielles Wachstum vieler Parameter
# - Verdopplung alle 18 Monate
#   - Prozessorgeschwindigkeit (# instr. per sec.)
#   - Hauptspeicherkosten pro Bit
#   - Anzahl Bits pro cm² Chipfläche
#   - Diskkosten pro Bit (halbiert)
#   - Kapazität der größten Disks
# - Aber: Sehr langsames Wachstum von
#   - Zugriffsgeschwindigkeit im Hauptspeicher
#   - Rotationsgeschwindigkeit von Festplatten
# - Folge: Latenz-Anteil wächst
#   - Bewegung von Daten innerhalb der Speicherhierarchie erscheint immer langsamer (im Vergleich zur Prozessorgeschwindigkeit)
#   
#   <img src="pictures/moores-law_1.png" alt="moores-law_1" width="500" style="background-color: white;"/>
#   <img src="pictures/moores-law_2.png" alt="moores-law_2" width="500" style="background-color: white;"/>
#     <img src="pictures/moores-law_3.png" alt="moores-law_3" width="500" style="background-color: white;"/>
#   <img src="pictures/moores-law_4.png" alt="moores-law_4" width="500" style="background-color: white;"/>
# 
# See also: http://www.computerhistory.org/timeline/memory-storage/ 

# ## Plattenkapazität
# 
# <img src="pictures/Plattenkapazität.png" alt="Plattenkapazität" width="500" style="background-color: white;"/>
# 
# http://en.wikipedia.org/wiki/Hard_disk_drive
# 
# 
# 
# 
# But: Access times are leveling
# 
# Maximum sustained bandwidth trend
# 
# <img src="pictures/Access_times.png" alt="Access_times" width="500" style="background-color: white;"/>
# 
# 
# Average seek time trend
# 
# <img src="pictures/Seek_times.png" alt="Seek_times" width="500" style="background-color: white;"/>
# 
# 
# http://www.storagenewsletter.com/news/disk/hdd-technology-trends-ibm

# ## SSDs
# 
#   - Persistente Speicherung basierend auf Halbleitern
#   - Keine mechanische Bewegung/Rotation
#   - Hoher Grad an Parallelität
#   
#   <img src="pictures/SSDs.png" alt="SSDs" width="500" style="background-color: white;"/>

# ## HDDs vs. SSDs
# 
# Vorteile von SSDs:
# - Schnelles Hochfahren, da keine Drehung erforderlich.
# - Schneller Random Access ohne Suchzeit.
# - Geringe Leselatenz.
# - Lesezeit immer fast gleich.
# - Keine Probleme durch Dateifragmentierung.
# - Stille Operationen.
# - Weniger Stromverbrauch.
# - Mechanische Zuverlässigkeit.
# - Immun gegen Magnete.
# - Weniger Gewicht.
# - Parallele Lesezugriffe.
# 
# Nachteile von SSDs:
# - Begrenzte Lebenszeit.
# - Verliert Daten nach 2-5 Jahren ohne Strom.
# - Können nicht defragmentiert werden.
# - Teuer.
# - Weniger Kapazität.
# - Asymmetrische Lese/Schreibgeschwindigkeit aufgrund der Flashtechnologie.
# - Leistung von SSDs schwindet mit der Zeit.
# - SATA-basierte SSDs haben sehr langsame Schreiboperationen.
# - DRAM-basierte SSDs benötigen mehr Strom als HDDs.
# - Kein sicheres Überschreiben.
# 
# https://databasearchitects.blogspot.com/2021/06/what-every-programmer-should-know-about.html
# 

# Übersicht
# 1. Speicherhierarchie
# 2. Disks
# 3. Effiziente Diskoperationen
#     - TPMMS
# 4. Zugriffsbeschleunigung
# 5. Diskausfälle
# 
# <img src="pictures/Festplatten_Vergleich_Früher_Heute.png" alt="Festplatten_Vergleich_Früher_Heute" width="500" style="background-color: white;"/>

# ## Aufbau
# 
# - Mehrere (5-10) gleichförmig rotierende Platten (z. B. 3.5" Durchmesser).
# - Für jede Plattenoberfläche (10-20) ein Schreib-/Lese-Kopf.
#   - Gleichförmige Bewegung.
# - Die magnetische Plattenoberfläche ist in Spuren eingeteilt.
# - Spuren sind als Sektoren fester Größe formatiert.
#   - Die Anzahl der Sektoren pro Spur kann sich unterscheiden.
# - Übereinander angeordnete Spuren bilden einen Zylinder.
# 
# <img src="pictures/Aufbau_1.png" alt="Aufbau_1" width="500" style="background-color: white;"/>
# <img src="pictures/Aufbau_2.png" alt="Aufbau_2" width="500" style="background-color: white;"/>
# 
# - Sektoren (1-8 KB) sind die kleinste physische Leseeinheit.
#   - Die Größe wird vom Hersteller festgelegt.
#   - Auf äußeren Spuren befinden sich mehr Sektoren.
# - Lücken zwischen den Sektoren nehmen etwa 10% der Spur ein.
#   - Diese Bereiche sind nicht magnetisiert und dienen zum Auffinden der Sektoranfänge.
# - Blöcke sind die logische Übertragungseinheit.
#   - Sie können aus einem oder mehreren Sektoren bestehen.
#   
#   <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Hard_disk_head.jpg" alt="Aufbau_3" width="500" style="background-color: white;"/>
#   
#     <img src="pictures/Aufbau_4.png" alt="Aufbau_4" width="500" style="background-color: white;"/>
#     
# hier: jede Spur hat gleiche Anzahl an Sektoren

# ## Zone Bit Recording
# 
# - Äußere Zylinder haben mehr Fläche.
#   - => Bei gleichen Radii führt dies zu einer (unnötig) niedrigeren Bitdichte.
# - Lösung: Zonen mit unterschiedlichen Sektoreinteilungen.
# 
# - Wir ignorieren dies.
# 
#     <img src="pictures/ZoneBitRecording.png" alt="ZoneBitRecording" width="500" style="background-color: white;"/>
# 

# ## Disk Controller
# 
# - Kontrolliert eine oder mehrere Disks.
# - Kontrolliert Bewegung der Schreib-/Lese-Köpfe.
#   - Spuren, die zu einem Zeitpunkt unter den Schreib-/Lese-Köpfen sind, bilden Zylinder.
# - Wählt Plattenoberfläche, auf die zugegriffen werden muss.
# - Wählt Sektor innerhalb der Spur, die sich aktuell unter dem Schreib-/Lese-Kopf befindet.
#   - Kontrolliert Start und Ende eines Sektors.
# - Überträgt Bits zwischen Disk und Hauptspeicher bzw. umgekehrt.
# 
# <img src="pictures/DiskController.png" alt="DiskController" width="500" style="background-color: white;"/>

# ## Beispiel - Megatron 747 disk
# 
# - Eigenschaften:
#   - 8 Platten mit 16 Plattenoberflächen (Durchmesser: 3,5“)
#   - 2^16 = 65.536 Spuren pro Oberfläche
#   - Durchschnittlich 2^8 = 256 Sektoren pro Spur
#   - 2^12 = 4.096 Byte pro Sektor
# - Gesamtkapazität:
#   - 16 x 65.536 x 256 x 4.096 = 2^40 Byte = 1 TB
# - Blocks:
#   - Z.B. 2^14 Byte (= 16 KB)
#   - 4 Sektoren pro Block (2^14 / 2^12)
#   - 64 Blöcke pro Spur (2^8 / 2^2) im Durchschnitt
# - Bitdichte (äußerste Spur):
#   - Bits pro Spur: 28 Sektoren x 2^12 Byte = 2^20 = 1024 KB = 8 MBit
#   - Spurlänge (äußerste Spur): 3,5“ · p ≈ 11‘‘
#   - Ca. 10% Lücken → Spurlänge von 9,9‘‘ hält 8 MBits
#   - 840.000 Bits pro Zoll

# ## Disk-Zugriffseigenschaften
# 
# - Voraussetzungen für Zugriff auf einen Block (lesend oder schreibend):
#   - S-/L-Kopf ist bei Zylinder positioniert, der die Spur mit dem Block enthält.
#   - Disk rotiert so, dass Sektoren, die der Block enthält, unter den S-/L-Kopf gelangen.
# - Latenzzeit:
#   - Zeit zwischen Anweisung, einen Block zu lesen, bis zum Eintreffen des Blocks im Hauptspeicher

# ## Latenzzeit
# 
# - Latenzzeit ist Summe aus vier Komponenten:
#     1. Kommunikationszeit zwischen Prozessor und Disk Controller:
#        - Bruchteil einer Millisekunde (ignorieren)
#        - Annahme hier: Keine Konkurrenz
# 
#     2. Seektime (Suchzeit) zur Positionierung des Kopfes unter richtigem Zylinder:
#        - Zwischen 0 und 40 ms (Zeit proportional zum zurückgelegten Weg)
#        - Startzeit (1 ms), Bewegungszeit (0 – 40 ms), Stopzeit (1 ms)
# 
#     3. Rotationslatenzzeit zur Drehung der Disk bis erster Sektor des Blocks unter S-/L-Kopf:
#        - Durchschnittlich ½ Umdrehung (4 ms)
#        - Optimierung durch Spur-Cache im Disk-Controller möglich
# 
#     4. Transferzeit zur Drehung der Disk bis alle Sektoren und die Lücken des Blocks unter S-/L-Kopf passiert sind:
#        - Ca. 16 KB-Block in ¼ ms (gleich genauer)

# ## Schreiben und Ändern von Blöcken
# 
# - Schreiben von Blöcken:
#   - Vorgehen und Zeit: Analog zum Lesen
#   - Zur Prüfung, ob Schreiboperation erfolgreich war, muss eine Rotation gewartet werden (Nutzung von Checksums (später))
# 
# - Ändern von Blöcken:
#     - Nicht direkt möglich
#       1. Lesen des Blocks in Hauptspeicher
#       2. Ändern der Daten
#       3. Zurückschreiben auf Festplatte
#       4. evtl. Korrektheit der Schreiboperation überprüfen
#   - Zeit: t_read + t_write
#   - aber: mit Glück ist Kopf noch in der Nähe (t_write ist billiger)

# ## Beispiel – Megatron 747 Disk
# 
# Wie lange dauert es, einen Block (16 KB = 16 384 Byte) zu lesen?
# 
# Here's the information about the time it takes to read a block with bullet points:
# 
# - Umdrehungsgeschwindigkeit: 7200 U · min-1
#   -> Eine Umdrehung in 8,33 ms
# 
# - Seektime:
#   - Start und Stopp zusammen: 1ms
#   - 1ms pro 4000 Zylinder, die überbrückt werden
#     1. Minimum (0 Zylinder): 0 ms
#     2. 1 Track: 1,00025 ms
#     3. Maximum (65.536 Zylinder): 65536/4000 + 1 = 17,38 ms
# 
# - Minimale Zeit, um den Block zu lesen:
#   - S-/L-Kopf steht über richtiger Spur und Platte ist schon richtig rotiert
#   - 4 Sektoren und 3 Lücken sind zu lesen
#   - 256 Lücken und 256 Sektoren pro Spur (durchschnittlich)
#   - Lücken bedecken 36° (10%), Sektoren bedecken 324° des Kreises (360°)
#   - 324° x 4 / 256 + 36° x 3 / 256 = 5,48° des Kreises durch Block bedeckt
#   - (5,48° / 360°) · 8,33 ms = 0,13 ms
# 
# - Maximale Zeit: Präsenzübung (25,84 ms)
# - Durchschnittliche Zeit: selber forschen und nachrechnen (10,76 ms)

# ## Übersicht
# 1. Speicherhierarchie
# 2. Disks
# 3. Effiziente Diskoperationen
#     - TPMMS
# 4. Zugriffsbeschleunigung
# 5. Diskausfälle
# 
# <img src="pictures/Speicherhierachie.png" alt="Speicherhierachie" width="500" style="background-color: white;"/>

# ## Algorithmen vs. DBMS
# 
# - Annahme bei Algorithmen:
#   - RAM-Berechnungsmodell
#     - Gesamte Daten passen in Hauptspeicher
#     - Daten befinden sich schon im Hauptspeicher
# 
# - Annahme bei Implementierung von DBMS:
#   - I/O-Modell: Gesamte Daten passen nicht in Hauptspeicher
# 
# - Externspeicher-Algorithmen funktionieren oft anders:
#   - Ein guter Externspeicher-Algorithmus muss nicht der beste Algorithmus lt. RAM-Modell sein
#   - Entwurfsziel: I/O vermeiden
# 
# - Gleiches kann auch für Hauptspeicher-Algorithmen gelten:
#   - Ausnutzen des Caches
#     - Cachegröße berücksichtigen
#     - Lokalität beachten („maximiere“ Anzahl der Cache Hits)

# ## I/O-Modell
# 
# - Beispiel: Einfaches DBMS
#     - Zu groß für Hauptspeicher
#     - Eine Disk, ein Prozessor, viele konkurrierende Nutzer / Anfragen
# 
# - Disk-Controller hält Warteschlange mit Zugriffsaufforderungen
#   - Abarbeitungsprinzip: First-come-first-served
#   - Jede Aufforderung erscheint zufällig
#     - Kopf ist also an zufälliger Position
# 
# Dominanz der I/O-Kosten
#   - Kosten des Lesens und Bewegens eines Blocks zwischen Disk und Hauptspeicher sind wesentlich größer als Kosten der Operationen auf den Daten im Hauptspeicher.
#   
#   -> Anzahl der Blockzugriffe (lesend und schreibend) ist eine gute Approximation der Gesamtkosten und sollten minimiert werden.
#   
#   

# ## Beispiel für das I/O-Modell (1): Indizes
# 
# - Relation R
# - Anfrage sucht nach dem Tupel t mit Schlüsselwert k
# - Index auf Schlüsselattribut
#   - Datenstruktur, die schnellen Zugriff auf Block ermöglicht, der t enthält
#   - Variante A des Index sagt nur, in welchem Block t liegt.
#   - Variante B sagt zusätzlich, an welcher Stelle innerhalb des Blocks t liegt.
# - Frage: Welche Indexvariante ist besser geeignet?
# 
# - Durchschnittlich 11 ms um 16 KB-Block zu lesen
#   - In dieser Zeit: viele Millionen Prozessoranweisungen möglich
# - Suche nach k auf dem Block kostet höchstens Tausende Prozessoranweisungen – selbst mit linearer Suche
# - Aber: Zusätzliche Informationen in Variante B nehmen Platz ein (höhere I/O-Kosten).

# ## Beispiel für das I/O-Modell (2): Sortierung
# 
# - Relation R
#   - 10 Millionen Tupel
#   - Verschiedene Attribute, eines davon ist Sortierschlüssel
#     - Nicht unbedingt eindeutig (kein Primärschlüssel)
#     - Hier vereinfachende Annahme: Sortierschlüssel ist eindeutig
#   - Gespeichert auf Diskblöcken der Größe 16.384 = 214 Byte
#   - Annahme: 100 Tupel passen in einen Block
#     - Tupelgröße ca. 160 Byte
#     - R belegt 100.000 Blöcke (1,64 Mrd. Bytes) auf der Festplatte
# - Verwendete Festplatte: 1 x Megatron 747
# - Verfügbarer Hauptspeicherpuffer: 100 MB (= 100 · 2^20)
#   - (100*2^20)/(2^14) = 6400 Blöcke von R passen in den Hauptspeicher
# - Ziel: Sortierung soll Anzahl der Lese- und Schreiboperationen minimieren
#   - Wenig "Durchläufe" durch die Daten

# ## Merge Sort
# 
# - Hauptspeicher-Algorithmus (Divide-and-Conquer Algorithmus)
# - Idee: Merge l ≥ 2 sortierte Listen zu einer größeren sortierten Liste.
#   - Wähle aus den sortierten Listen stets das kleinste Element und füge es der großen Liste hinzu.
# 
# | | Liste 1 | Liste 2 | Outputliste |
# |-|-|-|-|
# | 1. | 1,3,4,9 | 2,5,7,8 | - |
# | 2. | 3,4,9 | 2,5,7,8 | 1 |
# | 3. | 3,4,9 | 5,7,8 | 1,2 |
# | 4. | 4,9 | 5,7,8 | 1,2,3 |
# | 5. | 9 | 5,7,8 | 1,2,3,4 |
# | 6. | 9 | 7,8 | 1,2,3,4,5 |
# | 7. | 9 | 8 | 1,2,3,4,5,7 |
# | 8. | 9 | - | 1,2,3,4,5,7,8 |
# | 9. | - | - | 1,2,3,4,5,7,8,9 |
# 
# - Rekursion
#   - Teile eine Liste mit mehr als einem Element beliebig in zwei gleich lange Listen L1 und L2 auf.
#   - Sortiere L1 und L2 rekursiv.
#   - Merge L1 und L2 zu einer sortierten Liste zusammen.
# - Aufwand (Eingabegröße |R| = n)
#   - Mergen zweier sortierter Listen L1, L2: O(|L1| + |L2|) = O(n)
#   - Rekursionstiefe: log2 n
#     - In jedem Rekursionsschritt halbiert sich die Listenlänge.
#     - Nach i Schritten sind noch n / 2^i Elemente in der Liste.
#   - Ergo: O(n log n)
#     - Trifft untere Schranke für das vergleichsbasierte Sortieren.

# ## Two-Phase, Multiway Merge-Sort (TPMMS)
# 
# - TPMMS wird in vielen DBMS eingesetzt.
# - Besteht aus zwei Phasen:
#   - Phase 1:
#     - Lade jeweils so viele Tupel, wie in den Hauptspeicher passen.
#     - Sortiere die Teilstücke im Hauptspeicher.
#     - Schreibe die sortierten Teilstücke zurück auf die Festplatte.
#     - Ergebnis: viele sortierte Teillisten auf der Festplatte.
#   - Phase 2:
#     - Merge alle sortierten Teillisten zu einer einzigen großen Liste.
#     
# ## TPMMS - Phase 1
# 
# - Rekursionsanfang nun nicht nur mit einem oder zwei Elementen!
# - Sortierung der Teillisten z.B. mit Quicksort (worst-case, sehr selten O(n^2))
# 
# 1. Fülle den verfügbaren Hauptspeicher mit Diskblöcken aus der Originalrelation.
# 2. Sortiere die Tupel, die sich im Hauptspeicher befinden.
# 3. Schreibe die sortierten Tupel auf neue Blöcke der Disk.
#    - Das Ergebnis ist eine sortierte Teilliste.
# - Beispiel:
#    - 6,400 Blöcke im Hauptspeicher; insgesamt 100,000 Blöcke
#    - 16 Füllungen des Hauptspeichers erforderlich (letzte Füllung ist kleiner)
#    - Aufwand: 200,000 I/O-Operationen
#      - 100,000 Blöcke lesen
#      - 100,000 Blöcke schreiben
#    - Zeit: durchschnittlich 11 ms pro I/O-Operation
#      - 11 ms * 200,000 = 2,200 s = 37 min
#      - Prozessorzeit für das Sortieren ist vernachlässigbar.
# 
# ## TPMMS - Phase 2
# 
# - Naive Idee: paarweises Mergen von k sortierten Teillisten
#    - Erfordert 2 * log(k) Mal Lesen und Schreiben jedes Blocks (jedes Tupels)
#    - Im Beispiel: Ein Durchlauf für 16 sortierte Teillisten, einer für 8, einer für 4 und ein letzter für 2 sortierte Teillisten
#    - Insgesamt ist jeder Block an 8 I/O-Operationen beteiligt
# - Bessere Idee: Lesen nur den ersten Block jeder Teilliste
# 1. Suche den kleinsten Schlüssel unter den ersten Tupeln aller Blöcke.
#    - Lineare Suche (lin.), Priority Queue (log.)
# 2. Bewege dieses Element in den Output-Block (im Hauptspeicher).
# 3. Falls der Output-Block voll ist, schreibe ihn auf die Festplatte.
# 4. Falls ein Input-Block leer ist, lese den nächsten Block aus derselben Liste.
#    - Aufwand: 2 I/O-Operationen pro Block (und Tupel)
#    - Ebenfalls 37 Minuten
# - Laufzeit für TPMMS insgesamt: 74 Minuten
# 
# 
# ## Bemerkungen zur Blockgröße
# 
# - Beobachtung
#     - Je größer die Blockgröße, desto weniger I/O-Operationen werden benötigt.
#     - Die Transferzeit erhöht sich etwas
# - Beispiel bisher
#   - Blockgröße: 16 KB
#   - &#8709; Latenzzeit: 10,88 ms (davon nur 0,253 ms für Transfer)
# - Beispiel neu
#   - Blockgröße: 512 KB (16 * 32)
#   - &#8709; Latenzzeit: 20 ms (davon 8 ms für Transfer)
# - Es werden nur noch 12.500 I/O-Operationen für die Sortierung benötigt.
# - Die Gesamtzeit beträgt 4,16 Minuten.
# - Es ergibt sich eine 17-fache Beschleunigung!
# 
# - Nachteile der Blockvergrößerung:
#     - Blocks sollten sich nicht über mehrere Spuren erstrecken.
#     - Kleine Relationen nutzen nur Bruchteile eines Blocks, was zu Speicherverschwendung führt.
#     - Viele Datenstrukturen für Externspeicher bevorzugen die Aufteilung von Daten auf viele kleine Blöcke.
# 
# 
# ## TPMMS – Grenzen
# 
# - Notation:
#   - Blockgröße: B Bytes
#   - Hauptspeichergröße (für Blocks): M Bytes
#   - Tupelgröße: R Bytes
# - M / B Blöcke passen in den Hauptspeicher.
# - In Phase 2 wird Platz für einen Outputblock benötigt.
# - Phase 1 kann also genau (M / B) - 1 sortierte Teillisten erzeugen.
# - Ebenso oft kann der Hauptspeicher mit Tupeln gefüllt und sortiert werden (in Phase 1).
#   - Jede Füllung enthält M / R Tupel.
# - Maximal (M / R) * ((M / R) - 1) Tupel können sortiert werden.
# - Unser Beispiel:
#   - M = 104,857,600 Bytes
#   - B = 16,384 Bytes
#   - R = 160 Bytes
#   - Zusammen: maximale Eingabegröße von 4.2 Milliarden Tupeln (ca. 0.67 Terabyte)
# 
# <img src="pictures/TPMMS-Grenzen-Visualisierung.png" alt="TPMMS-Grenzen-Visualisierung" width="500" style="background-color: white;"/>
# 
# - Falls die Eingaberelation noch größer ist:
#   - Füge eine dritte Phase hinzu.
#   - Nutze TPMMS, um sortierte Listen der Größe M^2/RB zu erzeugen.
#   - Phase 3: Merge maximal M/B - 1 solcher Listen zu einer sortierten Liste zusammen.
# - Insgesamt M^3/RB^2 Tupel sind sortierbar.
# - Bezogen auf unser Beispiel: maximale Eingabegröße von 27 Billionen Tupeln (ca. 4.3 Petabytes).
# - Globale Betrachtung: Die zweite Phase ist die zusätzliche Phase.

# ## Zugriffsbeschleunigung
# 
# - Annahmen bisher:
#   - Nur eine Disk.
#   - Zufällige Blockzugriffe (viele kleine Anfragen).
# - Verschiedene Verbesserungsideen:
#   - Blöcke, die gemeinsam gelesen werden, auf dem gleichen Zylinder platzieren, um die Suchzeit zu reduzieren.
#   - Verteilung der Daten auf mehrere (kleine) Disks:
#     - Unabhängige Schreib-/Leseköpfe.
#     - Dadurch ermöglicht: mehrere (unabhängige) Blockzugriffe gleichzeitig.
#   - Spiegelung von Daten auf mehrere Disks.
#   - Verwendung eines Disk-Scheduling-Algorithmus.
#   - Prefetching von Blöcken.
#     - Ablegen von Blöcken im Hauptspeicher, die möglicherweise demnächst benötigt werden

# ## Daten gemäß Zylinder organisieren
# 
# - Seek time macht ca. 50% der durchschnittlichen Blockzugriffszeit aus.
#   - Megatron 747: seek time zwischen 0 und 40 ms.
# - Idee: Daten, die zusammen gelesen werden, auf dem gleichen Zylinder platzieren.
#   - Z.B. Tupel einer Relation.
#   - Falls ein Zylinder nicht ausreicht, werden mehrere nebeneinander liegende Zylinder genutzt.
# - Beim Lesen einer Relation fällt im besten Fall nur einmal die seek time und Rotationslatenz an.
#   - Minimale Zugriffszeit der Disk wird erreicht: Zugriffszeit wird nur noch durch die Transferzeit bestimmt.
# - Ein Zylinder der Megatron 747 fasst 16 x 64 = 1024 Blöcke.
#   - Dennoch sind 16 Umdrehungen erforderlich (+ 15x seek über je eine Spur).

# ## Zylinderorganisation – Beispiel
# 
# - Megatron 747-Festplatte:
#   - Mittlere Transferzeit pro Block: ¼ ms
#   - Mittlere seek time: 6,46 ms
#   - Mittlere Rotationslatenzzeit: 4,17 ms
#   - Jede der 16 Oberflächen mit 65.536 Spuren á 64 Blöcke (durchschnittlich)
#   
# - Sortierung von 10 Mio. Tupeln mittels TPMMS-Algorithmus dauerte 74 min
#     - 100.000 Blöcke von R belegen 1563 Spuren (98 Zylinder)
#     
# - Phase 1 – Lesen der Blöcke
#     - Hauptspeicher (6400 Blöcke) wird 16 mal gefüllt
#     - Müssen Blöcke von 6400/1024 = 6-7 Zylindern lesen, die aber direkt nebeneinander liegen
#         - nur 1 ms für Spurwechsel
#         
# - Keine Rotationslatenzzeit: Reihenfolge beim Lesen der Tupel egal
# - Zeit pro Füllung:
#     - 6,46 ms + 6 ms + 6x8ms + 1,6s ≈ 1,6 s
#     - (1.seek) + (ca. 6 Spurwechsel) + (6 Rotationen) + (Transfer 6400 Blöcke)
# - 1,6s x 16 Füllungen = 26s (<<18min)
# 
# - Phase 1 – Schreiben: analog zum Lesen ® zusammen 52s (vorher: 37 min)
#     - Achtung: Rotationslatenz eigentlich wieder relevant …
# 
# - Phase 2 wird nicht beschleunigt
#     - Lesen aus verschiedenen (verteilten) Teillisten
#     - Schreiben des Ausgabepuffers zwar sequentiell, aber unterbrochen von Leseoperationen

# ## Mehrere Disks
# 
# - Problem: S-/L-Köpfe einer Festplatte bewegen sich stets gemeinsam
# - Lösung: nutze mehrere Festplatten (mit unabhängigen Köpfen)
#   - Annahme: Disk-Controller, Hauptspeicher, Bus kommen mit höheren Transferraten klar
#   - Resultat: Division aller Zugriffszeiten durch Festplattenanzahl
# - Megatron 737 wie 747, aber nur 2 Platten -> 4 Plattenoberflächen
#   - Ersetze eine Megatron 747 durch vier Megatron 737
#   - Verteile R auf vier Festplatten
# - TPMMS – Phase 1
#   - Lesen: Von jeder Platte nur ¼ der Daten (1600 Blöcke)
#     - Günstige Zylinderorganisation: seek time und Rotationslatenz ≈ 0
#     - 1600 Blöcke × 0,25 ms (mittlere Transferzeit)= 400 ms pro Füllung
#     - 16 Füllungen x 400 ms = 6,4 s
#   - Schreiben: Jede Teilliste wird auf 4 Disks verteilt
#     - Wie Lesen: 6,4 s
#   - Zusammen nur 13 s
#     - statt 52 s zuvor; bzw. statt 37 min bei zufälliger Anordnung
#     
# TPMMS – Phase 2
#   - Verteilung nützt zunächst nichts
#     - Immer wenn Block einer Teilliste abgearbeitet ist, wird nächster Block dieser Teilliste in Hauptspeicher geladen
#     - -> Erst wenn nächster Block vollständig geladen ist, kann Mergen fortgesetzt werden
#   - Trick für Lesen: Mergen kann fortgesetzt werden, bevor Block vollständig im Hauptspeicher geladen wurde (erstes Element genügt schon)
#     - So können potenziell mehrere Blöcke parallel (jeweils einer pro Teilliste) geladen werden -> Verbesserung, wenn diese auf unterschiedlichen Festplatten sind
#     - Vorsicht: Sehr delikate Implementierung
#   - Schreiben des Outputs
#     - Verwende mehrere Output-Blöcke (hier: 4)
#     - Einer wird gefüllt während die anderen drei geschrieben werden (parallel, wenn Schreiben auf unterschiedliche Festplatten)
# - Geschätzte Beschleunigung von Phase 2: Faktor 2 bis 3
#   - Immerhin!

# ## Spiegelung
# 
# - Idee: Zwei oder mehr Festplatten halten identische Kopien
#   - Mehr Sicherheit vor Datenverlust
#   - Beschleunigter Lesezugriff (bei n Festplatten, bis zu n mal so schnell)
# - TPMMS, Phase 2, Lesen: Trick wie bei mehreren Disks klappt nicht immer
#   - Keine Verbesserung, falls Blöcke verschiedener Teillisten auf gleicher Festplatte liegen
#   - Bei Spiegelung kann garantiert werden, dass immer so viele Blöcke unterschiedlicher Teillisten parallel gefüllt werden wie Spiegelungen vorhanden sind
# - Weiterer Vorteil, auch ohne Parallelität (weniger als n Blöcke gleichzeitig)
#   - Auswahl der Festplatte möglich, auf die zugegriffen wird
#   - Wähle die Festplatte, deren Kopf am dichtesten an relevanter Spur steht
# - Anmerkungen
#   - Teuer
#   - Keine Beschleunigung des Schreibzugriffs (aber auch keine Verlangsamung)

# ## Disk Scheduling
# 
# - Idee: Disk-Controller entscheidet, welche Zugriffsanweisungen zuerst ausgeführt werden.
#   - Nützlich bei vielen kleinen Prozessen, je auf wenigen Blöcken
#   - OLTP
#   - Ziel: Erhöhung des Durchsatzes
# - Elevator Algorithmus
#   - Fahrstuhl fährt in Gebäude hoch und runter
#     - Hält an Stockwerken an, wenn jemand ein- oder aussteigen will.
#     - Dreht um, falls weiter oben/unten keiner mehr wartet.
#   - Diskkopf streicht über Oberfläche einwärts und auswärts
#     - Hält an Zylindern an, wenn es eine (oder mehrere) Zugriffsanweisung(en) gibt.
#     - Dreht um, falls in jeweiliger Richtung keine Anweisungen mehr ausstehen.

# ## First-First-First-Servce vs. Elevator Algorithmus
# 
# <img src="pictures/FFFS-vs-Elevator-Algo.png" alt="FFFS-vs-Elevator-Algo" width="500" style="background-color: white;"/>
# 

# ## Elevator Algorithmus
# 
# - Verbesserung steigt mit durchschnittlicher Anzahl von wartenden Anweisungen.
#   - So viele wartende Zugriffsanweisungen wie Anzahl Zylinder
#     - Jeder Seek geht über nur wenige Zylinder
#     - Durchschnittliche seek time (bezogen auf wartende Zugriffsanweisungen) wird verringert
#   - Mehr Zugriffsanweisungen als Zylinder
#     - Mehrere Zugriffsanweisungen pro Zylinder
#     - Sortierung um den Zylinder herum möglich
#     - Dadurch: Reduzierung der Rotationslatenzzeit
# - Nachteil (falls Anzahl wartender Anweisungen groß):
#   - Wartezeiten für einzelnen Zugriffsanweisungen können sehr groß werden!

# ## Prefetching
# 
# - Idee: Wenn man voraussagen kann, welche Blöcke in naher Zukunft gebraucht werden, kann man sie früh (bzw. während man sie sowieso passiert) in den Hauptspeicher laden.
# - TPMMS, Phase 2, Lesen: 16 Blöcke für die 16 Teillisten reserviert
#   - Viel Hauptspeicher frei
#   - Reserviere zwei Blöcke pro Teilliste
#     - Fülle einen Block, während der andere abgearbeitet wird
#     - Wenn einer entleert ist, wechsele zum anderen
#   - Aber: Laufzeit wird nicht verbessert
# - Idee: Kombination mit guter Spur- oder Zylinderorganisation
#   - TPMMS, Phase 1, Schreiben: Schreibe Teillisten auf ganze, aufeinanderfolgende Spuren / Zylinder
#   - TPMMS, Phase 2, Lesen: Lese ganze Spuren / Zylinder, wenn aus einer Liste ein neuer Block benötigt wird.
# - Idee für das Schreiben analog:
#   - Zögere Schreiboperationen hinaus bis ganz Spur / ganzer Zylinder geschrieben werden kann
#   - Verwende mehrere Ausgabepuffer
#     - Während einer auf Festplatte geleert wird, in anderen schreiben

# ## Zusammenfassung
# 
# - Speicherhierarchie
# - Aufbau einer Festplatte
#   - Zylinder, Spuren, Sektoren
# - Latenzzeit von Diskzugriffen
#   - Kommunikationszeit, Suchzeit, Rotationszeit, Transferzeit
# - Berechnung mit IO Modell
#   - Blocklesezeit, Blockgröße, Hauptspeicherkapazität
# - Externspeicher-Algorithmen
#   - Minimierung von IO
#   - TPMMS
#   - Grenzen durch Hauptspeicher festgelegt
# - Fünf "Tricks"
#   - Zylinderorganisation
#   - Verwendung mehrerer Festplatten
#   - Spiegelung
#   - Scheduling mit Elevator Algorithmus
#   - Prefetching
