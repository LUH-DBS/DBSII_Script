#!/usr/bin/env python
# coding: utf-8

# # Indizes
# ## Motivation: Platzierung der Tupel in Blöcke
# 
# - Naiv: Beliebig verteilen
#      - Aber: SELECT * FROM R
#      - Jeden Block untersuchen
# - Besser: Tupel einer Relation zusammenhängend speichern
#      - Aber: SELECT * FROM R WHERE a=10
#      - Alle Datensätze betrachten
# - Noch besser: Index
#      - Input: Eigenschaften von Datensätzen (z.B: Feldwert)
#      - „Suchschlüssel“ (Primärschlüssel, Sekundärschlüssel, Sortierschlüssel, Suchschlüssel)
#      - Schneller Output: Die entsprechenden Tupel
#      - Nur wenige Datensätze werden betrachtet

# ## Indizes auf sequenziellen Dateien
# 
# ### Einfachste Form eines Index
# 
# - Gegeben sortierte Datei (data file)
#      - Sequenzielle Datei
#      
# - Indexdatei enthält Schlüssel-Pointer Paare
#      - Schlüsselwert K ist mit einem Pointer verbunden
#      - Pointer zeigt auf Datensatz, der den Schlüsselwert K hat
#      
# - Dichtbesetzter Index
#      - Ein Eintrag im Index für jeden Datensatz
#          
# - Dünnbesetzter Index
#     - Nur einige Datensätze sind im Index repräsentiert.
#     - Z.B. ein Eintrag pro Block
# 
# 

# ### Sequenzielle Dateien
# 
# - Index kann sich auf Sortierung des Schlüsselattributs verlassen
#      - Hier: Schlüssel ist Suchschlüssel
#      - Oft: Suchschlüssel = Primärschlüssel

# ### Dichtbesetzte Indizes
# 
# - Blocksequenz mit Schlüssel-Pointer Paaren
# - Jeder Schlüssel der Daten ist durch ein Paar repräsentiert
#      - Aber: Wesentlich kleinere Datenmenge
#      - Passt womöglich in den Hauptspeicher
#      - Nur ein I/O pro Zugriff
#      
# <br> 
# 
# - Sortierung der Paare = Sortierung der Daten
# 
# #### Anfragebearbeitung mit dichtbesetzten Indizes
# 
# - Gegeben Suchschlüssel K
# - Durchsuche Indexdatei nach K
# - Folge Pointer
# - Lade Block aus Datendatei
# - Beschleunigung
#      - Indexdatei hat nur wenige Blocks
#          - Indexdatei im Hauptspeicher <br>
# 
#      - Binäre Suche um K zu finden <br>
#      
# - Beispiel: 1.000.000 Tupel
#     - Block: 4096 Byte = 10 Tupel
#      - Gesamtgröße 400 MB
#      - Schlüsselfeld hat 30 Byte
#      - Pointer hat 8 Byte => 100 Paare pro Block
#      - Dichtbesetzter Index: 10.000 Blöcke für Index
#          - 40 MB => vielleicht OK im Hauptspeicher<br>
#          
#      - Binäre Suche: log2(10.000) ≈ 13
#          - => 13-14 Blocks pro Suche<br>
#      - Wichtigsten Blöcke im Hauptspeicher reichen

# ### Dünnbesetzte Indizes
# - Schlüsselwert ist immer kleinster Wert des referenzierten Blocks
# - Weniger Speicherbedarf 
# - Aber höherer Suchaufwand 
# - Nur ein Pointer pro Block 
# - Beispiel 
#      - 100.000 Datenblöcke, 100 Indexpaare pro Block 
#      - => 1.000 Blocks für Index 
#      - = 4MB
#      
# #### Anfragebearbeitung mit dünnbesetzten Indizes
# 
# 1. Suche im Index größten Schlüssel, der kleiner/gleich als Suchschlüssel ist.
#      - Binäre Suche (leicht modifiziert)
# 2. Hole assoziierten Datenblock
# 3. Durchsuche Block nach Datensatz
# -  Was kann ein dünnbesetzter Index nicht?
#     - SELECT 'TRUE' FROM R WHERE a=10
#     - Kann nicht ausschließlich mit Index beantwortet werden
#         - Im dicht-besetzten Index schon…<br>
#     - Auch: Semi-Join
# 

