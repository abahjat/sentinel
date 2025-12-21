import os
# Set your key for testing
# os.environ["OPENAI_API_KEY"] = "sk-..." 

from src.agents.monitor import monitor_node
from src.agents.gatekeeper import gatekeeper_node
from src.state import AgentState

def run_test():
    # 1. Initialize State
    state = AgentState(
        raw_artifacts=[], 
        screened_artifacts=[], 
        final_digest="", 
        iteration_count=0
    )

    # 2. Run Monitor
    print("--- 1. RUNNING MONITOR ---")
    state_update_1 = monitor_node(state)
    state.update(state_update_1) # meaningful state update
    
    # 3. Run Gatekeeper
    if state['raw_artifacts']:
        print(f"\n--- 2. RUNNING GATEKEEPER (Input: {len(state['raw_artifacts'])} items) ---")
        
        # Limit to first 5 for the test run to save tokens
        test_subset = state['raw_artifacts'][:5]
        state['raw_artifacts'] = test_subset
        
        state_update_2 = gatekeeper_node(state)
        state.update(state_update_2)
        
        print(f"\n✅ FINAL RESULT: {len(state['screened_artifacts'])} papers selected.")
        for item in state['screened_artifacts']:
            print(f"Title: {item['title']}\nReason: {item['relevance_reason']}\n")
    else:
        print("Monitor found no papers to check.")

if __name__ == "__main__":
    run_test()