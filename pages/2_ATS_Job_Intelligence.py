import streamlit as st
import os
import re
import json
from urllib.parse import quote_plus

from modules.job_matcher import match_resume_with_job

# Optional analytics history
try:
    from modules.career_analytics_store import (
        save_analytics_event,
        get_analytics_data
    )
    ANALYTICS_AVAILABLE = True
except Exception:
    ANALYTICS_AVAILABLE = False


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ATS & Job Intelligence | CAREERIQ AI",
    page_icon="C",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

def init_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


init_state("job_match_result", None)
init_state("job_description_text", "")
init_state("job_ai_review", "")
init_state("job_ai_error", "")
init_state("job_match_history", [])
init_state("job_recommendations", [])


# =========================================================
# PREMIUM WARM CREAM + PEACH THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #fff5eb,
        #fff0e3,
        #fff8f1
    );
    color: #38291f;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #75412c !important;
}

.main-heading {
    background: linear-gradient(
        115deg,
        #713b29 0%,
        #ae5937 55%,
        #e58b4e 100%
    );
    color: white !important;
    font-size: 36px;
    font-weight: 850;
    padding: 25px 30px;
    border-radius: 20px;
    margin-bottom: 20px;
    letter-spacing: 1px;
    box-shadow: 0 9px 24px rgba(125,61,35,.20);
    border-bottom: 4px solid #f5bd8f;
}

.subtitle {
    color: #8b624d;
    font-size: 15px;
    margin-bottom: 25px;
}

.section-heading {
    background: linear-gradient(
        110deg,
        #fff0e3,
        #ffe0c5,
        #ffead8
    );
    color: #783d27 !important;
    font-size: 25px;
    font-weight: 800;
    padding: 15px 22px;
    border-radius: 15px;
    border-left: 6px solid #c66a3e;
    box-shadow: 0 5px 16px rgba(153,82,45,.10);
    margin-top: 24px;
    margin-bottom: 18px;
}

.upload-card {
    background: rgba(255,255,255,.65);
    border: 2px dashed #e8ae88;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 20px;
}

.result-card {
    background: rgba(255,255,255,.90);
    border: 1px solid #efd5c2;
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(100,55,30,.07);
    transition: .25s ease;
}

.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(100,55,30,.13);
}

.result-number {
    color: #a64f30;
    font-size: 32px;
    font-weight: 850;
}

.result-label {
    color: #806657;
    font-size: 14px;
    font-weight: 650;
}

