import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agents.search_agent import search_papers, search_papers_multi
from agents.reader_agent import read_papers
from agents.idea_agent import generate_ideas
from agents.planner_agent import plan_research
from agents.experiment_agent import design_experiments
from rag.retriever import PaperRetriever

def run_pipeline(user_query: str, search_query: str = None, max_results: int = 5) -> dict:

    # Step 1 — Plan
    print(f"\n🧠 Planning research...")
    plan = plan_research(user_query)

    # Step 2 — Search
    print(f"\n🔍 Searching papers...")
    if search_query:
        papers = search_papers(search_query, max_results=max_results)
    else:
        papers = search_papers_multi(plan['search_queries'], max_per_query=3)

    print(f"📄 Found {len(papers)} papers")

    # Step 3 — Index + Retrieve
    print(f"📊 Indexing...")
    retriever = PaperRetriever()
    retriever.add_papers(papers)
    relevant = retriever.retrieve(user_query, top_k=3)

    # Step 4 — Read
    print(f"📖 Reading papers...")
    analyzed = read_papers(relevant)

    # Step 5 — Ideas
    print(f"💡 Generating ideas...")
    ideas = generate_ideas(analyzed, user_query)

    # Step 6 — Experiments
    print(f"🧪 Designing experiments...")
    experiments = design_experiments(ideas, user_query)

    return {
        "query": user_query,
        "plan": plan,
        "papers_found": len(papers),
        "papers_analyzed": analyzed,
        "ideas": ideas,
        "experiments": experiments
    }