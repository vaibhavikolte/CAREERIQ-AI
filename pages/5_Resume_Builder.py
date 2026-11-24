import streamlit as st
import os
import re
import json
import io
import time

from google import genai

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)

from xml.sax.saxutils import escape


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Resume Builder | CAREERIQ AI",
    page_icon="C",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "resume_ai_content": None,
    "resume_generated_data": None,
    "resume_project_count": 2,
    "rb_source_loaded": False,
    "rb_source_mode": "Create New Resume",
    "rb_prefill_signature": None
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DOMAIN OPTIONS
# =========================================================

DOMAIN_OPTIONS = [
    "All Relevant Domains",
    "Data Analytics & Business Intelligence",
    "Data Science & AI / Machine Learning",
    "Cloud Computing & DevOps",
    "Full Stack & Software Development",
    "Networking & Cybersecurity",
    "Quality Assurance & Testing",
    "UI/UX Design",
    "Digital Marketing",
    "Finance & Accounting",
    "Human Resources",
    "Business & Project Management",
    "Other Technical & Non-Technical Roles"
]


# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #FFF9F3 0%,
        #FFF1E7 55%,
        #FFF8EF 100%
    );
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.builder-title {
    color: #493124;
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -1px;
    margin-bottom: 2px;
}

.builder-subtitle {
    color: #927767;
    font-size: 15px;
    margin-bottom: 22px;
}

.hero-card {
    background: linear-gradient(
        115deg,
        #6D4435,
        #C87952,
        #F0B77C
    );
    padding: 28px 30px;
    border-radius: 22px;
    color: white;
    margin: 18px 0 25px 0;
    box-shadow: 0 12px 30px rgba(128, 75, 48, 0.14);
}

.hero-heading {
    font-size: 27px;
    font-weight: 850;
    margin-bottom: 7px;
}

.hero-description {
    font-size: 14px;
    color: #FFF7F0;
    line-height: 1.7;
}

.section-card {
    background: rgba(255,255,255,0.76);
    border: 1px solid #F1DED0;
    border-radius: 18px;
    padding: 20px;
    margin: 12px 0;
}

.info-card {
    background: #FFF0E5;
    border: 1px solid #F4D7C4;
    border-radius: 14px;
    padding: 15px 17px;
    color: #714B39;
    margin: 10px 0 18px 0;
}

.preview-card {
    background: #FFFFFF;
    border: 1px solid #F0DCCE;
    border-radius: 15px;
    padding: 18px;
    margin: 10px 0;
}

