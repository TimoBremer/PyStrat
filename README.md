# PyStrat
Analysing and dating of complex geological or archaeological stratigraphic sequences. 
- Indirect relations between soil- or geological layeres are deduced from known direct ones (above, under, equal to). 
- Possible contradictions are pointed out. 
- Absolute dates or periods are correlated with the stratigraphic relations. 
- If useful, suggestions for subperiods are made.

## Purpose of the Program
Die stratigrafische Methode beruht auf vier Regeln: den Gesetzen der Lagerung, der ursprünglichen Horizontalität, der ursprünglichen Kontinuität und der stratigrafischen Abfolge.
In der Archäologie ist die Anwendung des Stratigrafiegesetzes besonders von E. Harris etabliert worden. Zur Visualisierung entwickelte er die sogenannte Harris-Matrix, in der ausschließlich Beziehungen von direkt aneinander grenzenden Schichten dargestellt werden – keine indirekten (Abb. XY). 
Mit einer Harris-Matrix können kleinere stratigraphische Sequenzen übersichtlich dargestellt werden, bei größeren Komplexen entsteht allerdings ein undurchsichtiges durcheinander aus Kästchen und Linien.
Ziel der stratigrafischen Analyse ist letztlich die Datierung der Schichten. Hierfür sind die in einer Harris-Matrix nicht erfassten indirekten Beziehungen zwischen den Schichten von großer Bedeutung: Wenn beispielsweise Schicht 1 über Schicht 2 liegt und Schicht 2 über Schicht 3, liegt auch Schicht 1 indirekt auch über Schicht 3. Wenn nun Schicht 3 in das Jahr 1631 datiert, lässt sich aus der Analyse der indirekten Beziehungen ableiten, dass Schicht 1 und 2 jünger als 1631 sind. Bei vielen Schichten und mehreren Datierungen werden die Beziehungen so komplex, dass eine Analyse "von Hand", mithilfe von Harris-Matrices, nahezu unmöglich ist. In solchen Fällen ist eine digitale Auswertung erforderlich.

## Install and Start
- Install Python 3 on your machine.
- Copy all files above to a directory of your choice (except the "input_data" examples folder) .
- Run the "run_pystrat.py"-script.

## Howto
After starting the programm, three tabs for data-input appear. It is mandatory to insert data into the first table (Stratigraphical Relations), the other tables could be left blank. You can insert data directly into the tables or upload text-files by pressing the import-button. Changes could be saved to new text-files for reuse on next run.\
You can run the program by pressing "Start" in the lower part. Afterwards, one or more new tabs will appear. These show logical contradictions in the input data, if there are any. Otherwise the results and possibly suggestions for subphases are displayed. All these tables can also be saved as text-files.\
If any conflicts in the input-data were found, you can overwrite the tables directly to fix it and run the program consecutively until no more errors are found. After that, the correct tables could be saved.
### Input Stratigraphical Relations
The first table ist the most important one. It is for entering the stratigraphic relations observed in the field. The logical structure is aligned with the direction of reading: The Left feature is under/above or equal to right feature. For example feature 2 is above feature 6:
| **left** |**relation**|**right**|
--- | --- | ---
feature 2|above|feature 6

Until now, you can display the relations in English (under/above/equal) or in German (unter/ueber/gleich). When you import a text file, the rows must be comma-separated and there must be no column headers. When the feature names are text-strings, they should be set in parentheses:

    "feature 1",above,"feature 6"
    "feature 4",under,"feature 1"

Such files could be created by exporting spreadsheets from Microsoft Excel or Libre/OpenOffice Calc as csv-tables.  

### Input Absolute Data or Periods
In the second table you can assign dates or periods to the findings. The first column is for the feature. It makes sense that all the features listed here should appear in the first table of the stratigraphic relations. One option is to use absolute dates. The time before Christ can be displayed with negative numbers:
| **feature** |**date/period**|
--- | ---
feature 1|1066
feature 4|-350

Another option is the use of period names:
| **feature** |**date/period**|
--- | ---
feature 1|Holocene
feature 4|Pleistocene

If these names are words instead of numbers or alphabetical sequences, the program is not able to order the phases (Pleistocene is older than Holocene)In this case it is recommended to assign an order to the periods in the following table.\
If you import the data from a file, the formatting rules are similar to the first table: It must be a comma-separated text-file with no column headers, textstrings should be in parantheses:

    "feature 1",1066
    "feature 4",-350

### Input Periods Order
Often, there are logical inconsistencies beween the stratigraphical sequence and the dating of the features: If feature 1 is above feature 2, feature 2 could not be younger then feature 1. If the program should detect such inconsistencies it must "know" the order of the phases. The program tries to derive this order from the alphabetical order of the period names or the period numbers. Thus, period names like "Period 1, Period 2..." could be analysed automatically. But when you use period names like the above mentioned "Holocene, Pleistocene..." it is necessary to define the order in this table. You can do this by assigning numbers to the period names.The oldes periods must be assigned to the lowest numbers, the youngest to the highest ones. The steps between the periods do not matter, you can start with "10, 20, 30..." for instance, in case you have to insert any periods in between afterwards:
| **period** |**order**|
--- | ---
Holocene|130
Pleistocene|120
Pliocene|110

The formatting of an import-file must be similar to the other insert-tables:

    "Holocene",130
    "Pleistocene",120
    "Pliocene",110

