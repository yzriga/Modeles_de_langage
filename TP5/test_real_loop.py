# TP5/test_real_loop.py - Forcer vraiment la boucle avec 2 tentatives
import uuid
import os

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState
from TP5.agent.graph_minimal import build_graph

# Hack temporaire : modifier le RAG tool pour simuler un échec au 1er appel
def patch_rag_tool_for_test():
    """Patch temporaire pour forcer l'échec au premier appel"""
    import TP5.agent.tools.rag_tool as rag_module
    original_rag_search = rag_module.rag_search_tool
    
    # Compteur d'appels
    call_count = [0]
    
    def mock_rag_search(run_id: str, query: str, k: int = 5, filters=None):
        call_count[0] += 1
        print(f"[DEBUG] RAG call #{call_count[0]} with query: {query[:50]}...")
        
        # Premier appel : retourner evidence vide (simuler échec)
        if call_count[0] == 1:
            print("[DEBUG] Simulating failure on first call - returning empty evidence")
            from TP5.agent.logger import log_event
            import time
            t0 = time.time()
            log_event(run_id, "tool_call", {
                "tool": "rag_search",
                "args_hash": "forced_empty",
                "latency_ms": 50,
                "status": "ok",
                "k": k,
                "n_docs": 0,
                "note": "forced_empty_for_test"
            })
            return []  # Evidence vide !
        
        # Deuxième appel : utiliser la vraie fonction
        print("[DEBUG] Second call - using real RAG")
        return original_rag_search(run_id, query, k, filters)
    
    # Appliquer le patch
    rag_module.rag_search_tool = mock_rag_search
    return original_rag_search

if __name__ == "__main__":
    # Appliquer le patch temporaire
    original_func = patch_rag_tool_for_test()
    
    emails = load_all_emails()
    e = emails[0]  # E01 - attestation scolarité
    
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )

    print(f"=== TESTING FORCED LOOP - EMAIL {e['email_id']} ===")
    print(f"Subject: {e['subject']}")
    print(f"This test forces empty evidence on 1st retrieval to trigger the loop")

    app = build_graph()
    out = app.invoke(state)

    print("\n=== FINAL RESULT AFTER FORCED LOOP ===")
    print(f"Decision intent: {out['decision'].intent}")
    print(f"Retrieval attempts: {out['budget'].retrieval_attempts}")
    print(f"Evidence count: {len(out['evidence'])}")
    print(f"Evidence OK: {out.get('evidence_ok', 'N/A')}")
    print(f"Last draft had valid citations: {out.get('last_draft_had_valid_citations', 'N/A')}")
    print(f"Final retrieval query: {out['decision'].retrieval_query}")
    
    if out['draft_v1']:
        print(f"Final draft: {out['draft_v1'][:200]}...")
    else:
        print("No final draft")
        
    print(f"Errors: {out['errors']}")
    
    # Restaurer la fonction originale
    import TP5.agent.tools.rag_tool as rag_module
    rag_module.rag_search_tool = original_func
    print("\n[DEBUG] Original RAG function restored")