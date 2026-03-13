import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def design_experiments(ideas: str, user_query: str) -> str:
    """Design concrete experiments for the generated research ideas."""

    prompt = f"""You are an expert ML research scientist.

A researcher is exploring: "{user_query}"

They have these research ideas:
{ideas}

For each idea, design a concrete experiment plan in this exact format:

EXPERIMENT 1:
TITLE: (name of experiment)
DATASET: (specific public dataset to use, with source)
MODEL: (exact model architecture)
BASELINE: (what to compare against)
METRICS: (evaluation metrics)
EXPECTED RESULT: (what success looks like)
COMPUTE: (estimated compute needed)
---

Be specific. Name real datasets (NASA battery dataset, UCI ML repo, etc).
Name real model architectures (LSTM, Transformer, FedAvg, etc).
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from agents.search_agent import search_papers
    from agents.reader_agent import read_papers
    from agents.idea_agent import generate_ideas
    from rag.retriever import PaperRetriever

    query = "How can federated learning be applied to EV battery monitoring?"

    papers = search_papers("federated learning battery degradation", max_results=5)
    retriever = PaperRetriever()
    retriever.add_papers(papers)
    relevant = retriever.retrieve(query, top_k=3)
    analyzed = read_papers(relevant)
    ideas = generate_ideas(analyzed, query)
    experiments = design_experiments(ideas, query)

    print(f"\n{'='*60}")
    print("🧪 EXPERIMENT DESIGNS")
    print('='*60)
    print(experiments)