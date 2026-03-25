import re

def summarize(text):
    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) < 5:
        return text[:300]

    keywords = [
        "research", "study", "result", "data",
        "analysis", "technology", "development",
        "model", "system"
    ]

    scored = []

    for s in sentences:
        score = 0

        for k in keywords:
            if k in s.lower():
                score += 1

        score += len(s) / 100
        scored.append((score, s))

    scored.sort(reverse=True)

    top_sentences = [s for _, s in scored[:5]]

    return " ".join(top_sentences)