# ### Mehrstufiger Index
# Auch ein Index kann unangenehm groß sein.
# - Nimmt viel Speicher ein 
# - Kostet viel I/O 
#      - Auch bei binärer Suche
# - Idee: Index auf den Index 
#     - Zweiter Index macht nur als dünnbesetzter Index Sinn. <br>
# - Theoretisch auch dritte, vierte, … Ebene 
#     - B-Baum aber besser
#     
# #### Mehrstufiger Index Beispiel
# 
# 100.000 Datenblöcke, 100 Indexpaare pro Block
# - => 1.000 Blöcke für Index erster Stufe = 4MB
# - => 10 Blöcke für Index zweiter Stufe = 40KB
#      - Kann mit Sicherheit im Hauptspeicher verbleiben (weiter: liegt im Hauptspeicher)
# - Vorgehen zur Anfragebearbeitung
#     1. Suche im Index zweiter Stufe größten Schlüssel, der kleiner/gleich als Suchschlüssel ist.
#     2. Hole entsprechenden Block im Index erster Stufe (eventuell schon im Hauptspeicher)
#     3. Suche in dem Block größten Schlüssel, der kleiner/gleich als Suchschlüssel ist.
#     4. Hole entsprechenden Datenblock.
#     5. Suche Datensatz (falls Index erster Stufe dünnbesetzt ist).
# - Zusammen: 2 I/Os

# ### Indizes für Nicht-eindeutige Suchschlüssel
# 
# Annahme bisher: Suchschlüssel ist auch Schlüssel bzw.eindeutig in der Relation
# - Annahme weiter: Relation ist nach Suchschlüssel sortiert 
# - Idee 1: Dichtbesetzter Index 
#     - Ein Paar im Index für jeden Datensatz 
#     - Anfragebearbeitung: 
#          - Suche erstes Paar mit K. 
#          - Wähle alle weiteren mit K (direkt dahinter) 
#          - Hole entsprechende Datensätze. 
#          
# - Idee 2: Nur ein Indexpaar pro eindeutigem Schlüsselwert K.
#      - Der zeigt auf ersten Datensatz mit K.
#      - Weitere Datensätze mit K folgen direkt. 
#      - Wichtig: Blöcke haben Pointer auf jeweils nächsten Block     
#      
# - Idee 3: Dünnbesetzter Index wie gehabt 
#      - Datenwert im Index jeweils Datensatz am Blockanfang
# - Anfragebearbeitung 
#      - Suche letzten Eintrag E1 im Index, dessen Datenwert ≤ K
#      - Suche von dort im Index nach vorn bis zu einem Eintrag E2 mit Datenwert < K
#      - Hole alle Datenblöcke zwischen und inklusive E1 und E2.
# - Beispiel: K = 20: Rückwärtssuche ist nötig <br>
# 
# - Idee 4: Dünnbesetzter Index, aber
#      - Datenwert im Index ist der kleinste neue Wert im entsprechenden Datenblock.
#      - Hier Grenzfall: Welche Werte hat der Index? 
#      - Test: K= 20 bzw. K = 30
# - Anfragebearbeitung einfacher 
#      - Suche im Index nach Paar mit (Datenwert = K) oder (größter Wert mit < K aber nächster Wert ist > K).
#      - Hole Datenblock und gegebenenfalls folgende Datenblöcke.
# - Statt ⊥ auch „30“

# ### Änderungsoperationen
# 
# Daten ändern sich (Insert, Update, Delete).
# - Annahme bisher: Daten füllen Blöcke perfekt und ändern sich nicht
# - Änderungen im Datenblock: Siehe auch voriger Foliensatz
#      - Overflow Blocks
#          - In dünnbesetzten Indizes nicht repräsentiert
#      - Neue Blöcke in der Sequenz
#          - Benötigen neuen Indexeintrag
#          - Indexänderungen bergen dieselben Probleme wie Datenänderungen: Platzierung der Blöcke; Indizes höherer Stufe
#      - Tupel verschieben
#          - Index muss angepasst werden.
# - Generelle Regel: Indizes können wie normale data files behandelt werden. Gleiche Strategien können angewendet werden.
# 
# 
# **Änderungsoperationen Beispiele**
# 
# **Beispiel 1**
# 
# - Datensatz mit K = 30 wird gelöscht.
# - Annahme: Block kann/soll nicht reorganisiert werden. 
#      - Ersatz durch tombstone
# - Datensatz 40 wird nicht verschoben.
# - Index kann reorganisiert werden. 
#      - Main memory
#      
# **Beispiel 2**
# 
# - Datensatz mit K = 30 wird gelöscht. 
#     - Annahme: Block kann/soll reorganisiert werden.
#     - Datensatz 40 wird verschoben
#     - Index wird aktualisiert
# - Nun auch Datensatz mit K=40 Löschen 
#      - Leerer Block entsteht 
#      - Index wird aktualisiert (löschen) 
#      - Index wird reorganisiert
#      
# **Beispiel 3**  
# 
# - Einfügen eines Datensatzes 15
#      - Block 1 ist voll.
#      - Datensatz 20 wird in nächsten Block verschoben.
#          - Block wird reorganisiert.
#      - Datensatz 15 wird eingefügt.
#      - Index wird aktualisiert.
#          - 20 statt 40
# 
# **Beispiel 4**
# 
# - Wieder Datensatz 15 einfügen 
#      - Diesmal mit Overflow Blocks 
#      - Block 1 ist voll. 
#      - Datensatz 20 wird in Overflow Block verschoben.
#      - Datensatz 15 wird eingefügt. 
#      - Index bleibt gleich

