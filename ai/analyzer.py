from .sections import (
    detect_sections,
    get_missing_sections,
)

from .skills import (
    extract_skills,
    categorize_skills,
)

from .keywords import (
    extract_keywords,
    compare_keywords,
    calculate_similarity,
)


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be",
    "by", "can", "for", "from", "has", "have",
    "in", "is", "it", "of", "on", "or", "our",
    "that", "the", "their", "this", "to", "was",
    "we", "who", "with", "you", "your",
    "will", "would", "should", "could", "may",
    "must", "more", "such", "than", "then",
    "into", "about", "over", "under", "using",
    "use", "used", "also", "very", "good",
    "preferred", "working", "looking", "seeking",
    "role", "candidate", "candidates",
    "responsible", "responsibilities",
    "requirements", "requirement",
}


def clean_keywords(keywords):
    """
    Remove common English words and duplicates.
    """

    cleaned = []

    for keyword in keywords:

        keyword = keyword.strip().lower()

        if not keyword:
            continue

        if keyword in STOP_WORDS:
            continue

        if len(keyword) <= 2:
            continue

        if keyword not in cleaned:
            cleaned.append(keyword)

    return cleaned


def calculate_resume_keyword_score(
    text,
    skills,
    keywords,
):
    """
    Calculate general ATS keyword quality
    when no Job Description is supplied.
    """

    text_lower = text.lower()

    # Technical skills component
    skill_score = min(
        50,
        len(skills) * 4
    )

    professional_keywords = [
        "data",
        "analysis",
        "analytics",
        "dashboard",
        "project",
        "experience",
        "education",
        "development",
        "programming",
        "database",
        "business",
        "reporting",
        "visualization",
        "machine learning",
        "problem solving",
        "communication",
    ]

    found = sum(
        1
        for keyword in professional_keywords
        if keyword in text_lower
    )

    professional_score = min(
        35,
        found * 3
    )

    # Keyword diversity
    keyword_count = len(keywords)

    diversity_score = min(
        15,
        keyword_count
    )

    return round(
        min(
            skill_score
            + professional_score
            + diversity_score,
            100
        ),
        2
    )


def calculate_section_score(text):
    """
    Calculate resume section completeness.
    """

    detected = detect_sections(text)

    important_sections = [
        "summary",
        "skills",
        "experience",
        "education",
        "projects",
    ]

    found = sum(
        1
        for section in important_sections
        if section in detected
    )

    return round(
        (found / len(important_sections)) * 100,
        2
    )


def calculate_formatting_score(text):
    """
    Basic ATS readability checks.
    """

    score = 100

    text_length = len(text.strip())
    word_count = len(text.split())
    line_count = text.count("\n")

    if text_length < 300:
        score -= 30

    if "\t" in text:
        score -= 5

    if line_count < 10:
        score -= 10

    if word_count < 100:
        score -= 20

    # Extremely long resume
    if word_count > 1200:
        score -= 10

    return max(
        0,
        min(score, 100)
    )


def calculate_experience_score(text):
    """
    Evaluate experience using action verbs,
    measurable achievements and experience signals.
    """

    text_lower = text.lower()

    action_verbs = [
        "developed",
        "designed",
        "built",
        "implemented",
        "created",
        "analyzed",
        "improved",
        "automated",
        "optimized",
        "managed",
        "maintained",
        "collaborated",
        "engineered",
        "configured",
        "tested",
    ]

    experience_terms = [
        "experience",
        "intern",
        "internship",
        "worked",
        "project",
        "role",
        "developer",
        "engineer",
    ]

    action_count = sum(
        1
        for verb in action_verbs
        if verb in text_lower
    )

    experience_count = sum(
        1
        for term in experience_terms
        if term in text_lower
    )

    # Base score
    score = min(
        45,
        action_count * 5
    )

    score += min(
        20,
        experience_count * 4
    )

    # Measurable achievement signals
    measurable_signals = [
        "%",
        "10,000",
        "5,000",
        "2,000",
        "1,000",
        "500",
        "200",
        "100",
        "million",
        "thousand",
        "reduced",
        "increased",
        "improved",
        "saved",
        "growth",
        "accuracy",
        "performance",
    ]

    measurable_count = sum(
        1
        for signal in measurable_signals
        if signal.lower() in text_lower
    )

    score += min(
        35,
        measurable_count * 5
    )

    return min(
        100,
        score
    )


def calculate_overall_score(
    keyword_score,
    skills_score,
    section_score,
    experience_score,
    formatting_score,
):
    """
    Calculate weighted ATS score.
    """

    score = (
        keyword_score * 0.30
        + skills_score * 0.25
        + section_score * 0.15
        + experience_score * 0.10
        + formatting_score * 0.20
    )

    return round(
        min(score, 100),
        2
    )


