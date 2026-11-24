
import os
import tempfile
import hashlib
import time
from pathlib import Path

import streamlit as st

from modules.resume_parser import parse_resume
from modules.ats_analyzer import calculate_ats_score
from modules.career_analytics_store import (
    save_analytics_event,
    get_analytics_data
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Resume Intelligence | CAREERIQ AI",
    page_icon="C",
    layout="wide"
)

# =========================================================
# THEME - ORIGINAL PEACH STYLE
# =========================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#fff5eb,#fff0e3,#fff8f1);
    color: #38291f;
}
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1,h2,h3 {
    color: #75412c !important;
}


.main-heading {
    background: linear-gradient(115deg,#713b29 0%,#ae5937 55%,#e58b4e 100%);
    color: #ffffff !important;
    font-size: 36px;
    font-weight: 850;
    padding: 25px 30px;
    border-radius: 20px;
    margin-bottom: 28px;
    letter-spacing: 1px;
    box-shadow: 0 9px 24px rgba(125,61,35,.20);
    border-bottom: 4px solid #f5bd8f;
}

.section-heading {
    background: linear-gradient(110deg,#fff0e3,#ffe0c5,#ffead8);
    color: #783d27 !important;
    font-size: 30px;
    font-weight: 800;
    padding: 16px 22px;
    border-radius: 15px;
    border-left: 6px solid #c66a3e;
    box-shadow: 0 5px 16px rgba(153,82,45,.10);
    margin-top: 22px;
    margin-bottom: 20px;
    letter-spacing: .3px;
}
.upload-card {
    background: rgba(255,255,255,.55);
    border: 2px dashed #e8ae88;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 25px;
}
.result-card {
    background: rgba(255,255,255,.88);
    border: 1px solid #efd5c2;
    border-radius: 18px;
    padding: 22px;
    min-height: 130px;
    box-shadow: 0 5px 18px rgba(100,55,30,.06);
}
.result-number {
    color: #a64f30;
    font-size: 34px;
    font-weight: 800;
}
.result-label {
    color: #806657;
    font-size: 14px;
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
[data-testid="stFileUploader"] {
    background: #fffaf5;
    border-radius: 15px;
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
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "resume_result": None,
    "resume_text": "",
    "ai_review": "",
    "ai_error": "",
    "last_analysis_hash": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_text(uploaded_file):

    suffix = Path(uploaded_file.name).suffix.lower()

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:
            temp.write(uploaded_file.getvalue())
            temp_path = temp.name

        parsed = parse_resume(temp_path)

        if isinstance(parsed, str):
            return parsed

        if isinstance(parsed, dict):
            return str(
                parsed.get("text")
                or parsed.get("resume_text")
                or ""
            )

        return ""

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def get_real_ats_score(ats_result):

    if isinstance(ats_result, dict):
        score = ats_result.get("score")
    elif isinstance(ats_result, (int, float)):
        score = ats_result
    else:
        score = None

    if score is None:
        raise ValueError(
            "ATS analyzer did not return a score."
        )

    score = float(score)

    if not 0 <= score <= 100:
        raise ValueError(
            "ATS score must be between 0 and 100."
        )

    return score


def normalize_list(value):

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return [
            key for key, val in value.items()
            if val
        ]

    return []


def get_missing_sections(text):

    text = text.lower()

    expected = {
        "Professional Summary": [
            "summary", "profile", "objective"
        ],
        "Education": [
            "education", "academic"
        ],
        "Work Experience": [
            "experience", "employment", "internship"
        ],
        "Technical Skills": [
            "skills", "technical skills"
        ],
        "Projects": [
            "projects", "project"
        ],
        "Certifications": [
            "certification", "certificate"
        ]
    }

    missing = []

    for section, keywords in expected.items():
        if not any(word in text for word in keywords):
            missing.append(section)

    return missing


def calculate_readiness(text, missing_sections):

    word_count = len(text.split())

    section_score = (
        (6 - len(missing_sections)) / 6
    ) * 60

    length_score = min(word_count / 400, 1) * 25

    contact_score = 15 if (
        "@" in text and any(c.isdigit() for c in text)
    ) else 0

    return round(
        min(100, section_score + length_score + contact_score)
    )


def get_api_key():

    key = None

    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

    if not key:
        key = os.getenv("GEMINI_API_KEY")

    return key


# =========================================================
# GEMINI MODEL DISCOVERY
# =========================================================

def generate_gemini_review(resume_text):

    from google import genai

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Configure your Gemini API key first."
        )

    client = genai.Client(api_key=api_key)

    # Discover models available to this API key.
    available_models = []

    try:
        for model in client.models.list():

            name = getattr(model, "name", "") or ""

            actions = getattr(
                model,
                "supported_actions",
                []
            ) or []

            if not name:
                continue

            if "generateContent" in actions:
                available_models.append(
                    name.replace("models/", "")
                )

    except Exception:
        available_models = []

    preferred = [
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite"
    ]

    model_candidates = [
        name for name in preferred
        if name in available_models
    ]

    if not model_candidates:
        model_candidates = available_models

    if not model_candidates:
        raise RuntimeError(
            "No model supporting generateContent was found "
            "for this API key."
        )

    prompt = f"""
You are an expert professional resume reviewer.

Analyze the following resume carefully.

Write a detailed and personalized review with these sections:

1. Overall Resume Evaluation
2. Resume Strengths
3. Weaknesses and Problems
4. ATS Formatting Improvements
5. Technical Skills Improvements
6. Missing or Weak Resume Sections
7. Specific Actionable Recommendations
8. Final Professional Verdict

Important instructions:
- Analyze only information actually present in the resume.
- Never invent work experience or qualifications.
- Do not guarantee job selection.
- Give practical recommendations for an entry-level candidate.
- Do not assign an artificial ATS score.

RESUME:

{resume_text[:18000]}
"""

    errors = []

    for model_name in model_candidates:

        for attempt in range(2):

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                review = getattr(response, "text", None)

                if review and review.strip():
                    return review

                errors.append(
                    f"{model_name}: Empty response"
                )

            except Exception as error:

                message = str(error)
                errors.append(
                    f"{model_name}: {message[:250]}"
                )

                # A 404 means try another available model.
                if "404" in message or "NOT_FOUND" in message:
                    break

                # Retry temporary server errors.
                if (
                    "503" in message
                    or "UNAVAILABLE" in message
                    or "429" in message
                ):
                    if attempt == 0:
                        time.sleep(3)
                        continue

                break

    raise RuntimeError(
        "Gemini could not generate the review. "
        + " | ".join(errors[-3:])
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-heading">RESUME INTELLIGENCE</div>',
    unsafe_allow_html=True
)
if st.button("← Back to Home", key="resume_back_home"):
    st.switch_page("app.py")
st.markdown(
    '<div class="section-heading">01 | Upload Your Resume</div>',
    unsafe_allow_html=True
)

# =========================================================
# UPLOAD
# =========================================================

st.markdown('<div class="upload-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"],
    key="resume_upload"
)

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ANALYSIS BUTTON
# =========================================================

if uploaded_file:

    st.caption(
        f"Selected file: {uploaded_file.name}"
    )

    if st.button(
        "Analyze My Resume",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Analyzing your resume..."
            ):

                resume_text = extract_text(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "Could not extract readable text "
                        "from this resume."
                    )
                    st.stop()

                ats_result = calculate_ats_score(
                    resume_text
                )

                # Existing ATS analyzer score only.
                ats_score = get_real_ats_score(
                    ats_result
                )

                sections = (
                    ats_result.get("sections", {})
                    if isinstance(ats_result, dict)
                    else {}
                )

                found_keywords = normalize_list(
                    ats_result.get("found_keywords", [])
                    if isinstance(ats_result, dict)
                    else []
                )

                missing_keywords = normalize_list(
                    ats_result.get("missing_keywords", [])
                    if isinstance(ats_result, dict)
                    else []
                )

                missing_sections = get_missing_sections(
                    resume_text
                )

                word_count = len(resume_text.split())

                readiness = calculate_readiness(
                    resume_text,
                    missing_sections
                )

                analysis_hash = hashlib.sha256(
                    (
                        uploaded_file.name
                        + resume_text
                    ).encode("utf-8")
                ).hexdigest()

                st.session_state.resume_text = resume_text

                st.session_state.resume_result = {
                    "file_name": uploaded_file.name,
                    "ats_score": ats_score,
                    "readiness": readiness,
                    "word_count": word_count,
                    "sections": sections,
                    "found_keywords": found_keywords,
                    "missing_keywords": missing_keywords,
                    "missing_sections": missing_sections
                }

                st.session_state.ai_review = ""
                st.session_state.ai_error = ""

                # Save once for each new resume analysis.
                if (
                    st.session_state.last_analysis_hash
                    != analysis_hash
                ):

                    save_analytics_event(
                        "resume_analysis",
                        score=ats_score,
                        details={
                            "file_name": uploaded_file.name,
                            "readiness": readiness,
                            "word_count": word_count,
                            "analysis_hash": analysis_hash
                        }
                    )

                    st.session_state.last_analysis_hash = (
                        analysis_hash
                    )

                st.success(
                    "Resume analysis completed successfully!"
                )

        except Exception as error:
            st.error(
                f"Resume analysis error: {error}"
            )


# =========================================================
# RESULTS - ONLY AFTER ANALYSIS
# =========================================================

result = st.session_state.resume_result

if result is not None:

    st.divider()

    st.markdown(
        '<div class="section-heading">02 | Resume Analysis Overview</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Analyzed Resume: " + result["file_name"]
    )

    # One card for each metric. No duplicate metrics.

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">
                {result['ats_score']:.0f}%
            </div>
            <div class="result-label">
                ATS SCORE
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">
                {result['readiness']}%
            </div>
            <div class="result-label">
                RESUME READINESS
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-number">
                {result['word_count']}
            </div>
            <div class="result-label">
                WORD COUNT
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ATS Score Progress")
    st.progress(result["ats_score"] / 100)

    st.markdown("### Resume Readiness Progress")
    st.progress(result["readiness"] / 100)

    # -----------------------------------------------------
    # SECTIONS
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">03 | Resume Sections</div>',
        unsafe_allow_html=True
    )

    sections = result["sections"]

    if isinstance(sections, dict) and sections:

        cols = st.columns(3)

        for index, (name, value) in enumerate(
            sections.items()
        ):

            with cols[index % 3]:

                if value:
                    st.success(str(name))
                else:
                    st.warning(str(name))

    elif isinstance(sections, list) and sections:
        st.write(sections)

    else:
        st.info(
            "Section details were not returned by the ATS analyzer."
        )

    # -----------------------------------------------------
    # KEYWORDS
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">04 | Keyword Analysis</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.markdown("### Found Keywords")

        if result["found_keywords"]:
            for keyword in result["found_keywords"]:
                st.success(str(keyword))
        else:
            st.info("No keyword details available.")

    with right:

        st.markdown("### Missing Keywords")

        if result["missing_keywords"]:
            for keyword in result["missing_keywords"]:
                st.warning(str(keyword))
        else:
            st.info("No missing keyword details available.")

    # -----------------------------------------------------
    # MISSING SECTIONS
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">05 | Missing Resume Sections</div>',
        unsafe_allow_html=True
    )

    if result["missing_sections"]:

        for section in result["missing_sections"]:
            st.warning(section)

    else:
        st.success(
            "All major resume sections appear to be present."
        )

    # -----------------------------------------------------
    # IMPROVEMENTS
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">06 | Improvement Suggestions</div>',
        unsafe_allow_html=True
    )

    suggestions = []

    if result["word_count"] < 250:
        suggestions.append(
            "Add more relevant details to make your resume informative."
        )

    if result["word_count"] > 900:
        suggestions.append(
            "Remove unnecessary details and keep the resume concise."
        )

    if result["missing_sections"]:
        suggestions.append(
            "Add the missing resume sections listed above."
        )

    if result["missing_keywords"]:
        suggestions.append(
            "Review relevant technical skills and keywords "
            "for your target role."
        )

    if not suggestions:
        suggestions.append(
            "Review spelling, formatting, consistency and "
            "measurable achievements before applying."
        )

    for suggestion in suggestions:
        st.info(suggestion)

    # -----------------------------------------------------
    # AI REVIEW
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">07 | AI Resume Review</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Generate a personalized review of your uploaded resume "
        "using Gemini AI."
    )

    if st.button(
        "Generate AI Resume Review",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Gemini AI is reviewing your resume..."
            ):

                review = generate_gemini_review(
                    st.session_state.resume_text
                )

                st.session_state.ai_review = review
                st.session_state.ai_error = ""

        except Exception as error:

            st.session_state.ai_error = str(error)

    if st.session_state.ai_review:

        st.markdown("### AI Generated Review")

        st.markdown(
            st.session_state.ai_review
        )

    elif st.session_state.ai_error:

        st.error(
            "AI review could not be generated."
        )

        st.caption(
            st.session_state.ai_error
        )

        st.info(
            "Your resume analysis is available. "
            "You can retry AI review."
        )

    # -----------------------------------------------------
    # HISTORY - ONLY AFTER ANALYSIS
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-heading">08 | Resume Analysis History</div>',
        unsafe_allow_html=True
    )

    try:

        records = get_analytics_data()

        history = [
            item for item in records
            if item.get("event_type") == "resume_analysis"
        ]

        # Remove exact duplicate display entries.
        unique_history = []
        seen = set()

        for item in reversed(history):

            details = item.get("details") or {}

            signature = (
                details.get("analysis_hash")
                or (
                    details.get("file_name"),
                    item.get("score"),
                    item.get("created_at")
                )
            )

            if signature in seen:
                continue

            seen.add(signature)
            unique_history.append(item)

        unique_history = unique_history[:5]

        if unique_history:

            for item in unique_history:

                details = item.get("details") or {}

                file_name = details.get(
                    "file_name",
                    "Resume"
                )

                created_at = item.get(
                    "created_at",
                    ""
                )

                with st.expander(
                    f"{file_name} | {created_at}"
                ):

                    score = item.get("score")

                    if score is not None:
                        st.metric(
                            "ATS Score",
                            f"{float(score):.0f}%"
                        )

                    st.write(
                        "Readiness:",
                        details.get("readiness", "N/A")
                    )

                    st.write(
                        "Word Count:",
                        details.get("word_count", "N/A")
                    )

        else:
            st.info(
                "No previous resume analysis found."
            )

    except Exception as error:

        st.warning(
            f"Could not load resume history: {error}"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<hr>
<div style="
    text-align:center;
    color:#987965;
    padding:15px;
">
    CAREERIQ AI | Intelligent Career Growth Platform
</div>
""", unsafe_allow_html=True)