# ## Sekundärindizes auf nichtsequenziellen Dateien
# 
# ### Motivation 
# - Annahme bisher: Datensätze sind nach Schlüssel sortiert
#      - „Primärindex“
# - Oft sinnvoll: Mehrere Indizes pro Relation
# - Schauspieler(Name, Adresse, Geschlecht, Geburtstag)
#      - Name ist Primärschlüssel => Primärindex
# ```
# SELECT Name, Adresse
# FROM Schauspieler
# WHERE Geburtstag = DATE '1952-01-01'
# ```
# 
# - Sekundärindex auf Geburtstag beschleunigt Anfragebearbeitung.
# 
# ``` CREATE INDEX GEB_IDX ON Schauspieler(Geburtstag)```
# 
# - Sekundärindizes bestimmen nicht Platzierung der Datensätze, sondern geben Speicherort an.
#      - Dünnbesetzte Sekundärindizes sind sinnlos.
#      - => Sekundärindizes sind immer dichtbesetzt.

# ### Aufbau von Sekundärindizes
# 
# - Dichtbesetzt; mit Duplikaten
# - Schlüssel-Pointer Paare
# - Schlüssel sind sortiert
# - Index zweiter Stufe wäre wiederum dünnbesetzt
# - Suche kostet idR mehr I/O
#      - Beispiel: Suche nach „20“ muss 5 Blöcke lesen.
#      - Ist nicht zu ändern: Daten sind halt nach einem anderen Schlüssel sortiert.
#      
# 

# ### Anwedungen
# 
# - Unterstützung von Selektionsbedingungen auf Nicht-Primärschlüssel
# - Datensätze liegen nicht sortiert vor.
#      - Sekundärindex auf Primärschlüssel
# - Datensätze aus zwei Relationen werden geclustered gespeichert.
#      - N:1 Beziehung zwischen R und S
#      - Speichere Datensätze aus R direkt beim entsprechenden Datensatz aus S.
#      - Clustered file
#      
# **Anwendung: Clustered file**
# 
# - Filme(Titel, Jahr, Länge, inFarbe, Studioname, Produzent)
# - Studio(Name, Adresse, Präsident)
# - Häufige mögliche Anfrageform:
# 
# ```
# SELECT Titel, Jahr
# FROM Filme, Studio
# WHERE Filme.Studioname = Studio.Name
# AND Präsident = ?
# ```
# 
# 1. Index auf Präsident findet schnell Studio-Datensatz.
# 2. Entsprechende Filme folgen direkt.
# - Anfragen direkt nach Filmen benötigen ebenfalls einen Sekundärindex
# 
# 

# ### Indirektion für Sekundärindizes
# 
# Bisherige Struktur verbraucht Platz: Datenwerte werden im Index mehrfach gespeichert.
# 
# - Spart Platz, falls
#     - Suchschlüssel größer sind als Bucketeintrag.
#     - Suchschlüssel im Durchschnitt mindestens zweimal auftauchen.
# - Weiterer Vorteil: Bestimmte Anfragen können direkt anhand der Buckets beantwortet werden.
#      - Mehrere Selektionsbedingungen, jeweils mit Sekundärindex: Schnittmenge der Pointer in Buckets
# - Filme(Titel, Jahr, Länge, inFarbe, Studioname, Produzent)
# 
# ```
# SELECT Titel FROM Filme
# WHERE StudioName = 'Disney'
# AND Jahr = 1995
# ```
# 
# **Indirektion im Alltag**

# ### Invertierte Indizes
# 
# Motivation: Dokumenten-Retrieval
# - Sichtweise Dokument als Relation
#     - Dok(hatKatze, hatHund, hatHaus, …)
#     - Tausende/Millionen Boolesche Attribute: True bedeutet das Dokument enthält das Wort.
#     - Idee 1: Sekundärindex auf jedes Attribut
#         - Aber: Nur die True-Werte werden indiziert
#     - Idee 2: Alle Indizes in einen kombiniert, die „invertierte Liste“
#         - Verwendet Indirektion
#         
# - Pointer in den Buckets
#      - Auf ein Dokument
#      - Auf eine Stelle im Dokument
# - Erweiterung: Bucket speichert nicht nur Stelle sondern auch Metadaten
#      - Art des Vorkommens (Titel, Abstract, Text, Tabelle, …)
#      - Satz (fett, kursiv, …)
#      - …
# - Anfragen: AND, OR, NOT
#      - Durch Mengenoperationen auf den Pointermengen
#      
# Suche nach Dokumenten, die Hunde und Katzen vergleichen
# - Dokument erwähnt „Hund“ im Titel
# - Dokument erwähnt „Katze“ in einem Anker (Link auf anderes Dokument)

