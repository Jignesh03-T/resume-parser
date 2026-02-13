import re
from app.parser.keywords import (
    EDUCATION_KEYWORDS,
    SKILLS_KEYWORDS,
    CERTIFICATION_KEYWORDS
)
def confidence_from_text(text):
    if not text:
        return 0.0
    length = len(text.split())
    return min(length / 50.0, 1.0)

# -------------------------------------------------
# SECTION HEADERS (FOR FUTURE USE: EXPERIENCE, ETC.)
# -------------------------------------------------

SECTION_HEADERS = {
    "experience": [
        "experience", "work experience", "professional experience"
    ],
    "projects": [
        "projects", "academic projects"
    ],
    "awards": [
    "activities & achievements",
    "activities and achievements",
    "achievements",
    "awards",
    "honors"],
    

    "publications": [
        "publications", "books", "research"
    ],

    "certifications": [
    "certifications",
    "certification",
    "certificate",
    "certificates",
    "courses","Coursework","COURSEWORK",
    "professional courses", 
    "professional certifications",
    "training & certifications",
    "courses & certifications",
    "courses",
    "training"
]

}
# -----------------------------
# AWARDS / ACTIVITIES FILTERING
# -----------------------------

AWARD_POSITIVE_WORDS = {
    "winner", "rank", "award", "prize", "honor", "honours",
    "first", "second", "third"
}

ACTIVITY_NEGATIVE_WORDS = {
    "volunteer", "member", "participant",
    "organizer", "organised", "organized",
    "lead", "leadership", "representative"
}

# -------------------------------------------------
# COMMON UTILITIES
# -------------------------------------------------

def safe_value(value):
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() == "nan":
        return ""
    return value


def split_sections(text: str) -> dict:
    """
    Rule-based section splitter.
    Currently used only to PREPARE for experience / AI.
    Does NOT affect existing extraction.
    """
    text_lower = text.lower()
    matches = []

    for section, keywords in SECTION_HEADERS.items():
        for kw in keywords:
            m = re.search(rf"(?:\n|^)\s*{kw}\s*(?:\n|:)", text_lower)
            if m:
                matches.append((m.start(), section))
                break

    matches.sort(key=lambda x: x[0])

    sections = {k: "" for k in SECTION_HEADERS.keys()}

    for i, (start, section) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        sections[section] = text[start:end].strip()

    # fallback if no headers found
    if not any(sections.values()):
        sections["experience"] = text

    return sections
def clean_achievements(text):
    if not text:
        return ""

    stop_headers = [
        "personal details",
        "languages",
        "date of birth",
        "dob",
        "address"
    ]

    lines = []

    for line in text.split("\n"):
        l = line.strip()

        if not l:
            continue

        # stop if personal info section starts
        l_lower = l.lower()

# reject activities
        if any(w in l_lower for w in ACTIVITY_NEGATIVE_WORDS):
            continue

# keep only awards
        if not any(w in l_lower for w in AWARD_POSITIVE_WORDS):
            continue


        # normalize formatting
        l = l.replace("|", " | ")
        l = re.sub(r"\s+", " ", l)

        # remove bullets
        l = l.lstrip("•-* ")

        lines.append(l)

    return "\n".join(lines)

# -------------------------------------------------
# FIELD EXTRACTION (RULE-BASED)
# -------------------------------------------------

def extract_email(text):
    match = re.search(
        r"[a-zA-Z0-9._%+-]+@(gmail|hotmail|yahoo)\.com",
        text,
        re.IGNORECASE
    )
    return safe_value(match.group() if match else "")


def extract_mobile(text):
    candidates = re.findall(r"\+?\d[\d\s\-]{8,14}\d", text)

    for c in candidates:
        digits = re.sub(r"\D", "", c)

        if len(digits) == 10:
            return digits
        if len(digits) > 10 and digits[-10:].startswith(tuple("6789")):
            return digits[-10:]

    return ""


def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:5]:
        if 2 <= len(line.split()) <= 4:
            return line.title()
    return ""


