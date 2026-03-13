import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def read_papers(papers: list[dict]) -> list[dict]:
    """Summarize and extract key info from each paper."""
    
    results = []
    
    for paper in papers:
        print(f"📖 Reading: {paper['title'][:60]}...")
        
        prompt = f"""You are a research assistant. Analyze this paper and extract key information.

Paper Title: {paper['title']}
Abstract: {paper['summary']}

Extract and return in this exact format:
PROBLEM: (what problem does this paper solve?)
METHOD: (what method/approach do they use?)
RESULTS: (what are the key results or contributions?)
RELEVANCE: (why is this relevant to federated learning and EV batteries?)
"""
        
        response = client.chat.completions.create(
           model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        
        analysis = response.choices[0].message.content
        
        results.append({
            "title": paper["title"],
            "url": paper["url"],
            "published": paper["published"],
            "analysis": analysis
        })
    
    return results


if __name__ == "__main__":
    from agents.search_agent import search_papers
    from rag.retriever import PaperRetriever

    # Search
    papers = search_papers("federated learning EV battery", max_results=3)
    
    # Retrieve most relevant
    retriever = PaperRetriever()
    retriever.add_papers(papers)
    relevant = retriever.retrieve("battery health prediction decentralized", top_k=2)
    
    # Read and analyze
    analyzed = read_papers(relevant)
    
    for paper in analyzed:
        print(f"\n{'='*60}")
        print(f"📄 {paper['title']}")
        print(f"🔗 {paper['url']}")
        print(f"\n{paper['analysis']}")