# ### B-Bäume
# 
# ####  Allgemein
# Bisher: Zweistufiger Index zur Beschleunigung des Zugriffs
# - Allgemein: B Bäume (hier „B+ Bäume“)
#     - So viele Stufen wie nötig
#     - Blöcke sind stets mindestens zur Hälfte gefüllt
#     - Overflow blocks nicht notwendig
#     
# #### Struktur
# - Index-Blöcke in einem Baum organisiert
# - Balanciert
#      - Jeder Weg von Wurzel zu Blatt ist gleich lang.
# - Parameter n
#      - Jeder Block enthält bis zu n Suchschlüssel
#      - Jeder Block enthält bis zu n+1 Pointer
#      - Also wie Indexblock zuvor, aber ein zusätzlicher Pointer
# - Wahl von n
#      - n so groß wie möglich entsprechend der Blockgröße
#      - 4096 Byte pro Block; 4 Byte pro Schlüssel; 8 Byte pro Pointer
#      - 4n + 8(n+1) ≤ 4096 => n = 340
#      
# **Erinnerung: Datenstrukturen und Algorithmen: B-Bäume**
# 
# * „Maximale Ausgeglichenheit“
# 
# #### Einfügen in B-Bäume – Beispiel
# 
# #### Hier B+ Baum**
# 
# - Schlüssel in Blätter sind Schlüssel aus den Daten
#      - Sortiert über alle Blätter verteilt (von links nach rechts)
# - Wurzel: mindestens zwei verwendete Pointer.
#      - Alle Pointer zeigen auf einen B-Baum Block in Ebene darunter.
# - Blätter: Der letzte Pointer zeigt auf das nächste Blatt (rechts).
#      - Von den übrigen n Pointern werden mindestens $\lfloor(n+1)/2\rfloor$ verwendet.
#      - Zeigen auf Datenblöcke
# - Innere Knoten: Pointer zeigen auf B-Baum Blöcke darunterliegender Ebenen
#      - Mindestens $\lceil(n+1)/2\rceil$ sind verwendet
#      - Falls j Pointer verwendet werden, gibt es j–1 Schlüssel in dem Block
#          - Keys K1, … , Kj-1
#      - Erster Pointer zeigt auf Teilbaum mit Schlüsselwerten < K1.
#      - Zweiter Pointer auf Teilbaum mit Schlüsselwerten ≥ K1 und < K2 usw
#      
# #### Rechenbeispiele
# 
# n = 3
# - Alle Knoten: Maximal 3 Suchschlüssel und 4 Pointer
# - Wurzel: Mindestens 1 Suchschlüssel und 2 Pointer
# - Innere Knoten: Mindestens 1 Suchschlüssel und 2 Pointer
# - Blätter: Mindestens 2 Suchschlüssel und 3 Pointer
# 
# n = 4
# - Alle Knoten: Maximal 4 Suchschlüssel und 5 Pointer
# - Wurzel: Mindestens 1 Suchschlüssel und 2 Pointer
# - Innere Knoten: Mindestens $\lceil(n+1)/2\rceil$ Pointer = 3 Pointer
#      - => Mindestens 2 Suchschlüssel
# - Blätter:
#      - 1 Pointer zum nächsten Blatt + mindestens $\lfloor(n+1)/2\rfloor$ weitere Pointer = 3 Pointer
#      - => Mindestens 2 Suchschlüssel
# n = 5
# - Alle Knoten: Maximal 5 Suchschlüssel und 6 Pointer
# - Wurzel: Mindestens 1 Suchschlüssel und 2 Pointer
# - Innere Knoten: Mindestens $\lceil(n+1)/2\rceil$ Pointer = 3 Pointer
#     - => Mindestens 2 Suchschlüssel
# - Blätter:
#      - 1 Pointer zum nächsten Blatt + mindestens $\lfloor(n+1)/2\rfloor$ weitere Pointer = 4 Pointer
#      - => Mindestens 3 Suchschlüssel
# 
# 
# 
# 

# #### Alternative Definition
# 
# - Bisher: Parameter n
#     - Block hat mindestens $\lfloor(n+1)/2\rfloor$ Suchschlüssel
#     - Block hat höchstens n Suchschlüssel
# - Alternativ in Lehrbüchern: Parameter k
#     - Block hat mindestens k Suchschlüssel
#     - Block hat höchstens 2k Suchschlüssel
#     - Block hat immer x + 1 Pointer (wie bisher)
# - Immer
#     - Ein innerer Block hat immer einen Pointer mehr als Anzahl Suchschlüssel
#     - Ein Blatt hat immer ebenso viele Pointer wie Suchschlüssel
#         - Plus verkettete Liste