div.stButton > button {
    background: linear-gradient(
        100deg,
        #C87952,
        #E6A16F
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 11px 18px;
    font-weight: 750;
    transition: all .2s ease;
}

div.stButton > button:hover {
    background: linear-gradient(
        100deg,
        #A95F3D,
        #D88959
    );
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(160, 91, 58, .18);
}

div[data-testid="stDownloadButton"] button {
    background: linear-gradient(
        100deg,
        #56866C,
        #78A987
    );
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 750;
}

div[data-testid="stDownloadButton"] button:hover {
    background: #426F56;
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 10px;
    border-color: #EBD6C8;
    background: #FFFEFC;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border-radius: 10px;
    border-color: #EBD6C8;
}

h1, h2, h3 {
    color: #573C2F;
}

label {
    color: #624638 !important;
    font-weight: 600 !important;
}

hr {
    border-color: #F0DED1;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="builder-title">AI Resume Builder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="builder-subtitle">'
    'Create a professional, ATS-friendly resume with AI assistance.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero-card">
<div class="hero-heading">
Build Your Future. Present Your Potential.
</div>
<div class="hero-description">
Transform your experience, skills and projects into a
professional resume. Use your existing CAREERIQ AI resume
or start from scratch. Review and edit every detail before
generating your final PDF.
</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_text(value):

    if value is None:
        return ""

    if isinstance(value, (list, tuple)):
        return ", ".join(
            str(x) for x in value if x
        )

    if isinstance(value, dict):
        return json.dumps(
            value,
            ensure_ascii=False
        )

    return str(value).strip()


def get_resume_source():

    return clean_text(
        st.session_state.get("resume_text", "")
    )


def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return match.group(0) if match else ""


def extract_phone(text):

    match = re.search(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
        text
    )

    return match.group(0) if match else ""


def extract_link(text, platform):

    pattern = rf'https?://(?:www\.)?{platform}\.[^\s|,]+'

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(0).rstrip(".,)") if match else ""


def extract_location(text):

    match = re.search(
        r'(?:Location|Address|City)\s*[:\-]\s*([^\n|]+)',
        text,
        re.IGNORECASE
    )

    return match.group(1).strip() if match else ""


def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored = [
        "resume",
        "curriculum vitae",
        "profile",
        "professional summary",
        "contact"
    ]

    for line in lines[:8]:

        if (
            len(line) <= 55
            and not any(
                word in line.lower()
                for word in ignored
            )
            and "@" not in line
            and not re.search(r'\d{5,}', line)
        ):
            return line

    return ""


def extract_section(text, headings):

    lines = text.splitlines()

    capture = False
    collected = []

    stop_words = [
        "education",
        "experience",
        "work experience",
        "projects",
        "technical skills",
        "skills",
        "certifications",
        "achievements",
        "languages",
        "professional summary",
        "summary"
    ]

    for line in lines:

        current = line.strip()
        low = current.lower().strip(":# ")

        if any(
            low == heading.lower()
            for heading in headings
        ):
            capture = True
            continue

        if capture:

            if low in stop_words:
                break

            collected.append(current)

    return "\n".join(
        line for line in collected if line
    ).strip()


def get_tool1_data():

    raw_text = get_resume_source()

    result = st.session_state.get(
        "resume_result",
        None
    )

    if not isinstance(result, dict):
        result = {}

    def pick(*keys):

        for key in keys:

            value = result.get(key)

            if value:
                return clean_text(value)

        return ""

    name = pick(
        "name",
        "full_name",
        "candidate_name"
    )

    email = pick(
        "email",
        "email_address"
    )

    phone = pick(
        "phone",
        "mobile",
        "phone_number"
    )

    location = pick(
        "location",
        "address",
        "city"
    )

    linkedin = pick(
        "linkedin",
        "linkedin_url"
    )

    github = pick(
        "github",
        "github_url"
    )

    skills = pick(
        "skills",
        "technical_skills"
    )

    summary = pick(
        "summary",
        "professional_summary",
        "profile_summary"
    )

    if raw_text:

        name = name or extract_name(raw_text)
        email = email or extract_email(raw_text)
        phone = phone or extract_phone(raw_text)
        location = location or extract_location(raw_text)

        linkedin = linkedin or extract_link(
            raw_text,
            "linkedin"
        )

        github = github or extract_link(
            raw_text,
            "github"
        )

        skills = skills or extract_section(
            raw_text,
            [
                "Technical Skills",
                "Skills",
                "Technical Expertise"
            ]
        )

        summary = summary or extract_section(
            raw_text,
            [
                "Professional Summary",
                "Summary",
                "Profile"
            ]
        )

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin": linkedin,
        "github": github,
        "skills": skills,
        "summary": summary
    }


def set_default_if_empty(key, value):

    if value and not st.session_state.get(key):
        st.session_state[key] = value
        # =========================================================
# SOURCE SELECTION
# =========================================================

st.markdown("## Choose Your Resume Source")

tool1_resume_text = get_resume_source()
tool1_available = bool(tool1_resume_text)

source_options = [
    "Create New Resume",
    "Use Tool 1 Resume"
]

if not tool1_available:
    source_options = ["Create New Resume"]

selected_source = st.radio(
    "How would you like to build your resume?",
    source_options,
    horizontal=True,
    key="rb_source_mode"
)

if selected_source == "Use Tool 1 Resume":

    if not tool1_available:

        st.warning(
            "No resume was found in Tool 1. "
            "Please upload your resume in Resume Intelligence first."
        )

    else:

        st.markdown("""
        <div class="info-card">
            <b>Tool 1 Resume Connected</b><br>
            Your existing resume text will be used as a reference.
            You can edit the information below before generating
            your new resume.
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Load / Refresh Tool 1 Information",
            key="load_tool1_resume"
        ):

            extracted = get_tool1_data()

            for field, value in extracted.items():
                st.session_state[f"rb_{field}"] = value

            st.session_state.rb_source_loaded = True
            st.session_state.resume_ai_content = None
            st.session_state.resume_generated_data = None

            st.success(
                "Tool 1 information loaded. You can edit it below."
            )

            st.rerun()

        if not st.session_state.rb_source_loaded:

            st.caption(
                "Click Load / Refresh Tool 1 Information to pre-fill "
                "the editable fields."
            )

else:

    st.markdown("""
    <div class="info-card">
        <b>Start Fresh</b><br>
        Enter your information manually and create a completely
        new resume without using Tool 1.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 1. PERSONAL INFORMATION
# =========================================================

st.divider()
st.markdown("## 1. Personal Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Full Name *",
        key="rb_name",
        placeholder="Enter your full name"
    )

    location = st.text_input(
        "Location",
        key="rb_location",
        placeholder="City, State"
    )

    phone = st.text_input(
        "Phone Number",
        key="rb_phone",
        placeholder="+91 XXXXX XXXXX"
    )

with col2:

    email = st.text_input(
        "Email Address *",
        key="rb_email",
        placeholder="yourmail@example.com"
    )

    linkedin = st.text_input(
        "LinkedIn URL",
        key="rb_linkedin",
        placeholder="https://linkedin.com/in/..."
    )

    github = st.text_input(
        "GitHub URL",
        key="rb_github",
        placeholder="https://github.com/..."
    )


# =========================================================
# 2. CAREER DOMAIN AND ROLE
# =========================================================

st.divider()
st.markdown("## 2. Career Target")

col1, col2 = st.columns(2)

with col1:

    domain = st.selectbox(
        "Select Your Domain",
        DOMAIN_OPTIONS,
        key="rb_domain"
    )

with col2:

    target_role = st.text_input(
        "Target Job Role",
        key="rb_target_role",
        placeholder="e.g. Data Analyst, Python Developer"
    )

experience_level = st.selectbox(
    "Experience Level",
    [
        "Fresher / Entry Level",
        "Internship",
        "0–2 Years",
        "2–5 Years",
        "5+ Years"
    ],
    key="rb_experience_level"
)


# =========================================================
# 3. EXPERIENCE
# =========================================================

st.divider()
st.markdown("## 3. Experience")

col1, col2 = st.columns(2)

with col1:

    job_title = st.text_input(
        "Job Title",
        key="rb_job_title",
        placeholder="Job title / Internship role"
    )

with col2:

    company = st.text_input(
        "Company Name",
        key="rb_company",
        placeholder="Company name"
    )

duration = st.text_input(
    "Duration",
    key="rb_duration",
    placeholder="e.g. June 2025 – December 2025"
)

experience_details = st.text_area(
    "Describe Your Actual Work",
    key="rb_experience_details",
    placeholder=(
        "Mention your actual responsibilities, tasks, "
        "tools used and work completed."
    ),
    height=120
)


# =========================================================
# 4. TECHNICAL SKILLS
# =========================================================

st.divider()
st.markdown("## 4. Technical Skills")

skills = st.text_area(
    "Technical Skills (one category per line)",
    key="rb_skills",
    placeholder=(
        "Data Analytics: Data Cleaning, Data Visualization\n"
        "Microsoft Excel: Pivot Tables, VLOOKUP\n"
        "SQL: Joins, Subqueries\n"
        "Power BI: DAX, Power Query\n"
        "Python: Basic Python\n"
        "Developer Tools: GitHub"
    ),
    height=150
)

st.caption(
    "Format: Category Name: Skills. "
    "The category name will appear bold in your PDF resume."
)


# =========================================================
# 5. PROJECTS
# =========================================================

st.divider()
st.markdown("## 5. Projects")

st.caption(
    "Add your academic, personal, internship or professional projects."
)

project_count = st.session_state.resume_project_count

for i in range(project_count):

    with st.expander(
        f"Project {i + 1}",
        expanded=(i < 2)
    ):

        st.text_input(
            "Project Name",
            key=f"resume_project_{i}_name",
            placeholder="Enter project name"
        )

        st.text_input(
            "Tools / Technologies Used",
            key=f"resume_project_{i}_tools",
            placeholder="Python, SQL, Streamlit, Power BI..."
        )

        st.text_area(
            "Project Description",
            key=f"resume_project_{i}_details",
            placeholder=(
                "Explain what you built, the problem solved, "
                "features and your contribution."
            ),
            height=100
        )


add_col1, add_col2 = st.columns(2)

with add_col1:

    if st.button(
        "+ Add Another Project",
        use_container_width=True
    ):

        st.session_state.resume_project_count += 1
        st.rerun()

with add_col2:

    if st.session_state.resume_project_count > 1:

        if st.button(
            "- Remove Last Project",
            use_container_width=True
        ):

            last = st.session_state.resume_project_count - 1

            for suffix in [
                "name",
                "tools",
                "details"
            ]:

                st.session_state.pop(
                    f"resume_project_{last}_{suffix}",
                    None
                )

            st.session_state.resume_project_count -= 1
            st.rerun()


# =========================================================
# 6. EDUCATION
# =========================================================

st.divider()
st.markdown("## 6. Education")

education = []

for i in range(3):

    with st.expander(
        f"Education {i + 1}" +
        (" (Optional)" if i == 2 else ""),
        expanded=(i < 2)
    ):

        col1, col2 = st.columns(2)

        with col1:

            qualification = st.text_input(
                "Qualification",
                key=f"rb_edu_{i}_qualification",
                placeholder="B.Sc., B.Tech, HSC, SSC..."
            )

            college = st.text_input(
                "School / College / University",
                key=f"rb_edu_{i}_college",
                placeholder="Institution name"
            )

        with col2:

            year = st.text_input(
                "Passing Year",
                key=f"rb_edu_{i}_year",
                placeholder="2026"
            )

            education.append({
                "qualification": qualification,
                "college": college,
                "year": year
            })


# =========================================================
# 7. CERTIFICATIONS
# =========================================================

st.divider()
st.markdown("## 7. Certifications")

certifications_text = st.text_area(
    "Certifications (one per line)",
    key="rb_certifications",
    placeholder=(
        "Certification name - Provider\n"
        "Course / Certification - In Progress"
    ),
    height=100
)


# =========================================================
# 8. EXISTING SUMMARY
# =========================================================

st.divider()
st.markdown("## 8. Existing Summary")

manual_summary = st.text_area(
    "Existing Summary (Optional)",
    key="rb_summary",
    placeholder=(
        "Enter your existing professional summary. "
        "Gemini AI can improve the wording."
    ),
    height=100
)


# =========================================================
# COLLECT PROJECT DATA
# =========================================================

projects = []

for i in range(st.session_state.resume_project_count):

    project = {
        "name": st.session_state.get(
            f"resume_project_{i}_name",
            ""
        ).strip(),

        "tools": st.session_state.get(
            f"resume_project_{i}_tools",
            ""
        ).strip(),

        "details": st.session_state.get(
            f"resume_project_{i}_details",
            ""
        ).strip()
    }

    if any(project.values()):
        projects.append(project)


# =========================================================
# COLLECT EDUCATION DATA
# =========================================================

education = []

for i in range(3):

    item = {
        "qualification": st.session_state.get(
            f"rb_edu_{i}_qualification",
            ""
        ).strip(),

        "college": st.session_state.get(
            f"rb_edu_{i}_college",
            ""
        ).strip(),

        "year": st.session_state.get(
            f"rb_edu_{i}_year",
            ""
        ).strip()
    }

    if any(item.values()):
        education.append(item)


# =========================================================
# FINAL RESUME DATA
# =========================================================

data = {

    "name": name.strip(),
    "location": location.strip(),
    "phone": phone.strip(),
    "email": email.strip(),
    "linkedin": linkedin.strip(),
    "github": github.strip(),

    "domain": domain,
    "target_role": target_role.strip(),
    "experience_level": experience_level,

    "job_title": job_title.strip(),
    "company": company.strip(),
    "duration": duration.strip(),
    "experience_details": experience_details.strip(),

    "skills": skills.strip(),

    "projects": projects,
    "education": education,

    "certifications": [
        x.strip()
        for x in certifications_text.splitlines()
        if x.strip()
    ],

    "manual_summary": manual_summary.strip()
}


# =========================================================
# GEMINI API KEY
# =========================================================

def get_api_key():

    try:
        key = st.secrets.get(
            "GEMINI_API_KEY",
            ""
        )

    except Exception:
        key = ""

    return key or os.getenv("GEMINI_API_KEY", "")


# =========================================================
# GEMINI AI CALL
# =========================================================

def call_gemini(prompt):

    api_key = get_api_key()

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to .streamlit/secrets.toml."
        )

    client = genai.Client(
        api_key=api_key
    )

    models_to_try = [
        "gemini-3.8-flash",
        "gemini-2.5-flash",
        "gemini-3.5-flash-lite"
    ]

    last_error = None

    for model_name in models_to_try:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                if response.text:
                    return response.text.strip()

                last_error = ValueError(
                    f"{model_name} returned an empty response."
                )

            except Exception as error:

                last_error = error
                error_message = str(error).lower()

                temporary_error = any(
                    code in error_message
                    for code in [
                        "503",
                        "429",
                        "500",
                        "502",
                        "504"
                    ]
                )

                if temporary_error and attempt == 0:

                    time.sleep(3)
                    continue

                break

    raise RuntimeError(
        "Gemini AI is temporarily unavailable or no configured "
        f"model could complete the request. Last error: {last_error}"
    )


# =========================================================
# JSON EXTRACTOR
# =========================================================

def extract_json(response_text):

    cleaned = response_text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "Gemini did not return valid JSON."
        )

    return json.loads(
        cleaned[start:end + 1]
    )


