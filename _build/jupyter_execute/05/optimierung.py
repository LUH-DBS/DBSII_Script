#!/usr/bin/env python
# coding: utf-8

# # Optimierung

# In diesem Kapitel wird die Optimierung auf logischer Ebene betrachtet. Es geht mehr um die Daten selbst als um die Speicherabbildung. 

# ## Wiederholung: Anfragebearbeitung
# Zunächst eine kleine Wiederholung zur Anfragebearbeitung in Bezug auf das Grundproblem und den Ablauf.
# 
# ### Grundproblem
# Anfragen in SQL und der Relationalen Algebra sind deklarativ. Solche Anfragen müssen in ausführbare (prozedurale) Form transformiert werden. Also in echte ausführbare Programme. Die Ziele dabei sind ein "QEP" (prozeduraler Query Execution Plan) und Effizienz. Eine Anfrage soll schnell und wenige Ressourcen verbrauchen (CPU, I/O, RAM, Bandbreite). 

# ### Ablauf der Anfragebearbeitung
# 
# <img src="pictures/Ablauf-Anfragebearbeitung.png" alt="Ablauf-Anfragebearbeitung" width="250" style="background-color: white;"/>
# 
# 1. **Parsing**</br>
#     Als erstes wird die Anfrage geparsed und überprüft, ob diese syntaktisch korrekt ist. Danach werden die Elemente semantisch überprüft und ein Parsebaum erstellt. 
# 
# 2. **Wahl des logischen Anfrageplans**</br>
#     Im zweiten Schritt werden exponentiell viele Bäume mit logischen Operatoren erstellt. Darunter wird der optimale Plan ausgewählt, indem vorher logisch, regelbasiert und kostenbasiert optimiert wird. 
# 
# 3. **Wahl des physischen Anfrageplans**</br>
#     Anhand des logischen Plans wird ein ausführbares Programm mit physischen Operatoren erstellt. Das Programm enthält Algorithmen und Scan-Operatoren. Der optimale Plan wird physisch optimiert und dann ausgewählt. Zum Schluss wird der ausgewählte Anfrageplan ausgeführt. 

# <img src="pictures/Meme-Finish-SQL-Query.png" alt="Meme-Finish-SQL-Query" width="250" style="background-color: white;"/>

# ## Ablauf der Anfragebearbeitung 
# 
# Die einzelnen Schritte bei der Anfragebearbeitung werden nun genauer betrachtet. 

# ### Parsing 
# 
# <img src="pictures/Ablauf-Anfragebearbeitung_2.png" alt="Ablauf-Anfragebearbeitung_2" width="500" style="background-color: white;"/>
# 
# Beginnend beim Parsing wird auf **syntaktische Korrektheit** überprüft. Dafür wird eine Grammatik für einen Teil von SQL betrachtet. (SFW steht für SelectFromWhere): </br>
# 
# - Anfragen
#     - \<Anfrage> :: = \<SFW>
#     - \<Anfrage> :: = ( \<SFW> )
#     - die Mengenoperatoren fehlen
# - SFWs
#     - \<SFW> ::= SELECT \<SelListe> FROM \<FromListe> WHERE \<Bedingung>
#     - die Gruppierung, Sortierung etc. fehlen
# - Listen
#     - \<SelListe> ::= \<Attribut>, \<SelListe>
#     - \<SelListe> ::= \<Attribut>
#     - \<FromListe> ::= \<Relation>, \<FromListe>
#     - \<FromListe> ::= \<Relation>
# - Bedingungen
#     - \<Bedingung> ::= \<Bedingung> AND \<Bedingung>
#     - \<Bedingung> ::= \<Tupel> IN \<Anfrage>
#     - \<Bedingung> ::= \<Attribut> = \<Attribut>
#     - \<Bedingung> ::= \<Attribut> LIKE \<Muster>
# - \<Tupel>, \<Attribut>, \<Relation> und \<Muster> sind nicht durch eine grammatische Regel definiert
# 
# Die vollständige Grammatik kann man zum Beispiel [hier]( http://docs.openlinksw.com/virtuoso/GRAMMAR.html) finden. 
# </br></br>
# 
# Anschließend wird während der Übersetzung die **semantische Korrektheit** überprüft. Beantwortet werden dabei generell Fragen wie:
# - Existieren die Relationen und Sichten der FROM Klausel?
# - Existieren die Attribute in den genannten Relationen? Sind sie eindeutig?
# - Sind die Typen für die Vergleiche korrekt?
# - Ist die Aggregation korrekt?   
# 

# ## Algebraische Transformationsregeln 
# 
# <img src="pictures/Ablauf-Anfragebearbeitung_3.png" alt="Ablauf-Anfragebearbeitung_3" width="500" style="background-color: white;"/>
# 
# Das Ziel ist es aus dem Parsebaum einen logischen Anfrageplan zu erstellen. Ohne die Semantik der Anfrage zu ändern, soll sie in eine interne Darstellung verwandelt werden. Um die Anfrage effizienter auszuführen, sollen insbesondere kleine Zwischenergebnisse erzielt werden. </br>
# Am Ende sollen es äquivalente Ausdrücke sein. Zwei Ausdrücke der relationalen Algebra heißen äquivalent, falls sie die gleichen Operanden (=Relationen) nutzt und für jede mögliche Instanz der Datenbank stets die gleiche Antwortrelation ausgibt. 
# 
# 
# ### Kommutativität und Assoziativität
# 
# Die Gesetze gelten jeweils für Mengen und Multimengen. Die verwendeten Ausdrücke können in beide Richtungen verwendet werden. 
# 
# - ? ist kommutativ und assoziativ
#     - R ? S = S ? R
#     - (R ? S) ? T = R ? (S ? T)
# - ∪ ist kommutativ und assoziativ
#     - R ∪ S = S ∪ R 
#     - (R ∪ S) ∪ T = R ∪ (S ∪ T) 
# - ∩ ist kommutativ und assoziativ 
#     - R ∩ S = S ∩ R 
#     - (R ∩ S) ∩ T = R ∩ (S ∩ T)
# - ⨝ ist kommutativ und assoziativ 
#     - R ⨝ S = S ⨝ R 
#     - (R ⨝ S) ⨝ T = R ⨝ (S ⨝ T)
#     
# 
# ### Weitere Regeln
# 
# Für Selektionen und Projektionen gelten die folgenden Regeln: 
# 
# - Selektion σ
#     - $σ_{c1 AND c2}(R) = σ_{c1}(σ_{c2}(R))$
#     - $σ_{c1 OR c2}(R) = σ_{c1}(R) ∪ σ_{c2}(R)$
#         - nicht bei Multimengen
#     - $ σ_{c1}(σ_{c2}(R)) = σ_{c2}(σ_{c1}(R))$
#     - $ σ_{c}(R Φ S) ≡ (σ_{c}(R)) Φ (σ_{c}(S))$
#         - Φ ∈ {∪, ∩, -, ⨝}
#     - $ σ_{c}(R Φ S) ≡ (σ_{c}(R)) Φ S$
#         - Φ ∈ {∪, ∩, -, ⨝}
#         - Falls sich c nur auf die Attribute in R bezieht. 
# </br>
# 
# - Projektion π
#     - $π_{L}(R ⨝ S) = π_{L}(π_{M}(R) ⨝ π_{N}(S))$
#     - $π_{L}(R ⨝_{C} S) = π_{L}(π_{M}(R) ⨝_{C} π_{N}(S))$
#     - $π_{L}(R x S) = π_{L}(π_{M}(R) x π_{N}(S))$
#     - $π_{L}(σ_{c}(R)) = π_{L}(σ_{c}(π_{M}(R))$
# 

# ## Logische Anfragepläne
# 
# <img src="pictures/Ablauf-Anfragebearbeitung_4.png" alt="Ablauf-Anfragebearbeitung_4" width="500" style="background-color: white;"/>
# 
# Um nun zu einem logischen Anfrageplan zu gelangen, benötigt es zwei Schritte.

# ### Zwei Schritte 
# 
# **Schritt 1**</br>
# In Schritt 1 wird der Parsebaum in einen Ausdruck der relationalen Algebra übersetzt und dann wieder als Baum dargestellt. Unter anderem werden auch Subanfragen aufgelöst. Letzteres wird aber nicht in dieser Vorlesung weiter thematisiert. 
# </br>
# 
# **Schritt 2**</br>
# Der Baum wird im zweitem Schritt gemäß der Transformationsregeln umgeformt. Man kann auch "Vor-Optimierungen" mittels Heuristiken durchführen. Dazu zählt unter Anderem:
# - das Pushen von Selektionen,
# - das Einbauen und Pushen von Projektionen, 
# - das Zusammenfügen von Selektion und Kreuzprodukt zu einem Join,
# - die Gruppierung von Vereinigungen und Joins,
# - und eventuell das Verschieben und Einbauen von Duplikateliminierungen. 

