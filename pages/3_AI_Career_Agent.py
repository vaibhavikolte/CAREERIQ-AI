
import streamlit as st
import os
import re
import json
import time
from datetime import date

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Career Agent | CAREERIQ AI",
    page_icon="C",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "career_plan_result" not in st.session_state:
    st.session_state.career_plan_result = None

# =========================================================
# MULTI-DOMAIN CAREER DATABASE
# =========================================================

CAREER_DOMAINS = {
    "Data Analytics & Business Intelligence": {
        "roles": [
            "Data Analyst",
            "Business Analyst",
            "Power BI Developer",
            "SQL Developer",
            "Business Intelligence Analyst",
            "MIS Analyst"
        ],
        "skills": [
            "Excel", "SQL", "Power BI", "Tableau",
            "Power Query", "DAX", "Python", "Pandas",
            "NumPy", "Statistics", "Data Cleaning",
            "Data Visualization", "Data Modeling",
            "ETL", "MySQL", "Dashboard Development"
        ]
    },

    "Data Science & AI / Machine Learning": {
        "roles": [
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Science Intern",
            "NLP Engineer",
            "Computer Vision Engineer"
        ],
        "skills": [
            "Python", "R", "Statistics", "Probability",
            "Pandas", "NumPy", "Scikit-learn",
            "TensorFlow", "PyTorch", "Machine Learning",
            "Deep Learning", "NLP", "Computer Vision",
            "Feature Engineering", "Model Evaluation",
            "Generative AI", "LLM"
        ]
    },

    "Cloud Computing & DevOps": {
        "roles": [
            "Cloud Engineer",
            "AWS Cloud Engineer",
            "Azure Cloud Engineer",
            "DevOps Engineer",
            "Cloud Support Associate",
            "Site Reliability Engineer"
        ],
        "skills": [
            "AWS", "Microsoft Azure", "Google Cloud",
            "GCP", "Linux", "Docker", "Kubernetes",
            "Jenkins", "Git", "GitHub", "Terraform",
            "CI/CD", "Networking", "Python",
            "Cloud Security", "Shell Scripting"
        ]
    },

    "Full Stack Development": {
        "roles": [
            "Full Stack Developer",
            "Frontend Developer",
            "Backend Developer",
            "React Developer",
            "Node.js Developer",
            "Web Developer"
        ],
        "skills": [
            "HTML", "CSS", "JavaScript", "TypeScript",
            "React", "Angular", "Vue.js", "Node.js",
            "Express.js", "MongoDB", "MySQL",
            "PostgreSQL", "REST API", "Git",
            "GitHub", "Responsive Design"
        ]
    },

    "Software Development": {
        "roles": [
            "Software Developer",
            "Python Developer",
            "Java Developer",
            "C++ Developer",
            "Application Developer",
            "Software Engineer"
        ],
        "skills": [
            "Python", "Java", "C++", "C#",
            "Data Structures", "Algorithms",
            "OOP", "SQL", "Git", "GitHub",
            "Debugging", "Problem Solving",
            "API Development", "Software Design",
            "Testing"
        ]
    },

    "Networking": {
        "roles": [
            "Network Engineer",
            "Network Support Engineer",
            "Network Administrator",
            "NOC Engineer",
            "IT Support Engineer"
        ],
        "skills": [
            "Computer Networking", "TCP/IP", "DNS",
            "DHCP", "Routing", "Switching",
            "Cisco", "CCNA", "LAN", "WAN",
            "Firewalls", "Linux", "Network Security",
            "Wireshark", "Troubleshooting"
        ]
    },

    "Cybersecurity": {
        "roles": [
            "Cybersecurity Analyst",
            "SOC Analyst",
            "Security Engineer",
            "Penetration Tester",
            "Information Security Analyst"
        ],
        "skills": [
            "Cybersecurity", "Network Security",
            "Ethical Hacking", "Penetration Testing",
            "Linux", "Python", "Wireshark",
            "SIEM", "Splunk", "Incident Response",
            "Vulnerability Assessment", "Firewalls",
            "Cryptography", "Security Monitoring"
        ]
    },

    "QA & Software Testing": {
        "roles": [
            "QA Engineer",
            "Manual Tester",
            "Automation Tester",
            "Software Test Engineer",
            "API Tester"
        ],
        "skills": [
            "Manual Testing", "Automation Testing",
            "Selenium", "Java", "Python",
            "API Testing", "Postman", "JIRA",
            "Test Cases", "Bug Tracking",
            "Regression Testing", "SQL",
            "Performance Testing", "Pytest"
        ]
    },

    "UI/UX Design": {
        "roles": [
            "UI Designer",
            "UX Designer",
            "Product Designer",
            "UI/UX Designer",
            "Visual Designer"
        ],
        "skills": [
            "Figma", "Adobe XD", "Wireframing",
            "Prototyping", "User Research",
            "User Testing", "Design Systems",
            "Typography", "Color Theory",
            "Interaction Design", "Usability",
            "Information Architecture"
        ]
    },

    "Digital Marketing": {
        "roles": [
            "Digital Marketing Executive",
            "SEO Analyst",
            "Social Media Manager",
            "Content Marketing Executive",
            "Performance Marketing Executive"
        ],
        "skills": [
            "SEO", "SEM", "Google Ads",
            "Google Analytics", "Social Media Marketing",
            "Content Marketing", "Email Marketing",
            "Keyword Research", "Copywriting",
            "Meta Ads", "Marketing Analytics",
            "Campaign Management"
        ]
    },

    "Finance & Accounting": {
        "roles": [
            "Financial Analyst",
            "Accountant",
            "Accounts Executive",
            "Finance Associate",
            "Investment Analyst"
        ],
        "skills": [
            "Excel", "Financial Modeling",
            "Financial Analysis", "Accounting",
            "Bookkeeping", "Tally", "GST",
            "Taxation", "Budgeting",
            "Financial Reporting", "Forecasting",
            "Power BI", "Communication"
        ]
    },

    "Human Resources": {
        "roles": [
            "HR Executive",
            "HR Analyst",
            "Recruitment Coordinator",
            "Talent Acquisition Associate",
            "HR Generalist"
        ],
        "skills": [
            "Recruitment", "Talent Acquisition",
            "Interview Coordination", "HR Operations",
            "Payroll", "HR Analytics",
            "Excel", "Communication",
            "Employee Engagement", "Onboarding",
            "Performance Management",
            "Human Resource Management"
        ]
    },

    "Business & Project Management": {
        "roles": [
            "Project Coordinator",
            "Project Manager",
            "Product Analyst",
            "Business Operations Analyst",
            "Product Manager"
        ],
        "skills": [
            "Project Management", "Agile",
            "Scrum", "JIRA", "Communication",
            "Stakeholder Management",
            "Requirement Gathering", "Excel",
            "Problem Solving", "Risk Management",
            "Documentation", "Product Strategy",
            "Business Analysis"
        ]
    },

    "Custom / Other Career": {
        "roles": ["Other / Custom Role"],
        "skills": [
            "Communication", "Problem Solving",
            "Research", "Documentation",
            "Time Management", "Teamwork",
            "Technical Skills", "Project Management"
        ]
    }
}

# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {
    "Power BI": ["power bi", "powerbi"],
    "Power Query": ["power query"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Express.js": ["express.js", "express"],
    "Vue.js": ["vue.js", "vue"],
    "Microsoft Azure": ["azure", "microsoft azure"],
    "Google Cloud": ["google cloud", "gcp"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Computer Vision": ["computer vision"],
    "Generative AI": ["generative ai", "gen ai"],
    "NLP": ["nlp", "natural language processing"],
    "Data Structures": ["data structures", "dsa"],
    "OOP": ["oop", "object oriented programming"],
    "SQL": ["sql", "structured query language"],
    "Excel": ["excel", "microsoft excel"],
    "GitHub": ["github"],
    "Git": ["git"],
    "Power BI": ["power bi", "powerbi"]
}


def detect_resume_skills(resume_text, skill_list):

    found = []

    if not resume_text:
        return found

    text = resume_text.lower()

    for skill in skill_list:

        aliases = SKILL_ALIASES.get(
            skill,
            [skill.lower()]
        )

        for alias in aliases:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text):
                found.append(skill)
                break

    return found


# =========================================================
# GEMINI API KEY
# =========================================================

def get_gemini_api_key():

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if api_key:
        return api_key

    try:
        return str(
            st.secrets.get("GEMINI_API_KEY", "")
        ).strip()

    except Exception:
        return ""


