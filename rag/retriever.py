import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import faiss
import numpy as np
from rag.embeddings import embed_texts, embed_query


import faiss
import numpy as np
from rag.embeddings import embed_texts, embed_query

class PaperRetriever:
    def __init__(self):
        self.index = None
        self.papers = []

    def add_papers(self, papers: list[dict]):
        """Embed paper summaries and store in FAISS."""
        self.papers = papers
        texts = [p["title"] + " " + p["summary"] for p in papers]
        
        embeddings = embed_texts(texts)
        embeddings = np.array(embeddings).astype("float32")
        
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        
        print(f"✅ Indexed {len(papers)} papers")

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        """Find most relevant papers for a query."""
        query_vec = embed_query(query).astype("float32").reshape(1, -1)
        
        distances, indices = self.index.search(query_vec, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            paper = self.papers[idx]
            paper["score"] = float(distances[0][i])
            results.append(paper)
        
        return results


if __name__ == "__main__":
    # Quick test
    from agents.search_agent import search_papers

    papers = search_papers("federated learning EV battery")
    
    retriever = PaperRetriever()
    retriever.add_papers(papers)
    
    results = retriever.retrieve("battery health prediction decentralized")
    
    for r in results:
        print(f"\n📄 {r['title']}")
        print(f"📊 Score: {r['score']:.4f}")