# ### Beispiel - Anfragebearbeitung 
# 
# In diesem Beispiel ist ein Ausdruck der relationalen Algebra in einem Parsebaum dargestellt. Die zugehörige SQL-Anfrage wäre
# ```
# SELECT Nachname
# FROM mitarbeiter m, projekte p
# WHERE p.Budget < 40000
# AND m.p_id = p.p_id;
# ```
# 
# Man sollte damit beginnen das Kreuzprodukt mit der Selektion zu einem Join zu kombinieren. 
# 
# <img src="pictures/Anfragebearbeitung-Beispiel-1.png" alt="Anfragebearbeitung-Beispiel-1" width="500" style="background-color: white;"/>
# 

# Als nächstes sollte man versuchen die andere Selektion weiter nach unten zu pushen (Push-Down). Ziel ist es mit möglichst wenigen Tupeln in jedem Teilschritt zu arbeiten. Die gegebene Selektion kann direkt vor die Projekt-Relation geschoben werden. 
# 
# <img src="pictures/Anfragebearbeitung-Beispiel-2.png" alt="Anfragebearbeitung-Beispiel-2" width="500" style="background-color: white;"/>

# In einem weiterem Schritt können die benötigten Attribute aus den Ausgangsrelationen direkt rausprojiziert werden. 
# 
# <img src="pictures/Anfragebearbeitung-Beispiel-3.png" alt="Anfragebearbeitung-Beispiel-3" width="500" style="background-color: white;"/>

# ### Übergang zum Physischen Anfrageplan
# 
# Hierbei gibt es diverse Freiheitsgrade:
# 1. Die Reihenfolge und Gruppierung von assoziativen und kommutativen Operatoren können vertauscht werden. Das ist zum Beispiel der Fall bei Joins, Vereinigungen und Schnittmengen. 
# 2. Für jeden Operator kann ein Algorithmus gewählt werden. Damit sind die aus dem vorherigen Kapitel kennengelernten Hash-basierten, Sort-basierten oder auch One-Pass Algorithmen gemeint.
# 3. Es können zusätzliche Operatoren (Sort und Projektion), die im logischen Plan selbst nicht auftauchen, hinzugefügt werden. 
# 4. Außerdem kann der Modus des Datentransports zwischen den Operatoren gewählt werden. Modi wären eine temporäre Tabelle oder eine Pipeline mit Iterator. 
# 
# Dafür braucht man in jedem Fall zunächst eine Kostenabschätzung. Man möchte herausfinden, wann es sinnvoll ist, welche Operationsreihenfolgen zu nutzen und wie viel ein Plan gesamt kostet. 

# ## Kostenmodell 
# 
# Beim Kostenmodell werden die Kardinalitäten abgschätzt. Man möchte wissen wie viele Tupel es gibt und wie viele unterschiedliche Werte in den einzelnen Attributen einer Relation vorhanden sind. 
# 
# <img src="pictures/Ablauf-Anfragebearbeitung_5.png" alt="Ablauf-Anfragebearbeitung_5" width="500" style="background-color: white;"/>

# ### Kostenbasierte Optimierung (Wiederholung)
# 
# Konzeptionell werden alle denkbaren Ausführungspläne generiert. Die Kosten für jeden Plan werden anhand eines Kostenmodells bewertet. Dazu werden Statistiken und Histogramme hinzugezogen. Die Parameter werden anhand der Rechnerarchitektur, auf der die Datenbank aufgesetzt ist, kalibriert. Die Optimierung ist abhängig vom verfügbaren Speicher. Dann wird anhand des Aufwands-Kostenmodell geschaut was und wie optimiert werden soll. Entweder Durchsatz maximierend oder nicht Antwortzeit-minimierend. Entsprechend wird der günstigste Plan ausgeführt. Wichtig ist, dass nicht zu lange optimiert wird, da sich sonst der ganze Aufwand nicht lohnen könnte. 

# <img src="pictures/TimeCost-Meme.png" alt="TimeCost-Meme" width="350" style="background-color: white;"/>

# ### Problemgröße (Suchraum) (Wiederholung)
# 
# Wie zuvor erwähnt, werden konzeptionell alle denkbaren Ausführungspläne generiert. Man berechnet nun die Bushy-Pläne mit n Tabellen. Bushy-Plan bedeutet, dass der Baum immer balanciert ist. 
# 
# $$\frac{(2(n-1))!}{(n-1)!}$$ 
# 
# | n | $2^n$ | n! | $\frac{(2(n-1))!}{(n-1)!}$ |
# |-|-|-|-|
# | **2** | 4 | 2 | 2 |
# | **5** | 32 | 120 | 1680 |
# | **10** | 1024 | 3628800 | 1,76 * 10^10 |
# | **20** | 1048576 | 2,4 * 10^18 | 4,3 * 10^27 |
# 
# </br>
# 
# Die Anzahl der Deep-Pläne mit n Tabellen ist n!. Die Plankosten unterscheiden sich um viele Größenordnungen. Das Optimierungsproblem ist NP-hard (NP-Schwer). 
# </br>
# 
# Folie: Prof. Alfons Kemper, TU München.

# ### Kostenmodell (Wiederholung) 
# 
# Gegeben ist ein algebraischer Ausdruck z.B. ein Anfrageplan. Das Kostenmodell schätzt die Ausführungskosten für diesen Ausdruck. Im Kostenmodell werden Punkte wie die Indexinformationen, die Ballungs-Informationen (Clustering on disk), die DB-Kardinalitäten und die Attributverteilungen berücksichtigt. 
# 
# <img src="pictures/Kostenmodell.png" alt="Kostenmodell" width="500" style="background-color: white;"/>

# ### Statistiken (Wiederholung)
# 
# <img src="pictures/Statistiken-Histogram-of-arrivals.png" alt="Statistiken-Histogram-of-arrivals" width="500" style="background-color: white;"/>
# 
# Man kann unterschiedliche Statistiken für das Kostenmodell nutzen. Für die Statistiken kann man verschiedene Werte berücksichtigen. Zu jeder Basisrelation gibt es die Anzahl der tupel und die Größe der einzelnen Tupel. 
# Zu (jedem) Attribut gibt es den minimalen und maximalen Wert, eine Werteverteilung (Histogramm) und die Anzahl der distinct Werte. Zum System sind die Speichergröße, die Bandbreite, I/O- und CPU-Zeiten angegeben. 
# </br>
# 
# Das eigentliche Problem ist das Erstellen und Updaten der Statistiken. Wenn man eine Datenbank hat, die sich sehr schnell immer wieder verändert, müssen die Statistiken dazu auch häufig neu erstellt werden (```runstats()```). Dies kostet weitere Ressourcen. Man sollte sich überlegen wie genau man die Statistiken haben möchte und dementsprechend viel Zeit in das Optimieren investieren. Aus diesem Grund initiiert man meist nur explizit/manuell die Erstellung und das Update der Statistiken. 

# ### Kosten von Operationen
# 
# Das wesentliche Kostenmerkmal bei Operationen ist die Anzahl der Tupel im Input. Insbesondere ist die Frage, ob die Relation in den Hauptspeicher passt und man darauf Operationen wie Selektion, Projektion, Sortierung und Join ausführen kann.  </br>
# Der Output ist immer der Input des nächsten Operators. Deshalb schätzt ein Kostenmodell unter anderem für jede Operation die Anzahl der Ausgabetupel.
# Zum Schätzen wird die „Selektivität“ in Bezug auf Inputgröße herangezogen. Sie gibt an wie viele Eingabetupel ein Operator herausselektiert und wie viele Ausgabetupel dann erwartet werden können. Es wird auch „Selektivitätsfaktor“ (selectivity factor, sf) genannt. 
# - #Ausgabetupel = #Eingabetupel x Selektivität

# ### Kostenschätzung - Projektion 
# 
# Die Größe des Zwischenergebnisses kann bei der Projektion exakt ausgerechnet werden. </br>
# </br>
# **Beispiele**</br>
# Gegeben ist eine Relation R(A integer(4), B integer(4), C varchar(100)) mit einem Tupelheader von 12 Byte. 
# 
# **1:**</br>
# Somit ergeben sich insgesamt 120 Byte pro Tupel. Ein Block besteht aus 1024 Byte mit einem 24 Byte Header. Also sind es 8 Tupel pro Block. </br>
# Bei einer Relation R mit 10000 Tupeln: T(R) = 10000, kommt man bei 8 Tupeln pro Block, auf insgesamt 1250 Blöcke, die benötigt werden: B(R) = 1250.
# </br>
# 
# **2:**</br>
# $Q_{1} = \pi_{A+B,C}(R)$</br>
# Daraus ergeben sich 116 Byte pro Tupel. Bei 8 Tupeln pro Block hat man wieder 1250 Blöcke pro Tupel: B($Q_{1}$) = 1250.
# </br>
# 
# **3:**</br>
# $Q_{2} = \pi_{A,B}(R)$ </br>
# Man erhält 20 Byte pro Tupel. Insgesamt also 50 Tupel pro block und B($Q_{2}$) = 200. 
# 
# 

