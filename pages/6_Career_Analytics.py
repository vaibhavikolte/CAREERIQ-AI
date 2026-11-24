import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import html
import json
from datetime import date, timedelta

from modules.career_analytics_store import get_analytics_data


st.set_page_config(
    page_title="CareerIQ | Analytics",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PREMIUM DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --espresso: #38251F;
    --coffee: #59402F;
    --gold: #D5AD70;
    --gold-light: #EBD3A9;
    --ivory: #F8F1E7;
    --white: #FFFCF7;
    --ink: #3E2D24;
    --muted: #958271;
    --border: #E9DCCD;
    --sage: #849779;
    --terracotta: #B97C65;
}

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: var(--ivory);
    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

/* PAGE WIDTH */

.block-container {
    max-width: 100% !important;
    padding: 1.1rem 1.25rem 1.5rem !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

div[data-testid="stHorizontalBlock"] {
    gap: 0.8rem;
    align-items: stretch;
}

div[data-testid="column"] {
    min-width: 0 !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #38251F 0%,
        #493326 55%,
        #604431 100%
    );
    border-right: 1px solid #75573E;
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

section[data-testid="stSidebar"] * {
    color: #FFF2DF;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #E6BD7F;
    padding: 12px 5px 3px;
}

.brand span {
    color: #FFF5E8;
}

.brand-sub {
    color: #C9AD8E;
    font-size: 9px;
    letter-spacing: 2px;
    margin: 0 5px 30px;
}

.sidebar-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #DDBD8D;
    margin: 20px 5px 10px;
}