# =========================================================
# GEMINI MODEL DISCOVERY
# =========================================================

def get_available_gemini_models(client):

    models = []

    for model in client.models.list():

        name = getattr(model, "name", None)

        actions = getattr(
            model,
            "supported_actions",
            []
        ) or []

        if not name:
            continue

        if actions:

            supports_generation = any(
                "generatecontent" in str(action).lower().replace("_", "")
                for action in actions
            )

            if not supports_generation:
                continue

        name = str(name).replace("models/", "")

        if name not in models:
            models.append(name)

    models.sort(
        key=lambda x: (
            "flash" not in x.lower(),
            x.lower()
        )
    )

    return models


# =========================================================
# AI CAREER PLAN GENERATOR
# =========================================================

def generate_ai_career_plan(
    resume_text,
    domain,
    role,
    custom_role,
    experience,
    interests,
    current_skills,
    missing_skills
):

    try:

        from google import genai

        api_key = get_gemini_api_key()

        if not api_key:
            return None, "Gemini API key is missing."

        client = genai.Client(api_key=api_key)

        actual_role = (
            custom_role.strip()
            if role == "Other / Custom Role" and custom_role.strip()
            else role
        )

        prompt = f"""
You are CAREERIQ AI, an expert multi-domain career advisor.

Create a deeply personalized career development plan.

CAREER DOMAIN: {domain}
TARGET ROLE: {actual_role}
EXPERIENCE: {experience}
INTERESTS: {interests}

CONFIRMED SKILLS:
{current_skills}

SKILLS TO DEVELOP:
{missing_skills}

RESUME:
{resume_text[:9000] if resume_text else "No resume available."}

IMPORTANT:
This platform supports technology, business, finance, HR,
design, marketing, networking, cybersecurity and other careers.

Do not force data analytics recommendations on non-analytics roles.
Use tools and learning paths relevant to the selected domain.

Generate exactly:
1. Personalized profile assessment.
2. Five priority skills in order of importance.
3. Six-week learning roadmap.
4. Three original portfolio/practical project suggestions.
5. Interview preparation topics.
6. Resume and portfolio improvements.
7. Three immediate next actions.

The six-week roadmap must have six separate weeks.
Each week must contain a focus and 2 to 4 practical tasks.

Each project must include:
- Project title
- Project description
- Skills demonstrated
- Suggested tools
- Expected outcome

Projects must be suitable for the target role and experience level.

Return ONLY valid JSON, without Markdown fences.

Required JSON keys:
profile_assessment
priority_skills
six_week_roadmap
portfolio_projects
interview_preparation
resume_improvements
next_actions

six_week_roadmap must be an array of objects containing:
week, focus, tasks.

portfolio_projects must be an array of objects containing:
title, description, skills, tools, outcome.

Do not invent qualifications or skills.
Do not promise employment or selection.
Use professional and practical English.
"""

        try:
            models = get_available_gemini_models(client)
        except Exception:
            models = []

        if not models:
            models = [
                "gemini-2.5-flash",
                "gemini-2.0-flash"
            ]

        last_error = "No available Gemini model."

        for model_name in models[:5]:

            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )

                    answer = getattr(
                        response,
                        "text",
                        None
                    )

                    if answer and answer.strip():
                        return answer.strip(), (
                            f"Gemini AI connected successfully: {model_name}"
                        )

                    last_error = "Gemini returned an empty response."
                    break

                except Exception as error:

                    last_error = str(error)[:500]

                    temporary = any(
                        code in last_error.lower()
                        for code in [
                            "503", "429", "500", "504",
                            "temporarily unavailable"
                        ]
                    )

                    if temporary and attempt < 2:
                        time.sleep(2 ** (attempt + 1))
                        continue

                    break

        return None, last_error

    except Exception as error:

        return None, str(error)[:500]