# ### Kostenschätzung - Selektion
# 
# Im Gegensatz zur Projektion bleibt zwar die Tupelgröße, aber die Anzahl der Tupel sinkt bei der Selektion. </br>
# $Q=\sigma_{A=c}(R)$ </br>
# Die Formel zur Selektion zeigt einen Vergleich zwischen dem Attribut A und der Konstante c. Basierend auf Annahmen kann man die Anzahl der Ausgabetupel berechnen. Die erste Annahme ist, dass die Werte gleich verteilt sind. Die zweite, dass c einer dieser Werte ist. Zur Berechnung nutzt man die Formel $T(Q) = T(R) / V(R,A)$. $V(R,A)$ ist die Anzahl der distinct Werte in Spalte A. D.h. der Selektivitäsfaktor ist $1 / V(R,A)$. Bessere Abschätzungen sind mittels Histogrammen möglich.  
# <br>
# 
# $Q=\sigma_{A<c}(R)$</br>
# Der Vergleich der Selektion A < c macht eine Bereichsabfrage. Es gibt Möglichkeiten dies genau abzuschätzen. Einfachheitshalber nutzen wir hier eine erste Abschätzung: $T(Q) = T(R) / 2$. Typischer ist die Formel $T(Q) = T(R) / 3$.
# <br>
# 
# $Q=\sigma_{A \neq c}(R)$</br>
# Man möchte in der Selektion nicht die Attribute haben, die der Konstante c entsprechen. Eine erste einfache Abschätzung wäre es davon auszugehen, dass man (fast) alles zurückbekommt: $T(Q) = T(R)$. Etwas genauer ist stattdessen die Formel $T(Q) = T(R) * (V(R,A) - 1) / V(R,A)$. Sie ist sehr ähnlich zu der ersten Formel vom Vergleich ($Q=\sigma_{A=c}(R)$). Der Unterschied besteht darin, dass sie nicht alle Tupel zurückgibt, die gleich der Konstante sind, sondern genau das Gegenteil: Alle Tupel, die ungleich der Konstante sind. 
# </br>
# 
# Hat man Konjunktionen bei mehreren Selektionsbedingungen, multipliziert man die Selektivitätsfaktoren. Die Annahme dafür ist die Unabhängigkeit der Bedingungen. 
# 

# ### Selektivität schätzen
# 
# <img src="pictures/Selektivität-schätzen.png" alt="Selektivität-schätzen" width="500" style="background-color: white;"/>
# 
# Das Bild ist aus dem Werk für das System R von Selinger et al. aus dem Jahre 1979. Man sieht die Möglichkeiten zur Einschätzung der Selektivität. Beim Schätzen wird fast immer eine Gleichverteilung angenommen.

# ### Beispiel für Skew: Zipf-Verteilung
# 
# <img src="pictures/George-Kingsley-Zipf.png" alt="George-Kingsley-Zipf" width="200" style="background-color: white;"/>
# 
# Eine sehr bekannte Verteilung ist die Zipf-Verteilung von George Kingsley Zipf (1902 - 1950). Sie modelliert Worthäufigkeiten in den Texten einer Sprache. Die Wörter werden nach ihren Häufigkeiten sortiert. Die Häufigkeit des häufigsten Wortes sei dabei h. Wenn alles sortiert ist kann man beispielsweise für den i-ten Wert die Häufigkeit berechnen. Der i-te Wert tauch dann genau $h / i^{1/2}$ mal auf. Der zughörige Graph sieht wie folgt aus:
# 
# <img src="pictures/Beispiel-Skew-Graph.png" alt="Beispiel-Skew-Graph" width="500" style="background-color: white;"/>
# 
# Wenige Werte kommen sehr häufig vor, die vielen anderen Werte kommen hingegen sehr selten vor. Anhand der Verteilung könnte man nun probieren die Kardinalitätsabschätzung anzupassen. Dennoch sollte es eher gelassen werden. Die durchschnittliche Antwortkardinalität bleibt weiter $T(R) / V(R,A)$. Durch die Annahme, dass Konstanten in Selektionsbedingungen gleichverteilt gewählt werden, kann es bei der Zipf-Verteilung der Konstanten zu einer Unterschätzung kommen. 

# <img src="pictures/Zipfs-law.png" alt="Zipfs-law" width="500" style="background-color: white;"/>
# 
# A plot of the rank versus frequency for the first 10 million words in 30 Wikipedias (dumps from October 2015) in a [log-log](https://en.wikipedia.org/wiki/Log%E2%80%93log_plot) scale.
# 
# Das Beispiel zeigt das Prinzip von Zipf's law. Außerdem ist es unabhängig von der jeweils gewählten Sprache. 

# ### Kostenschätzung - Selektion
# 
# **Beispiele**</br>
# Gegeben ist eine Relation R mit T(R) = 10000 und V(R,A) = 50. 
# </br>
# 
# **1:**</br>
# $Q = \sigma_{A=10 AND B<20}(R)$</br>
# Die Ausgabetupel werden geschätzt mit $T(Q) = 10000 * 1/50 * 1/3 = 67$.
# </br>
# 
# **2:**</br>
# $Q = \sigma_{A=10 AND A>20}(R)$</br>
# Im ersten Moment würde man die Ausgabetupel mit $T(Q) = 10000 * 1/50 * 1/3 = 67$ schätzen. Bei genauerer Betrachtung fällt auf, dass die Bedingung so nicht möglich ist. Das Attribut kann gleichzeitig nicht genau 10 und über 20 sein. Besser ist die Abschätzung T(Q) = 0. Ein Optimierer sollte solche Fälle erkennen. 
# </br>

# ### Kostenschätzung - Selektion mit Disjunktion
# 
# 
# $Q = \sigma_{C1 OR C2}(R2)$</br>
# 
# **Idee 1**</br>
# Bilde die Summe der Ergebniskardinalitäten mit der Annahme, dass kein Tupel beide Bedingungen erfüllt. Dennoch kann es dazu führen, dass das Ergebnis größer als die Ursprungsrelation ist: T(Q) > T(R). 
# </br>
# 
# **Idee 2**</br>
# Daher könnte man nun das Minimum unter der Anzahl der Tupel in R und der Summe der Ergebniskardinalitäten wählen: $min[T(R), Summe der Ergebniskardinalitäten]$. Es ist keine perfekte Lösung, aber ein erster Versuch sich näher an das richtige Ergebnis heranzutasten. 
# </br>
# 
# **Idee 3**</br>
# Nutze die Wahrscheinlichkeitstheorie mit der Annahme, dass C1 und C2 unabhängig voneinander sind. Sei 
# - $T(R) = n$,
# - $T(\sigma_{C1}(R)) = m_{1}$ und 
# - $T(\sigma_{C2}(R)) = m_{2}$. 
# 
# Daraus ergibt sich
# $T(Q) = n(1-(1-\frac{m_{1}}{n})(1-\frac{m_{2}}{n}))$. Wobei der Term $(1-\frac{m_{1}}{n})$ den Anteil der Tupel, die nicht C1 entsprechen, beschreibt. Der zweite ähnliche Term $(1-\frac{m_{2}}{n})$ beschreibt den Anteil der Tupel, die nicht C2 entsprechen. 
# </br>
# 
# **Beispiel**</br>
# Sei die Selektion $Q = \sigma_{A=10 OR B<20}(R)$ gegeben. Bilde zunächst wie in Idee 1 beschrieben von separat die Ergebniskardinalitäten beider Bedingungen und addiere beide anschließend:
# - $T(\sigma_{A=10}(R)) = T(R) / V(R,A) = 10000 / 50 = 200$
# - $T(\sigma_{B<20}(R)) = T(R) / 3 = 3333$
# - $T(Q) = 200 + 3333 = 3533$
# 
# Eine bessere Schätzung wäre mit Idee 3 möglich:
# - $T(R) = 10000$,
# - $T(\sigma_{A=10}(R)) = 200$ und
# - $T(\sigma_{B<20}(R)) = 3333$. 
# 
# Setzt man diese Werte in die Formel der Wahrscheinlichkeitstheorie ein, erhält man als Ergebnis 3466:
# $T(Q) = n(1-(1-\frac{m_{1}}{n})(1-\frac{m_{2}}{n})) = 10000 (1-(1-\frac{200}{10000})(1-\frac{3333}{10000}))$
# 
# Die Formel kann deutlich vereinfacht werden $m_{1} + m_{2} - n (\frac{m_{1}}{n} * \frac{m_{2}}{n})$</br>
# $= 200 + 3333 - 10000(\frac{200}{10000} * \frac{3333}{10000})$</br>
# $= 3533 - (\frac{666600}{10000})$</br>
# $= 3533 - 67$</br>
# $= 3466$</br>
# 