def extract_skills(text):
    text_lower = text.lower()
    found = []

    for skill in SKILLS_KEYWORDS:
        if re.search(rf"\b{re.escape(skill)}\b", text_lower):
            found.append(skill)

    return ", ".join(sorted(set(found)))

DEGREE_DEFINITIONS = {
    "10th": {
        "patterns": [
            r"\b10th\b",
            r"\bclass 10\b",
            r"\bssc\b",
            r"\bsecondary school\b"
        ]
    },
    "12th": {
        "patterns": [
            r"\b12th\b",
            r"\bclass 12\b",
            r"\bhsc\b",
            r"\bhigher secondary\b",
            r"\bhigher school certificate\b"
        ]
    },
    "BCA": {
        "patterns": [
            r"\bbca\b",
            r"\bbachelor of computer applications\b"
        ]
    },
    "BTECH": {
        "patterns": [
            r"\bbtech\b",
            r"\bbachelor of technology\b"
        ]
    },
    "BE": {
        "patterns": [
            r"\bbe\b",
            r"\bbachelor of engineering\b"
        ]
    },
    "MCA": {
        "patterns": [
            r"\bmca\b",
            r"\bmaster of computer applications\b"
        ]
    },
    "MTECH": {
        "patterns": [
            r"\bmtech\b",
            r"\bmaster of technology\b"
        ]
    }
}