# =========================================================
# AI RESUME GENERATOR
# =========================================================

def generate_resume_content(candidate_data):

    prompt = f"""
You are an expert ATS resume writer and career specialist.

Create professional resume content for the candidate below.

CANDIDATE DATA:

{json.dumps(candidate_data, indent=2, ensure_ascii=False)}

Return ONLY valid JSON in this structure:

{{
    "professional_summary": "Professional summary",

    "experience_bullets": [
        "Bullet 1",
        "Bullet 2"
    ],

    "project_bullets": [
        {{
            "project_name": "Exact project name",
            "bullets": [
                "Bullet 1",
                "Bullet 2",
                "Bullet 3"
            ]
        }}
    ]
}}

STRICT RULES:

1. Use ONLY information provided by the candidate.
2. Never invent experience, skills, tools, achievements or metrics.
3. Never invent company names, dates or qualifications.
4. Keep exact project names and project order.
5. Write clear ATS-friendly professional English.
6. Adapt the language to the selected domain and target role.
7. Make the summary suitable for the stated experience level.
8. If the candidate is a fresher, do not imply professional experience.
9. If experience details are empty, return an empty experience_bullets list.
10. Do not claim an incomplete course or certification is completed.
11. Do not add technologies that are not in candidate information.
12. If project details are limited, do not fabricate features.
13. Return valid JSON only. No Markdown fences.
"""

    raw = call_gemini(prompt)

    content = extract_json(raw)

    if not isinstance(content, dict):

        raise ValueError(
            "Invalid AI response structure."
        )

    content.setdefault(
        "professional_summary",
        ""
    )

    content.setdefault(
        "experience_bullets",
        []
    )

    content.setdefault(
        "project_bullets",
        []
    )

    project_map = {}

    for item in content.get("project_bullets", []):

        if isinstance(item, dict):

            key = clean_text(
                item.get("project_name", "")
            ).casefold()

            project_map[key] = item.get(
                "bullets",
                []
            )

    matched_projects = []

    for project in candidate_data.get("projects", []):

        project_name = project.get(
            "name",
            ""
        ).strip()

        matched_projects.append({

            "project_name": project_name,

            "bullets": project_map.get(
                project_name.casefold(),
                []
            )

        })

    content["project_bullets"] = matched_projects

    return content
    # =========================================================