# ### Kostenschätzung - Join
# 
# In dieser Vorlesung betrachten wir nur den Natural Join. Das Verfahren beim Equijoin wäre analog dazu. Ein Thetajoin mit "<", ">" usw. wird wie zuvor geschätzt. Zum Beispiel mit $1/3 T(R) * 1/3 T(S)$.</br>
# 
# $R(X,Y) \Join S(Y,Z)$</br>
# Vereinfachend wird hier angenommen, dass wir nur über ein Attribut Y joinen. Ein Problem ist die Beziehung zwischen R.Y und S.Y. Man weiß nicht wie viele Elemente aus R.Y auch in S.Y auftauchen. Theoretisch kann man sagen, dass es disjunkte Mengen und nichts gleich ist. Damit würde man bei einem Join 0 Elemente erhalten: $T(R \Join S) = 0$. Eine weitere Möglichkeit wäre eine Fremdschlüsselbeziehung (mit einem Schlüssel in S). Dann wäre das Resultat die Menge an Tupeln in R: $T(R \Join S) = T(R)$. Es gibt noch eine dritte Möglichkeit, wenn man davon ausgeht, dass fast alles gleiche Werte sind: $T(R \Join S) = T(R) * T(S)$. </br>
# 
# Es müssen also wieder ein paar Annahmen getroffen werden. 
# Die erste Annahme sagt, dass die Werte eines Attributs, das in mehreren Relationen auftaucht, vom Beginn einer Liste gewählt wird. Das ist das sogenannte **Containment of Value Sets**. Falls also die Distinct-Werte der Relation R kleiner gleich den Distinct-Werten der anderen Relation S sind ($V(R,Y) \leq V(S,Y)$), dann taucht jeder Y-Wert in R auch in S auf. </br>
# Die zweite Annahme besagt, dass die Anzahl der Distinct-Werte eines nicht-Joinattributs erhalten bleiben: $V(R \Join S, X) = V(R,X)$. Auch **Preservation of Value Sets** genannt. Es ist realistisch, wenn von Gleichverteilung ausgegangen wird. Insbesondere, wenn die Relation S eine Fremdschlüsselbeziehung hat. Der einzige Fall bei dem es nicht mehr korrekt sein könnte ist, wenn das X ein Schlüssel ist.</br>
# </br>
# 
# Sei $V(R,Y) \leq V(S,Y)$, dann gilt:
# - jedes Tupel aus R hat eine $1 / V(S,Y)$ Chance, mit einem gegebenen S-Tupel zu joinen.
# - (da T(S) S-Tupel): Ein Tupel aus R hat $T(S) * 1/V(S,Y)$ Joinpartner in S. 
# - (da T(R) R-Tupel): $T(R \Join S) = T(R) * T(S) / V(S,Y)$.
# </br>
# 
# Falls $V(R,Y) \leq V(S,Y)$, dann gilt $T(R \Join S) = T(R) * T(S) / V(R,Y)$. </br>
# </br>
# 
# Allgemein gilt: $T(R \Join S) = T(R) * T(S) / max[V(R,Y), V(S,Y)]$.
# </br>
# 
# ### Kostenschätzung - Join Beispiel
# 
# Seien Joins zwischen drei Relationen gegeben:</br>
# $R(A,B) \Join S(B,C) \Join U(C,D)$.</br>
# 
# Die Anzahl der Tupel der Relationen ist wie folgt:
# - T(R) = 1.000
# - T(S) = 2.000
# - T(U) = 5.000
# 
# Die Selektionsfaktoren sind
# - V(R,B) = 20
# - V(S,B)= 50
# - V(S,C) = 100
# - V(U,C)=500
# 
# Die Joins werden in der Reihenfolge $(R \Join S) \Join U$ betrachtet. 
# Daher kann man zunächst $T(R \Join S)$ berechnen:
# $T(R \Join S) = T(R) * T(S) / max[V(R,B),V(S,B)] = 1.000 * 2.000 / 50 = 40.000$ </br>
# Aber man kann die Relation U auch direkt hinzujoin/heranmultiplizieren: $T(R \Join S \Join U) = T(R \Join S) * T(U) / max[V(R \Join S, C), V(U, C)] = 40.000 * 5.000 / max[100, 500] = 400.000$ </br>
# 
# 

# Zur Probe können Sie $T(R \Join (S \Join U))$ nachrechnen.

# 
# 
# <details>
#   <summary><strong>Lösung</strong></summary>
#     Auch wenn man zuerst die anderen Relationen miteinander joint, erhält man wieder das Selbe Ergebnis: 400000. 
# </details>
# 

# ### Kostenschätzung Join - Mehrere Attribute
# 
# $R(X,Y) \Join S(Y,Z)$</br>
# Y enthält nun mehr als ein Attribut. Die Schreibweise ist hier: $R(X,Y1,Y2) \Join S(Y1,Y2,Z)$</br>
# Die Ergebniskardinalität von $R \Join S$ entspricht dem Produkt der Kardinalitäten von R und S, dividiert durch das Produkt des jeweils größeren von V(R,Y) und V(S,Y) für jedes Join-Attribut Y: $T(R \Join S) = T(R) * T(S) / ( max[V(R,Y1),V(S,Y1)] * max[V(R,Y2),V(S,Y2)] )$

# ### Kostenschätzung - Mehrfacher Join
# 
# Im allgemeinen Fall $ S = R_{1} \Join R_{2} \Join ... \Join R_{n} $ wird in diesem Fall über das selbe Attribut A gejoint. Notiert wird es mit $V(R_{i}, A) = v_{i}$. Das Attribut A erscheint in k Relationen. Es gilt $v_{1} \leq v_{2} \leq ... \leq v_{k}$ mit $ k \leq n $. Die Frage ist nun wie die Kardinalität des Ergebnisses berechnet wird.</br>
# Dazu eine kleine Gedankenhilfe:
# Gegeben ist ein Tupel aus jeder der k Relationen. Gesucht wird die Wahrscheinlichkeit, dass alle im A-Wert übereinstimmen. Es gibt wieder das Containment of Value Sets: Jeder A-Wert von Tupeln aus $R_{1}$ taucht in den anderen Relationen auf. Ein Tupel aus $R_{i}$ hat eine Wahrscheinlichkeit von $1/v_{i}$ mit einem gegebenen Tupel aus $R_{1}$ übereinzustimmen. Zusammen ergibt sich $1 / v_{2} * v_{3} * … * v_{k}$. Die Wahrscheinlichkeiten der einzelnen Tupel der verschiedenen Relationen müssen nur multipliziert werden. </br>
# Für das Gesamtvorgehen ist der Ausgangspunkt also das Produkt aller Kardinalitäten zu bilden. Betrachtet man die Selektivität muss für jedes Attribut, das mehr als einmal auftaucht, durch das Produkt aller $v_{i}$ bis auf das kleinste ($v_{1}$ dividiert werden.
# 
# **Beispiel**</br>
# - Die Anfrage ist $R(A,B,C) \Join S(B,C,D) \Join U(B,E)$. 
# - Die Kardinalitäten sind
#     - T(R) = 1000;
#     - T(S) = 2000;
#     - T(U) = 5000.
# - Die DISTINCT Werte sind
#     - V(R,B): 20;
#     - V(R,C): 200;
#     - V(S,B): 50;
#     - V(S,C): 100;
#     - V(U,B): 200.
#  
# Vorgehen: Zunächst zählt man alle (Tupel-)Kombinationen der Relationen auf: $1000 * 2000 * 5000 = 10.000.000.000$. Dann werden die Wahrscheinlichkeiten für gemeinsame Attribute multipliziert. Die Relation B hat drei- und die Relation C hat zweimal gemeinsame Attribute. Für B ergibt sich: $1/50 * 1/200$. Für C wiederrum: $1/200$. 
# Zusammen ergibt sich: </br>
# $10.000.000.000 / (50 * 200 * 200)$</br>
# $= 10.000.000.000 / 2.000.000$</br>
# $= 5.000$

