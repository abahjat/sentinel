from src.graph import app
from src.state import AgentState

def main():
    print("🚀 Sentinel System Initialized")
    
    initial_state = AgentState(
        raw_artifacts=[],
        screened_artifacts=[],
        final_digest="",
        iteration_count=0
    )
    
    for output in app.stream(initial_state):
        for node_name, state_update in output.items():
            print(f"\n--- Step Completed: {node_name} ---")
            
            if node_name == "gatekeeper":
                count = len(state_update.get("screened_artifacts", []))
                print(f"   Use cases found: {count}")

            # New Output Logic for Analyst
            if node_name == "analyst":
                results = state_update.get("screened_artifacts", [])
                print(f"📊 ANALYST REPORT:")
                for paper in results:
                    icon = "💻" if paper['code_link'] else "📄"
                    print(f" {icon} [{paper['score']}/10] {paper['title']}")
                    if paper['code_link']:
                        print(f"    🔗 Repo: {paper['code_link']}")
                    print(f"    💡 Why: {paper['relevance_reason']}")
                    print("-" * 40)

if __name__ == "__main__":
    main()