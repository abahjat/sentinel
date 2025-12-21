import requests
from bs4 import BeautifulSoup
import time

def fetch_github_trending(language: str) -> list:
    """Scrapes GitHub Trending page for a specific language."""
    url = f"https://github.com/trending/{language}?since=daily"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []
    
    for row in soup.select('article.Box-row'):
        try:
            h1 = row.select_one('h2.h3 a')
            repo_name = h1.text.strip().replace('\n', '').replace(' ', '')
            link = "https://github.com" + h1['href']
            
            desc_tag = row.select_one('p.col-9')
            description = desc_tag.text.strip() if desc_tag else "No description provided."
            
            # Extract stats (stars)
            stars_tag = row.select_one('a.Link--muted')
            stars = stars_tag.text.strip() if stars_tag else "?"
            
            repos.append({
                "id": link, # Use URL as unique ID
                "title": f"{repo_name} ({stars} ⭐)",
                "summary": description,
                "url": link,
                "authors": [repo_name.split('/')[0]]
            })
        except Exception:
            continue
            
    return repos

def fetch_hackernews_top(limit: int = 20) -> list:
    """Fetches top stories from Hacker News API."""
    base_url = "https://hacker-news.firebaseio.com/v0"
    
    # Get Top IDs
    resp = requests.get(f"{base_url}/topstories.json")
    if resp.status_code != 200:
        return []
        
    top_ids = resp.json()[:limit]
    stories = []
    
    for item_id in top_ids:
        try:
            item_resp = requests.get(f"{base_url}/item/{item_id}.json")
            item = item_resp.json()
            
            # Only care about stories with URLs (ignore 'Ask HN' for now)
            if 'url' in item:
                stories.append({
                    "id": str(item['id']),
                    "title": item.get('title', 'Untitled'),
                    "summary": f"Hacker News discussion with {item.get('score', 0)} upvotes.",
                    "url": item['url'],
                    "authors": [item.get('by', 'unknown')]
                })
            time.sleep(0.1) # Be nice to the API
        except Exception:
            continue
            
    return stories