#!/usr/bin/env python
# coding: utf-8

# # Speicherung

# Physische Speicherstrukturen

# Zoom in die interne Ebene: Die 5-Schichten Architektur
# 
# <img src="pictures/5-Schichten-Architektur.png" alt="5-Schichten-Architektur" width="500" style="background-color: white;"/>
# 
# Auf der Datenmodellebene können Relationen definiert und die Relationale Algebra verwendet werden. Darunter liegt die logische Ebene. Auf dieser Ebene kann betrachtet werden, wo die Daten liegen bzw. wie diese verteilt sind. Die nächsten Ebenen kümmeren sich um die Speicherstrukturen, also wo die Daten physisch abgelegt wurden und über welche Puffer bzw. Schnittstellen auf diese zugegriffen werden kann. Unter diesen Ebenen liegt noch eine weitere Schnittstelle zum Betriebssystem. Dabei gibt es zwei Varianten wie man mit einem Betriebssystem umgeht. Bei der einen Variante versucht man mit dem System zusammenzuarbeiten, bei der anderen versucht man es zu umgehen. 
# 

# ## Speicherhierarchie
# 
# <img src="pictures/Speicherhierachie.png" alt="Speicherhierachie" width="300" style="background-color: white; float: left;"/>
# 
# | Speichermedium | Kosten | Zugriffszeiten | Kapazitäten |
# |---|---|---|---|
# | Register | Sehr teuer | < 1ns | 10KB |
# | Cache | Sehr teuer | 1-10ns | 10MB |  
# | Hauptspeicher | ~ 5€/GB | 100ns | 100GB | 
# | Festplatte | ~ 0.05€/GB | SSDs 100us </br> Festplatte 8-10ms | SSDs 5TB </br> Festplatte 50 TB | 
# | Archivspeicher | < 1€/GB | sec - min | ~ 1PB |

# Die Pyramide zur Speicherhierachie soll veranschaulichen, wie sich die Kosten, Zugriffszeiten und Kapazitäten der unterschiedlichen Speichermedien verhalten. <br>
# In Anbetracht der Kosten sind Archivspeicher sehr günstig verglichen mit Registern, die die teuerste Speicherform in dieser Pyramide darstellen. <br>
# Bei den Zugriffszeiten wiederrum ist der Archivspeicher am langsamsten und braucht Sekunden, wenn nicht Minuten. Wohingegen Register sehr schnelle Zugriffszeiten unter 1ns ermöglichen. <br>
# In Bezug auf die Kapazität, bietet der Archivspeicher am meisten Speicherplatz. Ein Register hat mit 10kB beispielsweise deutlich weniger zur Verfügung. <br><br>
# ~ Zahlen aus dem Foliensatz von Viktor Leis 2019

# ### Virtueller Speicher
# Jede Anwendung verwaltet einen virtuellen Adressraum. Dieser kann größer als der tatsächlich verfügbare Hauptspeicher sein. 
# Mit einem 32-bit Adressraum sind 2^32 unterschiedliche Adressen darstellbar.
# Jedes Byte hat dabei eine eigene Adresse. Dadurch lässt sich maximal eine Hauptspeichergröße von 4GB addressieren.  
# Heutzutage ist der 64-bit Adressraum der Standard. Damit lassen sich maximal 16 Exabyte addressieren. Dies ist deutlich mehr als ein gewöhlicher Computer/Laptop mit 1 oder 2 TB Speicher. Eine 64-bit Addressierung bietet somit noch deutlich mehr Potenzial. <br>
# Meistens ist aber deutlich weniger Hauptspeicher als Speicher auf der Festplatte vorhanden. Zur Abhilfe werden die Daten auf eine Disk ausgelagert. 
# Dazu müssen ganze Blöcke (Blockgröße zwischen 4 bis 56 KB) zwischen Hauptspeicher und Festplatte gelesen und geschrieben werden (Seiten des virtuellen Speichers). Es werden nicht einzelne ASCII-Zeichen, sondern ganze Blöcke, die beispielsweise mehrere ASCII-Zeichen enthalten, gelesen. Die Transferzeiten ändern sich nämlich kaum, wenn Blöcke anstelle von einzelnen Zeichen gelesen und geschreiben werden. Es können nicht beliebig viele Zeichen in einem Block sein. Irgendwann ist auch das zu viel. <br>
# Die Zugriffe werden durch ein Betriebssystem verwaltet und eingeschränkt. 
# Datenbankensysteme können Begriffe wie 'O_DIRECT' verwenden, um doch selbst die Positionen der Daten auf den Festplatten zu verwalten und eigene Bufferpoolmanager zu verwenden. Ein Betriebssystem hat beispielsweise mehrere Anwendungen für die es den Hauptspeicher verwalten muss. Daher kann es sein, dass das Betriebssystem eine Anwendung vorzieht, bevor es die Daten aus der Datenbank bearbeitet. 

