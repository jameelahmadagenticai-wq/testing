import re

def critique(summary):
    issues = []
    score = 10

    # Check for date
    if not re.search(r"\b(20\d{2}|19\d{2})\b", summary):
        issues.append("Missing dates")
        score -= 2

    # Check length
    if len(summary.split()) < 50:
        issues.append("Too short")
        score -= 2

    # Technical words
    tech_words = ["model", "algorithm", "network", "data", "system"]
    if not any(w in summary.lower() for w in tech_words):
        issues.append("Lacks technical detail")
        score -= 2

    # Improve query
    improved_query = ""

    if "Missing dates" in issues:
        improved_query += " latest "

    if "Lacks technical detail" in issues:
        improved_query += " technical research "

    if not improved_query:
        improved_query = "latest research study detailed explanation"

    return {
        "score": max(score, 1),
        "issues": issues,
        "improved_query": improved_query.strip()
    }