# #### Beispiel Blattknoten
# #### Beispiel innerer Knoten
# #### Beispiel B-Baum
# Dicht-besetzt: In den Blättern taucht sortiert jeder Schlüssel genau einmal auf.

# #### Anwendungen von B-Bäumen
# B-Bäume können verschiedene Index-Rollen übernehmen.
# - Suchschlüssel ist Primärschlüssel; dicht-besetzter Index
#      - Data file sortiert oder nicht
# -  Dünn-besetzter Index; data file ist sortiert
# - „Dünn-besetzter“ Index; data file ist nicht sortiert
#     - Indirektion
# - Suchschlüssel ist nicht Primärschlüssel
#     - Data file ist nach Suchschlüssel sortiert
#     - Pointer zeigen auf jeweils ersten Wert
#     - Jetzt dazu mehr …
#     
# #### B-Bäume auf nicht-Primärschlüsseln
# - Bedeutung der Pointer auf inneren Ebenen ändert sich.
#      - Gegeben: Schlüssel K1, … , Kj
#      - => Ki ist der kleinste neue Schlüsselwert, der vom (i+1)-ten Pointer erreichbar ist.
#          - D.h. es gibt keinen Schlüsselwert Ki im linken Teilbaum aber mindestens ein Vorkommen des Schlüsselwertes im Teilbaum vom (i+1)-ten Pointer an.
#         - Problem: Es gibt nicht immer einen solchen Schlüssel

# ### B-Bäume Suche
# 
# #### Allgemein
# 
# - Jetzt wieder: Suchschlüssel = Primärschlüssel
# - Dicht-besetzter Index
#      - Operationen für dünn-besetzte Indizes ähnlich
# - Gesucht sei K.
#     - Falls wir an einem Blattknoten sind:
#         - Suche K auf dem Knoten.
#     - Falls wir an einem inneren Knoten mit K1, K2, … Kn sind:
#     - Falls K < K1 gehe zu erstem Kind
#     - Falls K1 ≤ K < K2 gehe zu zweitem Kind
#     - …
#     - Falls Kn ≤ K gehe zu letztem Kind
#     
# #### Beispiel Suche im B-Baum
# 
# #### Bereichsanfragen (range queries)
# Anfragen mit Ungleichheit in WHERE Klausel
# ```
# SELECT * FROM R
# WHERE R.k > 40
# ```
# 
# ```
# SELECT * FROM R
# WHERE R.k >= 10 AND R.k <= 25
# ``` 
# 
# - Suche nach Bereich [a,b]
#     1. Suche in B-Baum nach a.
#         - Entsprechendes Blatt könnte a speichern.
#         - Suche auf dem Blatt alle relevanten Schlüssel.
#     2. Falls auf dem Blatt kein Wert > b
#         - Folge Pointer zu nächstem Blatt.
# - Bei offenen Bereichen [-∞ , b] bzw. [a, ∞] ist Suche ähnlich.
# 

# ### B-Bäume Updates
# 
# #### Einfügen in B-Bäume
# Rekursives Vorgehen:
# - Suche entsprechendes Blatt.
#      - Falls Platz herrscht, füge Schlüssel und Pointer ein.
# - Falls kein Platz: Überlauf
#      - Teile Blatt in zwei Teile und verteile Schlüssel gleichmäßig
#      - „split“
# - Teilung macht Einfügen eines neuen Schlüssel/Pointer-Paares im Elternknoten erforderlich
#      - Gehe rekursiv aufwärts im Baum vor
# - Ausnahme: Falls in Wurzel kein Platz
#      - Teile Wurzel in zwei
#      - Erzeuge neue Wurzel (mit nur einem Schlüssel)
#      
# **Kosten für Einfügen**
# - Sei h die Höhe des B-Baums
#      - Meist h = 3
# - Suche nach Blattknoten: h
# - Falls keine Teilung nötig: Gesamtkosten h + 1
#      - h Blöcke lesen, 1 Index-Block schreiben
# - Falls Teilung nötig
#      - Worst-case: Bis zur Wurzel
#     - Selbst Caching nützt nichts, da Knoten geschrieben werden müssen
#     - Insgesamt: 3 h + 1
#         - Auf jeder Ebene Suche und Überlaufbehandlung
#         - + neue Wurzel schreiben
#         