# =========================================================
# JSON RESPONSE PARSER
# =========================================================

def parse_ai_plan(response_text):

    if not response_text:
        return None

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

    try:
        data = json.loads(cleaned)

    except Exception:

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            return None

        try:
            data = json.loads(cleaned[start:end + 1])

        except Exception:
            return None

    required = [
        "profile_assessment",
        "priority_skills",
        "six_week_roadmap",
        "portfolio_projects",
        "interview_preparation",
        "resume_improvements",
        "next_actions"
    ]

    if not isinstance(data, dict):
        return None

    if not all(key in data for key in required):
        return None

    return data


# =========================================================
# THEME - WARM CREAM + PEACH
# =========================================================

st.html("""
<style>

.stApp {
    background: #fffaf6;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #352c29;
}

.hero {
    background: linear-gradient(
        115deg,
        #fff1e8 0%,
        #fbd9c8 100%
    );
    padding: 38px;
    border-radius: 22px;
    margin-bottom: 25px;
}

.hero-label {
    color: #c16f43;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero-title {
    color: #302827;
    font-size: 38px;
    font-weight: 900;
    margin-top: 10px;
}

.hero-description {
    color: #765b50;
    font-size: 15px;
    margin-top: 10px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #f1e3da;
    padding: 17px;
    border-radius: 14px;
}

div[data-testid="stExpander"] {
    background: #fffdfb;
    border: 1px solid #f1e3da;
    border-radius: 12px;
}

.stButton > button {
    background: #e99560;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 800;
    min-height: 45px;
}

.stButton > button:hover {
    background: #d77d48;
    color: white;
}

.stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid #e99560;
    color: #a85e35;
    font-weight: 700;
}

div[data-testid="stProgress"] > div > div {
    background-color: #e99560;
}

</style>
""")


# =========================================================
# HEADER
# =========================================================

if st.button("← Back to Home"):
    st.switch_page("app.py")

st.html("""
<div class="hero">

    <div class="hero-label">
        YOUR PERSONAL CAREER GUIDE
    </div>

    <div class="hero-title">
        AI Career Agent
    </div>

    <div class="hero-description">
        Build your career strategy with personalized skill-gap analysis,
        intelligent learning recommendations and a practical career roadmap.
    </div>

</div>
""")


# =========================================================
# RESUME CONNECTION
# =========================================================

resume_text = st.session_state.get("resume_text", "")

if resume_text:
    st.success("Resume connected successfully from Resume Intelligence.")
else:
    st.info(
        "No analyzed resume detected. "
        "You can still create a career plan by selecting your skills."
    )


# =========================================================
# CAREER INPUTS
# =========================================================

st.subheader("Build Your Career Strategy")

domain = st.selectbox(
    "Select Your Career Domain",
    list(CAREER_DOMAINS.keys()),
    key="career_domain"
)

domain_data = CAREER_DOMAINS[domain]

role = st.selectbox(
    "Select Your Target Role",
    domain_data["roles"],
    key="career_target_role"
)

custom_role = ""

if role == "Other / Custom Role":

    custom_role = st.text_input(
        "Enter Your Target Job Role",
        placeholder="Example: Blockchain Developer, Architect, Lawyer..."
    )

col1, col2 = st.columns(2)

with col1:

    experience = st.selectbox(
        "Experience Level",
        [
            "Student",
            "Fresher",
            "Less than 1 year",
            "1–2 years",
            "2–3 years",
            "3–5 years",
            "5+ years"
        ]
    )

with col2:

    interests = st.multiselect(
        "Your Career Interests",
        [
            "Technical Learning",
            "Practical Projects",
            "Research",
            "Problem Solving",
            "Business Strategy",
            "Creative Work",
            "Leadership",
            "Innovation",
            "Automation",
            "Professional Development"
        ]
    )

role_skills = domain_data["skills"]

