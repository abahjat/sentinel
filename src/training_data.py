import dspy

# Define your "Ground Truth" examples here.
# These act as the textbook for the AI to study.

train_examples = [
    dspy.Example(
        title="Attention Is All You Need",
        abstract="We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
        category="cs.CL",
        score="10",
        reasoning="Foundational paper for modern GenAI and LLMs. Essential reading for any AI Architect."
    ).with_inputs("title", "abstract", "category"),

    dspy.Example(
        title="A Survey of Deep Learning for Corn Disease Identification",
        abstract="This paper reviews various CNN models applied to identifying diseases in maize crops using leaf images.",
        category="cs.CV",
        score="2",
        reasoning="Specific agricultural application of computer vision. Not relevant to LegalTech, Text Analysis, or Enterprise Architecture."
    ).with_inputs("title", "abstract", "category"),

    dspy.Example(
        title="Optimizing .NET Garbage Collection for High-Throughput Microservices",
        abstract="We analyze the impact of server GC vs workstation GC in containerized environments running ASP.NET Core 8.",
        category="cs.SE",
        score="9",
        reasoning="Highly relevant to the user's specific stack (.NET) and role (Software Architect). Direct enterprise application."
    ).with_inputs("title", "abstract", "category")
]