# ### Kostenschätzung - Weitere Operationen
# 
# **Vereinigung** $(R \cup S)$</br>
# Bei einer Multimenge bildet man die Summe der Inputs. Bei einer normalen Menge wählt man eine Vereinigung der Relationen, die größer ist als die größte Relation und kleiner als die Summe der Tupel aller Relationen: $max[T(R), T(S)] \leq T(R \cup S) \leq T(R) + T(S)$. Z.B könnte man auch den Durchschnitt von Maximum und Summe berechnen: $AVG[T(R) + T(S), max[T(R), T(S)]]$.
# 
# **Schnittmenge** $(R \cap S)$</br>
# Die Schnittmenge der Relationen muss größer als 0, aber noch kleiner als die kleinste Relation sein: $0 ≤ T(R \cap S) \leq min[T(R), T(S)]$. Die erste Idee zur Vereinfachung ist es die kleinste Relation zu halbieren: $min[T(R), T(S)]/2$. Die zweite Idee ist es, es als Join aufzufassen. Dabei kommt es häufig zu einer extremen Unterschätzung. 
# 
# **Differenz**</br>
# Die Differenz muss kleiner als die anfängliche Relation und größer als das Maximum von 0 und der Differenz der Anzahl der Tupel der Relationen: $max[0,T(R) - T(S)] \leq T(R - S) \leq T(R)$. Hier wählt man z.B. eine Mitte mit $max[0, T(R) – T(S)/2]$.
# 
# **Duplikateliminierung**</br>
# $T(\delta(R)) = V(R, [A_{1}, ..., A_{n}])$. Die Anzahl der Tupel muss kleiner gleich der Anzahl der Ausgangsrelation sein. Es darf natürlich nicht weniger als ein Tupel vorhanden sein: $1 \leq T(\delta(R)) \leq T(R)$. Man kann auch die Distinct-Werte miteinander multiplizieren $T(\delta(R)) \leq \prod_{i} V(R, A_{i})$. Z.B. kann dafür auch $T(\delta(R)) = min[T(R)/2, \prod_{i} V(R, A_{i})]$ genutzt werden. 
# 
# **Gruppierung und Aggregation**</br>
# Die Anzahl der Tupel muss auf jeden Fall kleiner gleich der Anzahl der Tupel in der Ausgangsrelation sein, aber dennoch muss es mindestens ein Tupel geben: $1 \leq T(\gamma_{L}(R)) \leq T(R)$. 
# Falls nur ein Gruppierungsattribut gibt, gilt: $T(\gamma_{L}(R)) \leq V(R,L)$
# Falls mehrere es mehrere gibt muss multipliziert werden: $T(\gamma_{L}(R)) \leq \prod_{i} V(R, L_{i})$. Man kann auch die Formel $T(\gamma_{L}(R)) = min[T(R)/10, \prod_{i} V(R, A_{i})]$ nutzen.
# 

# ## Histogramme
# 
# Für genauere Berechnung werden Histogramme verwendet. Nun ist nicht mehr nur die Kardinalität bekannt, sondern auch die Verteilung der Werte. 
# 
# ### Ablauf der Anfragebearbeitung 
# 
# Im Ablauf befinden sich die Histogramme im Bereich der Kostenschätzung. 
# 
# <img src="pictures/Ablauf-Anfragebearbeitung_6.png" alt="Ablauf-Anfragebearbeitung_6" width="500" style="background-color: white;"/>

# ### Schätzung der Statistiken
# 
# Statistiken sind notwendig, um die Größe von Zwischenergebnissen zu berechnen, insbesondere T(R) und V(R,A). Statistiken werden auf Befehl des Administrators eingeholt. Zum Beispiel wird T(R) mittels Scan von R. V(R,A) kann mittels einer der vorigen Algorithmen ermittelt werden. Das ist ähnlich wie bei der Gruppierung auch separat für jedes Attribut. B(R) wird gezählt, falls R nicht clustered gespeichert ist. Falls es geclustered ist, dann wird $(T(R) / Tupel pro Block)$ berechnet.

# ### Schätzung der Statistiken - Histogramme
# 
# Histogramme stellen speichereffizient Werteverteilungen dar. Die Idee ist es, Gruppen von Werten (zusammenhängende Wertebereiche) in Buckets zusammenzufassen. Varianten von Buckets wären Equal-width und Equal-height. In den Buckets geht Genauigkeit verloren, weswegen man zusätzlich Häufigkeiten für die häufigsten Werte speichern kann. 
# Pro Bucket wird die durchschnittliche Anzahl der Tupel pro Einzel-Wert gespeichert. D.h. man nimmt innerhalb des Buckets eine Gleichverteilung an.
# **Vorteile** sind geringere Schätzfehler, da Verteilungsannahmen nur in kleineren Bereichen getroffen werden. Außerdem ist der Speicherverbrauch durch das Zusammenfassen in Gruppen geringer.
# Bei **Design und Wartung** bleiben ein paar Fragen offen: 
# - Wie werden Bucketgrenzen bestimmt?
# - Was wird pro Bucket gespeichert?
# - Wie werden Histogramme aktuell gehalten?

# ### Verteilungen - Körpergewicht
# 
# <img src="pictures/Verteilungen-Körpergewicht.png" alt="Verteilungen-Körpergewicht" width="500" style="background-color: white;"/>
# 
# In der Grafik sind Verteilungen zum Körpergewicht dargestellt. Die **Normalverteilung** hat einen Wertebereich von 120-40=80. Ihr Mittelwert beträgt 80 und die Standardabweichung (stddev) ist 12. Es betrifft 100.000 Personen. 
# Bei der **Gleichverteilung** wird angenommen, dass jede Gewichtsklasse mit der gleichen Häufigkeit auftaucht. Somit sind es 100.000/80=1250 Personen für jede Gewichtsklasse. Die Gleichverteilung ist somit in fast jedem Bereich fehleranfällig.
# Die einzigen genauen Punkte sind die Schnittpunkte der beiden Verteilungen. An den anderen Stellen kommt es zu groben Fehlschätzungen. 

# ### Equi-Width Histogramme
# 
# <img src="pictures/Equi-Width-Histogramme.png" alt="Equi-Width-Histogramme" width="500" style="background-color: white;"/>
# 
# Etwas besser ist es, eine feste Anzahl an Buckets mit jeweils gleicher Breite zu erstellen. Der Vorteil ist, dass die Grenzen nicht mitgespeichert werden müssen. Der Startpunkt und die Breite genügen. Es wird eine Gleichverteilung in jedem Bucket angenommen. Ein Histogramm kann mittels eines Scans von R berechnet werden. Quellen für Schätzfehler sind zu wenige Buckets und, wenn sich die Werteverteilung innerhalb der Buckets stark unterscheidet. 

# ### Equi-Height-Histogramme
# 
# <img src="pictures/Equi-Height-Histogramme.png" alt="Equi-Height-Histogramme" width="500" style="background-color: white;"/>
# 
# Eine andere Variation ist das Equi-Height Histogramm. Auch bekannt als Equi-depth-Histogramme bzw. Perzentile. Nun probiert man, dass innerhalb eines Buckets sehr ähnliche Werte gespeichert werden. Es gibt eine feste Anzahl an Buckets. Zum Beispiel 10 Stück für 10%, 20%, usw. Die Bucketgrenzen werden so gewählt, dass jedes Bucket ungefähr die gleiche Anzahl an Tupeln enthält. Hier sind es 10.000 Personen pro Bucket. Die Bucketgrenzen müssen gespeichert werden. Die Berechnung der Histogramme erfolgt durch Sortierung und gleichgroße Sprünge.

# ### Histogramme zur Schätzung für Joins
# 
# | Wertebereich Temperator °F | Januar | Juli |
# |-|-|-|
# |0-9|40|0|
# |10-19|60|0|
# |20-29|80|0|
# |30-39|50|0|
# |40-49|10|5|
# |50-59|5|20|
# |60-69|0|50|
# |70-79|0|100|
# |80-89|0|60|
# |90-99|0|10|
# 
# ```
# SELECT Januar.Tag, Juli.Tag
# FROM Januar, Juli
# WHERE Januar.temp = Juli.temp
# ```
# 
# Die Schätzung pro Wertebereich erfolgt mit $Histo1 · Histo2 / Breite$. Besonders interessant sind die Wertebereiche von 40-49 und 50-59, da sowohl im Januar, als auch im Juli ein jeweils ein Wert steht: $10·5/10 + 5·20/10 = 5 + 10 = 15$. Insgesamt sind es also 15 gemessene Werte. </br>
# Gibt es kein Histogramm, dann muss eine herkömmliche Schätzung gemacht werden. Man wüsste, dass es 245 Tupel  mit gleichverteilten Temperaturen pro Relation gibt. Die Berechnung für den Join ist dann 245·245/100 = 600 Tupel. 
# </br>
# 
# Eine neue **Variante** ist es, die Histogramme jeweils die 3 häufigsten Werte auflisten und den Rest gruppieren zu lassen. Besonders ist es für z.B. Zipf-verteilte Daten geeignet.
# 
# **Beispiel** 
# 
# Die Anfrage ist $R(A,B) \Join S(B,C)$.</br>
# Das Histogramm für R.B ist
# - 1: 200;
# - 0:150;
# - 5: 100;
# - Rest: 550.
# 
# Das Histogramm für S.B ist
# 0: 100;
# - 1: 80;
# - 2: 70;
# - Rest: 250.
# 
# Insgesamt gibt es in R 14 und in S 13 unterschiedlich Werte: V(R,B) = 14 und V(S,B) = 13. Die Resttupel in R (550 Tupel) haben somit 11 verschiedene Werte bei einer Annahme von je 50 Tupeln. Die Resttupel in S (250 Tupel) haben 10 verschiedene Werte bei einer Annahme von je 25 Tupeln. </br>
# Man kann eine genaue Schätzung für die Werte 0 und 1 von B machen: $150·100 + 200·80=31000$. Der Wert „2“ kommt geschätzt 50 mal in R und 70 mal in S vor: $50 · 70 = 3500$. Insgesamt also 3500 Tupel. Der Wert „5“ kommt geschätzt 25 mal in S und 100 mal in R vor: $100 · 25 = 2500$. Für 9 weitere gemeinsame Werte in R und S ergibt sich dann: $9 · (50 · 25) = 11250$.