.sidebar-current {
    background: linear-gradient(110deg, #D5AD70, #EBD3A9);
    color: #38251F !important;
    border-radius: 11px;
    padding: 12px;
    font-weight: 800;
    font-size: 12px;
    margin-bottom: 12px;
}

.sidebar-current * {
    color: #38251F !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
    border-radius: 9px;
    padding: 9px 10px;
    color: #F7E8D5 !important;
    font-size: 12px;
    font-weight: 600;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background: rgba(255, 236, 205, .12);
}

.growth-card {
    background: linear-gradient(145deg, #E7C58F, #C7975D);
    border: 1px solid #EFD6AD;
    border-radius: 15px;
    padding: 16px;
    margin-top: 28px;
    color: #38251F;
}

.growth-small {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: #67482C;
}

.growth-heading {
    font-size: 18px;
    font-weight: 800;
    margin-top: 10px;
    color: #38251F;
}

.growth-description {
    font-size: 10px;
    line-height: 1.6;
    margin-top: 6px;
    color: #624A34;
}

/* HEADER */

.topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 3px 0 10px;
}

.topline-tag {
    color: #A27B4F;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.page-heading {
    font-size: 29px;
    line-height: 1.2;
    font-weight: 800;
    color: #3C291F;
    letter-spacing: -1px;
}

.page-description {
    font-size: 12px;
    color: #998572;
    margin-top: 4px;
}

.section-heading {
    font-size: 16px;
    font-weight: 800;
    color: #493326;
    margin: 9px 0 5px;
}

/* CARDS */

.surface {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 5px 18px rgba(67, 45, 31, .045);
}

.surface-heading {
    color: #513B2C;
    font-size: 13px;
    font-weight: 800;
}

.surface-description {
    color: #A08E7D;
    font-size: 10px;
    margin-top: 4px;
}

/* KPI */

.kpi-card {
    background: #FFFCF7;
    border: 1px solid #E8D9C8;
    border-radius: 15px;
    padding: 13px;
    min-width: 0;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(67,45,31,.045);
}

.kpi-label {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #816A55;
    font-size: 10px;
    font-weight: 700;
    min-width: 0;
}

.kpi-symbol {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 27px;
    height: 27px;
    border-radius: 9px;
    background: #F0E2CC;
    color: #91683C;
    font-size: 13px;
    font-weight: 800;
}

.kpi-value {
    font-size: 25px;
    font-weight: 800;
    color: #3E2C21;
    margin-top: 10px;
}

.kpi-note {
    color: #A18E7D;
    font-size: 9px;
    margin-top: 3px;
}

.kpi-progress {
    height: 5px;
    background: #F0E9DF;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 11px;
}

.kpi-progress-fill {
    height: 100%;
    border-radius: 20px;
}

/* FILTERS */

div[data-testid="stSelectbox"] label {
    color: #836D59;
    font-size: 11px;
    font-weight: 700;
}

div[data-testid="stSelectbox"] > div > div {
    background: #FFFCF7;
    border: 1px solid #E4D4C2;
    border-radius: 10px;
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(110deg, #60442F, #916A43);
    border: 1px solid #A27A4F;
    color: #FFF9F0;
    border-radius: 10px;
    min-height: 40px;
    font-size: 11px;
    font-weight: 700;
}

.stButton > button:hover {
    background: #38251F;
    color: white;
    border-color: #D5AD70;
}

/* METRICS */

div[data-testid="stMetric"] {
    background: #FFFCF7;
    border: 1px solid #E8D9C8;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 4px 14px rgba(67,45,31,.04);
}

div[data-testid="stMetricLabel"] {
    color: #917B66;
    font-size: 11px;
}

div[data-testid="stMetricValue"] {
    color: #493326;
    font-weight: 800;
}

/* PLOTLY */

div[data-testid="stPlotlyChart"] {
    width: 100% !important;
    max-width: 100% !important;
    overflow: hidden !important;
}

/* TABLE */

div[data-testid="stDataFrame"] {
    border: 1px solid #E9DCCD;
    border-radius: 12px;
    overflow: hidden;
}

/* SKILLS */

.skill-chip {
    display: inline-block;
    border-radius: 20px;
    padding: 6px 10px;
    margin: 4px 4px 4px 0;
    font-size: 10px;
    font-weight: 600;
}

/* EMPTY STATE */

.empty-state {
    text-align: center;
    background: #FFFCF7;
    border: 1px dashed #D9C4A9;
    border-radius: 14px;
    padding: 24px 15px;
    color: #917B66;
    font-size: 11px;
}

/* FOOTER */

.footer {
    border-top: 1px solid #E8D9C8;
    padding-top: 12px;
    margin-top: 20px;
    color: #A08D7B;
    font-size: 9px;
    text-align: center;
}

/* RESPONSIVE */

@media (max-width: 900px) {
    .block-container {
        padding: 0.7rem !important;
    }

    .page-heading {
        font-size: 23px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================

def safe_details(value):
    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}

    return {}


def safe_latest_score(data):
    if data.empty:
        return None

    values = data["score"].dropna()

    if values.empty:
        return None

    return float(values.iloc[-1])


def score_text(value):
    return "—" if value is None else f"{value:.1f}%"


def make_kpi(title, value, note, percentage, color, symbol):
    percentage = max(0, min(100, float(percentage)))

    return f"""
    <div class="kpi-card">
        <div class="kpi-label">
            <div class="kpi-symbol">{symbol}</div>
            <span>{html.escape(title)}</span>
        </div>
        <div class="kpi-value">{html.escape(str(value))}</div>
        <div class="kpi-note">{html.escape(note)}</div>
        <div class="kpi-progress">
            <div class="kpi-progress-fill"
                 style="width:{percentage}%;background:{color};">
            </div>
        </div>
    </div>
    """


def show_empty(message):
    st.markdown(
        f'<div class="empty-state">{html.escape(message)}</div>',
        unsafe_allow_html=True
    )


def chart_layout(fig, height=300):
    fig.update_layout(
        height=height,
        autosize=True,
        margin=dict(l=12, r=12, t=18, b=18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans",
            size=10,
            color="#927D69"
        )
    )
    return fig


# =========================================================
# LOAD DATA
# =========================================================

try:
    records = get_analytics_data()

    df = pd.DataFrame(records)

except Exception as error:
    st.error(f"Could not load analytics data: {error}")
    st.stop()


required_columns = [
    "created_at",
    "score",
    "details",
    "event_type"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Analytics data is missing required fields: "
        + ", ".join(missing_columns)
    )
    st.stop()


df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

df["score"] = pd.to_numeric(
    df["score"],
    errors="coerce"
)

df["details"] = df["details"].apply(safe_details)

df = df.dropna(subset=["created_at"]).copy()
df = df.sort_values("created_at")


event_labels = {
    "resume_analysis": "Resume Analysis",
    "resume_jd_match": "Resume Job Match",
    "advanced_job_match": "Job Intelligence",
    "interview_mcq": "Interview Simulation"
}

df["activity_name"] = (
    df["event_type"].astype(str).map(event_labels)
    .fillna(df["event_type"].astype(str))
)
# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">CAREER<span>IQ</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-sub">AI CAREER INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-current">◈ &nbsp; Analytics Overview</div>',
        unsafe_allow_html=True
    )

    st.page_link("app.py", label="⌂  Home")

    st.page_link(
        "pages/1_Resume_Intelligence.py",
        label="▤  Resume Intelligence"
    )

    st.page_link(
        "pages/2_ATS_Job_Intelligence.py",
        label="▣  Job Intelligence"
    )

    st.page_link(
        "pages/3_AI_Career_Agent.py",
        label="✦  Career Agent"
    )

    st.page_link(
        "pages/4_AI_Interview_Simulation.py",
        label="◉  Interview Simulation"
    )

    st.page_link(
        "pages/5_Resume_Builder.py",
        label="▤  Resume Builder"
    )

    st.markdown(
        '<div class="sidebar-label">YOUR PROGRESS</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="growth-card">
        <div class="growth-small">CAREER GROWTH</div>
        <div class="growth-heading">Keep moving forward.</div>
        <div class="growth-description">
            Track your skills, understand your performance
            and prepare for your next career opportunity.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# MAIN PAGE
# =========================================================

st.markdown("""
<div class="topline">
    <div class="topline-tag">CAREER INTELLIGENCE / OVERVIEW</div>
</div>
<div class="page-heading">Analytics Overview</div>
<div class="page-description">
    Your career performance, progress and activity at a glance.
</div>
""", unsafe_allow_html=True)


# =========================================================
# FILTERS
# =========================================================

f1, f2, f3, f4 = st.columns([1, 1, 1, 0.75])

with f1:
    date_filter = st.selectbox(
        "Date Range",
        ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"]
    )

with f2:
    activity_filter = st.selectbox(
        "Activity",
        [
            "All Activities",
            "Resume Analysis",
            "Resume Job Match",
            "Job Intelligence",
            "Interview Simulation"
        ]
    )

with f3:
    chart_period = st.selectbox(
        "Chart View",
        ["Weekly", "Monthly"]
    )

with f4:
    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

    if st.button("↻  Refresh Data", use_container_width=True):
        st.rerun()


# =========================================================
# FILTER DATA
# =========================================================

today = date.today()

if date_filter == "Last 7 Days":
    start_date = today - timedelta(days=6)

elif date_filter == "Last 30 Days":
    start_date = today - timedelta(days=29)

elif date_filter == "Last 90 Days":
    start_date = today - timedelta(days=89)

else:
    start_date = df["created_at"].min().date()


filtered = df[
    (df["created_at"].dt.date >= start_date) &
    (df["created_at"].dt.date <= today)
].copy()


if activity_filter != "All Activities":
    filtered = filtered[
        filtered["activity_name"] == activity_filter
    ].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

resume_data = filtered[
    filtered["event_type"] == "resume_analysis"
]

jd_data = filtered[
    filtered["event_type"] == "resume_jd_match"
]

job_data = filtered[
    filtered["event_type"] == "advanced_job_match"
]

interview_data = filtered[
    filtered["event_type"] == "interview_mcq"
]

total_activities = len(filtered)
total_resumes = len(resume_data)
total_jobs = len(job_data)
total_interviews = len(interview_data)

latest_resume = safe_latest_score(resume_data)
latest_jd = safe_latest_score(jd_data)
latest_job = safe_latest_score(job_data)
latest_interview = safe_latest_score(interview_data)

activity_share = (
    total_resumes / total_activities * 100
    if total_activities else 0
)

job_share = (
    total_jobs / total_activities * 100
    if total_activities else 0
)

interview_share = (
    total_interviews / total_activities * 100
    if total_activities else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-heading">Your Activity at a Glance</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        make_kpi(
            "Total Activities",
            total_activities,
            "All saved events",
            100 if total_activities else 0,
            "#C49A60",
            "✦"
        ),
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        make_kpi(
            "Resume Analyses",
            total_resumes,
            "Resume intelligence",
            activity_share,
            "#D5AD70",
            "▤"
        ),
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        make_kpi(
            "Job Matches",
            total_jobs,
            "Job intelligence",
            job_share,
            "#849779",
            "⌕"
        ),
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        make_kpi(
            "Interview Tests",
            total_interviews,
            "Interview simulation",
            interview_share,
            "#B97C65",
            "◉"
        ),
        unsafe_allow_html=True
    )


# =========================================================
# CAREER ACTIVITY TRENDS
# =========================================================

st.markdown(
    '<div class="section-heading">Career Performance</div>',
    unsafe_allow_html=True
)

trend_col, score_col = st.columns([1.8, 1])

with trend_col:

    st.markdown("""
    <div class="surface">
        <div class="surface-heading">Career Activity Trends</div>
        <div class="surface-description">
            Track your activity and average score over time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not filtered.empty:

        trend = filtered.copy()

        if chart_period == "Weekly":
            trend["period"] = (
                trend["created_at"].dt.to_period("W").astype(str)
            )
        else:
            trend["period"] = (
                trend["created_at"].dt.to_period("M").astype(str)
            )

        summary = trend.groupby("period").agg(
            activities=("event_type", "count"),
            average_score=("score", "mean")
        ).reset_index()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=summary["period"],
                y=summary["activities"],
                mode="lines+markers",
                name="Activities",
                line=dict(
                    color="#BD9157",
                    width=3,
                    shape="spline"
                ),
                marker=dict(size=8),
                fill="tozeroy",
                fillcolor="rgba(189,145,87,0.12)"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=summary["period"],
                y=summary["average_score"],
                mode="lines+markers",
                name="Average Score",
                line=dict(
                    color="#66503D",
                    width=2,
                    dash="dot"
                ),
                marker=dict(size=6),
                yaxis="y2"
            )
        )

        fig.update_layout(
            yaxis=dict(
                title="Activities",
                showgrid=True,
                gridcolor="#EFE5D9",
                zeroline=False
            ),
            yaxis2=dict(
                title="Score %",
                overlaying="y",
                side="right",
                range=[0, 100],
                showgrid=False
            ),
            xaxis=dict(showgrid=False),
            legend=dict(
                orientation="h",
                y=1.12,
                x=0.2
            )
        )

        chart_layout(fig, 315)

        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False}
        )

    else:
        show_empty("No activity data available for this date range.")


# =========================================================
# PERFORMANCE SNAPSHOT
# =========================================================

with score_col:

    st.markdown("""
    <div class="surface">
        <div class="surface-heading">Performance Snapshot</div>
        <div class="surface-description">
            Your latest recorded scores.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Resume ATS Score", score_text(latest_resume))
    st.metric("Resume JD Match", score_text(latest_jd))
    st.metric("Job Match Score", score_text(latest_job))
    st.metric("Interview Score", score_text(latest_interview))
    # =========================================================
# ACTIVITY INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-heading">Activity Insights</div>',
    unsafe_allow_html=True
)

donut_col, bar_col = st.columns([1, 1.25])


# =========================================================
# DONUT CHART
# =========================================================

with donut_col:

    st.markdown("""
    <div class="surface">
        <div class="surface-heading">Career Activity Mix</div>
        <div class="surface-description">
            Distribution of your feature usage.
        </div>
    </div>
    """, unsafe_allow_html=True)

    activity_counts = filtered["activity_name"].value_counts()

    if not activity_counts.empty:

        donut = go.Figure(
            data=[
                go.Pie(
                    labels=activity_counts.index,
                    values=activity_counts.values,
                    hole=0.70,
                    sort=False,
                    marker=dict(
                        colors=[
                            "#B88B55",
                            "#624532",
                            "#D8B77D",
                            "#B97C65",
                            "#849779"
                        ],
                        line=dict(
                            color="#FFFCF7",
                            width=3
                        )
                    ),
                    textinfo="none",
                    hovertemplate=(
                        "%{label}<br>"
                        "Activities: %{value}<br>"
                        "%{percent}<extra></extra>"
                    )
                )
            ]
        )

        donut.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.08,
                x=0.5,
                xanchor="center",
                font=dict(size=9)
            ),
            annotations=[
                dict(
                    text=str(total_activities),
                    x=0.5,
                    y=0.54,
                    showarrow=False,
                    font=dict(size=24, color="#493326")
                ),
                dict(
                    text="Activities",
                    x=0.5,
                    y=0.41,
                    showarrow=False,
                    font=dict(size=10, color="#958271")
                )
            ]
        )

        chart_layout(donut, 310)

        st.plotly_chart(
            donut,
            width="stretch",
            config={"displayModeBar": False}
        )

    else:
        show_empty("No activity mix available.")


