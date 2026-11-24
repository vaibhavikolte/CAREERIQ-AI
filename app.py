
import streamlit as st
import textwrap
import html

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CAREERIQ AI | Career Platform",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# HTML RENDER FUNCTION
# =====================================================

def render_html(content):
    st.html(textwrap.dedent(content).strip())


# =====================================================
# PREMIUM DESIGN SYSTEM
# =====================================================

render_html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #E9824D;
    --primary-dark: #CB693A;
    --dark: #292522;
    --text: #514943;
    --muted: #93877F;
    --background: #FBF9F6;
    --white: #FFFFFF;
    --border: #EFE7E0;
    --soft-orange: #FFF0E7;
}

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: var(--background);
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1380px;
    padding: 1.8rem 3rem 2rem 3rem;
}

/* GLOBAL */

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.8rem;
}

/* HEADER */

.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 2px 28px 2px;
}

.logo {
    color: var(--dark);
    font-family: 'Manrope', sans-serif;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
}

.logo span {
    color: var(--primary);
}

.header-right {
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-tag {
    background: white;
    border: 1px solid var(--border);
    color: #B66D46;
    padding: 9px 16px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

/* HERO */

.hero-banner {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #FFF1E7 0%, #FBE1D1 55%, #F4D1BC 100%);
    border: 1px solid #F2DDCF;
    border-radius: 28px;
    padding: 65px 60px;
    min-height: 355px;
    margin-bottom: 30px;
    box-shadow: 0 15px 45px rgba(100, 65, 42, 0.07);
}

.hero-banner:before {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    background: rgba(255,255,255,0.25);
    right: -70px;
    top: -145px;
}

.hero-banner:after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    background: rgba(255,255,255,0.22);
    right: 200px;
    bottom: -155px;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 750px;
}

.hero-label {
    display: inline-block;
    background: rgba(255,255,255,0.75);
    color: #B96D43;
    padding: 9px 16px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 22px;
}

.hero-title {
    color: var(--dark);
    font-family: 'Manrope', sans-serif;
    font-size: clamp(42px, 5vw, 66px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -2.5px;
}

.hero-title span {
    color: var(--primary);
}

.hero-subtitle {
    color: #70574A;
    font-size: 21px;
    font-weight: 700;
    margin-top: 18px;
}

.hero-line {
    height: 5px;
    width: 70px;
    background: var(--primary);
    border-radius: 10px;
    margin: 23px 0;
}

.hero-description {
    max-width: 590px;
    color: #78665C;
    font-size: 15px;
    line-height: 1.9;
}

/* OVERVIEW */

.overview-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 0 0 42px 0;
}

.overview-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 21px 23px;
    box-shadow: 0 5px 18px rgba(70, 50, 35, 0.035);
}

.overview-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.overview-value {
    color: var(--dark);
    font-family: 'Manrope', sans-serif;
    font-size: 29px;
    font-weight: 800;
    margin-top: 7px;
}

.overview-note {
    color: #B27A5C;
    font-size: 11px;
    font-weight: 600;
    margin-top: 4px;
}

/* SECTION */

.section-top {
    margin-bottom: 25px;
}

.section-eyebrow {
    color: var(--primary-dark);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.section-heading {
    color: var(--dark);
    font-family: 'Manrope', sans-serif;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.section-description {
    color: var(--muted);
    font-size: 14px;
    margin-top: 7px;
    line-height: 1.7;
}

/* FEATURE CARDS */

.feature-card {
    position: relative;
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 25px 23px;
    min-height: 225px;
    box-shadow: 0 6px 22px rgba(70, 50, 35, 0.04);
    transition: all 0.25s ease;
    margin-bottom: 8px;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #EBC5AC;
    box-shadow: 0 16px 35px rgba(100, 65, 42, 0.09);
}

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
}

.card-number {
    color: var(--primary);
    font-family: 'Manrope', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.card-indicator {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #69B78D;
}

.card-title {
    color: var(--dark);
    font-family: 'Manrope', sans-serif;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 11px;
}

.card-description {
    color: #857970;
    font-size: 13px;
    line-height: 1.8;
    min-height: 68px;
}

.card-tag {
    display: inline-block;
    background: var(--soft-orange);
    color: #B96D43;
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.8px;
    margin-top: 12px;
}

/* STREAMLIT BUTTONS */

.stButton > button {
    width: 100%;
    min-height: 45px;
    background: var(--primary);
    color: white;
    border: 1px solid var(--primary);
    border-radius: 11px;
    font-size: 13px;
    font-weight: 800;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: var(--primary-dark);
    border-color: var(--primary-dark);
    color: white;
    transform: translateY(-2px);
}

.stButton > button:focus {
    box-shadow: 0 0 0 3px rgba(233,130,77,0.18);
}

/* FOOTER */

.footer {
    border-top: 1px solid var(--border);
    margin-top: 55px;
    padding: 25px 0 5px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    color: var(--muted);
    font-size: 12px;
}

.footer-brand {
    color: var(--dark);
    font-weight: 800;
}

/* RESPONSIVE */

@media (max-width: 900px) {
    .block-container {
        padding: 1rem 1.2rem;
    }

    .hero-banner {
        padding: 42px 30px;
    }

    .overview-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .main-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .hero-banner {
        padding: 35px 23px;
        min-height: auto;
    }

    .hero-subtitle {
        font-size: 17px;
    }

    .section-heading {
        font-size: 24px;
    }

    .footer {
        flex-direction: column;
        align-items: flex-start;
    }
}

</style>
""")


# =====================================================
# HEADER
# =====================================================

render_html("""
<div class="main-header">

    <div class="logo">
        CAREERIQ <span>AI.</span>
    </div>

    <div class="header-right">
        <div class="header-tag">
            YOUR AI CAREER PLATFORM
        </div>
    </div>

</div>
""")


# =====================================================
# HERO SECTION
# =====================================================

render_html("""
<div class="hero-banner">

    <div class="hero-content">

        <div class="hero-label">
            YOUR PERSONAL CAREER COMPANION
        </div>

        <div class="hero-title">
            Hello,<br>
            CAREERIQ <span>AI.</span>
        </div>

        <div class="hero-subtitle">
            Build Your Future. Unlock Your Potential.
        </div>

        <div class="hero-line"></div>

        <div class="hero-description">
            Your all-in-one career development platform.
            Analyze resumes, discover job opportunities,
            identify skill gaps, build professional resumes
            and prepare confidently for interviews.
        </div>

    </div>

</div>
""")


# =====================================================
# PLATFORM OVERVIEW
# =====================================================

render_html("""
<div class="overview-grid">

    <div class="overview-card">
        <div class="overview-label">CAREER TOOLS</div>
        <div class="overview-value">06</div>
        <div class="overview-note">Integrated career solutions</div>
    </div>

    <div class="overview-card">
        <div class="overview-label">CAREER DEVELOPMENT</div>
        <div class="overview-value">360°</div>
        <div class="overview-note">From resume to interview</div>
    </div>

    <div class="overview-card">
        <div class="overview-label">PLATFORM ACCESS</div>
        <div class="overview-value">All-in-One</div>
        <div class="overview-note">One place for your career journey</div>
    </div>

</div>
""")


# =====================================================
# FEATURE SECTION
# =====================================================

render_html("""
<div class="section-top">

    <div class="section-eyebrow">
        EXPLORE THE PLATFORM
    </div>

    <div class="section-heading">
        Your Career Toolkit
    </div>

    <div class="section-description">
        Explore powerful tools designed to support every stage
        of your professional journey.
    </div>

</div>
""")


# =====================================================
# FEATURE CARD FUNCTION
# =====================================================

def feature_card(number, title, description, tag):

    safe_number = html.escape(str(number))
    safe_title = html.escape(str(title))
    safe_description = html.escape(str(description))
    safe_tag = html.escape(str(tag))

    render_html(f"""
    <div class="feature-card">

        <div class="card-top">
            <div class="card-number">{safe_number}</div>
            <div class="card-indicator"></div>
        </div>

        <div class="card-title">{safe_title}</div>

        <div class="card-description">
            {safe_description}
        </div>

        <div class="card-tag">{safe_tag}</div>

    </div>
    """)


# =====================================================
# FIRST ROW - TOOLS 01, 02, 03
# =====================================================

col1, col2, col3 = st.columns(3, gap="large")


with col1:

    feature_card(
        "01",
        "Resume Intelligence",
        "Analyze your resume, discover strengths, identify missing details and understand your resume readiness.",
        "RESUME ANALYSIS"
    )

    if st.button("Explore Resume Intelligence", key="resume"):
        st.switch_page("pages/1_Resume_Intelligence.py")


with col2:

    feature_card(
        "02",
        "ATS & Job Intelligence",
        "Compare your resume with job descriptions, identify keyword gaps and understand job compatibility.",
        "JOB MATCHING"
    )

    if st.button("Explore Job Intelligence", key="job"):
        st.switch_page("pages/2_ATS_Job_Intelligence.py")


with col3:

    feature_card(
        "03",
        "AI Career Agent",
        "Explore suitable career paths, discover skill gaps and receive structured career development guidance.",
        "CAREER GUIDANCE"
    )

    if st.button("Explore Career Agent", key="career_agent"):
        st.switch_page("pages/3_AI_Career_Agent.py")


# =====================================================
# SECOND ROW - TOOLS 04, 05, 06
# =====================================================

col4, col5, col6 = st.columns(3, gap="large")


with col4:

    feature_card(
        "04",
        "AI Interview Simulation",
        "Practice technical and HR interview questions, evaluate your answers and improve your preparation.",
        "INTERVIEW PRACTICE"
    )

    if st.button("Start Interview Practice", key="interview"):
        st.switch_page("pages/4_AI_Interview_Simulation.py")


with col5:

    feature_card(
        "05",
        "Resume Builder",
        "Create a professional, structured and ATS-friendly resume with editable sections.",
        "RESUME CREATION"
    )

    if st.button("Build My Resume", key="resume_builder"):
        st.switch_page("pages/5_Resume_Builder.py")


with col6:

    feature_card(
        "06",
        "Career Analytics",
        "Explore your skills, analyze your career profile and track your professional development.",
        "CAREER ANALYTICS"
    )

    if st.button("View Career Analytics", key="career_analytics"):
        st.switch_page("pages/6_Career_Analytics.py")


# =====================================================
# FOOTER
# =====================================================

render_html("""
<div class="footer">

    <div>
        <span class="footer-brand">CAREERIQ AI.</span>
        &nbsp; Build Your Future. Unlock Your Potential.
    </div>

    <div>
        Your Career. Your Growth. Your Future.
    </div>

</div>
""")