# #### Löschen aus B-Bäumen
# - Suche entsprechenden Knoten
# - Lösche Schlüssel
# - Falls immer noch minimale Menge an Schlüsseln im Knoten
#      - Nichts tun
# - Falls zu wenig Schlüssel im Knoten: Merge (Verschmelzen)
#      - Falls ein Geschwisterknoten (links oder rechts) mehr als die minimale Schlüsselmenge hat, „klaue“ einen Schlüssel.
#         - Gegebenenfalls (fast immer) Schlüsselwerte der Eltern anpassen
#     - Falls nicht: Es existieren zwei Geschwister im Baum mit minimaler und sub-minimaler Schlüsselmenge
#         - => Diese Knoten können vereinigt werden.
#         - Schlüsselwerte der Eltern anpassen (gegebenenfalls rekursiv im Baum nach oben löschen)
#         
# **Kosten für Löschen**
# 
# - Suche und lokales Löschen: h + 1
#      - Schreibe Blattknoten
# - Bei merge mit Geschwisterknoten: h + 5
#      - Prüfe rechts und links
#      - Schreibe Block und veränderten Nachbarn
#      - Schreibe Elternknoten
# - Bei merge bis zur Wurzel: 3h - 2
# 
# **Löschen aus B-Bäumen?**
# - Annahme: Tendenziell wachsen Datenmengen
# - Folgerung: Nie Knoten des B-Baum löschen
#     - Knoten, die durch Löschen zu klein werden, werden früher oder später wieder gefüllt.
#     - Grabstein auf Datenblock genügt, B-Baum muss nicht geändert werden

# ### Effizienz von B-Bäumen
# 
# Suche, Einfügen und Löschen sollen möglichst wenig I/O-Operationen benötigen.
# - Je größer n gewählt wird, desto seltener müssen Blöcke verschmolzen oder getrennt werden.
#     - Meist auf Blattknoten beschränkt
# - Suche (best case)
#     - Anzahl I/Os entspricht der Höhe des Baums
#     - + 1 I/O auf den Daten für Lesen
#     - oder + 3 I/O auf den Daten für Einfügen oder Löschen
# - Typische Höhe eines B-Baums: 3
#     - 340 Schlüssel-Pointer-Paare pro Block
#     - Annahme: Füllstand durchschnittlich 255
#     - => 255 innere Knoten = > 255² = 65025 Blätter = 255³ Pointer
#     - Insgesamt über 16 Mio. Datensätze
#     - Maximal: 340³ = 39 Mio. Datensätze
# - Zugriff mit 2 I/Os: Nur Wurzel im Hauptspeicher
# - Zugriff mit 1 I/O: Wurzel und 255 innere Knoten im Hauptspeicher
# 
# #### Bulk-loading
# 
# - Einfügevarianten
#     - Einfügen von Daten in Relation, die bereits mit existierendem B-Baum indiziert ist.
#     - Erstellung eines neuen B-Baums auf existierenden Daten
#         - Sukzessives Einfügen jedes Datensatzes ist ineffizient.
#         - Immer wieder über die Wurzel suchen
#         - Viel I/O für Indexblöcke, die nicht im Hauptspeicher sind.
# - Besser: Vorsortierung
#     - Schritt 1: Erzeuge Schlüssel-Pointer Paare für alle Blöcke
#     - Schritt 2: Sortierung der Paare nach Suchschlüssel
#     - Schritt 3: Füge nun sukzessive die Paare ein
#     
# **Beispiel**
# - n = 3
# - Daten: 2; 3; 5; 7; 11; 13; 17; 19; 23; 29; 31; 37; 41; 43; 47
# - Erzeuge halbgefüllte Blattknoten
# 
# - Erzeuge Wurzel für erste beiden Blattknoten
# 
# - Füge nächstes Blatt ein
# 
# - Füge nächstes Blatt ein
# 
# - Füge nächstes Blatt ein
# 
# - Füge nächstes Blatt ein
# 
# - Füge letztes Blatt ein
# 
# **Bulk-Loading mit hohem Füllstand**
# - Schritt 1: Erzeuge Schlüssel-Pointer Paare für alle Blöcke
# - Schritt 2: Sortierung der Paare nach Suchschlüssel
# - Schritt 3: Erzeuge volle B-Baum Blätter
# - Schritt 4: Konstruiere innere Knoten aufgrund der Blätter
# - Ergebnis: Perfekter Füllstand
# - Anwendungen:
#      - Read-only Relationen
#      - Append-only Relationen