# PDF GENERATOR
# =========================================================

def create_resume_pdf(data, ai_content):

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.62 * inch,
        leftMargin=0.62 * inch,
        topMargin=0.48 * inch,
        bottomMargin=0.48 * inch,
        title=f"{data.get('name', 'Resume')} - Resume",
        author=data.get("name", "")
    )

    styles = getSampleStyleSheet()

    # -----------------------------------------------------
    # NAME STYLE
    # -----------------------------------------------------

    name_style = ParagraphStyle(
        "ResumeName",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=17,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=3
    )

    # -----------------------------------------------------
    # CONTACT STYLE
    # -----------------------------------------------------

    contact_style = ParagraphStyle(
        "ResumeContact",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=7
    )

    # -----------------------------------------------------
    # SECTION HEADING STYLE
    # -----------------------------------------------------

    section_style = ParagraphStyle(
        "ResumeSection",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=10.5,
        leading=13,
        textColor=colors.black,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    # -----------------------------------------------------
    # BODY STYLE
    # -----------------------------------------------------

    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9,
        leading=11.5,
        textColor=colors.black,
        spaceAfter=2
    )

    # -----------------------------------------------------
    # BULLET STYLE
    # -----------------------------------------------------

    bullet_style = ParagraphStyle(
        "ResumeBullet",
        parent=body_style,
        leftIndent=11,
        firstLineIndent=-7,
        spaceAfter=2
    )

    # -----------------------------------------------------
    # SUBTITLE STYLE
    # -----------------------------------------------------

    subtitle_style = ParagraphStyle(
        "ResumeSubtitle",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=9,
        leading=11.5,
        textColor=colors.black,
        spaceAfter=2
    )

    story = []

    # =====================================================
    # SECTION HEADING + BLACK DIVIDER LINE
    # =====================================================

    def add_section(title):

        story.append(
            Paragraph(
                escape(str(title).upper()),
                section_style
            )
        )

        story.append(
            HRFlowable(
                width="100%",
                thickness=0.6,
                color=colors.black,
                spaceBefore=2,
                spaceAfter=4
            )
        )

    # =====================================================
    # BULLET HELPER
    # =====================================================

    def add_bullets(items):

        for item in items or []:

            item = str(item or "").strip()

            if item:

                story.append(
                    Paragraph(
                        "• " + escape(item),
                        bullet_style
                    )
                )

    # =====================================================
    # NAME
    # =====================================================

    name = str(
        data.get("name", "")
    ).strip()

    if name:

        story.append(
            Paragraph(
                escape(name.upper()),
                name_style
            )
        )

    # =====================================================
    # CONTACT DETAILS
    # =====================================================

    contact_parts = []

    if data.get("location"):

        contact_parts.append(
            escape(str(data["location"]))
        )

    if data.get("phone"):

        contact_parts.append(
            escape(str(data["phone"]))
        )

    if data.get("email"):

        email = str(data["email"]).strip()

        contact_parts.append(
            f'<link href="mailto:{escape(email)}">'
            f'{escape(email)}</link>'
        )

    if data.get("linkedin"):

        linkedin = str(data["linkedin"]).strip()

        contact_parts.append(
            f'<link href="{escape(linkedin)}">LinkedIn</link>'
        )

    if data.get("github"):

        github = str(data["github"]).strip()

        contact_parts.append(
            f'<link href="{escape(github)}">GitHub</link>'
        )

    if contact_parts:

        story.append(
            Paragraph(
                "  |  ".join(contact_parts),
                contact_style
            )
        )

    story.append(
        Spacer(1, 5)
    )

    # =====================================================
    # PROFESSIONAL SUMMARY
    # =====================================================

    professional_summary = (
        ai_content.get("professional_summary", "").strip()
        or data.get("manual_summary", "").strip()
    )

    if professional_summary:

        add_section("Professional Summary")

        story.append(
            Paragraph(
                escape(professional_summary),
                body_style
            )
        )

        story.append(
            Spacer(1, 4)
        )

    # =====================================================
    # TECHNICAL SKILLS
    # =====================================================

    if data.get("skills"):

        add_section("Technical Skills")

        for line in str(data["skills"]).splitlines():

            line = line.strip()

            if not line:
                continue

            line = line.lstrip("•- ").strip()

            line = line.replace(
                "**",
                ""
            ).replace(
                "__",
                ""
            )

            if ":" in line:

                category, details = line.split(
                    ":",
                    1
                )

                formatted = (
                    f"<b>{escape(category.strip())}:</b>"
                )

                if details.strip():

                    formatted += (
                        " " + escape(details.strip())
                    )

                story.append(
                    Paragraph(
                        "• " + formatted,
                        body_style
                    )
                )

            else:

                story.append(
                    Paragraph(
                        "• " + escape(line),
                        body_style
                    )
                )

    # =====================================================
    # EXPERIENCE
    # =====================================================

    has_experience = any([
        data.get("job_title"),
        data.get("company"),
        data.get("duration"),
        data.get("experience_details"),
        ai_content.get("experience_bullets")
    ])

    if has_experience:

        add_section("Experience")

        experience_heading = []

        if data.get("job_title"):

            experience_heading.append(
                f"<b>{escape(data['job_title'])}</b>"
            )

        if data.get("company"):

            experience_heading.append(
                escape(data["company"])
            )

        if data.get("duration"):

            experience_heading.append(
                escape(data["duration"])
            )

        if experience_heading:

            story.append(
                Paragraph(
                    " | ".join(experience_heading),
                    subtitle_style
                )
            )

        experience_bullets = ai_content.get(
            "experience_bullets",
            []
        )

        if experience_bullets:

            add_bullets(
                experience_bullets
            )

        elif data.get("experience_details"):

            add_bullets(
                data["experience_details"].splitlines()
            )

    # =====================================================
    # PROJECTS
    # =====================================================

    projects = data.get(
        "projects",
        []
    )

    if projects:

        add_section("Projects")

        ai_projects = ai_content.get(
            "project_bullets",
            []
        )

        for project in projects:

            project_name = str(
                project.get("name", "")
            ).strip()

            project_tools = str(
                project.get("tools", "")
            ).strip()

            project_details = str(
                project.get("details", "")
            ).strip()

            if not any([
                project_name,
                project_tools,
                project_details
            ]):
                continue

            # Project name

            if project_name:

                story.append(
                    Paragraph(
                        f"<b>{escape(project_name)}</b>",
                        subtitle_style
                    )
                )

            # Technologies

            if project_tools:

                story.append(
                    Paragraph(
                        "<b>Technologies:</b> "
                        + escape(project_tools),
                        subtitle_style
                    )
                )

            # Find matching AI project bullets

            ai_project = next(
                (
                    item
                    for item in ai_projects
                    if item.get(
                        "project_name",
                        ""
                    ).casefold() == project_name.casefold()
                ),
                {}
            )

            project_bullets = ai_project.get(
                "bullets",
                []
            )

            if project_bullets:

                add_bullets(
                    project_bullets
                )

            elif project_details:

                add_bullets(
                    project_details.splitlines()
                )

            story.append(
                Spacer(1, 4)
            )

    # =====================================================
    # EDUCATION
    # =====================================================

    education = data.get(
        "education",
        []
    )

    if education:

        add_section("Education")

        for item in education:

            qualification = str(
                item.get("qualification", "")
            ).strip()

            college = str(
                item.get("college", "")
            ).strip()

            year = str(
                item.get("year", "")
            ).strip()

            if not any([
                qualification,
                college,
                year
            ]):
                continue

            if qualification:

                story.append(
                    Paragraph(
                        f"<b>{escape(qualification)}</b>",
                        subtitle_style
                    )
                )

            education_details = []

            if college:
                education_details.append(
                    escape(college)
                )

            if year:
                education_details.append(
                    escape(year)
                )

            if education_details:

                story.append(
                    Paragraph(
                        " | ".join(education_details),
                        body_style
                    )
                )

            story.append(
                Spacer(1, 3)
            )

    # =====================================================
    # CERTIFICATIONS
    # =====================================================

    certifications = data.get(
        "certifications",
        []
    )

    if certifications:

        add_section("Certifications")

        add_bullets(
            certifications
        )

    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# 9. GENERATE RESUME
