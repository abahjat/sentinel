import requests
from bs4 import BeautifulSoup
import re

def find_code_link(arxiv_id: str) -> str:
    """
    Scrapes the ArXiv abstract page to find GitHub/GitLab links.
    """
    url = f"https://arxiv.org/abs/{arxiv_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Check for standard "Code" section in ArXiv metadata (newer papers)
        # (ArXiv sometimes puts this in specific div classes, but regex is safer)
        
        # 2. Brute force search all links
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link['href']
            # Look for github.com but exclude standard footer links or unrelated projects
            if "github.com" in href or "gitlab.com" in href:
                # Basic filter to avoid generic links like 'github.com/about'
                if len(href) > 25 and "arxiv" not in href: 
                    return href
                    
        return ""
    except Exception as e:
        print(f"⚠️ Scraper Error for {arxiv_id}: {e}")
        return ""