# ### Sekundärspeicher: Festplatten
# Unter Sekundärspeicher fallen nicht nur (magnetische) Festplattens, sondern auch optische (read-only) Speicher.
# Im Wesentlichen gibt es auf Sekundärspeicher wahlfreien Zugriff (random access). Dabei kostet der Zugriff auf jedes Datum gleich viel, aber dafür muss man dort erst einmal hinkommen! <br>
# HDDs halten Daten aus Cache bzw. die Seiten des virtuellen Speichers von Anwendungsprogrammen. Außerdem halten sie Daten aus Dateisystemen. <br>
# Es gibt zwei Operationen auf Festplatten. Zum Einem Disk-read. Darunter versteht man das Kopieren eines Blocks in den Hauptspeicher. Zum Anderen Disk-write, dem Kopieren eines Blocks aus dem Hauptspeicher auf die Festplatte. Beides gilt jeweils als eine Disk-I/O-Operation. 

# ### Festplatten - Puffer
# Ein Bufferpool-Manager puffert Teile von Dateien. In diesem Beispiel mit einer  Blockgröße von 4 KB. Dabei werden immer 4KB in den Pool geladen. Dieser Block kann dann geschrieben oder auch verworfen werden. 
# 
#   <img src="pictures/Festplatten-Puffer.png" alt="Festplatten-Puffer" width="500" style="background-color: white;"/>
# 
# Das DBMS verwaltet die Positionen der Blöcke innerhalb der Datei selbst! Dafür ist nicht mehr das Betriebssystem zuständig. <br>
# Die Dauer für das Schreiben oder Lesen eines Blocks beträgt 10 bis 30 ms. In dieser kurzen Zeitspanne können viele Millionen Prozessoranweisungen ausgeführt werden. Somit dominiert das Lesen und Schreiben, also die I/O-Zeit, die Gesamtkosten. Die Blöcke sollten daher am besten im Hauptspeicher liegen. Das ist nicht immer möglich, da der Hauptspeicher meist zu klein ist. 
# <br><br>
# Die zuvor genannten Zahlen können je nach Betriebssystem variieren. Sie sind hier aber immer ungefähr im gleichen Skalierungsraum und sollen dabei helfen ein Gefühl für die Zugriffszeiten zu vermitteln. 

# ### Tertiärspeicher: Magnetbänder
# 
# Tertiärspeicher kann viele Terabyte (10^12 Bytes) Verkaufsdaten, sowie viele Petabyte (10^15 Bytes) Satellitenbeobachtungsdaten speichern. Für diesen Einsatzbereich wären Festplatten ungeeignet. Sie sind zu teuer aufgrund von Wartung und Strom. <br>
# Im Vergleich zum Sekundärspeicher sind zwar die I/O-Zeiten wesentlich höher, aber dafür steigt auch die Kapazität. Ein weiterer Vorteil sind die geringeren Kosten pro Byte gegenüber den Festplatten. <br>
# Auf Tertiärspeicher gibt es keinen wahlfreien, sondern zufälligen Zugriff (random access). Die Zugriffszeiten hängen dabei stark von der Position des jeweiligen Datensatzes (in Bezug auf die aktuelle Position des Schreib-/Lesekopfes) ab.
# 
# <img src="pictures/Magnetband.png" alt="Magnetband" width="300" style="background-color: white;"/>

