# PyStrat
Analysing and dating of complex geological or archaeological stratigraphic sequences. 
- Indirect relations between soil- or geological layeres are deduced from known direct ones (above, under, equal to). 
- Possible contradictions are pointed out. 
- Absolute dates or periods are correlated with the stratigraphic relations. 
- If useful, suggestions for subperiods are made.

## Purpose of the Program
Die stratigrafische Methode beruht auf vier Regeln: den Gesetzen der Lagerung, der ursprünglichen Horizontalität, der ursprünglichen Kontinuität und der stratigrafischen Abfolge.
In der Archäologie ist die Anwendung des Stratigrafiegesetzes besonders von E. Harris etabliert worden. Zur Visualisierung entwickelte er die sogenannte Harris-Matrix as seen below, in der ausschließlich Beziehungen von direkt aneinander grenzenden Schichten dargestellt werden – keine indirekten.\
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

Feature 1 dates somewhere in the timespan from 100 till the present. Feature 2 dates before 100. Feature 3 dates exactly in the year 100. Feature 4 dates somewhere in the timespan between 100 and 200.

### Suggestions for Subphases
Sometimes the periods are spanning several stratigraphic layers. In this case a suggestion is made to split the period into two suphases (period 1a and 1b for instance). In doing so, all features that have more layers below than above are assigned to "a" and vice versa.\

<img src="https://user-images.githubusercontent.com/34343137/149307235-e2e98b8e-0682-4dbd-aff1-26601497aa77.png" width=40% height=40% alt="Subphases Scheme">

But you have to bear in mind, that it is just a proposal: in theory, even hundreds of layers in a period could have been deposited within hours. It is therefore strongly recommended to check with other dating methods, that the layers in the subphases significantly differ in age.

## Operating Principles in Detail
The program has three main functions: the actual analysis, a contradiction analysis and an optional synchronization of the stratigraphy with absolute data. The stratigraphic analysis is used to derive all possible relationships between one finding and every other finding, not just between directly adjacent or superimposed findings. This includes the analysis of all equal relationships: Findings that are the same also share all other stratigraphic features as well as absolute dating. In addition, the above-below relationships are analyzed. These are often very long chains of the type: “If 1 over 2 and 2 over 3 is also 1 over 3”. Analyses of contradictions in the documentation become apparent when two contradictory types of relationships to a certain other finding arise in one finding, for example “1 is above 2 and 1 is equal to 2”. Since the stratigraphy laws are axioms without exceptions, such errors must be the result of incorrect documentation or data transfer. In most cases, these only become apparent in the course of the stratigraphic analysis and are very long chains. Each step of the stratigraphic analysis is checked for inconsistencies. If an error occurs, the error chain is determined (e.g. “1 is above 2, 2 is above 3 and 3 is above 1”). This is then output as an error message and the program is aborted. The errors must then be corrected and the stratigraphic analysis must be repeated until no more contradictions are found1. The final synchronization of the stratigraphy with absolute data or phases is optional. All possible statements from the stratigraphy and the absolute data are output. The synchronization of absolute data can be represented with equal relationships, for example “Finding 1 dates to phase 3”, if “Finding 1 equals finding 2”, then finding 2 also dates to phase 3. Statements on absolute dating can be derived from above-below relationships. An example: “Feature 1 dates to phase 3”, if “Feature 1 is above feature 2”, then feature 2 either also dates to phase 3 or is younger. Dating ranges can be determined from several statements about a feature. For example, if “Finding 1 is equal to/older than phase 3” and “equal to/younger than phase 5”, then finding 1 dates from phase 3 to 5.

## Program Structure
