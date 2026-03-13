import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ideas(analyzed_papers: list[dict], user_query: str) -> str:
    """Generate novel research ideas based on analyzed papers."""

    # Combine all analyses into one context
    papers_context = ""
    for i, paper in enumerate(analyzed_papers):
        papers_context += f"\nPaper {i+1}: {paper['title']}\n"
        papers_context += f"{paper['analysis']}\n"
        papers_context += "-" * 40

    prompt = f"""You are an expert AI research scientist.

A researcher is exploring this topic:
"{user_query}"

Based on these research papers:
{papers_context}

Generate 3 novel, specific, and actionable research ideas that:
1. Combine concepts from the papers above
2. Are directly relevant to the researcher's query
3. Have not been done before (to your knowledge)
4. Are feasible for a small research team

For each idea, provide:
IDEA TITLE: (short catchy title)
MOTIVATION: (why this is important)
APPROACH: (how to implement it)
NOVELTY: (what makes it new)
DATASET: (what data would you need)
---
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    from agents.search_agent import search_papers
    from rag.retriever import PaperRetriever
    from agents.reader_agent import read_papers

    query = "How can federated learning be applied to EV battery monitoring?"

    # Full pipeline
    print("🔍 Searching papers...")
    papers = search_papers("federated learning EV battery", max_results=5)

    print("📊 Indexing...")
    retriever = PaperRetriever()
    retriever.add_papers(papers)
    relevant = retriever.retrieve(query, top_k=3)

    print("📖 Reading papers...")
    analyzed = read_papers(relevant)

    print("💡 Generating ideas...")
    ideas = generate_ideas(analyzed, query)

    print(f"\n{'='*60}")
    print("💡 RESEARCH IDEAS")
    print('='*60)
    print(ideas)