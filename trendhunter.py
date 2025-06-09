import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import datetime

from pytrends.request import TrendReq

def get_google_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.today_searches(pn='IN')  # 'IN' for India
        return trending.tolist()[:10]
    except Exception as e:
        print(f"[Google Trends Error] {e}")
        return []

def get_tiktok_trends():
    url = 'https://www.tiktok.com/trending'
    headers = {'User-Agent': 'Mozilla/5.0'}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    tags = list(set([a.text for a in soup.find_all('a') if a.text.startswith('#')]))
    return tags[:10]

def get_x_trends():
    url = 'https://twitter.com/i/trends'
    headers = {'User-Agent': 'Mozilla/5.0'}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    text = soup.get_text()
    hashtags = list(set([line for line in text.split() if line.startswith('#')]))
    return hashtags[:10]

def merge_trends(google, tiktok, twitter):
    all_trends = google + tiktok + twitter
    keywords = {}
    for tag in all_trends:
        for word in tag.lower().split():
            keywords[word] = keywords.get(word, 0) + 1
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    return [kw[0] for kw in sorted_keywords[:3]]

def run_trendhunter():
    google = get_google_trends()
    tiktok = get_tiktok_trends()
    twitter = get_x_trends()
    top_trends = merge_trends(google, tiktok, twitter)
    print("🔥 Today's Viral Hooks:")
    for i, topic in enumerate(top_trends, 1):
        print(f"{i}. {topic.capitalize()}")

if __name__ == "__main__":
    run_trendhunter()

# trendhunter.py

import requests
from bs4 import BeautifulSoup
import psycopg2
import os

# Step 1: Scrape trending data
def fetch_trends():
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=IN"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    trends = []

    for item in items:
        title = item.title.text
        link = item.link.text
        trends.append({"title": title, "url": link})

    return trends

# Step 2: Save to PostgreSQL
def save_to_postgres(trends):
    DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        for trend in trends:
            cur.execute("INSERT INTO trends (title, url) VALUES (%s, %s)", (trend["title"], trend["url"]))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Trends saved to DB")

    except Exception as e:
        print("❌ Error saving to DB:", e)

# Main logic
if __name__ == "__main__":
    trends = fetch_trends()
    save_to_postgres(trends)