detected_skills = detect_resume_skills(
    resume_text,
    role_skills
)

st.markdown("#### Confirm Your Current Skills")

st.caption(
    "Resume detection is a suggestion. "
    "Select only the skills you actually know."
)

current_skills = st.multiselect(
    "Your Existing Skills",
    options=role_skills,
    default=detected_skills,
    key="career_current_skills"
)

if role == "Other / Custom Role":
    st.caption(
        "For a custom role, the AI will use your role name, "
        "resume and confirmed skills to build recommendations."
    )


# =========================================================
# GENERATE CAREER PLAN
# =========================================================

if st.button(
    "Generate My Personalized AI Career Plan",
    width="stretch"
):

    if role == "Other / Custom Role" and not custom_role.strip():

        st.error("Please enter your target job role.")

    else:

        missing_skills = [
            skill for skill in role_skills
            if skill not in current_skills
        ]

        coverage = round(
            len(current_skills) / len(role_skills) * 100
        ) if role_skills else 0

        with st.spinner(
            "Gemini AI is analyzing your career profile and generating your roadmap..."
        ):

            ai_result, ai_status = generate_ai_career_plan(
                resume_text=resume_text,
                domain=domain,
                role=role,
                custom_role=custom_role,
                experience=experience,
                interests=interests,
                current_skills=current_skills,
                missing_skills=missing_skills
            )

        ai_data = parse_ai_plan(ai_result)

        st.session_state.career_plan_result = {
            "domain": domain,
            "role": role,
            "custom_role": custom_role,
            "experience": experience,
            "interests": interests,
            "current_skills": current_skills,
            "missing_skills": missing_skills,
            "all_skills": role_skills,
            "coverage": coverage,
            "ai_result": ai_result,
            "ai_data": ai_data,
            "ai_status": ai_status,
            "date": str(date.today())
        }


# =========================================================
# DISPLAY CAREER PLAN
# =========================================================

