import re


SECTION_ALIASES = {
    "contact": [
        "contact",
        "contact information",
    ],
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical competencies",
        "competencies",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
    ],
    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
    ],
}


def normalize_text(text):
    """
    Normalize extracted resume text.
    """

    text = text.lower()

    # Replace repeated whitespace with a single space.
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def detect_sections(text):
    """
    Detect standard resume sections.

    Works even when PDF extraction puts
    multiple resume sections on one line.
    """

    normalized = normalize_text(text)

    detected = {}

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            alias_pattern = re.escape(
                alias.lower()
            )

            # Match the heading as a phrase,
            # not merely as part of another word.
            pattern = rf"(?<![a-z]){alias_pattern}(?![a-z])"

            if re.search(
                pattern,
                normalized
            ):
                detected[section] = True
                break

    return detected


def get_missing_sections(text):
    """
    Return important sections that were not detected.
    """

    detected = detect_sections(text)

    recommended_sections = [
        "summary",
        "skills",
        "experience",
        "education",
        "projects",
    ]

    missing = []

    for section in recommended_sections:

        if section not in detected:
            missing.append(section)

    return missing