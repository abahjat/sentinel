import dspy
import os
from typing import List
from src.state import Artifact, AgentState

# --- CONFIGURATION ---
# DSPy needs to be configured globally or contextually
# We will assume you set this up in the __init__ or main
# ---------------------

class PaperAssessor(dspy.Signature):
    """
    Assess if a technical paper or repo is relevant to a Master Software Engineer
    specializing in LegalTech, GenAI (RAG/Agents), and Digital Forensics.
    """
    
    title = dspy.InputField(desc="Title of the paper or repository")
    abstract = dspy.InputField(desc="Summary or abstract")
    category = dspy.InputField(desc="ArXiv category or Source (GitHub/HN)")
    
    reasoning = dspy.OutputField(desc="Brief technical justification for the score")
    score = dspy.OutputField(desc="Relevance score between 1 and 10", prefix="Score:")
    is_relevant = dspy.OutputField(desc="True if score >= 7, else False")

class GatekeeperDSPyAgent:
    def __init__(self, provider="anthropic"):
        # Configure the LM
        if provider == "anthropic":
            lm = dspy.LM(
                model="anthropic/claude-3-5-sonnet-20241022", # Added 'anthropic/' prefix
                api_key=os.environ.get("ANTHROPIC_API_KEY")
            )
        elif provider == "google":
            # Use the unified dspy.LM client
            lm = dspy.LM(
                model="gemini/gemini-2.5-pro", 
                api_key=os.environ.get("GOOGLE_API_KEY")
            )
        else:
            raise ValueError("Unknown provider")
            
        dspy.settings.configure(lm=lm)
        
        # Define the module: ChainOfThought adds an internal "thinking" step
        self.assessor = dspy.ChainOfThought(PaperAssessor)

    def filter_batch(self, artifacts: List[Artifact]) -> List[Artifact]:
        print(f"⚖️  Gatekeeper (DSPy): Assessing {len(artifacts)} items...")
        
        screened = []
        for art in artifacts:
            # DSPy prediction
            try:
                # We process one by one to use ChainOfThought effectively
                # (DSPy is fast enough for 50 items)
                pred = self.assessor(
                    title=art['title'],
                    abstract=art['summary'][:1000], # Truncate to save tokens
                    category=art['category']
                )
                
                # Parse Score
                try:
                    score = int(pred.score)
                except ValueError:
                    score = 0
                
                if score >= 7:
                    art['score'] = score
                    art['relevance_reason'] = pred.reasoning
                    screened.append(art)
                    print(f"  👉 KEEP: {art['title']} (Score: {score})")
                    
            except Exception as e:
                print(f"  ⚠️ Error processing {art['id']}: {e}")
                continue
                
        return screened

# LangGraph Node Wrapper
def gatekeeper_node(state: AgentState):
    # Initialize with your preferred provider
    # Ensure env vars are set!
    gatekeeper = GatekeeperDSPyAgent(provider="google")
    
    raw = state.get('raw_artifacts', [])
    screened = gatekeeper.filter_batch(raw)
    return {"screened_artifacts": screened}