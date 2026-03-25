from ddgs import DDGS

def search(query, max_results=8):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"]
            })
    return results