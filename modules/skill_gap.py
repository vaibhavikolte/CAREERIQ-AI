
LEARNING_ROADMAP = {
    "Excel": [
        "Learn formulas and functions",
        "Practice sorting, filtering and lookup functions",
        "Learn Pivot Tables and charts"
    ],
    "SQL": [
        "Learn SELECT, WHERE and ORDER BY",
        "Practice GROUP BY, HAVING and JOINS",
        "Learn subqueries and window functions"
    ],
    "Power BI": [
        "Learn Power BI Desktop",
        "Practice data cleaning in Power Query",
        "Build dashboards and reports"
    ],
    "Python": [
        "Learn Python basics and data types",
        "Practice Pandas and NumPy",
        "Perform data analysis using real datasets"
    ],
    "Power Query": [
        "Learn data transformation",
        "Practice merge and append queries",
        "Learn pivot and unpivot operations"
    ],
    "DAX": [
        "Learn calculated columns and measures",
        "Practice CALCULATE and filter functions",
        "Build KPI measures"
    ],
    "Tableau": [
        "Learn Tableau interface",
        "Practice charts and visualizations",
        "Build an interactive dashboard"
    ],
    "Statistics": [
        "Learn mean, median and mode",
        "Understand probability and distributions",
        "Practice correlation and hypothesis testing"
    ],
    "Data Visualization": [
        "Learn chart selection",
        "Understand dashboard design",
        "Practice storytelling with data"
    ],
    "Data Modeling": [
        "Understand relationships",
        "Learn star and snowflake schemas",
        "Practice building data models"
    ],
    "MySQL": [
        "Learn database fundamentals",
        "Practice SQL queries in MySQL",
        "Work with joins and aggregations"
    ],
    "Pandas": [
        "Learn Series and DataFrames",
        "Practice filtering and grouping",
        "Perform data cleaning"
    ],
    "NumPy": [
        "Learn arrays and array operations",
        "Practice mathematical functions",
        "Work with numerical datasets"
    ],
    "Machine Learning": [
        "Understand supervised and unsupervised learning",
        "Learn model training and testing",
        "Build a basic prediction model"
    ],
    "Scikit-learn": [
        "Learn preprocessing tools",
        "Practice regression and classification",
        "Evaluate model performance"
    ],
    "Data Analysis": [
        "Learn data cleaning techniques",
        "Practice exploratory data analysis",
        "Generate insights from datasets"
    ],
    "Data Analytics": [
        "Understand the data analytics lifecycle",
        "Practice data exploration",
        "Present data-driven insights"
    ],
    "Communication": [
        "Practice explaining analytical findings",
        "Improve presentation skills",
        "Communicate insights clearly"
    ]
}


def generate_skill_gap_report(missing_skills):

    roadmap = {}

    for skill in missing_skills:

        if skill in LEARNING_ROADMAP:

            roadmap[skill] = LEARNING_ROADMAP[skill]

        else:

            roadmap[skill] = [
                f"Understand the fundamentals of {skill}",
                f"Practice {skill} with hands-on exercises",
                f"Build a small project using {skill}"
            ]

    return roadmap
