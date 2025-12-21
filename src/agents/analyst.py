from typing import List
from src.state import AgentState, Artifact
from src.tools.scraper import find_code_link

class AnalystAgent:
    def __init__(self):
        pass

    def analyze(self, artifacts: List[Artifact]) -> List[Artifact]:
        print(f"🕵️  Analyst: Hunting for code implementations for {len(artifacts)} papers...")
        
        enriched_artifacts = []
        for art in artifacts:
            # 1. Try to find code
            code_url = find_code_link(art['id'])
            
            if code_url:
                art['code_link'] = code_url
                art['technical_depth'] = "Implementation Available"
                print(f"   💻 CODE FOUND: {code_url}")
            else:
                art['technical_depth'] = "Theory Only (No Repo Linked)"
                print(f"   📄 Theory Only: {art['title'][:40]}...")
            
            enriched_artifacts.append(art)
            
        return enriched_artifacts

# LangGraph Node Wrapper
def analyst_node(state: AgentState):
    analyst = AnalystAgent()
    screened = state.get('screened_artifacts', [])
    
    # Enrich the existing list
    analyzed = analyst.analyze(screened)
    
    return {"screened_artifacts": analyzed}