# =========================================================
# FEATURE USAGE BREAKDOWN
# =========================================================

with bar_col:

    st.markdown("""
    <div class="surface">
        <div class="surface-heading">Feature Usage Breakdown</div>
        <div class="surface-description">
            Discover which CAREERIQ AI tools you use most.
        </div>
    </div>
    """, unsafe_allow_html=True)

    feature_counts = (
        filtered["activity_name"]
        .value_counts()
        .sort_values(ascending=True)
    )

    if not feature_counts.empty:

        colors = [
            "#D8B77D",
            "#849779",
            "#B97C65",
            "#624532",
            "#B88B55"
        ]

        bar = go.Figure()

        bar.add_trace(
            go.Bar(
                x=feature_counts.values,
                y=feature_counts.index,
                orientation="h",
                marker=dict(
                    color=colors[:len(feature_counts)],
                    line=dict(width=0)
                ),
                text=feature_counts.values,
                textposition="inside",
                insidetextanchor="middle",
                cliponaxis=True,
                textfont=dict(
                    color="#FFFFFF",
                    size=10
                ),
                hovertemplate=(
                    "%{y}<br>"
                    "Uses: %{x}<extra></extra>"
                )
            )
        )

        bar.update_layout(
            showlegend=False,
            xaxis=dict(
                title="Number of uses",
                showgrid=True,
                gridcolor="#EFE5D9",
                zeroline=False
            ),
            yaxis=dict(
                showgrid=False,
                automargin=True
            ),
            bargap=0.38
        )

        chart_layout(bar, 310)

        st.plotly_chart(
            bar,
            width="stretch",
            config={"displayModeBar": False}
        )

    else:
        show_empty("No feature usage data available.")