# ### Erhebung von Statistiken
# 
# Die Statistiken können nicht dauernd aktuell gehalten werden. Sie werden nur periodisch erhoben werden. Statistiken ändern sich nicht laufend und auch nicht radikal. Auch falsche Statistiken funktionieren, wenn sie konsistent angewendet werden.
# Statistiken sollen selbst nicht zu einem hot-spot werden. Sie sollen nicht dauernd geändert werden, da sie oft gelesen werden. 
# Die Erhebung wird durch unterschiedliche Trigger ausgelöst. Sie kann regelmäßig bzw. periodisch ausgeführt werden oder nach einer festen Menge an Updates ausgelöst werden. Möglich wäre auch eine Erhebung, falls Schätzungen während der Anfrageausführung als zu ungenau erkannt werden. Außerdem kann sie auch durch einen Administrator ausgelöst werden. </br>
# Die Berechnung der Statistiken ist sehr aufwändig. Ein Grund, warum sie nicht andauernd aktuell gehalten werden. Eine Lösung, um den Aufwand zu reduzieren ist es, Sampling zu nutzen. Man nimmt eine Teilmenge der Daten und erhebt darauf Statistiken. Sampling wird hier aber nicht weiter vertieft. 

# ## Joinreihenfolge

# ### Enumeration Physischer Anfragepläne
# 
# Die erste Idee wäre es, eine **vollständige Enumeration** entlang aller Freiheitsgrade durchzuführen. Die Reihenfolge und die Gruppierung von assoziativen und kommutativen Operatoren kann abgeändert werden. Außerdem lässt sich der Algorithmus für jeden Operator und der Modus des Datentransports zwischen den Operatoren frei wählen.
# Zu jedem Anfrageplan wird ein Kostenplan berechnet und daraus der Plan mit den geringsten Kosten ausgewählt. Durch das Ausführen einer vollständigen Enumeration enstehen zu viele Anfragepläne. Beispielsweise werden Abschnitte in den Plänen mehrfach berechnet. Die Anzahl der Pläne muss reduziert werden. Daher werden diverse bessere Methoden wie die Heuristische Auswahl, Branch-and-Bound, Hill-Climbing und Dynamische Programmierung/Selinger-Style Optimization verwendet. 

# ### Heuristische Auswahl
# 
# Bei der Heuristischen Auswahl soll eine Sequenz bekannter Heuristiken angewendet werden, wie zum Beispiel ein Greedy-Verfahren für die Joinreihenfolge:
# 1. Wähle zuerst das Joinpaar mit dem kleinstem Zwischenergebnis.
# 2. Joine die Relation hinzu, die wiederum das kleinste Zwischenergebnis erzeugt.
# 3. usw.
# 
# Weitere Heuristiken wären unter Anderem:
# - Falls eine Selektion und ein Index auf ein Selektionsattribut gegeben sind, sollte man den Index-Scan wählen.
# - Führe mehrere Selektionen auf der selben Relation zugleich aus.
# - Falls der Index auf dem Joinattribut ist, soll ein Index-Join gewählt werden. 
# - Falls ein Joininput sortiert ist, soll man den Sort-Merge-Join wählen, sofern kein Index vorhanden ist.

# ### Branch and Bound
# 
# Eine weitere Idee ist Branch and Bound. Heuristiken werden zum Finden eines ersten guten Plans verwendet. Die Kosten des ersten guten Plans bilden sowohl eine obere Schranke für alle anderen Pläne, als auch für die Teilpläne. Für diverse Teile der Anfrage werden Pläne enumeriert. Es wird versucht einen Teil der Anfrage zu verbessern. Teilpläne, die mehr als die Schranke kosten, werden verworfen. Wenn ein besserer Gesamtplan gefunden wird, wird die Schranke gesenkt. Der Vorteil von Branch and Bound ist, dass die Optimierung jederzeit abgebrochen werden kann. 

# ### Hill-Climbing
# 
# <img src="pictures/Hill-Climbing.png" alt="Hill-Climbing" width="200" style="background-color: white;"/>
# 
# Hill Climbing beschreibt wie man einen ersten guten Plan mittels Heuristiken findet.
# Dazu werden schrittweise ähnliche Pläne mit niedrigeren Kosten gesucht. Unter ähnlich versteht man hier, dass sich ein anderer Plan nur um eine Änderung unterscheidet. Sobald kein ähnlicher Plan mehr besser ist, ist das Verfahren fertig. 
# Der Nachteil von Hill-Climbing ist, dass es sich um ein Lokales Optimum handelt. Global hätte es eventuell noch einen besseren Plan gegeben. Ein globales Optimum zu finden benötigt zu viel Zeit. </br>
# Es gibt verschiedene Varianten, um das Verfahren zu verbessern. Zum Einem das Iterative Improvement bei dem mit 10 verschiedenen Startplänen losgelegt wird. Zum Anderen das Simulated Annealing bei dem auch Verschlechterungen zugelassen werden. 

# ### Dynamische Programmierung & Selinger-style Optimierung
# 
# Ein Verfahren zur Berechnung ist die Dynamische Programmierung.
# Es wird jeweils der beste Teilplan gesucht und verwendet, um einen höheren Teilplan zu bauen. Der Baum wird von unten nach oben (bottom-up) durchlaufen. </br>
# Selinger hat die Dynamische Programmierung erweitert und abgeändert (Selinger-Style). Es wird nicht nur der beste Plan, sondern auch verschiedene, interessante Sortiervarianten (interesting order) gemerkt. Die Kosten einiger Pläne dürfen höher sein, sofern sie andere Vorteile mit sich bringen. Das Verfahren beeinflusst nicht die Kardinalitäten von Zwischenergebnissen, sondern die I/O-Kosten.

# ### Richard Bellman
# 
# <img src="pictures/Richard-Bellman.png" alt="Richard-Bellman" width="300" style="background-color: white;"/>
# 
# Ein kurzer Exkurs zur Historie der Dynamischen Programmierung und dessen Erfinder. Richard Bellman (1920 - 1984) erhielt seinen PhD in Princeton. Er arbeitete unter Anderem von 1944 bis 1946 in Los Alamos.
# Während Bellman bei der Rand Corporation arbeitete, erfand er 1953 die Dynamische Programmierung. 
# Zur Mathematik hat er viele Beiträge zugesteuert wie z.B. den Bellman-Ford Algorithmus:
# Ein Algorithmus zum Berechnen aller kürzesten Wege für einen Startknoten.

# ### DP für Knapsack Problem
# 
# <img src="pictures/Knapsach-Zweihander.png" alt="Knapsach-Zweihander" width="150" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-SaintsChime.png" alt="Knapsack-SaintsChime" width="150" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-DragonriderBow.png" alt="Knapsack-DragonriderBow" width="150" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-Rapier.png" alt="Knapsack-Rapier" width="150" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-DragonCrestShield.png" alt="Knapsack-DragonCrestShield" width="150" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-ShortBow.png" alt="Knapsack-ShortBow" width="150" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-General.png" alt="Knapsack-General" width="400" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-Ausrüstung.png" alt="Knapsack-Ausrüstung" width="400" style="background-color: white;"/>
# 
# <img src="pictures/Knapsack-Rüstung.png" alt="Knapsack-Rüstung" width="300" style="background-color: white;"/>
# 
# https://darksouls3.wiki.fextralife.com/PvP+Builds
# 
# 
# Bei dem Knapsack Problem ist ein Rucksack mit begrenzten Gewicht gegeben. In den Rucksack möchte man möglichst gute Items ablegen. Die Items haben ein Gewicht und einen Nutzen. Das Gewicht des Rucksacks soll nicht überschritten werden.
# 
# Ein Beispiel zur Problemformulierung:
# > I can carry 15 KG at most.</br>
# > How can I maximize my damage (dps)?
# 

# ### Beispiel: Knapsack mit DP
# 
# <img src="pictures/Knapsack-mit-DP.png" alt="Knapsack-mit-DP" width="500" style="background-color: white;"/>
# 
# Die Lösung des Problems wird durch einen Rückwärtslauf ermittelt. Durch eine Tabelle werden nach und nach Items ausgewählt. Die Kapazität wird fortlaufend notiert und berechnet. Das Resultat ist der maximale Nutzen. 

