import requests
from bs4 import BeautifulSoup

def scrape(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9"
        }

        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            return ""

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return text[:5000]

    except Exception:
        return ""