# =========================================================
# SKILL GAP INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-heading">Skill Gap Insights</div>',
    unsafe_allow_html=True
)

matched_skills = set()
missing_skills = set()

for _, record in filtered.iterrows():

    details = record["details"]

    for key in [
        "matched_required",
        "matched_preferred",
        "matched_skills"
    ]:

        values = details.get(key, [])

        if isinstance(values, list):
            matched_skills.update(
                str(value).strip()
                for value in values
                if str(value).strip()
            )

    for key in [
        "missing_required",
        "missing_preferred",
        "missing_skills"
    ]:

        values = details.get(key, [])

        if isinstance(values, list):
            missing_skills.update(
                str(value).strip()
                for value in values
                if str(value).strip()
            )


skill_col1, skill_col2 = st.columns(2)


with skill_col1:

    st.markdown("""
    <div class="surface">
        <div class="surface-heading">Matched Skills</div>
        <div class="surface-description">
            Skills identified in your job matching activity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if matched_skills:

        tags = "".join(
            f'<span class="skill-chip" '
            f'style="background:#E8EDDF;color:#526449;'
            f'border:1px solid #CED8C2;">'
            f'{html.escape(skill)}</span>'
            for skill in sorted(matched_skills)
        )

        st.markdown(tags, unsafe_allow_html=True)

    else:
        show_empty("Matched skills will appear here.")


with skill_col2:

    st.markdown("""
    <div class="surface">
        <div class="surface-heading">Skills to Improve</div>
        <div class="surface-description">
            Skills identified as missing in your job matching activity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if missing_skills:

        tags = "".join(
            f'<span class="skill-chip" '
            f'style="background:#F5E7DE;color:#945F4D;'
            f'border:1px solid #E8CFC0;">'
            f'{html.escape(skill)}</span>'
            for skill in sorted(missing_skills)
        )

        st.markdown(tags, unsafe_allow_html=True)

    else:
        show_empty("Skills to improve will appear here.")


# =========================================================
# RECENT CAREER ACTIVITY
# =========================================================

st.markdown(
    '<div class="section-heading">Recent Career Activity</div>',
    unsafe_allow_html=True
)

recent = filtered.sort_values(
    "created_at",
    ascending=False
).head(15).copy()


if not recent.empty:

    recent["Date"] = recent["created_at"].dt.strftime(
        "%d %b %Y, %I:%M %p"
    )

    recent["Score"] = recent["score"].apply(
        lambda value: (
            f"{value:.1f}%"
            if pd.notna(value)
            else "Not scored"
        )
    )

    recent = recent.rename(
        columns={"activity_name": "Activity"}
    )

    st.dataframe(
        recent[["Date", "Activity", "Score"]],
        width="stretch",
        hide_index=True
    )

else:
    show_empty("Your recent activities will appear here.")


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    CAREERIQ AI &nbsp;·&nbsp; CAREER INTELLIGENCE DASHBOARD
    <br>
    Track your growth. Discover your potential. Build your future.
</div>
""", unsafe_allow_html=True)