# ### DP: Traveling Salesman Problem
# 
# <img src="pictures/DP-Traveling-Salesman-Problem.png" alt="DP-Traveling-Salesman-Problem" width="500" style="background-color: white;"/>
# 
# Ein ähnliches Verfahren wird beim Traveling Salesman Problem verwendet. Beim Traveling Salesman Problem sollen alle Städte besucht werden, ohne einen Pfad mehrmals zu betreten. Gesucht ist der kürzeste Pfad, der es ermöglicht. 

# ### Dynamic Programming (Held–Karp Algorithmus)
# 
# <img src="pictures/Dynamic-Programming.png" alt="Dynamic-Programming" width="200" style="background-color: white;"/>
# 
# Zunächst wird a als Anfangs- und Endpunkt betrachtet. Für alle anderen Knoten i wird der Pfad mit den Minimalkosten von a nach i, welcher alle anderen Knoten enthält, gesucht. Sei $cost(i)$ definiert als Kosten des Pfades. $cost(i) + dist(i, a)$ entspricht dann der Rundreise mit $dist(i, a)$ als Distanz von i nach a. Das Ergebnis ist das Minimum der $[cost(i) + dist(i, a)]$ Pfade.</br>
# Mittels DP wird cost(i) berechnet:
# Sei $C(S, i)$ die Minimalkosten für ein Pfad von a nach i, der jeden Knoten in S genau
# einmal besucht. Gestartet wird mit allen Teilmengen S der Größe 2. Für diese werden $C(S, i)$ berechnet. Im nächsten Schritt werden Stufenweise die Teilmengen der Größe 3, 4 u.s.w. betrachtet. 
# 
# 1. Für $|S| = 2$ gilt: $S ={a, i}$ und $C(S, i) = dist(a, i)$.
# 2. Für $|S| > 2$ gilt:  $C(S, i) = min{ C(S-\{i\}, j) + dist(j, i)}$, wenn $j \neq i$ und $j \neq a$.
# 
# - $C(\{a,b\},b) = 3$
# - $C(\{a,c\} ,c) = 4$
# - $C(\{a,d\} ,d) = 2$
# - $C(\{a,e\} ,e) = 7$
# - $C(\{a,b,c\},c) = min\{C(\{a,b\},b)+dist(b,c)\}=3+4=7$
# - $C(\{a,b,d\},d) = min\{C(\{a,b\},b)+dist(b,d)\}=3+6=9$
# - $C(\{a,b,e\},e) = min\{C(\{a,b\},e)+dist(b,e)\}=3+3=6$
# - $C(\{a,b,c\},b) = min\{C(\{a,c\},c)+dist(c,b)\}=4+4=8$
# - $C(\{a,b,d\},b) = min\{C(\{a,d\},d)+dist(d,b)\}=2+6=8$
# - $...$
# - $C(\{a,b,c,d\},c) = min\{C(\{a,b,d\},d)+dist(d,c), C(\{a,b,d\},b)+dist(b,c)\}=min\{9+5,8+4\}=12$
# - $...$
# 
# 
# Die Komplexität ist mit $O(n^{2}2^{n})$ immernoch sehr hoch, aber vieles muss nicht mehr doppelt berechnet werden. Das Verfahren ist zwar besser als Backtracking aber noch zu schwer.
# 

# ### Dynamische Programmierung
# 
# Die Dynamische Programmierung ist ein Optimaler Algorithmus. Schwierigkeiten dabei sind die Annahmen. Zum Einem muss das Prinzip der Optimalität gelten. Ein optimaler Teilplan führt immer zu einem optimalen Gesamtplan. Zum Anderen muss das Problem geschickt in Teilprobleme aufgeteilt werden. Der Aufwand kann zwar immernoch exponentiell sein, aber es können sich Operationen und Verdopplungen gespart werden.
# Klassische Anwendungen für die Dynamische Programmierung sind das Knapsack Problem, das Traveling Salesman Problem, die Maschinenbelegung und das Transportproblem.

# ### Anwendung für Left-Deep Bäume
# 
# ### Anfrageplanung
# 
# <img src="pictures/Anfrageplanung.png" alt="Anfrageplanung" width="500" style="background-color: white;"/>
# 
# Bei der heuristischen Einschränkung des Suchraums gibt es bei den Anfragen keine Kreuzprodukte. Diese werden aussortiert. Das gilt nicht bei expliziten Kreuzprodukten in der Anfrage. Die Selektionsbedingungen sollen so früh wie möglich eingesetzt werden. 
# Betrachtet werden nur links-tiefe (left-deep) Bäume. Es wird nie die parallele Ausführung von Joins betrachtet. Es wird immer davon ausgegangen, dass ein Join nach dem Andern ausgeführt wird. 

# ### Anfragebearbeitung – Optimierung
# 
# Bei der Optimierung wird nur die Joinreihenfolge und nicht die Parallelität betrachtet. Bei mehr-Prozessor Systemen wiederrum wird nicht nur die Reihenfolge, sondern auch die Parallelisierung berücksichtigt. Bei verteilten System kommen noch die Speicherorte der Zwischenergebnisse hinzu. Der Join ist i.d.R. der teuerste Operator. 
# Die Optimierung konzentriert sich auf die beste Reihenfolge. Ziel sind möglichst geringe Zwischenkosten. 
# Weitere Optimierungsschritte, wie das Schieben der Selektionen nach unten, werden später angewandt. 
# Bei n Relationen gibt es $n!$ Alternativen, aber meistens enthalten die Alternativen ein kartesisches Produkt.

# ### Dynamische Programmierung: Optimierung im System-R
# 
# <img src="pictures/Selinger.png" alt="Selinger" width="200" style="background-color: white;"/>
# 
# Das Verfahren von Selinger ist auch bekannt unter dem Namen: “Selinger-style query optimization”. Selinger ist eine Pionierin im Bereich von Datenbanksystemen. Ein klassischer Artikel zur Anfrageoptimierung ist \[SAC+79\]. Ursprünglich wurde das Verfahren bei IBM im System-R eingesetzt und ist heutzutage weit verbreitet.
# </br></br>
# Die Grundidee der Optimierung ist es, nur “Left-deep” Anfragebäume zu verwenden. D.h. nur die Joinreihenfolge ist von Bedeutung. Die innere und die äußere Relation bleibt unberücksichtigt.
# Anfragepläne werden durch dynamische Programmierung (DP) von unten nach oben (bottom-up) generiert. 
# Zusätzlich sind auch interesting orders (interessante Sortierungen) und interesting sites (interessante Ausführungsorte) wichtig, werden aber in anderen Veranstaltungen behandelt. 

# <img src="pictures/AccessPathSelection-IBM.png" alt="AccessPathSelection-IBM" width="500" style="background-color: white;"/>
# 
# Das Paper der IBM Research Division zu "Access Path Selection in a Relational Database Management System." 

# ### Bottom-up Anfrageplangenerierung
# 
# ■ Annahme 1:
# Nach dem Join über k Relationen ist die Wahl der Join-Methode die k+1te Relation hinzuzujoinen unabhängig
# von den vorigen Join-Methoden.
# □ Joinmethoden: Nested Loops, Hashjoin, Sort-Merge Join usw.
# ■ Annahme 2:
# Jeder Teilplan eines optimalen Plans ist ebenfalls optimal.
# □ Entspricht dem Prinzip der Optimalität
# □ Anders: Wenn sich zwei Pläne nur in einem Teilplan unterscheiden, so ist der Plan mit dem besseren Teilplan
# auch der bessere Gesamtplan
# ■ Bottom-up Anfrageplangenerierung:
# □ Berechne die optimalen Pläne für den Join über (jede Kombination von) k Relationen
# o Suboptimale Pläne werden verworfen
# o Erweitere diese Pläne zu optimalen Plänen für k+1 Relationen.
# o usw. bis k = n

# ### Dynamische Programmierung
# 
# <img src="pictures/Dynamische-Programmierung.png" alt="Dynamische-Programmierung" width="500" style="background-color: white;"/>

# ### DP – Grundidee für Anfrageoptimierung
# 
# <img src="pictures/Dynamische-Programmierung_2.png" alt="Dynamische-Programmierung_2" width="400" style="background-color: white;"/>
# 
# ■ Für jede Kombination merke (in einer Hilfstabelle):
# □ Geschätzte Größe des Ergebnisses (Kardinalität)
# □ Geschätzte minimale Kosten
# – Hier zur Vereinfachung: Größe des Zwischenergebnisses
# □ Joinreihenfolge, die diese Kosten verursacht (= optimaler Teilplan)
# ■ Induktion über Anzahl der Relationen im Plan
# □ $N=1$: Für jede Relation
# – Kardinalität = Kardinalität der Relation
# – Kosten = 0 (zur Vereinfachung)
# – Joinreihenfolge: n/a
# □ $N=2$: Für jedes Relationenpaar R, S
# – Kardinalität = $|R| \times |S| \times sf$
# – Kosten = 0
# – Joinreihenfolge: kleinere Relation links
# – Clou: R und S jeweils mit besten access-path
# □ $N=3$: Für jedes Tripel R, S, T
# – Clou: Nur bestes Relationenpaar aus dem Tripel wird um dritte Relation ergänzt