def extract_education(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results = {}

    STOP_HEADERS = [
        "experience", "projects", "skills",
        "awards", "activities", "personal",
        "publications", "hobbies"
    ]

    DEGREE_KEYWORDS = [
        "bachelor", "master", "bca", "mca",
        "b.tech", "m.tech", "msc", "m.sc",
        "bsc", "b.sc", "mba", "diploma",
        "phd", "class 10", "class 12",
        "ssc", "hsc"
    ]

    def normalize_degree(line):
        lower = line.lower()

        if "msc-cs" in lower or "msc cs" in lower:
            return "MSc"
        if "m.c.a" in lower or "mca" in lower:
            return "MCA"
        if "b.c.a" in lower or "bca" in lower:
            return "BCA"
        if "h.s.c" in lower or "hsc" in lower or "class 12" in lower:
            return "12th"
        if "s.s.c" in lower or "ssc" in lower or "class 10" in lower:
            return "10th"

        # Fallback: take first meaningful academic phrase
        clean = re.split(r"\||–|-", line)[0].strip()
        clean = clean.split(",")[0].strip()
        clean = re.sub(r"\s+", " ", clean)
        return clean

    def extract_score(line):
        # Remove year ranges like 2018-2019
        line = re.sub(r"\b\d{4}\s*[-–]\s*\d{4}\b", "", line)

        # Percentage keyword format
        keyword_match = re.search(
            r"percentage\s*(\d+(?:\.\d+)?)",
            line,
            re.IGNORECASE
        )
        if keyword_match:
            value = keyword_match.group(1)
            return value + "%"

        # Decimal CGPA
        cgpa_match = re.search(
            r"\b\d+\.\d+\s*cgpa\b",
            line,
            re.IGNORECASE
        )
        if cgpa_match:
            return cgpa_match.group().upper()

        # Decimal percentage
        percent_decimal = re.search(
            r"\b\d+\.\d+%",
            line
        )
        if percent_decimal:
            return percent_decimal.group()

        # Integer percentage
        percent_int = re.search(
            r"\b\d+%",
            line
        )
        if percent_int:
            return percent_int.group()

        return None

    for i, line in enumerate(lines):
        lower = line.lower()

        # Stop if new section
        if any(stop in lower for stop in STOP_HEADERS):
            continue

        # Detect degree line
        if not any(k in lower for k in DEGREE_KEYWORDS):
            continue

        degree = normalize_degree(line)

        if degree in results:
            continue

        # 1️⃣ Same line first
        score = extract_score(line)

        # 2️⃣ Fallback: next 1–3 lines
        if not score:
            for j in range(i + 1, min(i + 4, len(lines))):
                next_lower = lines[j].lower()

                # Stop if new degree encountered
                if any(k in next_lower for k in DEGREE_KEYWORDS):
                    break

                # Stop if new section encountered
                if any(stop in next_lower for stop in STOP_HEADERS):
                    break

                score = extract_score(lines[j])
                if score:
                    break

        if score:
            results[degree] = score

    # Output order
    output = []

    if "10th" in results:
        output.append(f"10th {results['10th']}")
    if "12th" in results:
        output.append(f"12th {results['12th']}")

    for key in results:
        if key not in ["10th", "12th"]:
            output.append(f"{key} {results[key]}")

    return "\n".join(output)



CERT_ISSUER_HINTS = [
    "ibm", "google", "microsoft", "amazon", "aws",
    "coursera", "udemy", "edx", "simplilearn",
    "nasscom", "tcs", "ion", "infosys",
    "oracle", "cisco", "meta", "skillup",
    "smartbridge", "accenture"
]
EDUCATION_BLOCK_WORDS = {
    "mca", "bca", "ssc", "hsc",
    "school", "college", "university"
}

ACTIVITY_BLOCK_WORDS = {
    "volunteer", "hackathon", "fest",
    "competition", "winner", "representative"
}

CERT_TITLE_HINTS = {
    "certification", "certified", "course",
    "training", "cloud", "django",
    "analytics", "computing"
}

def extract_certifications(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    results = []
    capture = False

    # Start only on these headers (case-insensitive)
    START_HEADERS = [
        "certification",
        "certifications",
        "certification & trainings",
        "certifications & trainings",
        "training",
    ]

    # Stop immediately on these headers
    STOP_HEADERS = [
        "activities",
        "competitions",
        "achievements",
        "projects",
        "experience",
        "personal details",
        "date of birth",
        "gender",
        "address",
        "hobbies",
        "nationality",
        "education",
        "skills",
        "publications",
    ]

    # Personal data keywords to reject
    PERSONAL_KEYWORDS = [
        "email", "@", "phone", "mobile",
        "date of birth", "dob", "gender",
        "address", "nationality"
    ]

    # Activity/competition indicators to reject
    ACTIVITY_KEYWORDS = [
        "competition", "winner", "volunteer",
        "participant", "hackathon"
    ]

    for line in lines:
        lower = line.lower()

        # Detect start header
        if any(h in lower for h in START_HEADERS):
            capture = True
            continue

        # Stop at first new section
        if capture and any(h in lower for h in STOP_HEADERS):
            break

        if not capture:
            continue

        clean = line.lstrip("•-* ").strip()
        clean_lower = clean.lower()

        # Skip short lines
        if len(clean.split()) < 3:
            continue

        # Reject personal data
        if any(k in clean_lower for k in PERSONAL_KEYWORDS):
            continue

        # Reject activities
        if any(k in clean_lower for k in ACTIVITY_KEYWORDS):
            continue

        results.append(clean)

    if not results:
        return "No certification data available"

    return "\n".join(results)








# -------------------------------------------------
# MAIN ROW EXTRACTION (CALLED BY PIPELINE)
# -------------------------------------------------
    AWARD_POSITIVE_WORDS = {
    "winner", "rank", "award", "prize", "honor", "honours",
    "first", "second", "third" }

    ACTIVITY_NEGATIVE_WORDS = {
    "volunteer", "member", "participant",
    "organizer", "organised", "organized",
    "lead", "leadership", "representative"
    }

def extract_row(text):
    # section split prepared (not yet used)
    sections = split_sections(text)

    

    education_text = extract_education(text)
    certifications_text = extract_certifications(text)
    experience_text = sections.get("experience", "")
    publications_text = sections.get("publications", "")
    raw_achievements = sections.get("awards", "")
    cleaned_achievements = clean_achievements(raw_achievements)

    return {
    "Name": extract_name(text),
    "Email": extract_email(text),
    "Mobile": extract_mobile(text),
    "Skills": extract_skills(text),

    "Education": education_text,
    "Certifications": certifications_text,
    "Experience": experience_text,
    "Publications": publications_text,
    "Awards": cleaned_achievements,

}


    # confidence values (NOT shown in UI yet)
    confidence_from_text(experience_text),
    confidence_from_text(projects_text),
    confidence_from_text(awards_text),
    confidence_from_text(publications_text),



