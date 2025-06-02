import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import datetime

def get_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    today = datetime.date.today().strftime("%Y-%m-%d")
    pytrends.build_payload(kw_list=[""])
    trending = pytrends.trending_searches(pn='united_states')
    return trending[0].tolist()[:10]

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
