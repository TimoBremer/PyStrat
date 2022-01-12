# PyStrat
Analysing and dating of complex geological or archaeological stratigraphic sequences. Indirect relations between soil- or geological layeres are deduced from known direct ones (above, under, equal to). Possible contradictions are pointed out. Absolute dates or phases are correlated with the stratigraphic relations. If useful, suggestions for subphases are made.

## Purpose of the Program
Die stratigrafische Methode beruht auf vier Regeln: den Gesetzen der Lagerung, der ursprünglichen Horizontalität, der ursprünglichen Kontinuität und der stratigrafischen Abfolge.
In der Archäologie ist die Anwendung des Stratigrafiegesetzes besonders von E. Harris etabliert worden. Zur Visualisierung entwickelte er die sogenannte Harris-Matrix, in der ausschließlich Beziehungen zwischen Schichten dargestellt werden, die direkt aneinander grenzen (Abb. XY). 
Mit einer Harris-Matrix können kleinere stratigraphische Sequenzen übersichtlich dargestellt werden, bei größeren Komplexen entsteht allerdings ein undurchsichtiges durcheinander aus Kästchen und Linien.
Ziel der stratigrafischen Analyse ist letztlich die Datierung der Schichten. Hierfür sind die in einer Harris-Matrix nicht erfassten indirekten Beziehungen zwischen den Schichten von großer Bedeutung: Wenn beispielsweise Schicht 1 über Schicht 2 liegt und Schicht 2 über Schicht 3, liegt auch Schicht 1 indirekt auch über Schicht 3. Wenn nun Schicht 3 in das Jahr 1631 datiert, lässt sich aus der Analyse der indirekten Beziehungen ableiten, dass Schicht 1 und 2 jünger als 1631 sind. Bei vielen Schichten und mehreren Datierungen werden die Beziehungen so komplex, dass eine Analyse "von Hand", mithilfe von Harris-Matrices, nahezu unmöglich ist. In solchen Fällen kann ist eine digitale Auswertung erforderlich.

## Install and Start
- Install Python 3 on your machine.
- Copy all files above to a directory of your choice (except the "input_data" examples folder) .
- Run the "run_pystrat.py"-script.

## Howto
After starting the programm, three tabs for data-input appear. It is mandatory to insert data into the first table (Stratigraphical Relations), the other tables could be left blank. You can insert data directly into the tables or upload text-files by pressing the import-button. Changes could be saved to new text-files for reuse on next run.
You can run the program by pressing "Start" in the lower part. Afterwards, one or more new tabs will appear. These show logical contradictions in the input data, if there are any. Otherwise the results and possibly suggestions for subphases are displayed. All these tables can also be saved as text-files.
If any conflicts in the input-data were found, you can overwrite the tables directly to fix it and run the program consecutively until no more errors are found. After that, the correct tables could be saved.
### Input Stratigraphical Relations
This is the most important table, for entering the stratigraphic relations observed in the field. The logical structure is aligned with the direction of reading: The Left feature is under/above or equal to right feature. For example feature 2 is above feature 6.

| **left** |**relation**|**right**|
--- | --- | ---
feature 2|above|feature 6

Until now you can display the relations in English (under/above/equal) or in German (unter/ueber/gleich). When you import a text file, the rows must be comma-separated and there must be no line header. Feature names should be in parentheses:
    
    "feature 1",above,"feature 6"
    "feature 4",under,"feature 1"

### Input Absolute Data

### Input Periods Order

### Conflicts in Stratigraphy 

### Conflicts between Stratigraphy and Absolute Dates

### Results Stratigraphy

### Results Dating

## Operating Principles in Detail
Das Programm verfügt über drei Hauptfunktionen: der eigentlichen Analyse, einer Widerspruchsanalyse und einer optionalen Synchronisierung der Stratigrafie mit absoluten Daten.
Über die stratigrafische Analyse werden  alle möglichen Beziehungen eines Befundes zu jedem anderem, nicht bloß von direkt neben- oder übereinanderliegenden Befunden, hergeleitet. Das umfasst die Analyse aller Gleich-Beziehungen: Befunde, die gleich sind, teilen auch sämtliche anderen stratigrafischen Merkmale sowie absolute Datierungen. Außerdem werden die Über-Unter-Beziehungen analysiert. Dabei handelt es sich oft um sehr lange Ketten der Art: „Wenn 1 über 2 und 2 über 3 ist auch 1 über 3“.
Analysen von Widersprüchen in der Dokumentation zeichnen sich ab, wenn sich bei einem Befund zwei einander widersprechende Arten von Beziehungen zu einem bestimmten anderen Befund ergeben, beispielsweise „1 ist über 2 und 1 ist gleich 2“. Da es sich bei den Stratigrafiegesetzen um Axiome ohne Ausnahmen handelt, müssen solche Fehler Resultat einer fehlerhaften Dokumentation oder Übertragung der Daten sein. Zumeist zeichnen sich diese erst im Verlauf der stratigrafischen Analyse ab und es handelt sich um sehr lange Ketten.
Jeder Schritt der stratigrafischen Analyse wird auf Widersprüche geprüft. Wenn ein Fehler auftritt, wird die Fehlerkette ermittelt (beispielsweise „1 ist über 2, 2 ist über 3 und 3 ist über 1“). Anschließend wird diese als Fehlermeldung ausgegeben und das Programm abgebrochen. Die Fehler müssen dann korrigiert werden und die stratigrafische Analyse muss so lange wiederholt werden, bis keine Widersprüche mehr gefunden werden1.
Die abschließende Synchronisation der Stratigrafie mit absoluten Daten oder Phasen ist optional. Dabei werden alle aus der Stratigrafie und den absoluten Daten möglichen Aussagen ausgegeben. Die Synchronisation absoluter Daten kann mit Gleich-Beziehungen dargestellt werden, beispielsweise „Befund 1 datiert in Phase 3“, wenn nun „Befund 1 gleich Befund 2“ datiert auch Befund 2 in Phase 3. Aus Über-Unter-Beziehungen lassen sich Aussagen zu absoluten Datierungen ableiten. Ein Beispiel: „Befund 1 datiert in Phase 3“, wenn „Befund 1 über Befund 2“ ist, datiert Befund 2 entweder ebenfalls in Phase 3 oder ist jünger. Datierungsspannen lassen sich aus mehreren Aussagen zu einem Befund ermitteln. Wenn beispielsweise „Befund 1 ist gleich/älter Phase 3“ und „gleich/jünger Phase 5“, dann datiert Befund 1 von Phase 3 bis 5.

## Program Structure
