from src.agents.monitor import monitor_node
from src.state import AgentState

# Mock initial state
initial_state = AgentState(
    raw_artifacts=[], 
    screened_artifacts=[], 
    final_digest="", 
    iteration_count=0
)

# Run the node
print("Starting Monitor Test...")
output = monitor_node(initial_state)

# Inspect output
if output['raw_artifacts']:
    print(f"\nSUCCESS: Retrieved {len(output['raw_artifacts'])} items.")
    for item in output['raw_artifacts'][:3]:
        print(f" - [{item['category']}] {item['title']}")
else:
    print("WARNING: No items found (check internet or ArXiv API status).")