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

import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Fetch DB URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Function to connect and ensure table exists
def init_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trends (
            id SERIAL PRIMARY KEY,
            keyword TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Function to insert a trend
def insert_trend(keyword):
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute("INSERT INTO trends (keyword) VALUES (%s)", (keyword,))
    conn.commit()
    cur.close()
    conn.close()

# Example usage:
if __name__ == "__main__":
    init_db()
    insert_trend("AI Tools India")