# ### B-Baum Varianten: B-Baum (ohne „+“)
# 
# - Bisher: B+ Baum
#     - Pointer auf Datensätze nur in Blattknoten
# - B-Baum
#     - Pointer auf Datensätze in allen Knoten
#     
# - Vorteil: Durchschnittlich schnellere Suche als in B+-Bäumen
# - Nachteil: Blätter und innere Knoten haben unterschiedliche Struktur
#     - Verwaltung schwieriger
# - Nachteil: Weniger bushy; Platz wird für Pointer auf Datensätze „verschwendet“
#     - Dadurch größere Höhe
# - Nachteil: Löschen ist komplizierter
#     - Löschung kann auch in inneren Knoten geschehen.
#     - Schlüssel von einem Blatt muss gegebenenfalls nach oben wandern.
#     
# **B*-Bäume**
# - B*-Baum
#     - Bei Überlauf werden nicht gleich zwei halb-leere Knoten erzeugt.
#     - Stattdessen Neuverteilung über beide Nachbar-Blätter
#     - Falls nicht möglich, erzeuge 3 neue Blätter aus 2 alten Blättern
#     - Dadurch bessere Speicherausnutzung: Mindestens 66%
#     
# **Präfix-B+-Baum**
# - Präfix-B+-Baum
#     - Falls Suchschlüssel ein String ist => Hoher Speicherbedarf
#     - Besser: Speichere nur „Trennwert“
#     - Was trennt „Korn“ von „Licht“?
#     - Am besten: Kleinster Trennwert
#         - „L“
#         - Präfix von „Licht“
#         
# **B+-Bäume für BLOBs (und CLOBs)**
# - Idee: Suchschlüssel repräsentiert Offsets im BLOB anstatt Suchschlüssel
#     - Blätter zeigen auf Datenseiten des BLOBs
#     - Positional B-Tree

# ### Hashtabellen
# 
# #### Allgemeine Hash-Tabellen
# **Hashtabellen – Grundprinzip**
# - Hashfunktion
#     - Input: Suchschlüssel K (Hash-Schlüssel)
#     - Output: Integer zwischen 0 und B−1
#         - B = Anzahl Buckets
#     - Oft z.B. MOD(K/B) („Divisionsrestmethode“)
#         - Bei Strings: Weise jedem Buchstaben Integer zu und summiere diese.
# - Bucketarray
#     - Array aus B Headern für B verkettete Listen
# 
# **Hashtabellen auf Festplatten**
# - Bisher (im Studium): Hashtabellen im Hauptspeicher
# - Nun: Blöcke statt Pointer auf Listen
#     - Datensätze, die auf einen gemeinsamen Wert gehashed werden, werden in dem entsprechenden Block gespeichert.
#     - Overflowblocks können ergänzt werden.
# - Annahme: Zuordnung eines Hashwerts zur Speicheradresse eines Blocks möglich
#     - Z.B.: Hashwert stellt Offset dar
#     
# **Einfügen in Hashtabellen**
# 1. Berechne Hashwert
# 2. Falls Platz, füge Datensatz in entsprechenden Block ein
# - Oder in einen Overflowblock mit Platz
# 3. Falls nicht, erzeuge neuen Overflowblock und füge dort ein
# - Beispiel: Füge H ein
#     - h(H) = 2
# - Beispiel: Füge G ein
#     - h(G) = 1
#     
# **Löschen in Hashtabellen** 
# 1. Suche Bucket (+ Overflowblocks)
# 2. Suche Datensatz / Datensätze
# 3. Lösche sie
# 4. Gegebenenfalls Reorganisation und Entfernung von Overflowblocks
#     - Gefahr der Oszillation
# - Beispiel: Lösche C
#     - G bewegen

# #### Vorschau: Consistent Hashing
# 
# - Problem of hash fragmentation:
#     - Traditional hash functions require remapping of all tuples when a node goes offline
#     - Because hash function must map to fewer nodes.
# - Consistent hash function:
#     - Minimizes the degree of remapping in case of the addition or removal of locations (nodes, slots)
#     - Only K/n keys need to be remapped on average (K ... total number of keys, n ... number of slots)
#     - Distributed Hash Tables (DHT)
#     
# #### Effizienz statischer Hashtabellen
# 
# - Idealerweise: Pro Bucket nur ein Block 
#     - Zugriffszeit lesen: 1 I/O 
#     - Zugriffszeit Einfügen / Löschen: 2 I/O 
#     - Viel besser als Dicht- oder Dünnbesetzte Indizes 
#     - Besser als B-Bäume o Aber Nachteil: Bereichsanfragen nicht unterstützt o => Kein sequentielles Lesen von Disk 
# - Weiteres Problem: B wird einmalig festgelegt 
#     - Lange Listen von Overflowblöcken 
#     - „Statische Hashtabellen“ 
# - Lösung: „Dynamische Hashtabellen“ 
#     - Hashtabellen können wachsen 
#     - Ideal: B ≈ Anzahl Datensätze / Datensätze pro Block o => Ca. 1 Block pro Bucket