### Conflicts in Stratigraphy
This table appears, if there are any conflicts in the stratigraphic sequence. Sometimes these inconsitencies are very short and easy to fix, like: feature 1 is above feature 2; feature 1 is equal to feature 2. But these "conflict-chains" could also spread over several hundred relations. The problem is, that these errors "grow" in most times during the analysing process: Feature 1 is above and also equal to feature 2. If feature 3 now is equal to feature 2 it is also above or equal to feature 1 and so on. In most times this leads to an almost endless list of contradicotory stratigraphic results, which is useless for further analysis. Therefore the errors have to be fixed carefully, to get a proper result.\
In theory the stratigraphic rules are exakt and axiomatic, so inoconsistencies do not exist in reality. They are man-made due to errors in the observation of the sequencies. Thus, the best but time consuming way is to get into the documentation again and find the mistake in the obsvervation of the geological or archaeological sequence. As a more pragmatic approach, you can delete all problematic relations in the first table of the stratigraphic relations.

### Conflicts between Stratigraphy and Absolute Dates
Despite conflicts within the stratigraphic sequence, there could be contradictions between the stratigraphy and datings, which are displayed in this table in necessary. For instance: feature 1 is above feature 2, so feature 1 is younger. There is a contradiction when feature 1 dates in the year 1100 and feature 2 in the year 1200. Absolute datings are often based on several different methods, natural sciences, finds in features etc. For this reason, the absolute dates are not that accurate and beyond doubt than relative date derived from stratigraphic sequences. It is a good idea so, to start the search for the error with the absolute dates. But it is to say, that the impact of such errors on the result is compartively low, as long as the relative dates are assigned to a correct stratigraphic sequence.

### Results Stratigraphy
The stratigraphic results are displayed, if no contradictions were found. The only relation is "above", so it is not displayed: the feature in the left column is always above the feature in the right column.
Generally the stratigraphic results are very large, because many indirect relations can be derived from the direct stratigraphic relations. For itself, the table has little informative value. Rather, it is the base to which the absolute data will be added in the next step, so it may therefore be useful to trace the resulting dating.

### Results Dating
This table is the main goal of the program, because it shows the results of combining stratigraphy and absolute dates. In doing so, chronological statements can be made about findings that do not themselves contain any clues for dating.\
Dates in the "from"-column means that the corresponding feature is younger or as old as; dates in the "till" column means younger or as old as. If there is the same value in the the "from"- and the "till"-column, the feature dates exaktly in this year or period. For instance:
| **feature** |**from**|**till**
--- |---|---
feature 1|100|
feature 2| |100
feature 3|100|100
feature 4|100|200

Feature 1 dates somewhere in the timespan from 100 till today. Feature 2 dates before 100. Feature 3 dates exactly in the year 100. Feature 4 dates somewhere in the timespan between 100 and 200.

### Suggestions for Subphases

## Operating Principles in Detail
Das Programm verfügt über drei Hauptfunktionen: der eigentlichen Analyse, einer Widerspruchsanalyse und einer optionalen Synchronisierung der Stratigrafie mit absoluten Daten.
Über die stratigrafische Analyse werden alle möglichen Beziehungen eines Befundes zu jedem anderem, nicht bloß von direkt neben- oder übereinanderliegenden Befunden, hergeleitet. Das umfasst die Analyse aller Gleich-Beziehungen: Befunde, die gleich sind, teilen auch sämtliche anderen stratigrafischen Merkmale sowie absolute Datierungen. Außerdem werden die Über-Unter-Beziehungen analysiert. Dabei handelt es sich oft um sehr lange Ketten der Art: „Wenn 1 über 2 und 2 über 3 ist auch 1 über 3“.
Analysen von Widersprüchen in der Dokumentation zeichnen sich ab, wenn sich bei einem Befund zwei einander widersprechende Arten von Beziehungen zu einem bestimmten anderen Befund ergeben, beispielsweise „1 ist über 2 und 1 ist gleich 2“. Da es sich bei den Stratigrafiegesetzen um Axiome ohne Ausnahmen handelt, müssen solche Fehler Resultat einer fehlerhaften Dokumentation oder Übertragung der Daten sein. Zumeist zeichnen sich diese erst im Verlauf der stratigrafischen Analyse ab und es handelt sich um sehr lange Ketten.
Jeder Schritt der stratigrafischen Analyse wird auf Widersprüche geprüft. Wenn ein Fehler auftritt, wird die Fehlerkette ermittelt (beispielsweise „1 ist über 2, 2 ist über 3 und 3 ist über 1“). Anschließend wird diese als Fehlermeldung ausgegeben und das Programm abgebrochen. Die Fehler müssen dann korrigiert werden und die stratigrafische Analyse muss so lange wiederholt werden, bis keine Widersprüche mehr gefunden werden1.
Die abschließende Synchronisation der Stratigrafie mit absoluten Daten oder Phasen ist optional. Dabei werden alle aus der Stratigrafie und den absoluten Daten möglichen Aussagen ausgegeben. Die Synchronisation absoluter Daten kann mit Gleich-Beziehungen dargestellt werden, beispielsweise „Befund 1 datiert in Phase 3“, wenn nun „Befund 1 gleich Befund 2“ datiert auch Befund 2 in Phase 3. Aus Über-Unter-Beziehungen lassen sich Aussagen zu absoluten Datierungen ableiten. Ein Beispiel: „Befund 1 datiert in Phase 3“, wenn „Befund 1 über Befund 2“ ist, datiert Befund 2 entweder ebenfalls in Phase 3 oder ist jünger. Datierungsspannen lassen sich aus mehreren Aussagen zu einem Befund ermitteln. Wenn beispielsweise „Befund 1 ist gleich/älter Phase 3“ und „gleich/jünger Phase 5“, dann datiert Befund 1 von Phase 3 bis 5.

## Program Structure