from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.monitor import monitor_node
from src.agents.industry_monitor import industry_monitor_node 
from src.agents.analyst import analyst_node
from src.agents.journalist import journalist_node
#from src.agents.gatekeeper import gatekeeper_node
from src.agents.gatekeeper_dspy import gatekeeper_node # Use this for DSPy

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("monitor", monitor_node)
workflow.add_node("industry_monitor", industry_monitor_node) 
workflow.add_node("gatekeeper", gatekeeper_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("journalist", journalist_node)

# Define Edges
# We want both monitors to run at the start.
workflow.set_entry_point("monitor") 

# This is a bit of a hack for a linear graph: 
# We chain them: Monitor -> Industry -> Gatekeeper.
# (For true parallel execution, we'd need a 'start' node branching to both, 
# but chaining is safer for simple state updates).
workflow.add_edge("monitor", "industry_monitor")
workflow.add_edge("industry_monitor", "gatekeeper")

workflow.add_edge("gatekeeper", "analyst")
workflow.add_edge("analyst", "journalist")
workflow.add_edge("journalist", END)

app = workflow.compile()