# ### Tertiärspeicher
# 
# Ad-hoc können Daten auf Magnetbändern/Magnetbandspulen und Kasseten gespeichert werden. Die Speichermedien werden oft von Menschenhand in die jeweiligen Regale gelegt und geordnet. Daher der Tertiärspeicher in dem Fall gut beschriftet werden. Durch Magnetbandroboter (Silo) kann dieser Prozess ersetzt bzw. optimiert werden. Der Roboter bedient anstelle des Menschen die Magnetbänder (Kassetten). Der Einsatz von Robotern beschleunigt das Verfahren um das zehnfache. <br>
# Die Idee ist ähnlich zu CDs, DVDs und Juke-Boxes. Ein Roboterarm extrahiert das jeweilige Medium (CD oder DVD). Der Tertiärspeicher hat wieder eine hohe Lebensdauer von ca. 30 Jahren. Somit ist es wahrscheinlicher, dass kein Lesegerät mehr existiert, als dass der Tertiärspeicher nicht mehr funktioniert. 
#   
#    <img src="pictures/Tertiärspeicher.png" alt="Tertiärspeicher" width="300" style="background-color: white;"/>

# ### Moore's Law (Gordon Moore, 1965)
# 
#   <img src="pictures/moores-law_1.png" alt="moores-law_1" width="400" style="background-color: white;"/>
#   <img src="pictures/moores-law_2.png" alt="moores-law_2" width="300" style="background-color: white;"/>
# 
# Moore's Law beschreibt das exponentielle Wachstum vieler Parameter. Zu einer Verdopplung kommt es alle 18 Monate. Es können sich beispielsweise die folgenden Parameter verdoppeln bzw. halbieren:
#   - Prozessorgeschwindigkeit (# instr. per sec.)
#   - Hauptspeicherkosten pro Bit
#   - Anzahl Bits pro cm² Chipfläche
#   - Diskkosten pro Bit (halbiert)
#   - Kapazität der größten Disks
#   
# Dahingegen kommt es aber zu einer sehr langsamen Verbesserung bei der Zugriffsgeschwindigkeit im Hauptspeicher und der Rotationsgeschwindigkeit von Festplatten, da es physikalisch deutlich schwerer und teurer ist zu realisieren. Als Folge daraus wächst der Latenz-Anteil. Die Bewegung von Daten innerhalb der Speicherhierarchie erscheint immer langsamer (im Vergleich zur Prozessorgeschwindigkeit).
# 
# <img src="pictures/moores-law_3.png" alt="moores-law_3" width="500" style="background-color: white;"/>
# 
# In dem Diagramm ist die Anzahl der Transistoren in Abhängigkeit der Zeit dargestellt worden. 
# 
# <img src="pictures/moores-law_4.png" alt="moores-law_4" width="500" style="background-color: white;"/>
# 
# See also: http://www.computerhistory.org/timeline/memory-storage/ 

# ### Plattenkapazität
# 
# <img src="pictures/Plattenkapazität.png" alt="Plattenkapazität" width="500" style="background-color: white;"/>
# 
# http://en.wikipedia.org/wiki/Hard_disk_drive
# 
# Wie man aus diesem Diagramm entnehmen kann, wächst die Plattenkapazität exponentiell. <br>
# Die Zugriffszeiten hingegen gleichen sich langsam an. Im folgendem Bild wird der Trend zur maximal anhaltenden Bandbreite gezeigt.
# 
# <img src="pictures/Access_times.png" alt="Access_times" width="500" style="background-color: white;"/>
# 
# 
# Auch die Suchzeiten halbieren sich immer seltener. Daraus ergibt sich der folgende Trend:
# 
# <img src="pictures/Seek_times.png" alt="Seek_times" width="500" style="background-color: white;"/>
# 
# 
# http://www.storagenewsletter.com/news/disk/hdd-technology-trends-ibm

