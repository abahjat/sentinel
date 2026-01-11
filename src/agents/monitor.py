import arxiv
import re
from typing import List
from datetime import datetime, timedelta, timezone
from src.state import Artifact
from src.memory import get_processed_ids, mark_as_processed

class MonitorAgent:
    def __init__(self):
        # Specific codes for your profile:
        # cs.SE = Software Engineering (Architecture, Testing, Maintenance)
        # cs.AI = Artificial Intelligence (General)
        # cs.CR = Cryptography & Security (Digital Forensics context)
        # cs.CL = Computation & Language (LLMs, NLP)
        self.categories = ["cs.SE", "cs.AI", "cs.CR", "cs.CL"]

    def fetch_latest(self, days_back: int = 3) -> List[Artifact]:
        """
        Fetches metadata for papers published in the last N days.
        """
        # 1. Load Memory
        existing_ids = get_processed_ids()
        print(f"🧠 Memory: Loaded {len(existing_ids)} previously processed papers.")

        client = arxiv.Client()
        search_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        
        search = arxiv.Search(
            query=search_query,
            max_results=100, # Increased fetch limit since we will filter many out
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        artifacts = []
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

        print(f"🕵️  Sentinel Monitor: Scanning ArXiv (Last {days_back} days)...")

        for result in client.results(search):
            if result.published.replace(tzinfo=timezone.utc) < cutoff_date:
                break
            
            # Extract paper ID and strip version number (e.g., 2401.12345v2 -> 2401.12345)
            raw_id = result.entry_id.split('/')[-1]
            paper_id = re.sub(r'v\d+$', '', raw_id)

            # 2. DEDUPLICATION CHECK
            if paper_id in existing_ids:
                continue # Skip this paper, we saw it already

            artifact: Artifact = {
                "id": paper_id,
                "title": result.title.replace('\n', ' '),
                "summary": result.summary.replace('\n', ' '),
                "authors": [a.name for a in result.authors],
                "published_date": result.published.strftime("%Y-%m-%d"),
                "source_url": result.pdf_url,
                "category": result.primary_category,
                "source_type": "arxiv", 
                "score": 0,
                "relevance_reason": "",
                "technical_depth": "",
                "code_link": ""
            }
            artifacts.append(artifact)

        print(f"✅ Found {len(artifacts)} NEW candidate papers (after deduplication).")
        return artifacts

def monitor_node(state):
    monitor = MonitorAgent()
    new_artifacts = monitor.fetch_latest(days_back=5)
    
    # Mark papers as processed IMMEDIATELY to prevent race conditions
    if new_artifacts:
        mark_as_processed([art['id'] for art in new_artifacts])
    
    return {"raw_artifacts": new_artifacts}
    