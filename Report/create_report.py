from pathlib import Path
import csv
from datetime import date

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE = Path.cwd()
REPORT = BASE / "Report"
GRAPHS = BASE / "Outputs" / "Graphs"
RESULTS = BASE / "Outputs" / "Results"
SCRIPTS = BASE / "R_Scripts"

REPORT.mkdir(parents=True, exist_ok=True)

OUTPUT = REPORT / "Week_1_Data_Analysis_Internship_Report.docx"

doc = Document()

# Page layout
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Default font
styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(10.5)
styles["Normal"].paragraph_format.space_after = Pt(6)

for style_name in ["Title", "Heading 1", "Heading 2"]:
    styles[style_name].font.name = "Calibri"

styles["Heading 1"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 1"].font.size = Pt(17)
styles["Heading 2"].font.color.rgb = RGBColor(46, 116, 181)
styles["Heading 2"].font.size = Pt(13)

# Header
for section in doc.sections:
    header = section.header.paragraphs[0]
    header.text = "VIRTUAL R DATA ANALYST INTERNSHIP  |  WEEK 1"
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in header.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(100, 100, 100)

# Footer with page number
for section in doc.sections:
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Data Analysis Internship Report  |  Page ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)

def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def set_cell_text(cell, text, bold=False, color=None, size=9):
    cell.text = str(text)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = bold
            run.font.size = Pt(size)
            if color:
                run.font.color.rgb = RGBColor(*color)

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    for i, heading in enumerate(headers):
        set_cell_text(
            table.rows[0].cells[i],
            heading,
            bold=True,
            color=(255, 255, 255)
        )
        shade_cell(table.rows[0].cells[i], "1F4E79")

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], value)

    doc.add_paragraph()
    return table

def heading(text, level=1):
    doc.add_heading(text, level=level)

def paragraph(text, bold_start=None):
    p = doc.add_paragraph()
    if bold_start and text.startswith(bold_start):
        p.add_run(bold_start).bold = True
        p.add_run(text[len(bold_start):])
    else:
        p.add_run(text)
    return p

def bullet(text):
    doc.add_paragraph(text, style="List Bullet")

def add_image(filename, caption, width=6.0):
    path = GRAPHS / filename
    if path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Inches(width))
        cap = doc.add_paragraph(caption)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in cap.runs:
            run.italic = True
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(90, 90, 90)
    else:
        paragraph("Graph not found: " + filename)

def read_csv_rows(filename):
    path = RESULTS / filename
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f))

def add_csv_table(filename, title, max_rows=15):
    rows = read_csv_rows(filename)
    if not rows:
        paragraph("Result file unavailable: " + filename)
        return
    heading(title, 2)
    add_table(rows[0], rows[1:max_rows + 1])

def add_code_appendix(filename, title):
    path = SCRIPTS / filename
    doc.add_page_break()
    heading(title, 1)

    if not path.exists():
        paragraph("Source file not found: " + filename)
        return

    code = path.read_text(encoding="utf-8-sig")
    for line in code.splitlines():
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(7.5)
        run.font.color.rgb = RGBColor(40, 40, 40)

# ============================================================
# COVER PAGE
# ============================================================

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("VIRTUAL R DATA ANALYST INTERNSHIP")
r.bold = True
r.font.size = Pt(17)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("WEEK 1 PROJECT REPORT")
r.bold = True
r.font.size = Pt(25)
r.font.color.rgb = RGBColor(31, 78, 121)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("DATA CLEANING AND PRELIMINARY ANALYSIS")
r.bold = True
r.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Titanic Passenger Dataset")
r.font.size = Pt(15)
r.font.color.rgb = RGBColor(46, 116, 181)

for _ in range(2):
    doc.add_paragraph()

