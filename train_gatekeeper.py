import dspy
from dspy.teleprompt import BootstrapFewShot
from src.agents.gatekeeper_dspy import GatekeeperDSPyAgent, PaperAssessor
from src.training_data import train_examples

# 1. Initialize the Agent (This loads your Hardcoded Key)
# We use 'google' since that's what you set up
agent = GatekeeperDSPyAgent(provider="google")

# 2. Define a simple metric to tell DSPy if it did a good job
# We check if the predicted score matches your example score roughly
def validate_score(example, pred, trace=None):
    try:
        # Allow a small margin of error (e.g. 8 vs 9 is fine)
        return abs(int(example.score) - int(pred.score)) <= 1
    except:
        return False

# 3. Set up the Optimizer
# "BootstrapFewShot" will act like a teacher: 
# It runs your examples through the model, sees what works, 
# and saves the best "demonstrations" into the prompt.
print("🧠 Training the Gatekeeper... this may take a minute.")

teleprompter = BootstrapFewShot(metric=validate_score, max_bootstrapped_demos=3)

# 4. Compile (Train)
# This creates a new, optimized version of your module
compiled_gatekeeper = teleprompter.compile(agent.assessor, trainset=train_examples)

# 5. Save the "Brain"
output_file = "src/gatekeeper_optimized.json"
compiled_gatekeeper.save(output_file)

print(f"✅ Optimization Complete! Saved smart brain to {output_file}")