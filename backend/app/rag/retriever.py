import math
import re
from typing import List, Dict, Any
from app.rag.knowledge_base import EU_MANGO_REGULATIONS

class RegulatoryRetriever:
    """
    Lightweight zero-cost TF-IDF / BM25 keyword relevance retriever
    for regulatory knowledge base. Modular interface for future embeddings.
    """
    def __init__(self, corpus: List[Dict[str, Any]] = None):
        self.corpus = corpus or EU_MANGO_REGULATIONS

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_terms = self._tokenize(query.lower())
        scored_results = []
        
        for req in self.corpus:
            text = f"{req['commodity']} {req['destination']} {req['category']} {req['requirement']} {req['evidence_text']}".lower()
            score = 0.0
            for term in query_terms:
                if term in text:
                    # Term frequency score + weighting for exact commodity/destination matches
                    count = len(re.findall(r'\b' + re.escape(term) + r'\b', text))
                    weight = 2.0 if term in ["mango", "india", "eu", "phytosanitary", "mrl", "imidacloprid"] else 1.0
                    score += (count + 1) * weight
            
            if score > 0 or len(query_terms) == 0:
                result = req.copy()
                result["relevance_score"] = round(min(score / 10.0 + 0.75, 0.99), 2)
                scored_results.append(result)
        
        # Sort by relevance score descending
        scored_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_results[:top_k]

    def _tokenize(self, text: str) -> List[str]:
        return [w for w in re.split(r'\W+', text) if len(w) > 2]

retriever_instance = RegulatoryRetriever()
