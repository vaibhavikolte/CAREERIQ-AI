
import random

QUESTION_BANK = {

    "Excel": [
        ("Which function counts numeric cells?", ["COUNT()", "COUNTA()", "SUM()", "LEN()"], "COUNT()", "COUNT counts numeric cells."),
        ("Which function counts non-empty cells?", ["COUNT()", "COUNTA()", "SUM()", "MAX()"], "COUNTA counts non-empty cells."),
        ("Which function adds values based on a condition?", ["SUMIF()", "COUNT()", "LEFT()", "TRIM()"], "SUMIF adds values meeting a condition."),
        ("Which function counts cells meeting criteria?", ["COUNTIF()", "SUM()", "AVERAGE()", "ROUND()"], "COUNTIF counts cells meeting criteria."),
        ("Which function removes extra spaces?", ["TRIM()", "CLEAN()", "LEFT()", "UPPER()"], "TRIM removes extra spaces."),
        ("Which function combines text?", ["CONCAT()", "COUNT()", "MAX()", "IFERROR()"], "CONCAT combines text."),
        ("Which function handles errors in formulas?", ["IFERROR()", "SUMIF()", "MATCH()", "LEN()"], "IFERROR returns an alternative when a formula errors."),
        ("Which function returns the current date?", ["TODAY()", "NOW()", "DATEVALUE()", "YEAR()"], "TODAY returns the current date."),
        ("Which function looks up a value vertically?", ["VLOOKUP()", "HLOOKUP()", "COUNTIF()", "SUM()"], "VLOOKUP searches vertically."),
        ("Which function looks up a value horizontally?", ["HLOOKUP()", "VLOOKUP()", "INDEX()", "MATCH()"], "HLOOKUP searches horizontally."),
        ("Which feature summarizes large datasets?", ["Pivot Table", "WordArt", "Page Layout", "Flash Fill"], "Pivot Tables summarize data."),
        ("Which feature displays selected records?", ["Filter", "Merge", "Wrap Text", "Freeze Panes"], "Filter displays matching records."),
        ("Which feature highlights cells based on rules?", ["Conditional Formatting", "Data Validation", "Sort", "Protect Sheet"], "Conditional Formatting applies visual rules."),
        ("Which feature restricts allowed cell entries?", ["Data Validation", "Filter", "Flash Fill", "Subtotal"], "Data Validation controls allowed inputs."),
        ("Which function returns the largest value?", ["MAX()", "MIN()", "AVERAGE()", "COUNT()"], "MAX returns the largest value."),
        ("Which function returns the smallest value?", ["MIN()", "MAX()", "SUM()", "COUNTA()"], "MIN returns the smallest value."),
        ("Which function calculates the mean?", ["AVERAGE()", "MEDIAN()", "MODE()", "COUNT()"], "AVERAGE calculates the arithmetic mean."),
        ("Which function returns a value based on a condition?", ["IF()", "SUM()", "LEFT()", "FIND()"], "IF evaluates a logical condition."),
        ("Which function extracts characters from the left?", ["LEFT()", "RIGHT()", "MID()", "LEN()"], "LEFT extracts characters from the beginning."),
        ("Which function extracts characters from the right?", ["RIGHT()", "LEFT()", "MID()", "TRIM()"], "RIGHT extracts characters from the end."),
        ("Which function returns the position of text?", ["FIND()", "SUM()", "MAX()", "ROUND()"], "FIND returns the position of text."),
        ("Which function joins text with a delimiter?", ["TEXTJOIN()", "COUNTIF()", "AVERAGE()", "VALUE()"], "TEXTJOIN combines text using a delimiter."),
        ("Which shortcut saves a workbook?", ["Ctrl+S", "Ctrl+C", "Ctrl+V", "Ctrl+P"], "Ctrl+S saves the workbook."),
        ("Which chart is suitable for trends over time?", ["Line Chart", "Pie Chart", "Doughnut Chart", "Radar Chart"], "Line charts show trends over time."),
        ("What does Remove Duplicates do?", ["Removes repeated records", "Deletes formulas", "Sorts data", "Hides rows"], "It removes duplicate records."),
        ("What is a workbook?", ["An Excel file", "A single cell", "A formula", "A chart"], "A workbook is an Excel file."),
        ("What is a worksheet?", ["A spreadsheet tab", "A complete folder", "A database server", "A chart type"], "A worksheet is a sheet inside a workbook."),
        ("Which reference stays fixed when copied?", ["Absolute reference", "Relative reference", "Mixed text", "Named range"], "Absolute references use dollar signs."),
        ("Which function returns the number of characters?", ["LEN()", "LEFT()", "COUNT()", "VALUE()"], "LEN returns text length."),
        ("Which feature fills patterns automatically?", ["Flash Fill", "Goal Seek", "Solver", "Scenario Manager"], "Flash Fill detects and completes patterns.")
    ],

    "SQL": [
        ("Which command retrieves data?", ["SELECT", "INSERT", "UPDATE", "DELETE"], "SELECT retrieves data."),
        ("Which clause filters rows?", ["WHERE", "HAVING", "GROUP BY", "ORDER BY"], "WHERE filters rows before grouping."),
        ("Which clause filters grouped results?", ["HAVING", "WHERE", "SELECT", "DISTINCT"], "HAVING filters groups."),
        ("Which clause groups rows?", ["GROUP BY", "ORDER BY", "WHERE", "JOIN"], "GROUP BY groups rows."),
        ("Which keyword removes duplicate results?", ["DISTINCT", "UNIQUE ROW", "FILTER", "REMOVE"], "DISTINCT returns unique results."),
        ("Which function counts rows?", ["COUNT()", "SUM()", "MAX()", "ROUND()"], "COUNT counts rows or non-null values."),
        ("Which function returns the average?", ["AVG()", "SUM()", "MIN()", "LEN()"], "AVG calculates the average."),
        ("Which function returns the highest value?", ["MAX()", "MIN()", "COUNT()", "AVG()"], "MAX returns the highest value."),
        ("Which JOIN returns matching rows from both tables?", ["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "FULL JOIN"], "INNER JOIN returns matching rows."),
        ("Which JOIN keeps all rows from the left table?", ["LEFT JOIN", "INNER JOIN", "CROSS JOIN", "RIGHT JOIN"], "LEFT JOIN preserves all left-table rows."),
        ("Which command inserts new records?", ["INSERT", "UPDATE", "DELETE", "SELECT"], "INSERT adds records."),
        ("Which command modifies existing records?", ["UPDATE", "INSERT", "DROP", "SELECT"], "UPDATE modifies records."),
        ("Which command removes selected rows?", ["DELETE", "CREATE", "ALTER", "SELECT"], "DELETE removes records."),
        ("Which command removes a table structure?", ["DROP", "TRUNCATE", "UPDATE", "INSERT"], "DROP removes the table itself."),
        ("Which command removes all rows but keeps the table?", ["TRUNCATE", "DROP", "ALTER", "CREATE"], "TRUNCATE removes all rows."),
        ("Which constraint uniquely identifies each row?", ["PRIMARY KEY", "FOREIGN KEY", "CHECK", "DEFAULT"], "A primary key uniquely identifies rows."),
        ("Which key references another table's key?", ["FOREIGN KEY", "PRIMARY KEY", "CANDIDATE KEY", "SUPER KEY"], "A foreign key creates a reference."),
        ("Which operator checks a range?", ["BETWEEN", "LIKE", "IN", "EXISTS"], "BETWEEN checks an inclusive range."),
        ("Which operator searches a pattern?", ["LIKE", "BETWEEN", "AND", "NOT"], "LIKE performs pattern matching."),
        ("Which wildcard represents multiple characters in LIKE?", ["%", "_", "#", "*"], "% represents zero or more characters."),
        ("Which wildcard represents one character in LIKE?", ["_", "%", "#", "*"], "_ represents one character."),
        ("Which operator checks multiple possible values?", ["IN", "BETWEEN", "LIKE", "IS NULL"], "IN checks a list of values."),
        ("Which condition checks missing values?", ["IS NULL", "= NULL", "EQUAL NULL", "EMPTY"], "IS NULL checks null values."),
        ("Which clause sorts query results?", ["ORDER BY", "GROUP BY", "HAVING", "WHERE"], "ORDER BY sorts results."),
        ("Which sorting direction is ascending?", ["ASC", "DESC", "UP", "LOW"], "ASC sorts in ascending order."),
        ("Which function replaces NULL with another value in many SQL systems?", ["COALESCE()", "COUNT()", "MAX()", "ROUND()"], "COALESCE returns the first non-null expression."),
        ("What does COUNT(*) count?", ["All rows", "Only text values", "Only unique rows", "Only null rows"], "COUNT(*) counts all rows."),
        ("Which command changes a table structure?", ["ALTER", "UPDATE", "INSERT", "SELECT"], "ALTER changes table structure."),
        ("What is a subquery?", ["A query inside another query", "A backup table", "A database user", "A column alias"], "A subquery is nested inside another query."),
        ("Which JOIN returns every combination of two tables?", ["CROSS JOIN", "INNER JOIN", "LEFT JOIN", "SELF JOIN"], "CROSS JOIN produces a Cartesian product.")
    ],

    "Power BI": [
        ("Which language is used for Power BI calculations?", ["DAX", "Python", "HTML", "CSS"], "DAX is used for calculations."),
        ("Which tool transforms data?", ["Power Query", "PowerPoint", "Word", "Notepad"], "Power Query transforms data."),
        ("What does a relationship connect?", ["Tables", "Reports", "Workspaces", "Dashboards"], "Relationships connect tables."),
        ("Which visual shows trends over time?", ["Line Chart", "Pie Chart", "Card", "Gauge"], "Line charts show trends."),
        ("What does a slicer do?", ["Filters visuals", "Deletes data", "Creates columns", "Exports reports"], "Slicers filter report visuals."),
        ("What is a measure?", ["A dynamic calculation", "A source file", "A page", "A relationship"], "Measures calculate results in filter context."),
        ("What is a calculated column?", ["A row-level calculated column", "A visual", "A report page", "A data source"], "Calculated columns compute values for rows."),
        ("Which view manages table relationships?", ["Model View", "Reading View", "Web View", "Print View"], "Model View manages relationships."),
        ("What is Power Query's formula language?", ["M", "DAX", "SQL only", "VBA"], "Power Query uses M."),
        ("Which storage mode imports data into the model?", ["Import", "DirectQuery", "Live only", "Streaming only"], "Import stores data in the model."),
        ("Which mode queries the source when visuals are used?", ["DirectQuery", "Import", "Export", "Snapshot"], "DirectQuery queries the source."),
        ("Which visual is suitable for comparing categories?", ["Bar Chart", "Card", "Gauge", "Map only"], "Bar charts compare categories."),
        ("What is a dashboard in Power BI Service?", ["A single-page canvas", "A data table", "A DAX function", "A relationship"], "A dashboard is a single-page canvas."),
        ("What does drill-through allow?", ["Navigate to detailed page context", "Delete a page", "Change data type", "Refresh a gateway"], "Drill-through opens detail pages filtered by context."),
        ("What does a tooltip display?", ["Additional information on hover", "A data source", "A relationship", "A refresh schedule"], "Tooltips show additional information."),
        ("What is a star schema?", ["Fact table linked to dimensions", "One flat table only", "A chart layout", "A DAX operator"], "A star schema has a central fact table and dimensions."),
        ("What does a fact table usually contain?", ["Events and numeric measures", "Only descriptions", "Only images", "Report titles"], "Fact tables store events and measures."),
        ("What do dimension tables usually contain?", ["Descriptive attributes", "Only calculations", "Only measures", "Visual settings"], "Dimensions describe business entities."),
        ("Which function evaluates an expression for each row of a table?", ["SUMX()", "SUM()", "COUNT()", "MAX()"], "SUMX iterates over a table."),
        ("Which function returns the sum of a column?", ["SUM()", "SUMX()", "AVERAGE()", "RELATED()"], "SUM adds a column's values."),
        ("Which function modifies filter context?", ["CALCULATE()", "COUNT()", "LEN()", "FORMAT()"], "CALCULATE evaluates an expression in modified filter context."),
        ("Which function counts rows in a table?", ["COUNTROWS()", "COUNT()", "SUM()", "RELATED()"], "COUNTROWS counts table rows."),
        ("What does refresh do?", ["Updates data from sources", "Deletes measures", "Changes theme", "Creates a relationship"], "Refresh updates imported data."),
        ("What is a PBIX file?", ["Power BI Desktop file", "Excel macro", "SQL backup", "CSV file"], "PBIX is a Power BI Desktop report file."),
        ("Which feature combines files from a folder?", ["Folder connector", "Bookmarks", "Tooltips", "Q&A only"], "The Folder connector can combine files."),
        ("What does unpivot do?", ["Turns columns into attribute-value rows", "Deletes rows", "Sorts data", "Creates a chart"], "Unpivot converts columns into rows."),
        ("What does append queries do?", ["Stacks rows from tables", "Joins columns by key", "Deletes duplicates", "Changes relationships"], "Append stacks rows."),
        ("What does merge queries do?", ["Joins tables using matching columns", "Stacks rows only", "Creates a bookmark", "Publishes a report"], "Merge joins tables using matching columns."),
        ("What is row-level security?", ["Restricts data by user", "Changes visual colors", "Compresses images", "Refreshes data"], "RLS restricts which rows users can see."),
        ("Which feature saves a report navigation state?", ["Bookmark", "Slicer", "Measure", "Gateway"], "Bookmarks capture a report view.")
    ],

    "Python": [
        ("Which keyword defines a function?", ["def", "function", "define", "fun"], "def defines a function."),
        ("Which type stores key-value pairs?", ["Dictionary", "List", "Tuple", "Set"], "Dictionaries store key-value pairs."),
        ("Which library is used for data analysis?", ["Pandas", "Turtle", "Tkinter", "Pygame"], "Pandas is widely used for data analysis."),
        ("Which symbol starts a comment?", ["#", "//", "/*", "<!--"], "# starts a Python comment."),
        ("Which function returns collection length?", ["len()", "size()", "count()", "length()"], "len returns the number of items."),
        ("Which data type is immutable?", ["Tuple", "List", "Dictionary", "Set"], "Tuples are immutable."),
        ("Which keyword handles exceptions?", ["try", "catch", "error", "check"], "try starts exception handling."),
        ("Which keyword creates a class?", ["class", "object", "defclass", "struct"], "class defines a class."),
        ("Which operator checks equality?", ["==", "=", "!=", ">"], "== compares equality."),
        ("Which operator means exponentiation?", ["**", "^", "//", "%"], "** performs exponentiation."),
        ("Which collection stores unique items?", ["Set", "List", "Tuple", "String"], "Sets store unique elements."),
        ("Which method adds an item to a list?", ["append()", "add()", "insertall()", "push()"], "append adds an item to the end."),
        ("Which method removes the last list item by default?", ["pop()", "removeall()", "delete()", "clearone()"], "pop removes and returns an item."),
        ("Which keyword starts a loop over items?", ["for", "repeat", "loop", "iterate"], "for iterates over an iterable."),
        ("Which keyword exits a loop?", ["break", "stop", "exitloop", "end"], "break exits a loop."),
        ("Which keyword skips to the next iteration?", ["continue", "skip", "passloop", "next"], "continue skips the current iteration."),
        ("Which library is commonly used for numerical arrays?", ["NumPy", "Flask", "Django", "Tkinter"], "NumPy provides numerical arrays."),
        ("Which Pandas function reads a CSV file?", ["read_csv()", "open_csv()", "load_csv()", "csv_read()"], "read_csv loads CSV data."),
        ("Which Pandas method displays the first rows?", ["head()", "top()", "first()", "show()"], "head displays the first rows."),
        ("Which Pandas method displays summary statistics?", ["describe()", "info()", "shape()", "columns()"], "describe provides descriptive statistics."),
        ("Which Pandas method checks missing values?", ["isnull()", "isblank()", "missing()", "empty()"], "isnull identifies missing values."),
        ("Which Pandas method removes missing rows?", ["dropna()", "fillna()", "remove()", "deletena()"], "dropna removes missing values."),
        ("Which Pandas method replaces missing values?", ["fillna()", "dropna()", "replaceall()", "clearna()"], "fillna fills missing values."),
        ("Which Pandas method combines DataFrames by key?", ["merge()", "appendtext()", "concatstr()", "joinfile()"], "merge combines DataFrames using keys."),
        ("Which function converts text to an integer?", ["int()", "str()", "floattext()", "number()"], "int converts a value to an integer."),
        ("Which function creates a sequence of numbers?", ["range()", "sequence()", "series()", "numbers()"], "range generates an integer sequence."),
        ("What does None represent?", ["Absence of a value", "Zero", "Empty string", "False only"], "None represents no value."),
        ("Which statement imports a module?", ["import", "include", "using", "require"], "import loads a module."),
        ("What does a lambda create?", ["Anonymous function", "Class", "Loop", "Module"], "lambda creates an anonymous function."),
        ("Which block runs whether an exception occurs or not?", ["finally", "except", "raise", "assert"], "finally runs during normal or exceptional exit.")
    ]
}


def get_fallback_questions(category, count=10):
    pool = QUESTION_BANK[category]

    history = st.session_state.mcq_history.get(category, [])

    available = [
        q for q in pool
        if q[0] not in history
    ]

    # Reset history only after all questions have been used
    if len(available) < count:
        st.session_state.mcq_history[category] = []
        available = pool.copy()

    selected = random.sample(available, count)

    questions = []

    for question, options, answer, explanation in selected:
        questions.append({
            "question": question,
            "options": options,
            "answer": answer,
            "explanation": explanation
        })

    return questions
