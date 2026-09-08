SKILL_DATABASE = {
    "python": "Programming",
    "java": "Programming",
    "javascript": "Programming",
    "typescript": "Programming",
    "c++": "Programming",
    "c": "Programming",

    "django": "Backend",
    "flask": "Backend",
    "fastapi": "Backend",
    "spring": "Backend",
    "node.js": "Backend",
    "express": "Backend",

    "html": "Frontend",
    "css": "Frontend",
    "bootstrap": "Frontend",
    "react": "Frontend",
    "angular": "Frontend",
    "vue": "Frontend",

    "sql": "Database",
    "mysql": "Database",
    "postgresql": "Database",
    "mongodb": "Database",
    "sqlite": "Database",
    "oracle": "Database",

    "git": "Tools",
    "github": "Tools",
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "linux": "Operating Systems",
    "aws": "Cloud",
    "azure": "Cloud",
    "gcp": "Cloud",

    "machine learning": "AI/ML",
    "deep learning": "AI/ML",
    "natural language processing": "AI/ML",
    "nlp": "AI/ML",
    "tensorflow": "AI/ML",
    "pytorch": "AI/ML",
    "scikit-learn": "AI/ML",

    "rest api": "API",
    "restful api": "API",
    "api": "API",
    "graphql": "API",

    "power bi": "Analytics",
    "tableau": "Analytics",
    "excel": "Analytics",
    "pandas": "Analytics",
    "numpy": "Analytics",
}


def extract_skills(text):
    """
    Extract known technical skills from resume text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in SKILL_DATABASE:

        if skill in text_lower:
            found_skills.append(skill)

    return sorted(found_skills)


def categorize_skills(skills):
    """
    Group skills by category.
    """

    categorized = {}

    for skill in skills:

        category = SKILL_DATABASE.get(
            skill,
            "Other"
        )

        if category not in categorized:
            categorized[category] = []

        categorized[category].append(skill)

    return categorized