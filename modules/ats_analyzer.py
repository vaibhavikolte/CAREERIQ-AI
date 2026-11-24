
import re


# ----------------------------------
# ATS KEYWORD DATABASE
# ----------------------------------

ATS_KEYWORDS = [
    "Excel",
    "SQL",
    "MySQL",
    "Power BI",
    "Power Query",
    "DAX",
    "Python",
    "Pandas",
    "NumPy",
    "Tableau",
    "Data Analysis",
    "Data Analytics",
    "Data Visualization",
    "Data Modeling",
    "Statistics",
    "Machine Learning",
    "Communication",
    "Problem Solving",
    "Dashboard",
    "Reporting",
    "ETL",
    "Data Cleaning"
]


# ----------------------------------
# CHECK RESUME SECTIONS
# ----------------------------------

def check_sections(text):

    text_lower = text.lower()

    sections = {
        "Education": ["education", "academic"],
        "Skills": ["skills", "technical skills"],
        "Projects": ["projects", "project experience"],
        "Experience": ["experience", "work experience", "internship"],
        "Certifications": ["certifications", "certificates"]
    }

    results = {}

    for section, keywords in sections.items():

        results[section] = any(
            keyword in text_lower for keyword in keywords
        )

    return results


# ----------------------------------
# CHECK ATS KEYWORDS
# ----------------------------------

def check_keywords(text):

    found = []
    missing = []

    text_lower = text.lower()

    for keyword in ATS_KEYWORDS:

        pattern = r"(?<!\w)" + re.escape(keyword.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found.append(keyword)
        else:
            missing.append(keyword)

    return found, missing


# ----------------------------------
# CALCULATE RESUME SCORE
# ----------------------------------

def calculate_ats_score(text):

    score = 0

    sections = check_sections(text)

    # Contact details: 20 points
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", text):
        score += 10

    if re.search(r"(?:\+91[\s-]?)?[6-9]\d{9}", text):
        score += 10

    # Resume sections: 40 points
    section_weights = {
        "Education": 10,
        "Skills": 10,
        "Projects": 10,
        "Experience": 5,
        "Certifications": 5
    }

    for section, weight in section_weights.items():

        if sections[section]:
            score += weight

    # Relevant keywords: 20 points
    found, missing = check_keywords(text)

    keyword_score = min(len(found), 10) * 2
    score += keyword_score

    # Resume length: 20 points
    word_count = len(text.split())

    if 150 <= word_count <= 1000:
        score += 20

    elif 80 <= word_count < 150:
        score += 10

    elif 1000 < word_count <= 1500:
        score += 10

    return {
        "score": min(score, 100),
        "sections": sections,
        "found_keywords": found,
        "missing_keywords": missing,
        "word_count": word_count
    }
