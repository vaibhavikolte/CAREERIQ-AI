
import re

from modules.profile_extractor import SKILLS_DATABASE


def extract_job_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS_DATABASE:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text_lower):

            found_skills.append(skill)

    return found_skills


def match_resume_with_job(resume_text, job_description):

    resume_skills = extract_job_skills(resume_text)

    required_skills = extract_job_skills(job_description)

    matched_skills = [
        skill
        for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in resume_skills
    ]

    if required_skills:

        match_score = round(
            (len(matched_skills) / len(required_skills)) * 100,
            2
        )

    else:

        match_score = 0

    return {
        "match_score": match_score,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required": len(required_skills)
    }
