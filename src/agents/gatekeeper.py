import json
from typing import List
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import Artifact, AgentState

# --- CONFIGURATION ---
# Toggle this between "claude" and "gemini"
PROVIDER = "gemini" 

# ⚠️ SECURITY WARNING: Hardcoding keys is risky. Do not commit this file to public GitHub.
ANTHROPIC_KEY = "sk-ant-..." 
GOOGLE_KEY = "AIzaSyCcaRXBm-" 
# ---------------------

class GatekeeperAgent:
    def __init__(self):
        self.provider = PROVIDER
        
        if self.provider == "claude":
            self.llm = ChatAnthropic(
                model="claude-4-5-sonnet-latest",
                temperature=0,
                api_key=ANTHROPIC_KEY
            )
        elif self.provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro", # 'pro' is best for complex reasoning/coding tasks
                temperature=0,
                google_api_key=GOOGLE_KEY
            )
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _build_batch_prompt(self, artifacts: List[Artifact]) -> str:
        """Helper to format a batch of papers for the LLM to read at once."""
        batch_text = ""
        for art in artifacts:
            batch_text += f"ID: {art['id']}\nCATEGORY: {art['category']}\nTITLE: {art['title']}\nABSTRACT: {art['summary'][:800]}...\n---\n"
        return batch_text

    def filter_batch(self, artifacts: List[Artifact]) -> List[Artifact]:
        """
        Sends a batch of papers to the LLM and returns only the relevant ones.
        """
        if not artifacts:
            return []

        print(f"⚖️  Gatekeeper ({self.provider.upper()}): Analyzing {len(artifacts)} papers...")

        system_prompt = """
        You are the Chief Technology Officer and Principal Architect for a high-level LegalTech and AI software firm. 
        Your user is a Master Software Engineer (PhD) and Expert in GenAI, .NET, and Digital Forensics.

        YOUR TASK:
        Review the list of incoming items (Research Papers, GitHub Repos, News).
        Select ONLY highly relevant items.
        
        CRITERIA FOR SELECTION (Score 7+/10):
        1. **GenAI & LLMs:** RAG architectures, Agentic frameworks, or novel NLP techniques applicable to law/text analysis.
        2. **Software Engineering:** Enterprise architecture, .NET ecosystem, high-scale system design.
        3. **LegalTech/Forensics:** E-discovery, digital evidence, security, or compliance automation.
        
        CRITERIA FOR SELECTION (Score 7+/10):
        1. **GenAI & LLMs:** Novel architectures, RAG tools, or high-performance local inference.
        2. **.NET & Enterprise:** New C# frameworks, Microsoft enterprise tools, high-scale architecture.
        3. **Security/Forensics:** Digital evidence tools, security breaches, zero-day analysis.
        4. **High-Signal Tools:** Trending GitHub repos that solve complex engineering problems (ignore "learn python" lists).

        OUTPUT FORMAT:
        Return a valid JSON object with a single key "selected_ids". 
        The value should be a list of objects, each containing:
        - "id": The exact ID of the paper.
        - "score": Integer 1-10.
        - "reason": A brief, punchy sentence on why this matters.
        
        Example JSON:
        {
          "selected_ids": [
            {"id": "2310.12345", "score": 9, "reason": "Proposes a novel RAG method that reduces hallucination in legal texts."},
            {"id": "2310.67890", "score": 8, "reason": "New Zero-trust architecture relevant for enterprise security."}
          ]
        }
        """

        batch_content = self._build_batch_prompt(artifacts)
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Here is the batch of papers to review:\n\n{batch_content}")
        ])

        try:
            content = response.content.strip()
            
            # Formatting cleanup for different models
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            selection_data = json.loads(content)
            selected_map = {item['id']: item for item in selection_data.get('selected_ids', [])}
            
            screened = []
            for art in artifacts:
                if art['id'] in selected_map:
                    decision = selected_map[art['id']]
                    art['score'] = decision['score']
                    art['relevance_reason'] = decision['reason']
                    screened.append(art)
                    print(f"  👉 KEEP: {art['title']} (Score: {art['score']})")
            
            return screened

        except json.JSONDecodeError:
            print(f"❌ Gatekeeper Error: {self.provider} returned invalid JSON.")
            return []

# LangGraph Node Wrapper
def gatekeeper_node(state: AgentState):
    gatekeeper = GatekeeperAgent()
    raw = state.get('raw_artifacts', [])
    screened = gatekeeper.filter_batch(raw)
    return {"screened_artifacts": screened}