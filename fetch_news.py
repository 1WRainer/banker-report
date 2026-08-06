import feedparser
import json
from datetime import datetime, timedelta
import time

# Targeted RSS Feeds
FEEDS = [
    {"url": "https://news.google.com/rss/search?q=%22community+bank%22+OR+%22credit+union%22+when:24h&hl=en-US&gl=US&ceid=US:en", "scope": "Local & Regional"},
    {"url": "https://news.google.com/rss/search?q=%22Chase%22+OR+%22Bank+of+America%22+branch+expansion+when:24h&hl=en-US&gl=US&ceid=US:en", "scope": "National"},
    {"url": "https://news.google.com/rss/search?q=%22Chime%22+OR+%22SoFi%22+deposits+market+share+when:24h&hl=en-US&gl=US&ceid=US:en", "scope": "National"},
    {"url": "https://www.cutimes.com/rss/", "scope": "National"},
    {"url": "https://www.financialbrand.com/feed/", "scope": "National"}
]

def parse_category(title, summary):
    text = (title + " " + summary).lower()
    if any(k in text for k in ["chase", "bofa", "bank of america", "chime", "sofi", "branch", "expansion", "competition"]):
        return "Macro & Competition"
    elif any(k in text for k in ["marketing", "seo", "brand", "customer acquisition", "campaign", "ad"]):
        return "Marketing"
    elif any(k in text for k in ["acquisition", "merger", "growth", "loan", "sba", "deposit", "c&i"]):
        return "Bank Growth"
    return "Local & Regional"

def fetch_all():
    articles = []
    seen_titles = set()
    
    for feed in FEEDS:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries[:5]: # Take top items
            title = entry.title
            if title in seen_titles:
                continue
            seen_titles.add(title)
            
            summary = getattr(entry, 'summary', title)
            category = parse_category(title, summary)
            
            articles.append({
                "id": len(articles) + 1,
                "title": title,
                "source": parsed.feed.get("title", "Banking News"),
                "scope": feed["scope"],
                "category": category,
                "url": entry.link,
                "time": "Updated Today",
                "score": 90 + (len(articles) % 9),
                "summary": summary[:200] + "...",
                "actionable": "Key intelligence item for community bank and credit union leadership."
            })
            
    with open("data.json", "w") as f:
        json.dump(articles[:12], f, indent=2)

if __name__ == "__main__":
    fetch_all()