# ### SSDs
# Die persistente Speicherung von SSDs basiert auf Halbleitern. Sie haben keine mechanische Bewegung oder Rotation. Außerdem bieten SSDs einen hohen Grad an Parallelität. 
#   
#   <img src="pictures/SSDs.png" alt="SSDs" width="500" style="background-color: white;"/>

# ### HDDs vs. SSDs
# 
# Im Vergleich zu HDDs bieten SSDs einige Vorteile:
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
# SSDs besitzen aber auch Nachteile, die bei der Wahl zwischen HDD und SSD berücksichtigt werden sollten:
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
# Über weitere Vor- und Nachteile können Sie <a href="https://databasearchitects.blogspot.com/2021/06/what-every-programmer-should-know-about.html">hier</a> weiterlesen.
# 
# 

# ## Festplatten
# <img src="pictures/Festplatten_Vergleich_Früher_Heute.png" alt="Festplatten_Vergleich_Früher_Heute" width="400" style="background-color: white;"/>

# ### Aufbau
# 
# Eine Festplatte besteht aus mehreren (5-10) gleichförmig rotierenden Platten (z.B. 3.5" Durchmesser). Für jede Plattenoberfläche (10-20) gibt es einen Schreib-/Lese-Kopf, der sich gleichförmig bewegt. Die magnetische Plattenoberfläche ist in Spuren eingeteilt.
# Spuren sind als Sektoren fester Größe formatiert, wobei sich die Anzahl der Sektoren pro Spur unterscheiden kann. Übereinander angeordnete Spuren bilden einen Zylinder. Die Platten sind übereinander angeordnet, um Zugriffseffizienz zu ermöglichen. Der Kopf kann parallel auch an anderen Stellen lesen und schreiben. 
# 
# <img src="pictures/Aufbau_1.png" alt="Aufbau_1" width="500" style="background-color: white;"/>
# <img src="pictures/Aufbau_2.png" alt="Aufbau_2" width="500" style="background-color: white;"/>
# 
# Die Sektoren (1-8 KB) sind die kleinste physische Leseeinheit. Die Größe eines Sektors wird vom jeweiligen Hersteller festgelegt. Auf den äußeren Spuren befinden sich mehr Sektoren als auf den inneren.
# Zwischen den Sektoren existieren Lücken. Sie sind nicht magnetisiert und dienen zum Auffinden der Sektoranfänge. Diese Lücken nehmen etwa 10% der gesamten Spur ein. </br>
# Aus den Sektoren lesen wir Blöcke. Blöcke sind die logische Übertragungseinheit. Es ist also die Einheit, die wir auf einmal in den Hauptspeicher laden. Ein Block kann auch aus mehreren Sektoren bestehen.
#   
# <img src="https://upload.wikimedia.org/wikipedia/commons/7/75/Hard_disk_head.jpg" alt="Aufbau_3" width="500" style="background-color: white;"/>
#   
# <img src="pictures/Aufbau_4.png" alt="Aufbau_4" width="500" style="background-color: white;"/>
#     
# Hier in dieser Grafik hat jede Spur die gleiche Anzahl an Sektoren. Normalerweise haben die inneren weniger und die äußeren Spuren mehr Sektoren. Eine Ausnahme wäre es, wenn die Sektoren unterschiedlich groß sind. 

