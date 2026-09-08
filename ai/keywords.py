import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills import SKILL_DATABASE


# ------------------------------------------------------------
# Common English words that should not be treated as
# meaningful ATS keywords.
# ------------------------------------------------------------

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been",
    "being", "but", "by", "can", "could", "did", "do",
    "does", "doing", "for", "from", "had", "has", "have",
    "having", "he", "her", "here", "hers", "him", "his",
    "how", "i", "if", "in", "into", "is", "it", "its",
    "itself", "me", "more", "most", "my", "no", "not",
    "of", "on", "or", "our", "ours", "out", "over",
    "she", "should", "so", "some", "such", "than",
    "that", "the", "their", "theirs", "them", "then",
    "there", "these", "they", "this", "those", "through",
    "to", "under", "up", "very", "was", "we", "were",
    "what", "when", "where", "which", "while", "who",
    "whom", "why", "will", "with", "would", "you",
    "your", "yours",

    "about", "also", "already", "among", "because",
    "before", "during", "each", "further", "just",
    "may", "might", "must", "once", "only", "other",
    "own", "same", "should", "still", "too",

    "looking", "seeking", "candidate", "candidates",
    "role", "roles", "position", "positions",
    "responsible", "responsibilities",
    "requirement", "requirements",
    "preferred", "including", "etc",
}


# ------------------------------------------------------------
# Normalize text
# ------------------------------------------------------------

def normalize_text(text):
    """
    Normalize text for keyword comparison.
    """

    text = text.lower()

    text = text.replace("–", " ")
    text = text.replace("—", " ")
    text = text.replace("/", " ")
    text = text.replace("|", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ------------------------------------------------------------
# Tokenization
# ------------------------------------------------------------

def tokenize(text):
    """
    Extract meaningful individual tokens.
    """

    text = normalize_text(text)

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b",
        text
    )

    cleaned = []

    for word in words:

        word = word.lower().strip(".,;:()[]{}")

        if not word:
            continue

        if word in STOP_WORDS:
            continue

        if len(word) <= 2:
            continue

        cleaned.append(word)

    return cleaned


# ------------------------------------------------------------
# Skill extraction from arbitrary text
# ------------------------------------------------------------

def extract_job_skills(text):
    """
    Detect known technical skills from any job description.
    """

    normalized = normalize_text(text)

    found = []

    for skill in SKILL_DATABASE.keys():

        skill_normalized = normalize_text(
            skill
        )

        pattern = (
            rf"(?<![a-z0-9])"
            rf"{re.escape(skill_normalized)}"
            rf"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            normalized
        ):
            found.append(skill)

    return sorted(
        set(found)
    )


# ------------------------------------------------------------
# Extract meaningful keywords
# ------------------------------------------------------------

def extract_keywords(
    text,
    limit=40
):
    """
    Extract meaningful recurring words.

    Technical skills are prioritized, followed by
    professional vocabulary.
    """

    normalized = normalize_text(text)

    tokens = tokenize(normalized)

    frequency = Counter(tokens)

    # Start with known technical skills.
    skill_keywords = extract_job_skills(
        normalized
    )

    # Generic professional words that can be
    # useful in many different job descriptions.
    professional_words = {
        "analysis",
        "analytics",
        "architecture",
        "automation",
        "business",
        "communication",
        "database",
        "development",
        "engineering",
        "implementation",
        "management",
        "marketing",
        "optimization",
        "planning",
        "programming",
        "reporting",
        "research",
        "security",
        "testing",
        "visualization",
        "design",
        "strategy",
        "leadership",
        "documentation",
        "deployment",
        "integration",
        "performance",
        "quality",
        "operations",
        "support",
        "customer",
        "product",
        "software",
        "systems",
        "technical",
    }

    professional_matches = [
        word
        for word in professional_words
        if word in frequency
    ]

    # Frequently occurring meaningful words.
    frequent_words = [
        word
        for word, count in frequency.most_common()
        if count >= 1
    ]

    result = []

    # Technical skills first.
    for skill in skill_keywords:

        if skill not in result:

            result.append(skill)

    # Professional words next.
    for word in professional_matches:

        if word not in result:

            result.append(word)

    # Other meaningful words last.
    for word in frequent_words:

        if word not in result:

            result.append(word)

        if len(result) >= limit:
            break

    return result[:limit]