# ### DP – Beispiel
# 
# <img src="pictures/DP-Beispiel.png" alt="DP-Beispiel" width="200" style="background-color: white;"/>
# 
# ■ Anfrage über Relationen R, S, T, U.
# ■ Vier Join-Bedingungen

# <img src="pictures/DP-Beispiel_2.png" alt="DP-Beispiel_2" width="500" style="background-color: white;"/>

# <img src="pictures/DP-Beispiel_3.png" alt="DP-Beispiel_3" width="500" style="background-color: white;"/>

# <img src="pictures/DP-Beispiel_4.png" alt="DP-Beispiel_4" width="500" style="background-color: white;"/>

# ### DP - interesting orders (Interessante Sortierung)
# 
# ■ WdH.: Prinzip der Optimalität: Wenn sich zwei Pläne nur in einem Teilplan unterscheiden, so ist der Plan mit dem besseren Teilplan
# auch der bessere Gesamtplan.
# ■ Gegenbeispiel?
# □ $R(A,B) \Join S(A,C) \Join T(A,D)$
# □ Bester (lokaler) Plan für R ⋈ S: Hash-Join
# □ Best (globaler) Gesamtplan:
# – 1. Sort-merge Join über R und S
# – 2. Sort-merge Join mit T
# ■ Warum könnte dies so sein?
# □ Das Zwischenergebnis von R ⋈sort-mergeS ist nach Join-Attribut A sortiert.
# □ Dies ist eine interesting order, die später ausgenutzt werden kann:
# – Spätere sort-merge Joins
# – Gruppierung (`GROUP BY`)
# – Sortierung (`ORDER BY`)
# – Eindeutige Tupel (`DISTINCT`)
# 
# 
# 
# ■ Bei Auswahl des besten Teilplans:
# □ Kostenvergleich genügt nicht.
# – Es gibt keine vollständige Ordnung der Teilpläne nach Kosten.
# □ Auch Sortierungen müssen berücksichtigt werden.
# ■ Lösung: Für jede Kombination von Relationen, speichere mehrere Sortiervarianten:
# □ Nach jeder Variante der beteiligten Teilpläne
# □ Die “leere” Sortierung
# □ DP Tabellen werden „breiter“.
# ■ Kostenmodell muss verfeinert werden
# □ Echte I/O Kosten, statt Größe des Zwischenergebnisses
# ■ Merke außerdem Join- und Sortieroperationen, die diese Sortierung erzeugen.
# □ Also der Plan

# ### DP – Algorithmus
# 
# <img src="pictures/DP-Algorithmus.png" alt="DP-Algorithmus" width="500" style="background-color: white;"/>
# 
# Quelle: http://dx.doi.org/10.1145/371578.371598

# ## Physische Anfragepläne
# 
# ### Letzte Schritte
# 
# ■ Wahl des jeweiligen Algorithmus
# □ Wenn nicht schon zuvor (z.B. bei DP) geschehen
# □ Hier nur beispielhaft: Selektion und Join
# ■ Pipelining vs. Blocking
# ■ Zugriffsmethoden für Relationen
# 
# ■ Pipelining vs. Blocking
# 
# ■ Zugriffsmethoden für Relationen

# ### Wahl der Selektionsmethode
# 
# Wahl der Selektionsmethode
# ■ Schon kennengelernt
# □ Variante 1: Ganz R lesen und Selektionsbedingung auf jedes Tupel anwenden
# □ Variante 2: Falls Index auf Selektionsattribut vorhanden: Zugriff über Index
# – Voraussetzung: Index und Gleichheitsbedingung
# ■ Jetzt: Verallgemeinerung auf mehrere Selektionen auf verschiedenen Attributen
# □ Mit oder ohne Index
# □ Gleichheit oder Ungleichheit ($<$, $>$, $\leq$, $\geq$, $\neq$)
# 
# 
# ■ Annahme: Mindestens eine Selektionsbedingung kann einen Index verwenden.
# ■ Vorgehen mit Indizes (jeweils viele Alternativen):
# □ Verwende Indizes um Schnittmenge der Pointermengen zu ermitteln
# □ Lese diese Tupel ein (Index-scan)
# □ Wende darauf „Filter“-Operator an: Prüft alle übrigen Bedingungen
# ■ Vorgehen ohne Indizes
# □ Table-scan für ganz R
# □ Wende Filter-Operator für alle Bedingungen an
# ■ Filter-Operator findet nur im Hauptspeicher statt: Keine Kosten
# ■ Jetzt: Kostenvergleich der Alternativen

# ### Kostenvergleich der Selektionsmethoden
# 
# ■ Bisher: Kostenschätzung durch Schätzung der Ergebnisgröße
# □ Kardinalität des Zwischenergebnisses
# ■ Jetzt: Nur Implementierungsvarianten mit jeweils gleichem Ergebnis
# □ Deshalb wieder: Disk I/O
# □ Annahme: Indizes kosten nichts (da sehr kleine Datenmengen)
# ■ Beispiel: $sA=10$, $B<20(R)$
# □ Variante 1: Tablescan
# – $B(R)$ falls R clustered
# – $T(R)$ falls R nicht clustered
# □ Variante 2: Index auf A verwenden
# – $B(R)/V(R,A)$ falls Index clustering
# – $T(R)/V(R,A)$ falls Index nicht clustering
# □ Variante 3: Index auf B verwenden
# – $B(R)/3$ falls Index clustering
# – $T(R)/3$ falls Index nicht clustering
# □ Variante 4 …

# ### Kostenvergleich der Selektionsmethoden – Beispiel
# 
# ■ $sX=1$, $Y=2$, $Z<5(R)$
# □ $T(R) = 5.000$, $B(R) = 200$, $V(R,X)=100$, $V(R,Y)=500$
# □ R sei clustered
# □ Indizes auf X und Y nicht clustering
# □ Index auf Z clustering (B-Baum)
# ■ Variante 1: Table-scan und Filter
# □ Kosten: $B(R) = 200 I/O$
# ■ Variante 2: Index-scan mit X-Index; Filter für den Rest
# □ Kosten: $T(R)/V(R,X) = 5.000/100 = 50 I/O$
# ■ Variante 3: Index-scan mit Y-Index; Filter für den Rest
# □ Kosten: $T(R)/V(R,Y) = 5.000/500 = 10 I/O$
# ■ Variante 4: Index-scan mit (clustering) Z-Index; Filter für den Rest
# □ Kosten: $B(R)/3= 200/3 = 67 I/O$

# ### Wahl der Join-Methode
# 
# ■ Kosten je nach Joinmethode (siehe voriger Foliensatz)
# □ Annahme: Man kennt M (verfügbarer Hauptspeicher)
# – Und M ändert sich nicht während der Ausführung
# □ Annahme: Man kennt B(R), T(R), V(R, …)
# ■ Ideen falls Annahmen nicht stimmen
# □ One-pass oder Nested-loop Algorithmus als default
# – Prinzip „Hoffnung“
# □ Wähle Sort-merge-join falls mindestens ein Input bereits nach Joinattribut sortiert ist.
# □ Wähle Sort-merge-join bei mehr als einem Join auf gleichem Attribut
# – $(R(A,B) \Join S(B,C)) \Join T(B,D)$
# □ $R(A,B) \Join S(B,C)$: Falls R klein und Index auf S.B: Wähle Index-Join
# □ Falls weder Sortierung noch Indizes vorhanden sind: Wähle Hash-Join
# – Kosten hängen nur von kleinerem Input ab, nicht von beiden Inputs
# ■ Analoge Überlegungen für Mengenoperationen

# ### Pipelining vs. Blocking
# 
# ■ Naiv: Blocking (auch „Materialisierend“)
# □ Jeder Operator speichert sein Zwischenergebnis auf Disk
# ■ Besser: Vermischung der Ausführung verschiedener Operatoren
# □ Pipelining
# □ Kette von Iteratoren
# ■ Vorteile von Pipelining
# □ Weniger I/O
# □ Frühe Ergebnisse bei der Anwendung
# ■ Nachteile des Pipelining?
# □ Nicht jeder Operator funktioniert
# □ Anzahl CPUs zu gering
# □ Jeder Operator hat weniger Hauptspeicher
# □ => Ungünstigere Algorithmen müssen gewählt werden
# ■ Pipelining also nicht immer besser!