# ### Zone Bit Recording
# 
# Mehrere Spuren übereinander betrachtet ergeben einen Zylinder. Die äußeren Zylinder haben einen größeren Radius und somit auch mehr Fläche. Bei gleichen Radii führt dies zu einer (nicht notwendigen) niedrigeren Bitdichte.
# Die Lösung sind Zonen mit unterschiedlichen Sektoreinteilungen.
# Für die folgenden Berechnungen ignorieren wir diesen Fall.
# 
# <img src="pictures/ZoneBitRecording.png" alt="ZoneBitRecording" width="500" style="background-color: white;"/>
# 

# ### Disk Controller
# 
# Ein Disk Controller kontrolliert eine oder mehrere Disks und die Bewegung der Schreib-/Lese-Köpfe. 
# Außerdem wählt er die Plattenoberfläche, auf die zugegriffen werden muss und den Sektor innerhalb der Spur, die sich aktuell unter dem Schreib-/Lese-Kopf befindet. Dadurch kontrolliert er Start und Ende eines Sektors.
# Der Disk Controller überträgt noch Bits zwischen Disk und Hauptspeicher und umgekehrt.
# 
# <img src="pictures/DiskController.png" alt="DiskController" width="500" style="background-color: white;"/>

# ### Beispiel - Megatron 747 disk
# 
# Ein Beispiel ist die Megatron 747 Disk mit den folgenden Eigenschaften: </br>
# Sie hat 8 Platten mit 16 Plattenoberflächen. Der Durchmesser beträgt 3,5 Zoll.
# Sie hat 2^16 = 65.536 Spuren pro Oberfläche, durchschnittlich 2^8 = 256 Sektoren pro Spur und 2^12 = 4.096 Byte pro Sektor.</br></br>
# Die Gesamtkapazität ergibt sich durch multiplizieren von #Plattenoberflächen, Spuren pro Oberfläche, Sektoren pro Spur und Byte pro Sektor: 16 x 65.536 x 256 x 4.096 = 2^40 Byte = 1 TB. Insgesamt hat die Megatron eine Gesamtkapazität von einem Terrabyte. </br></br>
# Die Blöcke können beispielsweise eine Größe von 2^14 Byte (= 16 KB) haben. Dann passen 4 Sektoren in einen Block (2^14 / 2^12) und es gibt im Durchschnitt 64 Blöcke pro Spur (2^8 / 2^2). </br></br>
# Die Bitdichte für die äußerste Spur wird wie folgt berechnet:
# - Bits pro Spur: 28 Sektoren x 2^12 Byte = 2^20 = 1024 KB = 8 MBit
# - Die Spurlänge (äußerste Spur) beträgt 3,5“ · p ≈ 11‘‘
# - mit ca. 10% Lücken hat man eine Spurlänge von 9,9‘‘, die 8 MBits hält
# 
# Somit sind 840.000 Bits pro Zoll vorhanden. 

# ### Disk-Zugriffseigenschaften
# 
# Eine Voraussetzung für den Zugriff auf einen Block (lesend oder schreibend) ist, dass der S-/L-Kopf auf den richtigen Zylinder positioniert ist, der die Spur mit dem Block enthält. Dann muss die Disk so rotieren, dass Sektoren, die der Block enthält, unter den S-/L-Kopf gelangen. </br>
# Hierbei sprechen wir von der Latenzzeit. Sie beschreibt die Zeit zwischen der Anweisung einen Block zu lesen und bis zum Eintreffen des Blocks im Hauptspeicher.