if st.session_state.career_plan_result:

    plan = st.session_state.career_plan_result
    ai_data = plan.get("ai_data")

    st.divider()

    st.header("Your Personalized Career Roadmap")

    actual_role = (
        plan["custom_role"]
        if plan["role"] == "Other / Custom Role"
        else plan["role"]
    )

    st.markdown(f"### Target Role: {actual_role}")

    st.caption(
        f"Domain: {plan['domain']} | "
        f"Experience: {plan['experience']} | "
        f"Generated: {plan['date']}"
    )

    # -----------------------------------------------------
    # SKILL COVERAGE
    # -----------------------------------------------------

    st.subheader("1. Career Skill Coverage")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Confirmed Skills",
        f"{len(plan['current_skills'])}/{len(plan['all_skills'])}"
    )

    c2.metric(
        "Skills to Develop",
        len(plan["missing_skills"])
    )

    c3.metric(
        "Skill Coverage",
        f"{plan['coverage']}%"
    )

    st.progress(plan["coverage"] / 100)

    st.caption(
        "Coverage is based on skills you confirmed. "
        "It is not a hiring probability."
    )

    # -----------------------------------------------------
    # SKILL GAP ANALYSIS
    # -----------------------------------------------------

    st.divider()

    st.subheader("2. Personalized Skill Gap Analysis")

    left, right = st.columns(2)

    with left:

        st.markdown("#### Your Confirmed Skills")

        if plan["current_skills"]:

            for skill in plan["current_skills"]:
                st.markdown(f"- {skill}")

        else:
            st.info("No skills confirmed yet.")

    with right:

        st.markdown("#### Skills to Develop")

        if plan["missing_skills"]:

            for skill in plan["missing_skills"]:
                st.markdown(f"- {skill}")

        else:
            st.success("All listed role skills are confirmed.")

    # -----------------------------------------------------
    # AI PROFILE ASSESSMENT
    # -----------------------------------------------------

    st.divider()

    st.subheader("3. AI Career Profile Assessment")

    if ai_data:

        st.write(ai_data["profile_assessment"])

        st.markdown("#### AI-Prioritized Skills")

        for skill in ai_data["priority_skills"]:
            st.markdown(f"- {skill}")

    # -----------------------------------------------------
    # AI ROADMAP
    # -----------------------------------------------------

    st.divider()

    st.subheader("4. AI-Generated Six-Week Learning Roadmap")

    if ai_data:

        for index, week in enumerate(
            ai_data["six_week_roadmap"][:6]
        ):

            with st.expander(
                f"Week {week.get('week', index + 1)} – {week.get('focus', 'Learning Focus')}",
                expanded=(index == 0)
            ):

                for task in week.get("tasks", []):
                    st.markdown(f"- {task}")

    else:

        st.warning(
            "AI roadmap could not be generated for this attempt. "
            "Please retry after checking your Gemini API connection."
        )

    # -----------------------------------------------------
    # AI PROJECT SUGGESTIONS
    # -----------------------------------------------------

    st.divider()

    st.subheader("5. AI-Generated Portfolio Project Suggestions")

    if ai_data:

        for index, project in enumerate(
            ai_data["portfolio_projects"][:5],
            1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**Project {index}: {project.get('title', 'Project')}**"
                )

                st.write(
                    project.get("description", "")
                )

                if project.get("skills"):
                    st.markdown(
                        "**Skills:** "
                        + ", ".join(project["skills"])
                    )

                if project.get("tools"):
                    st.markdown(
                        "**Tools:** "
                        + ", ".join(project["tools"])
                    )

                if project.get("outcome"):
                    st.caption(
                        "Expected Outcome: "
                        + project["outcome"]
                    )

    else:

        st.warning(
            "AI project suggestions are not available because "
            "the AI response was not successfully generated."
        )

    # -----------------------------------------------------
    # INTERVIEW PREPARATION
    # -----------------------------------------------------

    st.divider()

    st.subheader("6. AI Interview Preparation")

    if ai_data:

        for topic in ai_data["interview_preparation"]:
            st.markdown(f"- {topic}")

    # -----------------------------------------------------
    # RESUME IMPROVEMENTS
    # -----------------------------------------------------

    st.divider()

    st.subheader("7. AI Resume & Portfolio Improvements")

    if ai_data:

        for item in ai_data["resume_improvements"]:
            st.markdown(f"- {item}")

    # -----------------------------------------------------
    # NEXT ACTIONS
    # -----------------------------------------------------

    st.divider()

    st.subheader("8. Your Next Three Actions")

    if ai_data:

        for index, action in enumerate(
            ai_data["next_actions"][:3],
            1
        ):
            st.markdown(f"**{index}.** {action}")

    # -----------------------------------------------------
    # AI STATUS
    # -----------------------------------------------------

    st.divider()

    st.subheader("Gemini AI Status")

    if ai_data:

        st.success(plan["ai_status"])

    else:

        st.error(
            "AI generation was unsuccessful. "
            "The roadmap and project suggestions were not generated by AI."
        )

        st.caption(plan["ai_status"])

        if st.button("Retry AI Generation"):
            st.session_state.career_plan_result = None
            st.rerun()

    # -----------------------------------------------------
    # DOWNLOAD REPORT
    # -----------------------------------------------------

    st.divider()

    st.subheader("9. Download Your Career Plan")

    report = f"""
CAREERIQ AI - PERSONALIZED CAREER PLAN

Date: {plan['date']}

DOMAIN:
{plan['domain']}

TARGET ROLE:
{actual_role}

EXPERIENCE:
{plan['experience']}

INTERESTS:
{', '.join(plan['interests'])}

CONFIRMED SKILLS:
{', '.join(plan['current_skills'])}

SKILLS TO DEVELOP:
{', '.join(plan['missing_skills'])}

SKILL COVERAGE:
{plan['coverage']}%

AI CAREER PLAN:
{plan['ai_result'] or plan['ai_status']}
"""

    st.download_button(
        "Download My Career Plan",
        data=report,
        file_name="CAREERIQ_AI_Career_Plan.txt",
        mime="text/plain",
        width="stretch"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CAREERIQ AI | Your Personal Career Companion | "
    "AI career guidance is informational and does not guarantee employment."
)