# ### Erweiterbare Hashtabellen
# 
# Neuerungen
# - Indirektion
#     - Bucket besteht aus Pointerarray statt Datenblock(s)
# - Wachstum
#     - Größe des Pointerarrays verdoppelt sich bei Bedarf
# - Sharing
#     - Buckets können sich Datenblöcke teilen
#     - Wenn es passt
# - Hashfunktion
#     - Berechnet (zu) großes Bitarray (k bit; z.B. k = 32)
#     - Bucketarray verwendet nur die ersten i Bits (i ≤ k)
#     - => $2^i$ buckets
#     
# <br> <br> 
# 
# - k = 4
# 
# #### Einfügen in erweiterbare Hashtabellen
# 
# - Ähnlich wie normale Hashtabelle
#     - Berechne h(K); wähle die ersten i Bits
#     - Suche Eintrag im Bucketarray und lade entsprechenden Block
# - Falls Platz: Füge neuen Datensatz ein.
# - Falls kein Platz und j < i (j ist aktuelle Bitanzahl des Blocks)
#     - Spalte Block entzwei (split)
#     - Verteile Datensätze gemäß des (j+1)ten Bits
#         - Falls 0: Verbleib
#         - Falls 1: Verschieben in neuen Block
#     - Setze j+1 als neue Bitanzahl der beiden neuen Blöcke
#     - Pointer im Bucketarray aktualisieren
#     - Was wäre Pech?
#         - Alle Datensätze landen wieder im gleichen Block. Dann wieder j++.
#         
# - Falls kein Platz und j = i (j ist aktuelle Bitanzahl des Buckets)
#     - Global: i++ => Länge des Bucketarrays verdoppelt sich
#     - Datenblöcke bleiben unverändert
#     - Zwei neue Pointer zeigen zunächst auf gleichen alten Block
#     - Dann: Spalte relevanten Block entzwei (split)
#         - Weiter wie zuvor (denn nun j < i)

# #### Analyse erweiterbarer Hashtabellen
# 
# - Vorteile
#     - Bei Suche: Nie mehr als ein Datenblock betrachten
#         - Keine Overflow Blocks
#     - Bucketarray eventl. im Hauptspeicher
# - Nachteile
#     - Bei Verdopplung und Split: Viel Arbeit
#         - => Ab und zu dauert ein Einfügen sehr lang: Planbarkeit!
#     - Bucketarray wächst schnell
#         - Passt eventuell nicht mehr in Hauptspeicher
#     - Platzverschwendung bei wenigen Datensätzen pro Block
#         - Beispiel: 2 Datensätze pro Block
#         - Datensatz 1: 00000000000000000001
#         - Datensatz 2: 00000000000000000010
#         - Datensatz 3: 00000000000000000011
#         - => i = 20 (also 220 = 1Mio buckets)

# ### Lineare Hashtabellen
# 
# Ziel: Anzahl Buckets wachse nur langsam.
# - Anzahl n der Buckets so gewählt, dass Datenblocks zu ca. 85% gefüllt sind.
# - Overflow Blocks sind zugelassen.
#     - Durchschnittliche Anzahl Overflow Blocks pro Block: <<1
# - log2n Bits zur Identifizierung der Buckets
#     - Wähle die jeweils letzten Bits des Hashwerts
#     
# #### Lineare Hashtabellen – Einfügen
# 
# - Berechne h(K)
# - Betrachte letzte i Bits; interpretiere als Integer m
# - Falls m < n: Füge Datensatz in Bucket m ein.
# - Falls m ≥ n:
#     - => Bucket m existiert noch nicht
# - Füge Datensatz in Bucket m–2i-1 ein.
#     - D.h. erstes Bit des Schlüssels wird zu 0 (vorher 1).
# - Falls kein Platz: Erzeuge Overflow Block
# - Berechne r/n
#     - Falls zu hoch (z.B. ≥ 1,7): Erzeuge einen neuen Bucket (n++)
#     - Neuer Bucket hat nichts mit betroffenem Bucket zu tun.
# - Falls nun n > 2i: i++
#     - D.h. alle Bitsequenzen erhalten eine 0 am Anfang
#     - Physisch ändert sich nichts

# #### Hashing vs. B-Baum
# 
# - Hashing effizient zur Feststellung der Existenz eines Wertes
#     - Overflow blocks nötig bei doppelten Schlüsseln
# - B-Baum effizient für Bereichsanfragen und hält Daten sortiert vor
# - Indexerzeugung in SQL:
# 
# ```
# CREATE [ UNIQUE ] INDEX indexname
# ON table ( column [ ASC | DESC ]
# [ , column [ ASC | DESC ] ... ] )
# [CLUSTER]
# [PCTFREE integer]
# ```
# 
#     - UNIQUE erlaubt NULL Werte
#     - PCTFREE bestimmt Füllgrad
#     - Keine Angabe über Art des Index
#     - Keine Angabe über Parameter
#     - Manchmal Hersteller-spezifische Syntax für Parameter
