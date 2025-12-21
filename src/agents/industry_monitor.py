from datetime import datetime
from src.state import Artifact
from src.tools.web_loaders import fetch_github_trending, fetch_hackernews_top
from src.memory import get_processed_ids

class IndustryMonitorAgent:
    def __init__(self):
        # We track C# (.NET context) and Python (AI context)
        self.languages = ["c#", "python"]

    def fetch_updates(self) -> list[Artifact]:
        artifacts = []
        processed_ids = get_processed_ids()
        today = datetime.now().strftime("%Y-%m-%d")
        
        print("🌍 Industry Monitor: Checking GitHub & Hacker News...")
        
        # 1. GitHub Trending
        for lang in self.languages:
            repos = fetch_github_trending(lang)
            for repo in repos:
                if repo['id'] in processed_ids: continue
                
                artifacts.append({
                    "id": repo['id'],
                    "title": f"[GitHub {lang.upper()}] {repo['title']}",
                    "summary": repo['summary'],
                    "authors": repo['authors'],
                    "published_date": today,
                    "source_url": repo['url'],
                    "category": "Tool/Repo",
                    "source_type": "github",
                    "code_link": repo['url'] # It IS the code
                })

        # 2. Hacker News
        stories = fetch_hackernews_top(limit=25)
        for story in stories:
            if story['id'] in processed_ids: continue
            
            artifacts.append({
                "id": story['id'],
                "title": f"[HackerNews] {story['title']}",
                "summary": story['summary'],
                "authors": story['authors'],
                "published_date": today,
                "source_url": story['url'],
                "category": "Industry News",
                "source_type": "hackernews",
                "code_link": ""
            })
            
        print(f"✅ Industry Monitor: Found {len(artifacts)} new items.")
        return artifacts

def industry_monitor_node(state):
    monitor = IndustryMonitorAgent()
    new_items = monitor.fetch_updates()
    return {"raw_artifacts": new_items}