# =========================================================

st.divider()

st.markdown(
    "## 9. Generate Your Resume"
)

st.markdown("""
<div class="info-card">
    Review your details carefully. Gemini AI will improve your
    professional summary and project / experience descriptions
    without adding information you have not provided.
</div>
""", unsafe_allow_html=True)


if st.button(
    "Generate Resume with AI",
    use_container_width=True
):

    has_project_details = any(
        p.get("details", "").strip()
        for p in projects
    )

    if not data["name"]:

        st.error(
            "Please enter your full name."
        )

    elif not data["email"]:

        st.error(
            "Please enter your email address."
        )

    elif not any([
        data["skills"],
        data["experience_details"],
        has_project_details,
        data["manual_summary"]
    ]):

        st.error(
            "Please enter skills, project details, experience "
            "or an existing summary before generating."
        )

    else:

        with st.spinner(
            "AI is creating your professional resume..."
        ):

            try:

                ai_content = generate_resume_content(
                    data
                )

                st.session_state.resume_ai_content = ai_content

                st.session_state.resume_generated_data = data.copy()

                st.success(
                    "Your AI-generated resume content is ready!"
                )

            except Exception as error:

                st.session_state.resume_ai_content = None

                st.session_state.resume_generated_data = None

                st.error(
                    "AI generation could not be completed. "
                    "Please check your Gemini API key, model access "
                    "or temporary API availability."
                )

                st.code(
                    str(error)[:700]
                )