# ### Latenzzeit
# 
# - Latenzzeit setzt sich aus der Summe von vier Komponenten zusammen:
#     1. Kommunikationszeit zwischen Prozessor und Disk Controller:
#        - Es beträgt nur den Bruchteil einer Millisekunde und kann daher bei Berechnungen hier ignoriert werden. 
# 
#     2. Seektime (Suchzeit) zur Positionierung des Kopfes unter richtigem Zylinder:
#        - Die Suchzeit ist zwischen 0 und 40 ms ( proportional zum zurückgelegten Weg).
#        - Sie setzt sich zusammen aus Startzeit (1 ms), Bewegungszeit (0 – 40 ms) und Stopzeit (1 ms).
# 
#     3. Rotationslatenzzeit zur Drehung der Disk bis der erste Sektor des Blocks unter S-/L-Kopf liegt:
#        - Durchschnittlich benötigt es eine halbe Umdrehung (4 ms) bis der erste Sektor des Blocks unter dem S-/L-Kopf liegt.
#        - Es ist eine Optimierung durch Spur-Cache im Disk-Controller möglich.
# 
#     4. Transferzeit zur Drehung der Disk bis alle Sektoren und die Lücken des Blocks unter S-/L-Kopf passiert sind:
#        - Es wird ca. ein 16 KB-Block in 0.25 ms passiert.

# ### Schreiben und Ändern von Blöcken
# 
# Das Schreiben von Blöcken ist in Bezug zu Vorgehen und Zeit analog zum Lesen. Um zu überprüfen, ob eine Schreiboperation erfolgreich war, muss eine Rotation gewartet werden. (Die Nutzung von Checksums wird später beschrieben). </br>
# 
# Das Ändern von Blöcken ist nicht direkt möglich. Sondern geschieht in 4 Schritten:
# 
# 1. Der jeweilige Block wird in den Hauptspeicher gelesen. 
# 2. Die Daten auf dem Block werden geändert.
# 3. Der Block wird auf die Festplatte zurückgeschrieben.
# 4. Zum Schluss wird eventuell die Korrektheit der Schreiboperation überprüft
# 
# Die Zeit für solch eine Operation ergibt sich aus t_read + t_write. Mit ein wenig Glück ist der Kopf noch in der Nähe, wodurch t_write billiger wird. 

# ### Beispiel – Megatron 747 Disk
# 
# Wie lange dauert es, einen Block (16 KB = 16 384 Byte) zu lesen?
# Diese Frage soll nun am Beispiel der Megatron 747 Disk beantwortet werden. </br>
# 
# Die Umdrehungsgeschwindigkeit beträgt 7200 U · min-1. Somit dauert eine Umdrehung 8,33 ms. </br>
# 
# Zunächst wird die Seektime berechnet: </br>
# Die Start- und Stopzeit beträgt zusammen eine Millisekunde. </br>
# Pro 4000 Zylinder wird 1ms benötigt:
#     - Minimal werden 0 Zylinder übersprungen und man bleibt an der Stelle an der man ist. Dafür werden 0ms benötigt.
#     - Wenn man eine Spur (Track) überspringt, kostet das 1,00025ms (≈1ms).
#     - Maximal werden 65.536 Zylinder übersprungen und das kostet 65536/4000 + 1 = 17,38ms.
# </br>
# 
# Als nächstes wird die minimale Zeit berechnet, um einen Block zu lesen: </br>
# Dafür muss der S-/L-Kopf über der richtigen Spur stehen und die Platte schon richtig rotiert worden sein. Ein Block (16KB) ist über 4 Sektoren und 3 Lücken verteilt. Diese müssen gelesen werden. Insgesamt gibt es durchschnittlich 256 Lücken und 256 Sektoren pro Spur (wurde in vorherigem Unterkapitel so definiert). Die Lücken bedecken 36° (10%) einer Spur. Die Sektoren bedecken 324° des Kreises (360°). </br> 
# Das Verhältnis wird berechnet mit 324° x 4 / 256 + 36° x 3 / 256 = 5,48°. Es sind also 5,48° des Kreises durch einen Block bedeckt.
# 5,48° im Verhältnis zur Gesamtrotation (360°) und einer Umdrehung ergeben dann eine Lesezeit von (5,48° / 360°) · 8,33 ms = 0,13 ms.
# 
# Die maximale Zeit zum Lesen eines Blocks wird in der Präsenzübung vertieft. (Kleiner Spoiler: Sie beträgt 25,84 ms).
# Die durchschnittliche Zeit können Sie selber erforschen und nachrechnen. (Dabei sollten sie auf ungefähr 10,76 ms kommen).