.info-card {
    background: #fffaf5;
    border: 1px solid #efd5c2;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.skill-tag {
    display: inline-block;
    background: linear-gradient(110deg,#ffe2ce,#fff0df);
    color: #8b482e;
    border: 1px solid #edc2a3;
    padding: 7px 13px;
    border-radius: 20px;
    margin: 5px 5px 5px 0;
    font-size: 13px;
    font-weight: 650;
}

.missing-tag {
    display: inline-block;
    background: #fff0e9;
    color: #a34d38;
    border: 1px solid #e9b6a5;
    padding: 7px 13px;
    border-radius: 20px;
    margin: 5px 5px 5px 0;
    font-size: 13px;
    font-weight: 650;
}

.stButton > button {
    background: linear-gradient(110deg,#a34f31,#df8b4e);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 11px 20px;
    transition: .2s;
}

.stButton > button:hover {
    background: linear-gradient(110deg,#7f3b27,#c76c3d);
    color: white;
    transform: translateY(-2px);
}

.stTextArea textarea,
.stTextInput input {
    background: #fffaf5 !important;
    border: 1px solid #e8c4aa !important;
    border-radius: 13px !important;
    color: #493328 !important;
}

[data-testid="stFileUploader"] {
    background: #fffaf5;
    border-radius: 15px;
    border: 1px solid #efd5c2;
    padding: 12px;
}

.stProgress > div > div > div > div {
    background-color: #d87942;
}

div[data-testid="stExpander"] {
    background: #fffdfb;
    border: 1px solid #efd5c2;
    border-radius: 13px;
}

hr {
    border-color: #e6cdbb;
}

@media (max-width: 768px) {
    .main-heading {
        font-size: 25px;
        padding: 19px;
    }

    .section-heading {
        font-size: 20px;
        padding: 13px;
    }

    .result-number {
        font-size: 25px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

if st.button("← Back to Home", key="job_back_home"):
    st.switch_page("app.py")

st.markdown(
    '<div class="main-heading">ATS & JOB INTELLIGENCE</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="subtitle">
AI-powered job matching, skill gap analysis and career opportunity discovery.
</div>
""", unsafe_allow_html=True)


# =========================================================
# RESUME DATA FROM TOOL 1
# =========================================================

resume_text = st.session_state.get("resume_text", "")
resume_result = st.session_state.get("resume_result", None)

st.markdown(
    '<div class="section-heading">01 | RESUME CONNECTION</div>',
    unsafe_allow_html=True
)

if not resume_text or not str(resume_text).strip():

    st.warning(
        "Resume Data Not Found. Please complete Resume Analysis in Tool 1 first."
    )

    if st.button("Go to Resume Intelligence"):
        st.switch_page("pages/1_Resume_Intelligence.py")

    st.stop()

else:

    st.markdown("""
    <div class="info-card">
        <strong style="color:#8b482e;">Resume Successfully Connected</strong>
        <p style="color:#806657;margin-bottom:0;">
        Your previously analyzed resume from Tool 1 will be used automatically.
        No second resume upload is required.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View Connected Resume Information"):
        st.write("Resume text length:", len(resume_text), "characters")

        if isinstance(resume_result, dict):
            st.json(resume_result)
        else:
            st.write("Candidate resume data is connected.")


# =========================================================
# JOB DESCRIPTION PASTE + DOMAIN SELECTION
# =========================================================

jd_paste = st.text_area(
    "Job Description",
    height=250,
    placeholder="Paste Job Description here...",
    key="job_description_input"
)

DOMAIN_OPTIONS = [
    "All Relevant Domains",
    "Data Analytics & Business Intelligence",
    "Data Science & AI / Machine Learning",
    "Cloud Computing & DevOps",
    "Full Stack & Software Development",
    "Networking & Cybersecurity",
    "Quality Assurance & Testing"
    "UI/UX Design",
    "Digital Marketing",
    "Finance & Accounting",
    "Human Resources",
    "Business & Project Management",
    "Other Technical & Non-Technical Roles"
]

preferred_domain = st.selectbox(
    "Preferred Job Domain for Vacancy Recommendations",
    DOMAIN_OPTIONS,
    key="preferred_job_domain"
)


# =========================================================
# MULTI-DOMAIN SKILLS
# =========================================================

DOMAIN_SKILLS = {

    "Data Analytics & Business Intelligence": {
        "skills": [
            "Excel", "Advanced Excel", "SQL", "Power BI",
            "Tableau", "Power Query", "DAX",
            "Data Visualization", "Data Cleaning",
            "Data Modeling", "Statistics", "Python",
            "ETL", "Reporting"
        ],
        "roles": [
            "Junior Data Analyst",
            "Business Intelligence Analyst",
            "Power BI Developer",
            "MIS Analyst",
            "SQL Analyst"
        ]
    },

    "Data Science & AI / Machine Learning": {
        "skills": [
            "Python", "R", "Machine Learning",
            "Deep Learning", "Artificial Intelligence",
            "Pandas", "NumPy", "Scikit-learn",
            "TensorFlow", "PyTorch", "Statistics",
            "Data Science", "Natural Language Processing",
            "NLP", "Computer Vision"
        ],
        "roles": [
            "Data Science Intern",
            "Junior Data Scientist",
            "Machine Learning Intern",
            "AI/ML Intern",
            "Python ML Developer"
        ]
    },

    "Cloud Computing & DevOps": {
        "skills": [
            "AWS", "Microsoft Azure", "Azure",
            "Google Cloud", "GCP", "Cloud Computing",
            "Docker", "Kubernetes", "Linux",
            "Jenkins", "Git", "GitHub", "CI/CD",
            "DevOps", "Terraform", "Cloud Security"
        ],
        "roles": [
            "Cloud Support Associate",
            "AWS Cloud Intern",
            "Azure Cloud Intern",
            "DevOps Intern",
            "Junior Cloud Engineer"
        ]
    },

    "Full Stack & Software Development": {
        "skills": [
            "HTML", "CSS", "JavaScript", "TypeScript",
            "React", "Angular", "Node.js", "Express.js",
            "MongoDB", "MySQL", "PostgreSQL",
            "Java", "C++", "C#", "Python",
            "Django", "Flask", "REST API",
            "Full Stack", "Software Development"
        ],
        "roles": [
            "Junior Full Stack Developer",
            "Frontend Developer Intern",
            "Backend Developer Intern",
            "Python Developer",
            "Junior Software Developer"
        ]
    },

    "Networking & Cybersecurity": {
        "skills": [
            "Computer Networking", "Networking",
            "TCP/IP", "DNS", "DHCP", "Routing",
            "Switching", "CCNA", "Cisco",
            "Network Security", "Cybersecurity",
            "Ethical Hacking", "Penetration Testing",
            "Firewall", "Wireshark", "Linux",
            "SOC", "SIEM"
        ],
        "roles": [
            "Network Support Engineer",
            "Junior Network Engineer",
            "Cybersecurity Intern",
            "SOC Analyst L1",
            "IT Support Engineer"
        ]
    },

    "Quality Assurance & Testing": {
        "skills": [
            "Manual Testing", "Software Testing",
            "Automation Testing", "Selenium",
            "Java", "Python", "Postman",
            "API Testing", "JIRA", "Test Cases",
            "Quality Assurance", "QA"
        ],
        "roles": [
            "QA Tester",
            "Software Test Engineer Intern",
            "Manual Testing Intern",
            "Automation Testing Intern"
        ]
    }
}


# =========================================================
# RESUME LOCATION DETECTION
# =========================================================

INDIAN_CITIES = [
    "Pune", "Mumbai", "Navi Mumbai", "Thane",
    "Nagpur", "Nashik", "Aurangabad", "Kolhapur",
    "Bengaluru", "Bangalore", "Hyderabad",
    "Chennai", "Delhi", "New Delhi", "Noida",
    "Gurugram", "Gurgaon", "Kolkata",
    "Ahmedabad", "Surat", "Vadodara",
    "Jaipur", "Indore", "Bhopal", "Chandigarh",
    "Kochi", "Coimbatore", "Mysuru", "Mysore",
    "Visakhapatnam", "Thiruvananthapuram",
    "Lucknow", "Patna"
]


def _collect_resume_values(data):

    values = []

    if isinstance(data, dict):

        for key, value in data.items():

            if isinstance(value, (str, int, float)):
                values.append((str(key).lower(), str(value)))

            elif isinstance(value, (dict, list, tuple)):
                values.extend(_collect_resume_values(value))

    elif isinstance(data, (list, tuple)):

        for item in data:
            values.extend(_collect_resume_values(item))

    return values


def detect_resume_location(resume_text, resume_result=None):

    labelled_values = []

    for key, value in _collect_resume_values(resume_result):

        if any(term in key for term in (
            "location", "address", "city", "current place"
        )):
            labelled_values.append(value)

    text = str(resume_text or "")

    for match in re.finditer(
        r"(?im)^\s*(?:current\s+)?(?:location|address|city)\s*[:\-]\s*(.+?)\s*$",
        text
    ):
        labelled_values.insert(0, match.group(1))

    for candidate_text in labelled_values + [text]:

        for city in sorted(INDIAN_CITIES, key=len, reverse=True):

            if re.search(
                r"(?i)(?<![a-z])" + re.escape(city) + r"(?![a-z])",
                candidate_text
            ):
                return city

    return ""


# =========================================================
# DOMAIN SKILL EXTRACTION
# =========================================================

def extract_domain_skills(text):

    text = str(text or "")
    found = []
    catalogue = []

    for domain_data in DOMAIN_SKILLS.values():
        catalogue.extend(domain_data["skills"])

    for skill in catalogue:

        pattern = (
            r"(?i)(?<![a-z0-9])"
            + re.escape(skill)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text):

            if skill.lower() not in {x.lower() for x in found}:
                found.append(skill)

    return found


# =========================================================
# SKILL CATEGORIZATION
# =========================================================

def categorize_preferred_skills(job_description, skills):

    preferred = []

    sentences = re.split(r"[\n.!?;]+", job_description)

    preferred_words = [
        "preferred",
        "nice to have",
        "good to have",
        "bonus",
        "plus",
        "advantage",
        "desirable"
    ]

    for skill in skills:

        skill_lower = str(skill).lower()

        for sentence in sentences:

            sentence_lower = sentence.lower()

            if (
                skill_lower in sentence_lower
                and any(word in sentence_lower for word in preferred_words)
            ):
                preferred.append(skill)
                break

    preferred = list(dict.fromkeys(preferred))

    required = [
        skill for skill in skills
        if skill not in preferred
    ]

    return required, preferred


# =========================================================
# GEMINI AI REVIEW
# =========================================================

def get_gemini_api_key():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        try:
            api_key = st.secrets.get("GEMINI_API_KEY")

        except Exception:
            api_key = None

    return api_key


def generate_ai_job_review(
    resume_text,
    job_description,
    match_data,
    required_skills,
    preferred_skills
):

    from google import genai

    api_key = get_gemini_api_key()

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Configure your Gemini API key."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert AI career advisor and ATS job matching analyst.

Analyze the candidate resume against the job description.

CANDIDATE RESUME:
{resume_text[:12000]}

JOB DESCRIPTION:
{job_description[:10000]}

SKILL MATCH DATA:
{json.dumps(match_data, ensure_ascii=False)}

REQUIRED SKILLS:
{json.dumps(required_skills, ensure_ascii=False)}

PREFERRED SKILLS:
{json.dumps(preferred_skills, ensure_ascii=False)}

Prepare a professional report with these sections:

1. Overall Job Fit Analysis
2. Candidate Strengths
3. Missing or Weak Skills
4. Experience and Qualification Alignment
5. Resume Improvement Suggestions
6. Practical Learning Roadmap
7. Final Recommendation

Use simple professional English.
Be honest and evidence-based.
Do not invent candidate experience or qualifications.
Do not promise job selection.
Do not treat skill match percentage as hiring probability.
"""

    try:
        available_models = list(client.models.list())

    except Exception as error:
        raise RuntimeError(
            f"Unable to fetch available Gemini models: {error}"
        )

    supported_models = []

    for model in available_models:

        model_name = getattr(model, "name", "") or ""

        supported_actions = (
            getattr(model, "supported_actions", []) or []
        )

        if (
            "generateContent" in supported_actions
            and "gemini" in model_name.lower()
        ):
            supported_models.append(model_name)

    if not supported_models:
        raise RuntimeError(
            "No Gemini model supporting generateContent was found."
        )

    supported_models.sort(
        key=lambda name: (
            "flash" not in name.lower(),
            name.lower()
        )
    )

    errors = []

    for model_name in supported_models:

        try:

            response = client.models.generate_content(
                model=model_name.replace("models/", ""),
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception as error:
            errors.append(f"{model_name}: {error}")

    raise RuntimeError(
        "Gemini AI could not generate the review:\n"
        + "\n".join(errors)
    )


# =========================================================
# JOB ROLE EXTRACTION
# =========================================================

def detect_job_title(job_description):

    patterns = [
        r"(?im)^\s*job title\s*[:\-]\s*(.+)$",
        r"(?im)^\s*position\s*[:\-]\s*(.+)$",
        r"(?im)^\s*role\s*[:\-]\s*(.+)$",
        r"(?im)^\s*job role\s*[:\-]\s*(.+)$"
    ]

    for pattern in patterns:

        match = re.search(pattern, job_description)

        if match:
            return match.group(1).strip()[:100]

    text = job_description.lower()

    signals = [
        (
            "Junior Data Scientist",
            ["machine learning", "data scientist", "deep learning",
             "artificial intelligence"]
        ),
        (
            "Cloud / DevOps Engineer",
            ["aws", "azure", "cloud engineer", "devops", "kubernetes"]
        ),
        (
            "Full Stack Developer",
            ["full stack", "frontend", "backend", "software developer",
             "react", "node.js"]
        ),
        (
            "Network / Cybersecurity Role",
            ["network engineer", "networking", "cybersecurity",
             "soc analyst", "ccna"]
        ),
        (
            "Software Test Engineer",
            ["quality assurance", "manual testing",
             "automation testing", "qa tester"]
        ),
        (
            "Data Analyst",
            ["power bi", "data analyst", "business intelligence",
             "tableau", "data visualization"]
        )
    ]

    for title, keywords in signals:

        if any(word in text for word in keywords):
            return title

    return "Entry-Level IT Role"


# =========================================================
# MULTI-DOMAIN JOB SEARCH LINKS
# =========================================================

def create_job_recommendations(
    resume_text,
    matched_skills,
    preferred_domain,
    resume_result=None
):

    resume_skills = extract_domain_skills(resume_text)

    combined_skills = {
        x.lower()
        for x in resume_skills + [str(x) for x in matched_skills]
    }

    location = detect_resume_location(
        resume_text,
        resume_result
    )

    if preferred_domain == "All Relevant Domains":

        selected_domains = [
            domain
            for domain, data in DOMAIN_SKILLS.items()
            if any(
                skill.lower() in combined_skills
                for skill in data["skills"]
            )
        ]

    else:
        selected_domains = [preferred_domain]

    recommendations = []

    for domain in selected_domains:

        for role in DOMAIN_SKILLS.get(domain, {}).get("roles", [])[:4]:

            search_phrase = f"{role} fresher entry level"

            if location:
                search_phrase += f" {location}"
            else:
                search_phrase += " India"

            linkedin_url = (
                "https://www.linkedin.com/jobs/search/?keywords="
                + quote_plus(search_phrase)
                + (
                    "&location=" + quote_plus(location + ", India")
                    if location else ""
                )
            )

            naukri_url = (
                "https://www.naukri.com/"
                + quote_plus(role.lower().replace(" ", "-"))
                + "-jobs"
                + (
                    "-in-" + quote_plus(location.lower().replace(" ", "-"))
                    if location else ""
                )
            )

            recommendations.append({
                "domain": domain,
                "role": role,
                "location": location or "India (location not found in resume)",
                "linkedin": linkedin_url,
                "naukri": naukri_url
            })

    return recommendations[:12], location, selected_domains
    # =========================================================
# ANALYZE JOB MATCH
# =========================================================

st.markdown(
    '<div class="section-heading">03 | AI JOB MATCH ANALYSIS</div>',
    unsafe_allow_html=True
)

if st.button(
    "Analyze Resume Against Job Description",
    key="analyze_job_match",
    use_container_width=True
):

    job_description = jd_paste.strip()

    if not job_description:

        st.warning("Please paste a Job Description.")

    else:

        try:

            with st.spinner("Analyzing job requirements and matching skills..."):

                match_data = match_resume_with_job(
                    resume_text,
                    job_description
                )

                if not isinstance(match_data, dict):
                    raise ValueError("Job matcher returned an invalid result.")

                matcher_skills = match_data.get("required_skills", []) or []
                domain_jd_skills = extract_domain_skills(job_description)

                all_skills = list(dict.fromkeys(
                    [str(skill) for skill in matcher_skills] + domain_jd_skills
                ))

                resume_skill_names = {
                    skill.lower() for skill in extract_domain_skills(resume_text)
                }

                resume_text_lower = str(resume_text).lower()

                matched_skills = [
                    skill for skill in all_skills
                    if skill.lower() in resume_skill_names
                    or re.search(
                        r"(?i)(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])",
                        resume_text_lower
                    )
                ]

                matched_lower = {x.lower() for x in matched_skills}

                missing_skills = [
                    skill for skill in all_skills
                    if skill.lower() not in matched_lower
                ]

                score = round(
                    (len(matched_skills) / len(all_skills)) * 100, 2
                ) if all_skills else 0.0

                match_data["required_skills"] = all_skills
                match_data["matched_skills"] = matched_skills
                match_data["missing_skills"] = missing_skills
                match_data["total_required"] = len(all_skills)
                match_data["match_score"] = score

                required_skills, preferred_skills = (
                    categorize_preferred_skills(
                        job_description,
                        all_skills
                    )
                )

                ai_review = ""
                ai_error = ""

                try:

                    with st.spinner("Generating AI Job Match Review..."):

                        ai_review = generate_ai_job_review(
                            resume_text,
                            job_description,
                            match_data,
                            required_skills,
                            preferred_skills
                        )

                except Exception as error:
                    ai_error = str(error)

                recommendations, detected_location, detected_domains = (
                    create_job_recommendations(
                        resume_text,
                        matched_skills,
                        preferred_domain,
                        resume_result
                    )
                )

                st.session_state.job_match_result = {
                    "score": score,
                    "match_data": match_data,
                    "required_skills": required_skills,
                    "preferred_skills": preferred_skills,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "job_title": detect_job_title(job_description),
                    "job_description": job_description,
                    "resume_location": detected_location,
                    "recommended_domains": detected_domains
                }

                st.session_state.job_description_text = job_description
                st.session_state.job_ai_review = ai_review
                st.session_state.job_ai_error = ai_error
                st.session_state.job_recommendations = recommendations

                history_item = {
                    "job_title": detect_job_title(job_description),
                    "score": score,
                    "matched": len(matched_skills),
                    "missing": len(missing_skills)
                }

                st.session_state.job_match_history.insert(
                    0,
                    history_item
                )

                if ANALYTICS_AVAILABLE:
                    try:
                        save_analytics_event(
                            "advanced_job_match",
                            score=score,
                            details=history_item
                        )
                    except Exception:
                        pass

                st.success("Job Match Analysis Completed!")

        except Exception as error:
            st.error(f"Job Analysis Error: {error}")


# =========================================================
# RESULTS
# =========================================================

result = st.session_state.job_match_result

if result is not None:

    score = result["score"]

    st.markdown(
        '<div class="section-heading">04 | MATCH SCORE OVERVIEW</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-card">
            <strong style="color:#8b482e;">Analyzed Job Role</strong>
            <h3 style="margin-top:7px;">{result["job_title"]}</h3>
            <span style="color:#806657;">
                Resume and Job Description compatibility analysis
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">RESUME–JOB MATCH</div>
                <div class="result-number">{score:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">MATCHED SKILLS</div>
                <div class="result-number">
                    {len(result["matched_skills"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">MISSING SKILLS</div>
                <div class="result-number">
                    {len(result["missing_skills"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Job Match Progress")

    st.progress(min(max(score / 100, 0.0), 1.0))

    if score >= 80:
        st.success("Strong Skill Match")

    elif score >= 60:
        st.info("Moderate Skill Match – Some improvements needed.")

    else:
        st.warning("Low Skill Match – Focus on the missing skills.")


    # =====================================================
    # REQUIRED AND PREFERRED SKILLS
    # =====================================================

    st.markdown(
        '<div class="section-heading">05 | JOB SKILL REQUIREMENTS</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Required Skills")

        if result["required_skills"]:

            for skill in result["required_skills"]:
                st.markdown(
                    f'<span class="skill-tag">{skill}</span>',
                    unsafe_allow_html=True
                )

        else:
            st.info("No required skills were extracted.")

    with col2:

        st.markdown("### Preferred Skills")

        if result["preferred_skills"]:

            for skill in result["preferred_skills"]:
                st.markdown(
                    f'<span class="skill-tag">{skill}</span>',
                    unsafe_allow_html=True
                )

        else:
            st.info(
                "No clearly labelled preferred skills were detected."
            )


    # =====================================================
    # MATCHED SKILLS
    # =====================================================

    st.markdown(
        '<div class="section-heading">06 | MATCHED SKILLS</div>',
        unsafe_allow_html=True
    )

    if result["matched_skills"]:

        for skill in result["matched_skills"]:
            st.markdown(
                f'<span class="skill-tag">✓ {skill}</span>',
                unsafe_allow_html=True
            )

    else:
        st.warning("No matching skills found.")


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    st.markdown(
        '<div class="section-heading">07 | MISSING SKILLS</div>',
        unsafe_allow_html=True
    )

    if result["missing_skills"]:

        for skill in result["missing_skills"]:
            st.markdown(
                f'<span class="missing-tag">+ {skill}</span>',
                unsafe_allow_html=True
            )

        st.info(
            "Focus on these skills to improve your compatibility "
            "with the selected job."
        )

    else:
        st.success("All extracted job skills are matched!")


    # =====================================================
    # AI JOB MATCH REVIEW
    # =====================================================

    st.markdown(
        '<div class="section-heading">08 | AI JOB MATCH REVIEW</div>',
        unsafe_allow_html=True
    )

    if st.session_state.job_ai_review:

        st.markdown(
            st.session_state.job_ai_review
        )

    elif st.session_state.job_ai_error:

        st.warning(
            "AI review could not be generated. "
            "The skill matching analysis is still available."
        )

        with st.expander("AI Generation Details"):
            st.code(st.session_state.job_ai_error)

    else:
        st.info("AI review is not available yet.")


    # =====================================================
    # IMPROVEMENT SUGGESTIONS
    # =====================================================

    st.markdown(
        '<div class="section-heading">09 | IMPROVEMENT SUGGESTIONS</div>',
        unsafe_allow_html=True
    )

    if result["missing_skills"]:

        for index, skill in enumerate(result["missing_skills"], 1):

            st.markdown(
                f"""
                <div class="info-card">
                    <strong style="color:#a64f30;">
                        {index}. Improve {skill}
                    </strong>
                    <p style="color:#806657;margin-bottom:0;">
                        Learn and practice this skill, then add relevant
                        practical work to your resume when completed.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.success(
            "No missing skills were detected by the current skill matcher."
        )


    # =====================================================
    # JOB VACANCY RECOMMENDATIONS
    # =====================================================

    st.markdown(
        '<div class="section-heading">10 | AI JOB VACANCY RECOMMENDATIONS</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="subtitle">
    Suggested job roles based on your connected resume,
    skills and job matching analysis.
    </div>
    """, unsafe_allow_html=True)

    recommendations = st.session_state.job_recommendations

    detected_location = result.get("resume_location", "")

    if detected_location:
        st.info(f"Resume location detected: {detected_location}, India")
    else:
        st.warning(
            "A city/location was not detected in the resume. "
            "Job searches will use India-wide results."
        )

    if not recommendations:
        st.info(
            "No resume skills were detected for the selected domain. "
            "Choose a specific domain above or add relevant skills to the resume."
        )

    for index, job in enumerate(recommendations, 1):

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">RECOMMENDED ROLE {index}</div>
                <h3 style="margin-top:8px;">{job["role"]}</h3>
                <strong style="color:#a64f30;">{job["domain"]}</strong>
                <p style="color:#806657;margin-bottom:0;">
                    Search location: {job["location"]}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        link1, link2 = st.columns(2)

        with link1:
            st.link_button(
                "LinkedIn Jobs ↗",
                job["linkedin"],
                use_container_width=True
            )

        with link2:
            st.link_button(
                "Naukri Jobs ↗",
                job["naukri"],
                use_container_width=True
            )

    st.caption(
        "These links open live job-search results on LinkedIn and Naukri. "
        "They are not verified individual vacancy records; confirm the "
        "employer, eligibility, location and posting date before applying."
    )


    # =====================================================
    # JOB MATCH HISTORY
    # =====================================================

    st.markdown(
        '<div class="section-heading">11 | JOB MATCH HISTORY</div>',
        unsafe_allow_html=True
    )

    history = st.session_state.job_match_history

    if history:

        for item in history[:10]:

            st.markdown(
                f"""
                <div class="info-card">
                    <strong style="color:#8b482e;">
                        {item["job_title"]}
                    </strong>
                    <p style="color:#806657;margin-bottom:0;">
                        Match: {item["score"]:.1f}% |
                        Matched: {item["matched"]} |
                        Missing: {item["missing"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("No job match history available yet.")

    st.markdown("---")

    if st.button("Analyze Another Job Description", key="new_job_analysis"):
        st.session_state.job_match_result = None
        st.session_state.job_ai_review = ""
        st.session_state.job_ai_error = ""
        st.session_state.job_recommendations = []
        st.session_state.job_description_text = ""
        st.rerun()

else:

    st.markdown(
        """
        <div class="info-card">
            <h3 style="color:#8b482e;">Ready for Job Matching?</h3>
            <p style="color:#806657;">
            Your resume is connected. Paste a job description above,
            choose a preferred domain for vacancy suggestions, and start
            your multi-domain job match analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )