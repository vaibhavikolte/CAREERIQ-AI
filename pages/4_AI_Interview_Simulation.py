import streamlit as st
import json
import re
from google import genai

from modules.career_analytics_store import save_analytics_event


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Interview Simulation | CAREERIQ AI",
    page_icon="C",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "mcq_questions": [],
    "mcq_category": None,
    "mcq_attempt": 0,
    "mcq_history": {},
    "mcq_source": None,
    "mcq_result": None,
    "mcq_ai_analysis": None,
    "mcq_submitted": False,
    "mcq_attempt_history": [],

    "ai_questions": [],
    "ai_answers": {},
    "ai_feedback": None,
    "ai_category": None,
    "ai_domain": None,
    "ai_role": None,
    "ai_level": "Fresher / Entry-Level",

    "hr_questions": [],
    "hr_category": None,
    "hr_answers": {},
    "hr_feedback": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CUSTOM CSS - WARM PEACH BROWN ORANGE THEME
# =========================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background: #FFF3E9;
    color: #603B2C;
}

/* MAIN CONTENT WIDTH */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADINGS */

h1, h2, h3, h4 {
    color: #713F2B !important;
    font-weight: 800 !important;
}

/* MAIN TITLE */

.main-title {
    background: linear-gradient(
        110deg,
        #713F2B,
        #B75D35,
        #E78B49
    );

    color: white !important;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 1px;

    padding: 35px;
    border-radius: 24px 24px 0 24px;

    border-bottom: 5px solid #F3B77D;

    box-shadow: 0 12px 25px rgba(125, 65, 37, 0.18);

    margin-bottom: 25px;
}

/* SUBTITLE */

.subtitle {
    color: #9B6047;
    font-size: 16px;
    margin-top: 15px;
    margin-bottom: 35px;
}

/* SECTION HEADINGS */

.section-heading {
    background: linear-gradient(
        110deg,
        #FFE2CB,
        #FFF0E3
    );

    color: #713F2B;
    padding: 22px 28px;

    border-left: 6px solid #C9693C;
    border-radius: 17px;

    font-size: 23px;
    font-weight: 800;

    margin-top: 25px;
    margin-bottom: 22px;
}

/* FEATURE CARDS */

.feature-card {
    background: #FFFFFF;
    padding: 24px;

    border-radius: 18px;
    border: 1px solid #F1D8C5;

    box-shadow: 0 5px 18px rgba(115, 67, 42, 0.07);

    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(115, 67, 42, 0.13);
}

/* SCORE CARDS */

.score-card {
    background: #FFFFFF;
    border: 1px solid #F1D8C5;

    border-radius: 18px;
    padding: 22px;

    text-align: center;

    box-shadow: 0 5px 18px rgba(115, 67, 42, 0.07);
}

.score-number {
    font-size: 38px;
    font-weight: 900;
    color: #C56837;
}

/* SOURCE LABEL */

.source-label {
    background: #FFE7D2;

    padding: 10px 16px;
    border-radius: 10px;

    color: #854527;
    font-weight: 700;

    display: inline-block;
    margin-bottom: 18px;
}

/* BUTTONS */

div.stButton > button,
div.stFormSubmitButton > button {

    background: linear-gradient(
        110deg,
        #A84E2D,
        #E58B48
    );

    color: white !important;

    border: none;
    border-radius: 14px;

    padding: 12px 22px;

    font-weight: 700;
    transition: all 0.25s ease;

    box-shadow: 0 5px 12px rgba(155, 78, 43, 0.16);
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {

    background: linear-gradient(
        110deg,
        #813D27,
        #C9693C
    );

    color: white !important;

    transform: translateY(-2px);

    box-shadow: 0 8px 18px rgba(155, 78, 43, 0.24);
}

/* INPUT BOXES */

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {

    background: #FFFFFF !important;

    border: 1px solid #EBD1BD !important;
    border-radius: 12px !important;
}

/* INPUT FOCUS */

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {

    border: 2px solid #D17A48 !important;
    box-shadow: 0 0 0 2px rgba(209, 122, 72, 0.12);
}

/* RADIO BUTTONS */

div[role="radiogroup"] {
    background: #FFFAF6;
    border: 1px solid #F1D8C5;
    border-radius: 12px;
    padding: 12px;
}

/* METRICS */

div[data-testid="stMetric"] {

    background: #FFFFFF;
    padding: 18px;

    border: 1px solid #F1D8C5;
    border-radius: 16px;

    box-shadow: 0 4px 14px rgba(115, 67, 42, 0.06);
}

/* PROGRESS BAR */

div[data-testid="stProgressBar"] > div {
    background: #F3DCCB;
    border-radius: 20px;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #A84E2D,
        #E58B48
    );
    border-radius: 20px;
}

/* EXPANDER */

div[data-testid="stExpander"] {

    background: #FFFFFF;
    border: 1px solid #F1D8C5;
    border-radius: 14px;

    margin-bottom: 12px;
}

/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* DIVIDERS */

hr {
    border-color: #EBD2C0 !important;
}

/* CAPTIONS */

.stCaption {
    color: #93664F !important;
}

/* RESPONSIVE */

@media (max-width: 768px) {

    .main-title {
        font-size: 25px;
        padding: 23px;
    }

    .subtitle {
        font-size: 14px;
    }

    .section-heading {
        font-size: 19px;
        padding: 16px;
    }

    .score-card {
        padding: 14px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# GEMINI AI CONNECTION
# =========================================================

def call_gemini(prompt):

    import time
    import os

    api_key = (
        st.secrets.get("GEMINI_API_KEY", "")
        or os.getenv("GEMINI_API_KEY", "")
    )

    if not api_key:
        raise Exception("Gemini API Key not found.")

    client = genai.Client(api_key=api_key)

    models_to_try = [
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash"
    ]

    errors = []

    for model_name in models_to_try:

        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                if response and response.text:
                    return response.text.strip()

                raise Exception("Empty Gemini response")

            except Exception as error:

                error_message = str(error)
                errors.append(f"{model_name}: {error_message}")

                retryable = any(
                    code in error_message
                    for code in ["503", "429", "500", "504"]
                )

                if retryable and attempt < 2:
                    time.sleep(2 ** (attempt + 1))
                    continue

                if not retryable:
                    break

    raise Exception(
        "All Gemini attempts failed: "
        + " | ".join(errors[-3:])
    )

# =========================================================
# JSON RESPONSE CLEANER
# =========================================================

def extract_json(text):

    text = text.strip()

    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1:
        raise ValueError(
            "AI response did not contain valid JSON."
        )

    return json.loads(text[start:end + 1])


# =========================================================
# GENERATE 10 MCQ QUESTIONS USING GEMINI AI
# =========================================================

def generate_mcq_questions(category, count=10):

    previous_questions = st.session_state.mcq_history.get(
        category, []
    )

    prompt = f"""
You are an expert interviewer creating a high-quality assessment.

Generate exactly {count} NEW multiple-choice questions.

Assessment subject: {category}
Candidate level: Fresher / Entry-Level

Difficulty distribution:
- 4 Easy
- 4 Medium
- 2 Interview-level

Avoid repeating these previous questions:
{json.dumps(previous_questions[-40:], indent=2)}

Requirements:
- Questions must be accurate and relevant to the selected subject.
- Test concepts, practical understanding and problem-solving.
- Each question must have exactly four meaningful options.
- Only one option must be correct.
- Include a clear, beginner-friendly explanation.
- Do not mention Data Analyst unless directly relevant.
- Do not repeat or paraphrase previous questions.

Return ONLY a valid JSON array:
[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option text",
    "explanation": "Simple explanation"
  }}
]
"""

    questions = extract_json(call_gemini(prompt))

    if not isinstance(questions, list) or len(questions) != count:
        raise ValueError(
            f"Gemini did not generate exactly {count} questions."
        )

    validated = []

    for item in questions:

        if not all(
            key in item
            for key in [
                "question",
                "options",
                "answer",
                "explanation"
            ]
        ):
            raise ValueError(
                "AI question format is incomplete."
            )

        if (
            not isinstance(item["options"], list)
            or len(item["options"]) != 4
        ):
            raise ValueError(
                "Each AI-generated question must have four options."
            )

        if item["answer"] not in item["options"]:
            raise ValueError(
                "Correct answer is not present in the options."
            )

        validated.append(item)

    return validated


# =========================================================
# CREATE A NEW MCQ TEST
# =========================================================

def create_new_mcq_test(category):

    try:
        questions = generate_mcq_questions(category, 10)

    except Exception as error:
        st.error(
            "Gemini AI could not generate the questions. "
            "No fixed question bank will be shown."
        )
        st.caption(
            "Check your Gemini API key, quota and model access, "
            "then try again."
        )
        st.code(str(error)[:700])
        return

    if not questions:
        st.error("Gemini AI did not return any questions.")
        return

    st.session_state.mcq_questions = questions
    st.session_state.mcq_category = category
    st.session_state.mcq_source = "Gemini AI – Live Generated"

    st.session_state.mcq_attempt += 1
    st.session_state.mcq_result = None
    st.session_state.mcq_ai_analysis = None
    st.session_state.mcq_submitted = False

    history = st.session_state.mcq_history.get(category, [])

    for question in questions:
        question_text = question["question"]

        if question_text not in history:
            history.append(question_text)

    st.session_state.mcq_history[category] = history


# =========================================================
# LOCAL PERFORMANCE REPORT
# =========================================================

def generate_local_performance_report(result):

    questions = result["questions"]
    answers = result["answers"]

    correct = []
    incorrect = []

    for index, question in enumerate(questions):

        selected = answers[index]
        correct_answer = question["answer"]

        if selected == correct_answer:
            correct.append(question)

        else:
            incorrect.append({
                "question": question["question"],
                "your_answer": selected,
                "correct_answer": correct_answer,
                "explanation": question["explanation"]
            })

    total = len(questions)
    score = result["score"]

    percentage = (
        round((score / total) * 100, 1)
        if total else 0
    )

    if percentage >= 80:
        performance = "Strong performance"

    elif percentage >= 60:
        performance = "Good effort, but revision is needed"

    elif percentage >= 40:
        performance = "Developing understanding"

    else:
        performance = "Needs focused practice"

    report = f"""
# CAREERIQ AI – Performance Report

## Test Summary

Subject: {result['category']}
Score: {score}/{total}
Percentage: {percentage}%
Assessment: {performance}

## Correct Answers

You answered {len(correct)} questions correctly.

"""

    if correct:

        for index, question in enumerate(correct, start=1):
            report += f"""
{index}. {question['question']}
Correct answer: {question['answer']}
"""

    else:
        report += "\nNo correct answers in this attempt.\n"

    report += f"""

## Questions to Revise

You answered {len(incorrect)} questions incorrectly.

"""

    if incorrect:

        for index, item in enumerate(incorrect, start=1):
            report += f"""
### {index}. {item['question']}

Your answer: {item['your_answer']}
Correct answer: {item['correct_answer']}

Explanation: {item['explanation']}

"""

    else:
        report += (
            "Excellent! No incorrect answers in this attempt.\n"
        )

    report += """
## Suggested 7-Day Improvement Plan

Day 1: Revise the concepts behind your incorrect answers.

Day 2: Practice basic questions from this subject.

Day 3: Solve medium-level interview questions.

Day 4: Review important definitions and syntax.

Day 5: Practice practical, scenario-based questions.

Day 6: Attempt a fresh 10-question mock test.

Day 7: Review mistakes and attempt another mock test.

## Important Note

This is a rule-based report generated from your test answers.
It is not a prediction of job selection or interview success.
"""

    return report


# =========================================================
# AI PERFORMANCE ANALYSIS
# =========================================================

def generate_mcq_performance_analysis(result):

    category = result["category"]
    score = result["score"]
    questions = result["questions"]
    answers = result["answers"]

    review = []

    for index, item in enumerate(questions):

        user_answer = answers[index]
        correct_answer = item["answer"]

        review.append({
            "question": item["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": user_answer == correct_answer,
            "explanation": item["explanation"]
        })

    prompt = f"""
You are a senior interviewer and learning performance analyst.

Analyze this candidate's MCQ test.

Subject: {category}
Score: {score}/{len(questions)}

Question-wise results:
{json.dumps(review, indent=2)}

Write a detailed report in simple English with these sections:

1. Overall performance assessment.
2. Strong concepts supported by correct answers.
3. Weak concepts supported by incorrect answers.
4. Explain why the candidate may be struggling.
5. Important concepts to revise.
6. A personalized 7-day improvement plan.
7. Five practical practice recommendations.

Rules:
- Use only evidence from the questions and answers.
- Do not invent unsupported topics.
- Do not claim mastery based on one question.
- Be honest and constructive.
- Do not predict job selection.
- Mention this is an assessment of this test attempt.
"""

    try:
        return call_gemini(prompt), "Gemini AI"

    except Exception:
        return (
            generate_local_performance_report(result),
            "Rule-Based Analysis"
        )


# =========================================================
# SUBMIT MCQ TEST + SAVE CAREER ANALYTICS
# =========================================================

def submit_mcq_test(questions, category):

    answers = []
    score = 0

    for index, question in enumerate(questions):

        selected = st.session_state.get(
            f"mcq_answer_{st.session_state.mcq_attempt}_{index}"
        )

        answers.append(selected)

        if selected == question["answer"]:
            score += 1

    total = len(questions)

    percentage = (
        round((score / total) * 100, 1)
        if total else 0
    )

    result = {
        "category": category,
        "score": score,
        "total": total,
        "percentage": percentage,
        "questions": questions,
        "answers": answers,
        "attempt": st.session_state.mcq_attempt
    }

    st.session_state.mcq_result = result
    st.session_state.mcq_submitted = True
    st.session_state.mcq_ai_analysis = None

    history = st.session_state.mcq_attempt_history

    history.append({
        "category": category,
        "attempt": st.session_state.mcq_attempt,
        "score": score,
        "total": total,
        "percentage": percentage
    })

    st.session_state.mcq_attempt_history = history

    try:

        save_analytics_event(
            event_type="interview_mcq",
            score=percentage,
            details={
                "category": category,
                "attempt": st.session_state.mcq_attempt,
                "score": score,
                "total": total,
                "percentage": percentage,
                "correct_answers": score,
                "incorrect_answers": total - score,
                "question_source": st.session_state.get(
                    "mcq_source", "Unknown"
                )
            }
        )

        st.session_state["mcq_analytics_saved"] = True

    except Exception as analytics_error:

        st.session_state["mcq_analytics_saved"] = False
        st.session_state["mcq_analytics_error"] = str(
            analytics_error
        )
        # =========================================================
# DISPLAY MCQ RESULTS
# =========================================================

def display_mcq_results():

    result = st.session_state.mcq_result

    if not result:
        return

    questions = result["questions"]
    answers = result["answers"]
    score = result["score"]
    total = result["total"]
    percentage = result["percentage"]
    category = result["category"]

    correct_count = score
    incorrect_count = total - score

    st.divider()

    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#713F18,#E98B2A,#F2C14E);
        padding:25px;
        border-radius:18px;
        color:white;
        margin-bottom:20px;
    ">
        <div style="font-size:14px;letter-spacing:2px;">
            CAREERIQ AI | PERFORMANCE CENTER
        </div>
        <div style="font-size:30px;font-weight:800;margin-top:8px;">
            Your Interview Performance
        </div>
        <div style="font-size:15px;margin-top:5px;">
            Your results, strengths and improvement journey.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {category} Assessment")
    st.caption(
        f"Attempt {result['attempt']} | Your actual test results"
    )

    if st.session_state.get("mcq_analytics_saved"):
        st.caption(
            "This interview attempt has been saved to Career Analytics history."
        )

    elif st.session_state.get("mcq_analytics_error"):
        st.warning(
            "Interview result is available, but analytics history could not be saved."
        )

    # SCORE CARDS

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Overall Score", f"{percentage}%")

    with c2:
        st.metric("Correct Answers", correct_count)

    with c3:
        st.metric("Incorrect Answers", incorrect_count)

    with c4:
        st.metric("Total Questions", total)

    # PERFORMANCE STATUS

    if percentage >= 80:
        status = "Excellent Performance"
        status_message = (
            "Great work! Keep practicing to maintain your performance."
        )

    elif percentage >= 60:
        status = "Good Performance"
        status_message = (
            "Good progress. Revise your incorrect answers to improve."
        )

    elif percentage >= 40:
        status = "Developing Performance"
        status_message = (
            "Focus on fundamentals and regular practice."
        )

    else:
        status = "Needs More Practice"
        status_message = (
            "Start with basic concepts and build your understanding."
        )

    st.success(f"**{status}** — {status_message}")

        # PERFORMANCE ANALYTICS

    st.divider()
    st.markdown("## Performance Analytics")

    chart_col1, chart_col2 = st.columns(2)

    # -----------------------------------------
    # ANSWER DISTRIBUTION
    # -----------------------------------------

    with chart_col1:

        st.markdown("#### Answer Distribution")

        answer_data = {
            "Answer": ["Correct", "Incorrect"],
            "Count": [
                int(correct_count),
                int(incorrect_count)
            ]
        }

        st.bar_chart(
            answer_data,
            x="Answer",
            y="Count",
            color="#269B70",
            height=350
        )

        st.caption(
            f"Correct: {correct_count} | "
            f"Incorrect: {incorrect_count}"
        )

    # -----------------------------------------
    # QUESTION-WISE PERFORMANCE
    # -----------------------------------------

    with chart_col2:

        st.markdown("#### Question-wise Performance")

        question_data = []

        for index, question in enumerate(questions):

            is_correct = (
                answers[index] == question["answer"]
            )

            question_data.append({
                "Question": f"Q{index + 1}",
                "Score": 1 if is_correct else 0
            })

        st.bar_chart(
            question_data,
            x="Question",
            y="Score",
            color="#E98B2A",
            height=350
        )

        st.caption(
            "1 = Correct Answer | 0 = Incorrect Answer"
        )

    # -----------------------------------------
    # LEARNING PROGRESS
    # -----------------------------------------

    st.divider()
    st.markdown("## Learning Progress")

    history = [
        item
        for item in st.session_state.mcq_attempt_history
        if item["category"] == category
    ]

    if history:

        trend_data = {
            "Attempt": [
                f"Attempt {item['attempt']}"
                for item in history
            ],
            "Percentage": [
                float(item["percentage"])
                for item in history
            ]
        }

        st.bar_chart(
            trend_data,
            x="Attempt",
            y="Percentage",
            color="#E98B2A",
            height=350
        )

        st.markdown("#### Recent Attempts")

        for item in history[-5:][::-1]:

            st.write(
                f"Attempt {item['attempt']}: "
                f"{item['score']}/{item['total']} "
                f"({item['percentage']}%)"
            )

    else:

        st.info(
            "Complete an MCQ test to view your learning progress."
        )

    # STRONG AND WEAK ANSWERS

    st.divider()
    st.markdown("## Strengths & Areas to Improve")

    strong_col, weak_col = st.columns(2)

    with strong_col:
        st.markdown("### Strong Answers")

        for index, question in enumerate(questions):

            if answers[index] == question["answer"]:
                st.success(
                    f"Q{index + 1}: {question['question']}"
                )

    with weak_col:
        st.markdown("### Needs Improvement")

        for index, question in enumerate(questions):

            if answers[index] != question["answer"]:
                st.error(
                    f"Q{index + 1}: {question['question']}"
                )

    # QUESTION-WISE REVIEW

    st.divider()
    st.markdown("## Detailed Answer Review")

    for index, question in enumerate(questions):

        selected = answers[index]
        correct_answer = question["answer"]

        with st.expander(
            f"Question {index + 1}: {question['question']}"
        ):

            if selected == correct_answer:
                st.success("Correct Answer")
            else:
                st.error("Incorrect Answer")

            st.write(
                "**Your Answer:**",
                selected or "Not answered"
            )

            st.write(
                "**Correct Answer:**",
                correct_answer
            )

            st.info(question["explanation"])

    # AI PERFORMANCE REPORT

    st.divider()

    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#34477D,#5268A5);
        padding:20px;
        border-radius:15px;
        color:white;
    ">
        <div style="font-size:13px;letter-spacing:1px;">
            CAREERIQ AI INTELLIGENCE
        </div>
        <div style="font-size:24px;font-weight:800;margin-top:6px;">
            Personalized AI Performance Report
        </div>
        <div style="font-size:14px;margin-top:5px;">
            Discover your improvement areas and get a learning plan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Generate My AI Performance Report",
        key=f"analysis_{category}_{result['attempt']}",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing your answers and preparing your report..."
        ):

            report, report_source = (
                generate_mcq_performance_analysis(result)
            )

            st.session_state.mcq_ai_analysis = report
            st.session_state.mcq_analysis_source = report_source

    if st.session_state.mcq_ai_analysis:

        st.caption(
            "Report Source: "
            + st.session_state.get(
                "mcq_analysis_source",
                "Rule-Based Analysis"
            )
        )

        st.markdown(st.session_state.mcq_ai_analysis)

        st.download_button(
            "Download Performance Report",
            data=st.session_state.mcq_ai_analysis,
            file_name=(
                f"CAREERIQ_{category}_Performance_Report.txt"
            ),
            mime="text/plain",
            key=f"download_{result['attempt']}",
            use_container_width=True
        )

    # RETAKE TEST

    st.divider()

    if st.button(
        "Retake Test – Generate Fresh Questions",
        key=f"retake_{result['attempt']}",
        use_container_width=True
    ):
        create_new_mcq_test(category)
        st.rerun()
        # =========================================================
# MULTI-DOMAIN OPTIONS
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
# DOMAIN-WISE JOB ROLES
# =========================================================

DOMAIN_ROLE_MAP = {

    "Data Analytics & Business Intelligence": [
        "Data Analyst",
        "Business Analyst",
        "Power BI Developer",
        "SQL Developer",
        "MIS Analyst",
        "BI Analyst"
    ],

    "Data Science & AI / Machine Learning": [
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Junior Data Scientist",
        "NLP Engineer"
    ],

    "Cloud Computing & DevOps": [
        "Cloud Engineer",
        "AWS Cloud Associate",
        "Azure Administrator",
        "DevOps Engineer",
        "Cloud Support Associate"
    ],

    "Full Stack & Software Development": [
        "Python Developer",
        "Java Developer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Software Engineer"
    ],

    "Networking & Cybersecurity": [
        "Network Engineer",
        "Cybersecurity Analyst",
        "SOC Analyst",
        "Network Support Engineer",
        "Security Analyst"
    ],

    "Quality Assurance & Testing": [
        "QA Engineer",
        "Manual Tester",
        "Automation Tester",
        "Software Test Engineer"
    ],

    "UI/UX Design": [
        "UI Designer",
        "UX Designer",
        "Product Designer",
        "UI/UX Designer"
    ],

    "Digital Marketing": [
        "Digital Marketing Executive",
        "SEO Analyst",
        "Social Media Executive",
        "Performance Marketing Associate"
    ],

    "Finance & Accounting": [
        "Accounts Assistant",
        "Financial Analyst",
        "Junior Accountant",
        "Finance Associate"
    ],

    "Human Resources": [
        "HR Executive",
        "Talent Acquisition Associate",
        "Recruitment Coordinator",
        "HR Generalist"
    ],

    "Business & Project Management": [
        "Project Coordinator",
        "Business Operations Associate",
        "Project Analyst",
        "Management Trainee"
    ],

    "Other Technical & Non-Technical Roles": [
        "Customer Success Associate",
        "Operations Associate",
        "Technical Support Executive",
        "Research Associate",
        "General Entry-Level Professional"
    ]
}


ALL_DOMAIN_ROLES = sorted({
    role
    for roles in DOMAIN_ROLE_MAP.values()
    for role in roles
})


def get_roles_for_domain(domain):

    if domain == "All Relevant Domains":
        return ALL_DOMAIN_ROLES

    return DOMAIN_ROLE_MAP.get(
        domain,
        ["General Entry-Level Professional"]
    )


# =========================================================
# GEMINI AI – TECHNICAL INTERVIEW QUESTIONS
# =========================================================

def generate_ai_interview_questions(
    domain,
    role,
    level,
    count=5
):

    prompt = f"""
You are a professional interviewer and assessment designer.

Generate exactly {count} original interview questions for:

Domain: {domain}
Target job role: {role}
Candidate level: {level}

Question mix:
- 2 foundational or conceptual questions
- 2 practical or job-task questions
- 1 realistic scenario-based question

IMPORTANT RULES:

- Every question must be directly relevant to the selected domain and role.
- Do not generate Data Analyst questions unless that is the selected role.
- Match the selected experience level.
- Questions must be clear, specific and realistic.
- Avoid duplicate or generic questions.
- Use simple professional English.
- Include practical situations from real job responsibilities.
- Do not ask questions unrelated to the selected role.

Return ONLY a valid JSON array containing exactly {count} strings.

Example:
[
    "Question 1?",
    "Question 2?",
    "Question 3?",
    "Question 4?",
    "Question 5?"
]
"""

    questions = extract_json(call_gemini(prompt))

    if not isinstance(questions, list) or len(questions) != count:
        raise ValueError(
            f"Gemini did not generate exactly {count} interview questions."
        )

    if not all(
        isinstance(q, str) and q.strip()
        for q in questions
    ):
        raise ValueError(
            "Gemini returned an invalid interview question."
        )

    return questions


# =========================================================
# GEMINI AI – HR QUESTIONS
# =========================================================

def generate_ai_hr_questions(
    domain,
    role,
    level,
    count=6
):

    prompt = f"""
Act as an experienced HR interviewer.

Domain: {domain}
Target role: {role}
Candidate level: {level}

Generate exactly {count} fresh HR and behavioral questions.

Cover:
- Self-introduction
- Career motivation
- Strengths and weaknesses
- Learning ability
- Teamwork
- Communication
- Handling challenges
- Role-specific motivation

Rules:
- Questions must suit the selected job role.
- Do not assume the candidate is applying for a Data Analyst position.
- Avoid duplicate questions.
- Keep questions suitable for the selected experience level.
- Use simple professional English.

Return ONLY a valid JSON array of exactly {count} strings.
"""

    questions = extract_json(call_gemini(prompt))

    if not isinstance(questions, list) or len(questions) != count:
        raise ValueError(
            f"Gemini did not generate exactly {count} HR questions."
        )

    if not all(
        isinstance(q, str) and q.strip()
        for q in questions
    ):
        raise ValueError(
            "Gemini returned an invalid HR question."
        )

    return questions


# =========================================================
# AI TECHNICAL ANSWER EVALUATION
# =========================================================

def evaluate_ai_interview(
    category,
    questions,
    answers
):

    prompt = f"""
Act as a senior interviewer for:

{category}

Evaluate this fresher / entry-level candidate's answers:

{json.dumps([
    {
        "question": q,
        "answer": answers.get(str(i), "")
    }
    for i, q in enumerate(questions)
], indent=2)}

Give a detailed report with these sections:

1. Overall feedback.
2. Strengths supported by the answers.
3. Areas to improve.
4. Technical or role-related accuracy.
5. Communication feedback.
6. Suggested improvements.
7. Sample answer guidance.
8. A short preparation plan.

Rules:
- Evaluate according to the selected job role.
- Do not use Data Analyst standards for unrelated domains.
- Be honest and constructive.
- Use simple English.
- Do not predict job selection.
- Do not give unsupported scores.
"""

    return call_gemini(prompt)


# =========================================================
# AI HR ANSWER EVALUATION
# =========================================================

def evaluate_hr_answers(
    answers,
    domain,
    role
):

    prompt = f"""
Act as an experienced HR interviewer.

Domain: {domain}
Target Job Role: {role}

Evaluate these candidate answers:

{json.dumps(answers, indent=2)}

Provide:

1. Overall communication assessment.
2. Strengths.
3. Weaknesses and unclear answers.
4. Answer quality and role relevance.
5. Suggestions to improve each answer.
6. A professional sample answer for the weakest response.
7. Final HR preparation suggestions.

Rules:
- Use simple English.
- Be constructive and realistic.
- Consider the selected job role.
- Do not predict job selection.
"""

    return call_gemini(prompt)
    # =========================================================
# MAIN PAGE HEADER
# =========================================================

st.markdown(
    '<div class="main-title">AI Interview Simulation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Practice technical interviews, test your knowledge and improve '
    'your interview performance with CAREERIQ AI.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# INTERVIEW TYPE SELECTION
# =========================================================

interview_type = st.selectbox(
    "Choose Interview Practice",
    [
        "Technical - Excel",
        "Technical - SQL",
        "Technical - Power BI",
        "Technical - Python",
        "AI Technical Interview",
        "HR Interview Practice"
    ]
)


# =========================================================
# TECHNICAL MCQ TESTS
# =========================================================

technical_categories = {
    "Technical - Excel": "Excel",
    "Technical - SQL": "SQL",
    "Technical - Power BI": "Power BI",
    "Technical - Python": "Python"
}


if interview_type in technical_categories:

    category = technical_categories[interview_type]

    st.markdown("### " + category + " Assessment")

    st.write(
        "Attempt 10 multiple-choice questions. "
        "Gemini AI will generate questions for your selected subject. "
        "Submit your answers to see your score and explanations."
    )

    if not st.session_state.mcq_questions or (
        st.session_state.mcq_category != category
    ):

        if st.button(
            f"Start {category} Test",
            key=f"start_{category}"
        ):
            create_new_mcq_test(category)
            st.rerun()

    if (
        st.session_state.mcq_questions
        and st.session_state.mcq_category == category
    ):

        source = st.session_state.mcq_source or "Unknown"

        st.markdown(
            f'<div class="source-label">'
            f'Question Source: {source}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.caption(
            f"Attempt number: {st.session_state.mcq_attempt}"
        )

        questions = st.session_state.mcq_questions

        if not st.session_state.mcq_submitted:

            with st.form(
                key=(
                    f"mcq_form_{category}_"
                    f"{st.session_state.mcq_attempt}"
                )
            ):

                for index, question in enumerate(questions):

                    st.markdown(
                        f"**Q{index + 1}. {question['question']}**"
                    )

                    st.radio(
                        "Select your answer:",
                        question["options"],
                        index=None,
                        key=(
                            f"mcq_answer_"
                            f"{st.session_state.mcq_attempt}_{index}"
                        )
                    )

                    st.write("")

                submitted = st.form_submit_button(
                    "Submit Test",
                    use_container_width=True
                )

            if submitted:
                submit_mcq_test(questions, category)
                st.rerun()

        else:
            display_mcq_results()


# =========================================================
# AI TECHNICAL INTERVIEW SECTION
# =========================================================

elif interview_type == "AI Technical Interview":

    st.subheader("AI-Generated Technical Interview")

    st.write(
        "Select your domain and target role. "
        "Gemini AI will create fresh, role-specific questions."
    )

    domain = st.selectbox(
        "Select your domain",
        DOMAIN_OPTIONS,
        key="ai_interview_domain"
    )

    role = st.selectbox(
        "Select your target job role",
        get_roles_for_domain(domain),
        key="ai_interview_role"
    )

    level = st.selectbox(
        "Select your experience level",
        [
            "Fresher / Entry-Level",
            "0–1 Year",
            "1–2 Years",
            "Intermediate"
        ],
        key="ai_interview_level"
    )

    if st.button(
        "Generate AI Interview Questions",
        key="generate_domain_interview",
        use_container_width=True
    ):

        with st.spinner(
            "Gemini AI is creating your role-specific questions..."
        ):

            try:

                questions = generate_ai_interview_questions(
                    domain,
                    role,
                    level,
                    5
                )

                st.session_state.ai_questions = questions

                st.session_state.ai_category = (
                    f"{domain} | {role} | {level}"
                )

                st.session_state.ai_domain = domain
                st.session_state.ai_role = role
                st.session_state.ai_level = level

                st.session_state.ai_feedback = None
                st.session_state.ai_answers = {}

                st.session_state.ai_question_set_id = (
                    st.session_state.get(
                        "ai_question_set_id", 0
                    ) + 1
                )

            except Exception as error:

                st.error(
                    "Gemini AI could not generate interview questions."
                )

                st.caption(
                    "Check the Gemini API key, quota and model access, "
                    "then try again."
                )

                st.code(str(error)[:500])

    # DISPLAY AI QUESTIONS

    if st.session_state.ai_questions:

        st.success(
            "AI-generated questions for "
            f"{st.session_state.get('ai_role', 'your selected role')} "
            "are ready."
        )

        st.caption(
            "Question source: Gemini AI live generation"
        )

        set_id = st.session_state.get(
            "ai_question_set_id", 1
        )

        with st.form(f"ai_interview_form_{set_id}"):

            answers = {}

            for index, question in enumerate(
                st.session_state.ai_questions
            ):

                st.markdown(
                    f"**Q{index + 1}. {question}**"
                )

                answers[str(index)] = st.text_area(
                    "Your answer",
                    key=f"ai_interview_answer_{set_id}_{index}",
                    height=110
                )

            evaluate = st.form_submit_button(
                "Submit My Answers for AI Evaluation",
                use_container_width=True
            )

        if evaluate:

            with st.spinner(
                "AI is evaluating your answers..."
            ):

                try:

                    feedback = evaluate_ai_interview(
                        st.session_state.ai_category,
                        st.session_state.ai_questions,
                        answers
                    )

                    st.session_state.ai_feedback = feedback
                    st.session_state.ai_answers = answers

                except Exception as error:

                    st.error(
                        "AI evaluation is temporarily unavailable."
                    )

                    st.code(str(error)[:400])

        if st.session_state.ai_feedback:

            st.divider()

            st.subheader("AI Interview Feedback")

            st.markdown(
                st.session_state.ai_feedback
            )

    st.divider()

    st.caption(
        "Generate another set to practice with a fresh batch "
        "of AI-created questions."
    )


# =========================================================
# AI-GENERATED HR INTERVIEW PRACTICE
# =========================================================

elif interview_type == "HR Interview Practice":

    st.subheader("AI-Generated HR Interview Practice")

    st.write(
        "Gemini AI creates HR and behavioral questions "
        "for your selected domain and job role."
    )

    hr_domain = st.selectbox(
        "Select your domain",
        DOMAIN_OPTIONS,
        key="hr_interview_domain"
    )

    hr_role = st.selectbox(
        "Select your target job role",
        get_roles_for_domain(hr_domain),
        key="hr_interview_role"
    )

    hr_level = st.selectbox(
        "Select your experience level",
        [
            "Fresher / Entry-Level",
            "0–1 Year",
            "1–2 Years",
            "Intermediate"
        ],
        key="hr_interview_level"
    )

    if st.button(
        "Generate AI HR Questions",
        key="generate_ai_hr_questions",
        use_container_width=True
    ):

        with st.spinner(
            "Gemini AI is preparing your HR interview..."
        ):

            try:

                questions = generate_ai_hr_questions(
                    hr_domain,
                    hr_role,
                    hr_level,
                    6
                )

                st.session_state.hr_questions = questions

                st.session_state.hr_category = (
                    f"{hr_domain} | {hr_role}"
                )

                st.session_state.hr_feedback = None
                st.session_state.hr_answers = {}

                st.session_state.hr_question_set_id = (
                    st.session_state.get(
                        "hr_question_set_id", 0
                    ) + 1
                )

            except Exception as error:

                st.error(
                    "Gemini AI could not generate HR questions."
                )

                st.caption(
                    "Check the Gemini API key, quota and model access, "
                    "then try again."
                )

                st.code(str(error)[:500])

    # DISPLAY AI HR QUESTIONS

    if st.session_state.hr_questions:

        st.success(
            "Your AI-generated HR questions are ready."
        )

        st.caption(
            "Question source: Gemini AI live generation"
        )

        set_id = st.session_state.get(
            "hr_question_set_id", 1
        )

        with st.form(f"hr_interview_form_{set_id}"):

            hr_answers = {}

            for index, question in enumerate(
                st.session_state.hr_questions
            ):

                st.markdown(
                    f"**Q{index + 1}. {question}**"
                )

                hr_answers[question] = st.text_area(
                    "Your answer",
                    key=f"hr_answer_{set_id}_{index}",
                    height=100
                )

            submitted = st.form_submit_button(
                "Evaluate My HR Answers",
                use_container_width=True
            )

        if submitted:

            with st.spinner(
                "AI is reviewing your HR answers..."
            ):

                try:

                    feedback = evaluate_hr_answers(
                        hr_answers,
                        hr_domain,
                        hr_role
                    )

                    st.session_state.hr_feedback = feedback
                    st.session_state.hr_answers = hr_answers

                except Exception as error:

                    st.error(
                        "HR evaluation is temporarily unavailable."
                    )

                    st.code(str(error)[:400])

        if st.session_state.hr_feedback:

            st.divider()

            st.subheader("Your AI HR Interview Feedback")

            st.markdown(
                st.session_state.hr_feedback
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CAREERIQ AI | Practice. Analyze. Improve. "
    "| AI-powered interview preparation across multiple career domains."
)


# =========================================================
# BACK TO HOME
# =========================================================

if st.button(
    "← Back to Home",
    key="interview_page_back_home",
    use_container_width=True
):

    st.switch_page("app.py")