def generate_recommendations(
    text,
    missing_sections,
    missing_keywords,
    skills,
    keyword_score,
    skills_score,
    section_score,
    experience_score,
    formatting_score,
    has_job_description,
):
    """
    Generate detailed and explainable
    resume improvement recommendations.
    """

    recommendations = []

    text_lower = text.lower()

    # -----------------------------------------
    # Sections
    # -----------------------------------------

    if missing_sections:

        recommendations.append(
            "Add the missing resume sections: "
            + ", ".join(missing_sections)
            + "."
        )

    # -----------------------------------------
    # Skills
    # -----------------------------------------

    if not skills:

        recommendations.append(
            "Add a dedicated Technical Skills "
            "section containing relevant tools, "
            "technologies and programming languages."
        )

    elif skills_score < 80:

        recommendations.append(
            "Expand your Technical Skills section "
            "with relevant technologies that you "
            "actually know or have used."
        )

    # -----------------------------------------
    # Job keywords
    # -----------------------------------------

    if has_job_description and missing_keywords:

        top_missing = missing_keywords[:8]

        recommendations.append(
            "Improve job keyword alignment by "
            "adding relevant missing terms where "
            "they truthfully match your experience: "
            + ", ".join(top_missing)
            + "."
        )

    elif not has_job_description:

        recommendations.append(
            "For a job-specific ATS analysis, "
            "paste the target Job Description. "
            "This will identify matched and missing "
            "keywords."
        )

    # -----------------------------------------
    # Experience
    # -----------------------------------------

    if experience_score < 90:

        recommendations.append(
            "Strengthen experience and project "
            "bullets with action verbs and "
            "measurable outcomes."
        )

    # -----------------------------------------
    # Measurements
    # -----------------------------------------

    measurable_patterns = [
        "%",
        "reduced",
        "increased",
        "improved",
        "saved",
        "10,000",
        "5,000",
        "2,000",
        "1,000",
        "500",
        "200",
        "100",
        "million",
        "thousand",
    ]

    has_measurement = any(
        pattern.lower() in text_lower
        for pattern in measurable_patterns
    )

    if not has_measurement:

        recommendations.append(
            "Add measurable achievements using "
            "percentages, numbers, time saved, "
            "revenue, accuracy, scale or "
            "performance improvements."
        )

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    if "summary" not in detect_sections(text):

        recommendations.append(
            "Add a concise professional summary "
            "tailored to your target role."
        )

    # -----------------------------------------
    # Formatting
    # -----------------------------------------

    if formatting_score < 90:

        recommendations.append(
            "Improve ATS readability by using "
            "standard headings, consistent spacing, "
            "simple formatting and machine-readable "
            "text."
        )

    # -----------------------------------------
    # Keyword score
    # -----------------------------------------

    if keyword_score < 80:

        recommendations.append(
            "Improve keyword coverage by naturally "
            "including relevant professional terms "
            "and technologies in your summary, "
            "skills, projects and experience."
        )

    # -----------------------------------------
    # Final fallback
    # -----------------------------------------

    if not recommendations:

        recommendations.append(
            "Your resume has strong ATS fundamentals. "
            "For further improvement, tailor it to "
            "each target Job Description and strengthen "
            "achievement-focused bullet points."
        )

    return recommendations


def analyze_resume(
    resume_text,
    job_description="",
):
    """
    Complete ATS resume analysis.

    Job Description is optional.

    Without Job Description:
        General ATS analysis.

    With Job Description:
        General ATS analysis +
        job-specific keyword matching.
    """

    # -----------------------------------------
    # Skills
    # -----------------------------------------

    skills = extract_skills(
        resume_text
    )

    categorized_skills = categorize_skills(
        skills
    )

    # -----------------------------------------
    # Sections
    # -----------------------------------------

    sections = detect_sections(
        resume_text
    )

    missing_sections = get_missing_sections(
        resume_text
    )

    # -----------------------------------------
    # Keywords
    # -----------------------------------------

    resume_keywords = extract_keywords(
        resume_text
    )

    resume_keywords = clean_keywords(
        resume_keywords
    )

    # -----------------------------------------
    # Job Description
    # -----------------------------------------

    has_job_description = bool(
        job_description
        and job_description.strip()
    )

    if has_job_description:

        keyword_result = compare_keywords(
            resume_text,
            job_description
        )

        keyword_score = keyword_result[
            "score"
        ]

        matched_keywords = clean_keywords(
            keyword_result["matched"]
        )

        missing_keywords = clean_keywords(
            keyword_result["missing"]
        )

        similarity_score = calculate_similarity(
            resume_text,
            job_description
        )

    else:

        keyword_score = (
            calculate_resume_keyword_score(
                resume_text,
                skills,
                resume_keywords,
            )
        )

        matched_keywords = []

        missing_keywords = []

        similarity_score = 0

    # -----------------------------------------
    # Individual scores
    # -----------------------------------------

    skills_score = min(
        100,
        len(skills) * 8
    )

    section_score = calculate_section_score(
        resume_text
    )

    experience_score = calculate_experience_score(
        resume_text
    )

    formatting_score = calculate_formatting_score(
        resume_text
    )

    # -----------------------------------------
    # Overall score
    # -----------------------------------------

    ats_score = calculate_overall_score(
        keyword_score,
        skills_score,
        section_score,
        experience_score,
        formatting_score,
    )

    # -----------------------------------------
    # Recommendations
    # -----------------------------------------

    recommendations = generate_recommendations(
        resume_text,
        missing_sections,
        missing_keywords,
        skills,
        keyword_score,
        skills_score,
        section_score,
        experience_score,
        formatting_score,
        has_job_description,
    )

    # -----------------------------------------
    # Return
    # -----------------------------------------

    return {

        "ats_score": ats_score,

        "keyword_score": keyword_score,

        "skills_score": skills_score,

        "section_score": section_score,

        "experience_score": experience_score,

        "formatting_score": formatting_score,

        "skills": skills,

        "categorized_skills": categorized_skills,

        "sections": sections,

        "missing_sections": missing_sections,

        "resume_keywords": resume_keywords,

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,

        "similarity_score": similarity_score,

        "recommendations": recommendations,
    }