# ------------------------------------------------------------
# Extract useful multi-word phrases
# ------------------------------------------------------------

def extract_phrases(
    text,
    limit=30
):
    """
    Extract common two-word professional phrases.
    """

    normalized = normalize_text(text)

    words = tokenize(normalized)

    phrases = Counter()

    for index in range(
        len(words) - 1
    ):

        first = words[index]
        second = words[index + 1]

        phrase = f"{first} {second}"

        phrases[phrase] += 1

    useful_phrases = []

    for phrase, count in phrases.most_common():

        parts = phrase.split()

        if len(parts) != 2:
            continue

        if all(
            part not in STOP_WORDS
            for part in parts
        ):
            useful_phrases.append(
                phrase
            )

        if len(useful_phrases) >= limit:
            break

    return useful_phrases


# ------------------------------------------------------------
# Compare resume with job description
# ------------------------------------------------------------

def compare_keywords(
    resume_text,
    job_text
):
    """
    Compare meaningful skills and keywords
    between a resume and job description.
    """

    resume_normalized = normalize_text(
        resume_text
    )

    job_normalized = normalize_text(
        job_text
    )

    # --------------------------------------------------------
    # Technical skills
    # --------------------------------------------------------

    resume_skills = set(
        extract_job_skills(
            resume_normalized
        )
    )

    job_skills = set(
        extract_job_skills(
            job_normalized
        )
    )

    matched_skills = sorted(
        resume_skills.intersection(
            job_skills
        )
    )

    missing_skills = sorted(
        job_skills.difference(
            resume_skills
        )
    )

    # --------------------------------------------------------
    # Professional keywords
    # --------------------------------------------------------

    resume_keywords = set(
        extract_keywords(
            resume_normalized,
            limit=60
        )
    )

    job_keywords = extract_keywords(
        job_normalized,
        limit=60
    )

    matched_keywords = []

    missing_keywords = []

    for keyword in job_keywords:

        if keyword in resume_keywords:

            if keyword not in matched_keywords:
                matched_keywords.append(
                    keyword
                )

        else:

            if keyword not in missing_keywords:
                missing_keywords.append(
                    keyword
                )

    # --------------------------------------------------------
    # Professional phrases
    # --------------------------------------------------------

    resume_phrases = set(
        extract_phrases(
            resume_normalized
        )
    )

    job_phrases = extract_phrases(
        job_normalized
    )

    matched_phrases = []

    missing_phrases = []

    for phrase in job_phrases:

        if phrase in resume_phrases:

            matched_phrases.append(
                phrase
            )

        else:

            missing_phrases.append(
                phrase
            )

    # --------------------------------------------------------
    # Weighted score
    # --------------------------------------------------------

    if job_skills:

        skill_match_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 60

    else:

        skill_match_score = 0

    if job_keywords:

        keyword_match_score = (
            len(matched_keywords)
            / len(job_keywords)
        ) * 30

    else:

        keyword_match_score = 0

    if job_phrases:

        phrase_match_score = (
            len(matched_phrases)
            / len(job_phrases)
        ) * 10

    else:

        phrase_match_score = 0

    total_score = (
        skill_match_score
        + keyword_match_score
        + phrase_match_score
    )

    return {
        "matched": sorted(
            set(
                matched_skills
                + matched_keywords
            )
        ),

        "missing": sorted(
            set(
                missing_skills
                + missing_keywords
            )
        ),

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "matched_phrases": matched_phrases,

        "missing_phrases": missing_phrases,

        "score": round(
            min(
                total_score,
                100
            ),
            2
        ),
    }


# ------------------------------------------------------------
# Resume / Job semantic similarity
# ------------------------------------------------------------

def calculate_similarity(
    resume_text,
    job_text
):
    """
    Calculate TF-IDF cosine similarity.
    """

    if not resume_text.strip():
        return 0

    if not job_text.strip():
        return 0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:

        vectors = vectorizer.fit_transform(
            [
                resume_text,
                job_text
            ]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(
            similarity * 100,
            2
        )

    except ValueError:

        return 0