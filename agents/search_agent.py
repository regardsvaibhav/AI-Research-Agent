import arxiv

def search_papers(query: str, max_results: int = 5) -> list[dict]:
    """Search Arxiv for relevant papers."""
    
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    for result in client.results(search):
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "summary": result.summary,
            "url": result.entry_id,
            "published": str(result.published.date()),
            "categories": result.categories
        })
    
    return papers


def search_papers_multi(queries: list[str], max_per_query: int = 3) -> list[dict]:
    """Search multiple queries and combine unique results."""
    
    all_papers = []
    seen_urls = set()
    
    for query in queries:
        papers = search_papers(query, max_results=max_per_query)
        for p in papers:
            if p["url"] not in seen_urls:
                all_papers.append(p)
                seen_urls.add(p["url"])
    
    return all_papers


if __name__ == "__main__":
    results = search_papers("federated learning EV battery")
    for p in results:
        print(f"\n📄 {p['title']}")
        print(f"📅 {p['published']}")
        print(f"🔗 {p['url']}")