# ## Effiziente Diskoperationen
# 
# Die Kopfbewegungen sollen möglichst minimiert werden, sodass der Kopf nicht die ganze Zeit von Spur zu Spur oder von Block zu Block hin- und herspringt. Dies zieht gewisse Anforderungen mit sich: Zum Einem sollen die Daten auf der Festplatte sinnvoll liegen. Zum Anderen sollte es Indexstrukturen geben, sodass man nicht Suchen muss. 

# ### Algorithmen vs. DBMS
# 
# Zuvor war die Annahme bei Algorithmen (wie in der Vorlesung 'Datenstrukturen und Algorithmen'), dass die gesamten Daten in den RAM passen (RAM-Berechnungsmodell) und sie auch bereits dort im Hauptspeicher liegen. 
# 
# Die Annahme bei der Implementierung von DBMS ist das I/O-Modell. Die gesamten Daten passen nicht mehr in Hauptspeicher.
# 
# Die Externspeicher-Algorithmen funktionieren oft anders. Ein guter Externspeicher-Algorithmus muss nicht der beste Algorithmus laut RAM-Modell sein. Sein primäres Entwurfsziel ist es I/O zu vermeiden. 
# 
# Das Gleiche kann auch für Hauptspeicher-Algorithmen gelten. Diese nutzen den Cache aus und berücksichtigen die Cachegröße. Es wird versucht die Lokalität zu nutzen und alle fernerliegende Zugriffe zu vermeiden („maximiere“ Anzahl der Cache Hits).

# ### I/O-Modell
# 
# Als Beispiel sei ein einfaches DBMS gegeben. Dieses ist zu groß für den  Hauptspeicher. Es gibt eine Disk, einen Prozessor und viele konkurrierende Nutzer bzw. Anfragen.
# 
# Der Disk-Controller hält und organisiert eine Warteschlange (Priority Queue) mit Zugriffsaufforderungen auf die Datenbank. Das Abarbeitungsprinzip der Zugriffsaufforderungen ist hierbei first-come-first-served. Generell muss angenommen werden, dass jede Aufforderung zufällig ist. Also der Kopf an einer zufälligen Position ist. 
# 
# Außerdem dominieren die I/O-Kosten. Wir berücksichtigen nicht was im Hauptspeicher geschieht. Die Kosten des Lesens und Bewegens eines Blocks zwischen Disk und Hauptspeicher sind wesentlich größer als die Kosten der Operationen auf den Daten im Hauptspeicher.
#   
# Die Anzahl der Blockzugriffe (lesend und schreibend) ist eine gute Approximation der Gesamtkosten und sollte minimiert werden. Anhanddessen kann die Effizienz von Algorithmen beschrieben werden. 

# 16:05

# ### Beispiel für das I/O-Modell (1): Indizes
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

# ### Beispiel für das I/O-Modell (2): Sortierung
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

# ### Merge Sort
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

# ### Two-Phase, Multiway Merge-Sort (TPMMS)
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
# ### TPMMS - Phase 1
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
# ### TPMMS - Phase 2
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
# ### Bemerkungen zur Blockgröße
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
# ### TPMMS – Grenzen
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

# ### Daten gemäß Zylinder organisieren
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

# ### Zylinderorganisation – Beispiel
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

# ### Mehrere Disks
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

# ### Spiegelung
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

# ### Disk Scheduling
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

# ### First-First-First-Servce vs. Elevator Algorithmus
# 
# <img src="pictures/FFFS-vs-Elevator-Algo.png" alt="FFFS-vs-Elevator-Algo" width="500" style="background-color: white;"/>
# 

# ### Elevator Algorithmus
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

# ### Prefetching
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
