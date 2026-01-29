# TP5/test_actual_loop.py - Test réel de la boucle avec mock direct
import uuid
from unittest.mock import patch

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState
from TP5.agent.graph_minimal import build_graph
from TP5.agent.tools.rag_tool import rag_search_tool

if __name__ == "__main__":
    emails = load_all_emails()
    e = emails[0]  # E01
    
    # Créer un état avec budget réduit pour forcer la limite
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )
    # Forcer max_retrieval_attempts = 2
    state.budget.max_retrieval_attempts = 2

    print(f"=== TESTING REAL LOOP - EMAIL {e['email_id']} ===")
    print(f"Subject: {e['subject']}")
    print(f"Max retrieval attempts set to: {state.budget.max_retrieval_attempts}")

    # Utiliser un mock pour forcer l'échec au 1er appel
    call_count = [0]
    
    def mock_rag_search(run_id: str, query: str, k: int = 5, filters=None):
        call_count[0] += 1
        print(f"[MOCK] RAG call #{call_count[0]} - Query: {query[:60]}...")
        
        if call_count[0] == 1:
            # Premier appel : retourner vide pour forcer safe mode
            print("[MOCK] First call - returning empty evidence to trigger loop")
            from TP5.agent.logger import log_event
            import time
            log_event(run_id, "tool_call", {
                "tool": "rag_search",
                "args_hash": "mock_empty",
                "latency_ms": 100,
                "status": "ok", 
                "k": k,
                "n_docs": 0,
                "note": "mock_empty_first_call"
            })
            return []
        else:
            # Deuxième appel : utiliser vraie fonction 
            print(f"[MOCK] Call #{call_count[0]} - using real RAG")
            # Appeler directement la vraie fonction importée
            from TP5.agent.tools.rag_tool import _hash_args, _format_snippet
            from langchain_chroma import Chroma
            from langchain_ollama import OllamaEmbeddings
            from TP5.agent.logger import log_event
            from TP5.agent.state import EvidenceDoc
            import time
            
            filters = filters or {}
            t0 = time.time()
            args = {"query": query, "k": k, "filters": filters}
            args_hash = _hash_args(args)
            
            try:
                emb = OllamaEmbeddings(base_url="http://127.0.0.1:11435", model="nomic-embed-text")
                vectordb = Chroma(collection_name="tp4_rag", embedding_function=emb, persist_directory="TP4/chroma_db")
                retriever = vectordb.as_retriever(search_kwargs={"k": k})
                docs = retriever.invoke(query)
                
                evidence = []
                for i, d in enumerate(docs, start=1):
                    meta = d.metadata or {}
                    evidence.append(EvidenceDoc(
                        doc_id=f"doc_{i}",
                        doc_type=str(meta.get("doc_type", "unknown")),
                        source=str(meta.get("source", "unknown")),
                        snippet=_format_snippet(d),
                        score=meta.get("score"),
                    ))
                
                log_event(run_id, "tool_call", {
                    "tool": "rag_search",
                    "args_hash": args_hash,
                    "latency_ms": int((time.time() - t0) * 1000),
                    "status": "ok",
                    "k": k,
                    "n_docs": len(evidence),
                    "note": "real_call_after_rewrite"
                })
                return evidence
            except Exception as e:
                log_event(run_id, "tool_call", {
                    "tool": "rag_search", 
                    "args_hash": args_hash,
                    "latency_ms": int((time.time() - t0) * 1000),
                    "status": "error",
                    "error": str(e)
                })
                return []

    # Appliquer le mock
    with patch('TP5.agent.tools.rag_tool.rag_search_tool', side_effect=mock_rag_search):
        app = build_graph()
        out = app.invoke(state)

    print("\n=== FINAL RESULT AFTER REAL LOOP TEST ===")
    print(f"Decision intent: {out['decision'].intent}")
    print(f"Retrieval attempts: {out['budget'].retrieval_attempts}")
    print(f"Evidence count: {len(out['evidence'])}")
    print(f"Evidence OK: {out.get('evidence_ok', 'N/A')}")
    print(f"Last draft had valid citations: {out.get('last_draft_had_valid_citations', 'N/A')}")
    print(f"Final retrieval query: '{out['decision'].retrieval_query}'")
    
    if out['draft_v1']:
        print(f"Final draft: {out['draft_v1'][:150]}...")
    else:
        print("No final draft generated")
        
    print(f"Total RAG calls made: {call_count[0]}")
    print(f"Errors: {out['errors']}")