add_table(
    ["Report Information", "Details"],
    [
        ["Intern Name", "Sahil S. Jadhao"],
        ["Internship", "Virtual R Data Analyst Internship"],
        ["Internship Duration", "07 July 2026 – 04 August 2026"],
        ["Project", "Week 1 – Data Cleaning and Preliminary Analysis"],
        ["Programming Language", "R"],
        ["Development Environment", "Visual Studio Code"],
        ["Dataset", "Titanic Passenger Dataset"],
        ["Report Date", date.today().strftime("%d %B %Y")]
    ]
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Submitted as part of the Week 1 internship assignment")
r.italic = True
r.font.size = Pt(10)

doc.add_page_break()

# ============================================================
# ABSTRACT AND CONTENTS
# ============================================================

heading("ABSTRACT")
paragraph(
    "This report presents the data cleaning and preliminary exploratory "
    "analysis of the Titanic passenger dataset using the R programming "
    "language. The dataset contains 891 passenger records and 12 original "
    "variables. The work includes data inspection, duplicate checking, "
    "missing-value treatment, outlier detection, normalization, categorical "
    "encoding, descriptive statistics, visualization and correlation analysis."
)
paragraph(
    "The cleaning process retained all 891 passenger records. Missing Age "
    "and Embarked values were treated, while the Cabin variable was removed "
    "because of its high proportion of missing observations. Fare outliers "
    "were identified and flagged rather than deleted. The final cleaned "
    "dataset contains 891 records and 14 columns."
)

heading("TABLE OF CONTENTS")
contents = [
    "1. Introduction",
    "2. Objectives",
    "3. Dataset Description",
    "4. Tools and Technologies",
    "5. Data Importing and Initial Inspection",
    "6. Data Cleaning and Preprocessing",
    "7. Outlier Detection",
    "8. Data Normalization and Categorical Encoding",
    "9. Exploratory Data Analysis",
    "10. Correlation Analysis",
    "11. Key Findings",
    "12. Conclusion",
    "13. Project Output Files",
    "14. Appendix – R Source Code"
]
for item in contents:
    bullet(item)

# ============================================================
# INTRODUCTION
# ============================================================

heading("1. INTRODUCTION")
paragraph(
    "Data analysis is the process of inspecting, cleaning, transforming and "
    "interpreting data to discover useful information. Data cleaning is an "
    "important stage because incomplete, duplicated or inconsistent data can "
    "affect analytical results."
)
paragraph(
    "This project uses the Titanic passenger dataset to demonstrate a "
    "practical data analysis workflow in R. The analysis focuses on passenger "
    "survival, passenger class, gender, age and fare."
)

heading("2. OBJECTIVES")
for item in [
    "Import and understand a real-world dataset using R.",
    "Identify missing values and duplicate records.",
    "Apply appropriate missing-value treatment.",
    "Detect potential outliers using the IQR method.",
    "Normalize selected numerical variables.",
    "Encode categorical variables for analysis.",
    "Perform exploratory data analysis and descriptive statistics.",
    "Study relationships between selected numerical variables.",
    "Create graphs and export cleaned data and analytical results."
]:
    bullet(item)

# ============================================================
# DATASET
# ============================================================

heading("3. DATASET DESCRIPTION")
paragraph(
    "The Titanic dataset contains information about passengers aboard the "
    "RMS Titanic. It includes demographic details, ticket and fare information, "
    "family relationships, passenger class, embarkation port and survival status."
)

add_table(
    ["Dataset Property", "Value"],
    [
        ["Dataset", "Titanic passenger training dataset"],
        ["Original observations", "891"],
        ["Original variables", "12"],
        ["Final observations", "891"],
        ["Final variables", "14"],
        ["Target variable", "Survived"],
        ["Numerical variables", "Age, Fare, SibSp, Parch, etc."],
        ["Categorical variables", "Sex, Pclass, Embarked"],
        ["Data format", "CSV"]
    ]
)

heading("3.1 Description of Important Variables", 2)
add_table(
    ["Variable", "Description"],
    [
        ["PassengerId", "Unique passenger identification number."],
        ["Survived", "Survival indicator: 0 = No, 1 = Yes."],
        ["Pclass", "Passenger ticket class: 1, 2 or 3."],
        ["Name", "Passenger name."],
        ["Sex", "Passenger gender recorded in the dataset."],
        ["Age", "Passenger age in years."],
        ["SibSp", "Number of siblings or spouses aboard."],
        ["Parch", "Number of parents or children aboard."],
        ["Ticket", "Ticket identification information."],
        ["Fare", "Passenger fare."],
        ["Cabin", "Cabin identification information."],
        ["Embarked", "Port of embarkation."]
    ]
)

# ============================================================
# TOOLS AND INITIAL INSPECTION
# ============================================================

heading("4. TOOLS AND TECHNOLOGIES")
add_table(
    ["Tool / Package", "Purpose"],
    [
        ["R 4.6.2", "Statistical programming and analysis."],
        ["Visual Studio Code", "Code editing and execution."],
        ["dplyr", "Data manipulation."],
        ["ggplot2", "Data visualization."],
        ["tidyr", "Data transformation support."],
        ["readr", "CSV data import and export."],
        ["corrplot", "Correlation matrix visualization."]
    ]
)

heading("5. DATA IMPORTING AND INITIAL INSPECTION")
paragraph(
    "The Titanic CSV file was imported into R using read_csv() from the "
    "readr package. Initial inspection was performed using dimension, "
    "structure, preview, missing-value counts and summary statistics."
)
paragraph("The original dataset contained 891 rows and 12 columns.")

add_table(
    ["Variable", "Missing Values", "Percentage"],
    [
        ["Age", "177", "19.87%"],
        ["Cabin", "687", "77.10%"],
        ["Embarked", "2", "0.22%"],
        ["All other variables", "0", "0%"]
    ]
)

add_image(
    "missing_values.png",
    "Figure 1: Missing values in the original Titanic dataset."
)

# ============================================================
# CLEANING
# ============================================================

heading("6. DATA CLEANING AND PREPROCESSING")
heading("6.1 Duplicate Checking", 2)
paragraph(
    "The duplicated rows and duplicated PassengerId values were checked. "
    "The analysis detected zero duplicate rows and zero duplicate passenger IDs."
)

heading("6.2 Missing-Value Treatment", 2)
add_table(
    ["Variable", "Original Missing Values", "Treatment", "Final Status"],
    [
        ["Age", "177", "Median imputation by Pclass and Sex; overall median fallback if needed.", "0 missing"],
        ["Embarked", "2", "Mode imputation.", "0 missing"],
        ["Cabin", "687", "Removed due to high missingness.", "Column removed"]
    ]
)
paragraph(
    "Age values were imputed using the median age of passengers belonging "
    "to the same passenger class and sex group. Embarked missing values "
    "were replaced using the mode. Cabin was excluded from the cleaned "
    "dataset because approximately 77.10% of its observations were missing."
)

heading("6.3 Missing-Value Comparison", 2)
add_csv_table(
    "missing_value_comparison.csv",
    "Missing-value comparison output"
)

heading("7. OUTLIER DETECTION")
paragraph(
    "Potential outliers in the Fare variable were identified using the "
    "Interquartile Range (IQR) method. The lower and upper thresholds were "
    "calculated using Q1 - 1.5 × IQR and Q3 + 1.5 × IQR."
)
add_table(
    ["Outlier Measure", "Actual Result"],
    [
        ["Lower threshold", "-26.724"],
        ["Upper threshold", "65.6344"],
        ["Detected Fare outliers", "116"],
        ["Records retained", "891"]
    ]
)
paragraph(
    "The detected outliers were flagged in a new Fare_Outlier column. "
    "They were not deleted because unusually high fares may represent "
    "valid passenger observations."
)
add_image(
    "fare_boxplot.png",
    "Figure 2: Boxplot used for Fare outlier detection."
)

heading("8. DATA NORMALIZATION AND CATEGORICAL ENCODING")
heading("8.1 Min-Max Normalization", 2)
paragraph(
    "Min-Max normalization was applied to Age and Fare. This transformation "
    "scales numerical values to a range from 0 to 1. The resulting variables "
    "were stored as Age_Normalized and Fare_Normalized."
)
paragraph(
    "The original Age and Fare columns were retained so that the normalized "
    "values could be compared with the original measurements."
)

heading("8.2 Categorical Encoding", 2)
paragraph(
    "Sex, Pclass and Embarked were converted into categorical factors. "
    "A one-hot encoded matrix was generated using model.matrix() and exported "
    "as titanic_encoded.csv."
)

# ============================================================
# EDA
# ============================================================

heading("9. EXPLORATORY DATA ANALYSIS")
paragraph(
    "Exploratory Data Analysis (EDA) was performed to understand passenger "
    "survival patterns and the distributions of important variables."
)

heading("9.1 Overall Survival Distribution", 2)
add_table(
    ["Survival Status", "Passengers", "Percentage"],
    [
        ["Did not survive", "549", "61.6%"],
        ["Survived", "342", "38.4%"]
    ]
)
paragraph(
    "Out of 891 passengers, 342 survived and 549 did not survive. "
    "The overall survival percentage was approximately 38.4%."
)
add_image(
    "survival_distribution.png",
    "Figure 3: Overall passenger survival distribution."
)

heading("9.2 Survival by Gender", 2)
add_table(
    ["Gender", "Total Passengers", "Survivors", "Survival Rate"],
    [
        ["Female", "314", "233", "74.2%"],
        ["Male", "577", "109", "18.9%"]
    ]
)
paragraph(
    "The observed survival rate was higher among female passengers (74.2%) "
    "than male passengers (18.9%) in this dataset."
)
add_image(
    "survival_by_gender.png",
    "Figure 4: Passenger survival counts by gender."
)

heading("9.3 Survival by Passenger Class", 2)
add_table(
    ["Passenger Class", "Total", "Survivors", "Survival Rate"],
    [
        ["First class", "216", "136", "63.0%"],
        ["Second class", "184", "87", "47.3%"],
        ["Third class", "491", "119", "24.2%"]
    ]
)
paragraph(
    "The first-class group had the highest observed survival rate at 63.0%, "
    "followed by second class at 47.3% and third class at 24.2%."
)
add_image(
    "survival_by_class.png",
    "Figure 5: Passenger survival counts by passenger class."
)

heading("9.4 Age Distribution", 2)
add_table(
    ["Age Statistic", "Value"],
    [
        ["Mean age", "29.11 years"],
        ["Median age", "26 years"],
        ["Minimum age", "0.42 years"],
        ["Maximum age", "80 years"],
        ["Standard deviation", "13.3 years"]
    ]
)
paragraph(
    "After missing-value treatment, the mean passenger age was approximately "
    "29.11 years and the median was 26 years."
)
add_image(
    "age_distribution.png",
    "Figure 6: Distribution of passenger ages after cleaning."
)

heading("9.5 Fare Distribution", 2)
add_table(
    ["Fare Statistic", "Value"],
    [
        ["Mean fare", "32.20"],
        ["Median fare", "14.45"],
        ["Minimum fare", "0"],
        ["Maximum fare", "512.33"],
        ["Standard deviation", "49.7"]
    ]
)
paragraph(
    "The mean fare was higher than the median fare. The distribution includes "
    "some high-value fares, which is consistent with the outlier detection results."
)
add_image(
    "fare_distribution.png",
    "Figure 7: Distribution of passenger fares."
)

# ============================================================
# CORRELATION
# ============================================================

heading("10. CORRELATION ANALYSIS")
paragraph(
    "Pearson correlation analysis was performed on selected numerical "
    "variables: Survived, Pclass, Age, SibSp, Parch and Fare. PassengerId "
    "was excluded because it is an identifier rather than a meaningful "
    "measurement for this analysis."
)

add_table(
    ["Variable Pair", "Correlation", "Interpretation"],
    [
        ["Survived – Pclass", "-0.338", "Moderate negative relationship."],
        ["Survived – Fare", "+0.257", "Weak positive relationship."],
        ["Survived – Age", "-0.060", "Very weak negative relationship."],
        ["SibSp – Parch", "+0.415", "Moderate positive relationship."],
        ["Pclass – Fare", "-0.549", "Moderate negative relationship."]
    ]
)

paragraph(
    "Pclass is numerically coded from 1 (first class) to 3 (third class). "
    "Therefore, its negative correlation with survival indicates that higher "
    "class-number values were associated with lower survival in this dataset. "
    "Correlation indicates association and does not prove causation."
)
add_image(
    "correlation_heatmap.png",
    "Figure 8: Pearson correlation heatmap of selected numerical variables."
)

heading("11. KEY FINDINGS")
for item in [
    "The original dataset contained 891 passenger records and 12 variables.",
    "No duplicate rows or duplicate passenger IDs were detected.",
    "177 missing Age values and 2 missing Embarked values were treated.",
    "The Cabin variable was removed due to 687 missing values.",
    "A total of 116 Fare observations were flagged as potential outliers.",
    "All 891 records were retained in the cleaned dataset.",
    "The cleaned dataset contains 14 columns and has no remaining missing values.",
    "The overall survival rate was approximately 38.4%.",
    "Female passengers had a higher observed survival rate than male passengers.",
    "First-class passengers had the highest observed survival rate among the three classes.",
    "Age and Fare were normalized, and categorical variables were encoded.",
    "The correlation analysis showed a negative association between Pclass and survival."
]:
    bullet(item)

# ============================================================
# CONCLUSION
# ============================================================

heading("12. CONCLUSION")
paragraph(
    "The Week 1 data cleaning and preliminary analysis task was completed "
    "successfully using R. The Titanic dataset was imported, inspected, "
    "cleaned and transformed. Missing values were handled using suitable "
    "statistical methods, duplicates were checked, and potential Fare "
    "outliers were detected and flagged."
)
paragraph(
    "Min-Max normalization and categorical encoding were performed. "
    "Exploratory analysis revealed differences in survival rates across "
    "gender and passenger class. Descriptive statistics and correlation "
    "analysis provided additional understanding of the dataset."
)
paragraph(
    "The project generated cleaned data, encoded data, analytical CSV files "
    "and visualizations. These outputs provide a foundation for further "
    "statistical analysis and predictive modelling. The findings describe "
    "associations in the dataset and should not be interpreted as proof of "
    "causal relationships."
)

heading("13. PROJECT OUTPUT FILES")
add_table(
    ["Folder", "Generated Files"],
    [
        ["Dataset", "titanic_train.csv"],
        ["R_Scripts", "week1_analysis.R, week1_cleaning.R, week1_eda.R"],
        ["Outputs/Results", "titanic_cleaned.csv, titanic_encoded.csv, fare_outliers.csv, missing_value_comparison.csv, survival_summary.csv, gender_survival.csv, class_survival.csv, age_summary.csv, fare_summary.csv, correlation_matrix.csv"],
        ["Outputs/Graphs", "8 PNG visualizations"],
        ["Report", "This Word report"]
    ]
)

# ============================================================
# APPENDIX: COMPLETE SOURCE CODE
# ============================================================

add_code_appendix(
    "week1_analysis.R",
    "APPENDIX A – INITIAL DATA ANALYSIS SOURCE CODE"
)

add_code_appendix(
    "week1_cleaning.R",
    "APPENDIX B – DATA CLEANING SOURCE CODE"
)

add_code_appendix(
    "week1_eda.R",
    "APPENDIX C – EXPLORATORY DATA ANALYSIS SOURCE CODE"
)

# Final save
doc.save(OUTPUT)

print("\n========================================")
print("WORD REPORT CREATED SUCCESSFULLY")
print("========================================")
print(f"Report: {OUTPUT}")
print(f"File size: {OUTPUT.stat().st_size:,} bytes")
print("Graphs embedded:", sum(1 for p in GRAPHS.glob("*.png")))
print("R scripts included:", sum(1 for p in SCRIPTS.glob("*.R")))
print("========================================")