# =========================================================
# 10. AI RESUME PREVIEW
# =========================================================

if st.session_state.resume_ai_content:

    ai_content = st.session_state.resume_ai_content

    saved_data = st.session_state.resume_generated_data

    st.divider()

    st.markdown(
        "## 10. AI Resume Preview"
    )

    st.markdown("""
    <div class="info-card">
        <b>AI Content Generated</b><br>
        Review the generated content below before downloading.
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # SUMMARY PREVIEW
    # -----------------------------------------------------

    st.markdown(
        "### Professional Summary"
    )

    preview_summary = (
        ai_content.get("professional_summary", "").strip()
        or saved_data.get("manual_summary", "")
    )

    st.markdown(
        f'<div class="preview-card">'
        f'{escape(preview_summary)}'
        f'</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # EXPERIENCE PREVIEW
    # -----------------------------------------------------

    if (
        saved_data.get("job_title")
        or saved_data.get("company")
        or ai_content.get("experience_bullets")
    ):

        st.markdown(
            "### Experience"
        )

        if saved_data.get("job_title"):

            st.markdown(
                f"**{saved_data['job_title']}**"
            )

        if saved_data.get("company"):

            st.caption(
                saved_data["company"]
            )

        if saved_data.get("duration"):

            st.caption(
                saved_data["duration"]
            )

        if ai_content.get("experience_bullets"):

            for bullet in ai_content["experience_bullets"]:

                st.markdown(
                    f"- {bullet}"
                )

        elif saved_data.get("experience_details"):

            st.write(
                saved_data["experience_details"]
            )

    # -----------------------------------------------------
    # PROJECT PREVIEW
    # -----------------------------------------------------

    st.markdown(
        "### Projects"
    )

    for index, project in enumerate(
        saved_data.get("projects", []),
        start=1
    ):

        if not project.get("name"):
            continue

        st.markdown(
            f"**{index}. {project['name']}**"
        )

        if project.get("tools"):

            st.caption(
                f"Tools: {project['tools']}"
            )

        ai_project = next(
            (
                item
                for item in ai_content.get("project_bullets", [])
                if item.get(
                    "project_name",
                    ""
                ).casefold() == project["name"].casefold()
            ),
            {}
        )

        if ai_project.get("bullets"):

            for bullet in ai_project["bullets"]:

                st.markdown(
                    f"- {bullet}"
                )

        elif project.get("details"):

            st.write(
                project["details"]
            )

    # -----------------------------------------------------
    # EDUCATION PREVIEW
    # -----------------------------------------------------

    if saved_data.get("education"):

        st.markdown(
            "### Education"
        )

        for item in saved_data["education"]:

            details = [
                item.get("qualification", ""),
                item.get("college", ""),
                item.get("year", "")
            ]

            details = [
                x for x in details if x
            ]

            if details:

                st.markdown(
                    " | ".join(details)
                )

    # -----------------------------------------------------
    # CERTIFICATIONS PREVIEW
    # -----------------------------------------------------

    if saved_data.get("certifications"):

        st.markdown(
            "### Certifications"
        )

        for certification in saved_data["certifications"]:

            st.markdown(
                f"- {certification}"
            )

    # =====================================================
    # 11. PDF DOWNLOAD
    # =====================================================

    st.divider()

    st.markdown(
        "## 11. Download Your Resume"
    )

    try:

        pdf_file = create_resume_pdf(
            saved_data,
            ai_content
        )

        safe_name = re.sub(
            r"[^A-Za-z0-9_-]",
            "_",
            saved_data["name"]
        )

        st.success(
            "Your ATS-friendly A4 resume PDF is ready."
        )

        st.download_button(
            label="Download Resume as PDF",
            data=pdf_file,
            file_name=f"{safe_name}_Resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as error:

        st.error(
            "PDF generation failed."
        )

        st.code(
            str(error)[:500]
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#987C6C;
    padding:15px;
    font-size:13px;
">
    CAREERIQ AI · AI Resume Builder<br>
    Build. Improve. Achieve.
</div>
""", unsafe_allow_html=True)


if st.button(
    "← Back to Home",
    use_container_width=True
):

    st.switch_page("app.py")