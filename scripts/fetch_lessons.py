import requests
from bs4 import BeautifulSoup
import json

ARCHIVE_URL = "https://linux1st.com/archives.html"

def fetch_article_links():
    resp = requests.get(ARCHIVE_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    
    links = []
    for a in soup.select("a[href*='/archives/']"):
        title = a.text.strip()
        url = a["href"]
        if url.startswith("/"):
            url = "https://linux1st.com" + url
        links.append({"title": title, "url": url})

    return links

if __name__ == "__main__":
    data = fetch_article_links()
    with open("linux1st_articles.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ saved to linux1st_articles.json")
