
import re


# Skills database
SKILLS_DATABASE = [
    "Excel",
    "Advanced Excel",
    "SQL",
    "MySQL",
    "Power BI",
    "Power Query",
    "DAX",
    "Python",
    "Pandas",
    "NumPy",
    "Tableau",
    "Machine Learning",
    "Data Analysis",
    "Data Visualization",
    "Data Modeling",
    "Statistics",
    "Scikit-learn",
    "Communication"
]


def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    result = re.search(pattern, text)

    return result.group(0) if result else "Not Found"


def extract_phone(text):

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    result = re.search(pattern, text)

    return result.group(0) if result else "Not Found"


def extract_name(text):

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    ignored_words = [
        "resume", "curriculum vitae",
        "cv", "profile", "contact"
    ]

    for line in lines[:8]:

        if len(line) > 50:
            continue

        if any(word in line.lower() for word in ignored_words):
            continue

        if "@" in line or any(char.isdigit() for char in line):
            continue

        if re.fullmatch(r"[A-Za-z .'-]+", line):
            return line

    return "Not Found"


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS_DATABASE:

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


def extract_education(text):

    education_keywords = [
        "BSc", "B.Sc", "Bachelor of Science",
        "BCA", "BBA", "B.Com",
        "MSc", "M.Sc", "MBA", "MCA",
        "HSC", "SSC", "12th", "10th",
        "Bachelor", "Master", "Diploma"
    ]

    found_education = []

    for line in text.split("\n"):

        for keyword in education_keywords:

            if keyword.lower() in line.lower():
                clean_line = line.strip()

                if clean_line and clean_line not in found_education:
                    found_education.append(clean_line)

                break

    return found_education


def extract_profile(text):

    profile = {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "Education": extract_education(text)
    }

    return profile
