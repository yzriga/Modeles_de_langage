# TP5/test_force_loop.py - Forcer la boucle en modifiant directement l'exécution
import uuid

from TP5.load_test_emails import load_all_emails  
from TP5.agent.state import AgentState, Decision
from TP5.agent.nodes.maybe_retrieve import maybe_retrieve
from TP5.agent.nodes.draft_reply import draft_reply
from TP5.agent.nodes.check_evidence import check_evidence
from TP5.agent.nodes.rewrite_query import rewrite_query

if __name__ == "__main__":
    emails = load_all_emails()
    e = emails[0]
    
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )
    
    # Simuler une decision qui demande retrieval
    state.decision = Decision(
        intent="reply",
        category="admin", 
        priority=3,
        risk_level="low",
        needs_retrieval=True,
        retrieval_query="attestation scolarité règlement",
        rationale="Test case for loop"
    )
    
    print("=== MANUAL LOOP TEST ===")
    print(f"Email: {e['email_id']} - {e['subject']}")
    print(f"Initial query: '{state.decision.retrieval_query}'")
    
    # === PREMIÈRE TENTATIVE ===
    print("\n--- FIRST RETRIEVAL ATTEMPT ---")
    state.budget.max_retrieval_attempts = 2
    
    # Simuler maybe_retrieve qui retourne evidence vide
    state.budget.retrieval_attempts += 1
    state.budget.tool_calls_used += 1
    state.evidence = []  # Forcer evidence vide !
    print(f"Forced empty evidence. Attempts: {state.budget.retrieval_attempts}")
    
    # Draft reply avec evidence vide -> safe mode
    print("\n--- FIRST DRAFT ATTEMPT ---")
    state_after_draft1 = draft_reply(state)
    print(f"Draft result: last_draft_had_valid_citations = {state_after_draft1.last_draft_had_valid_citations}")
    print(f"Draft text: {state_after_draft1.draft_v1[:100]}...")
    
    # Check evidence -> devrait indiquer evidence_ok = False
    print("\n--- CHECK EVIDENCE ---")  
    state_after_check = check_evidence(state_after_draft1)
    print(f"Evidence OK: {state_after_check.evidence_ok}")
    print(f"Should trigger rewrite: {not state_after_check.evidence_ok and state_after_check.budget.retrieval_attempts < 2}")
    
    # === DEUXIÈME TENTATIVE ===
    if not state_after_check.evidence_ok and state_after_check.budget.retrieval_attempts < state_after_check.budget.max_retrieval_attempts:
        print("\n--- QUERY REWRITE ---")
        state_after_rewrite = rewrite_query(state_after_check)
        print(f"Original query: '{state.decision.retrieval_query}'")  
        print(f"Rewritten query: '{state_after_rewrite.decision.retrieval_query}'")
        
        # Deuxième retrieval - cette fois avec vraie evidence
        print("\n--- SECOND RETRIEVAL ATTEMPT ---")
        state_final = maybe_retrieve(state_after_rewrite)
        print(f"Final evidence count: {len(state_final.evidence)}")
        print(f"Final attempts: {state_final.budget.retrieval_attempts}")
        
        # Deuxième draft
        print("\n--- SECOND DRAFT ATTEMPT ---")  
        state_final_draft = draft_reply(state_final)
        print(f"Final draft citations valid: {state_final_draft.last_draft_had_valid_citations}")
        print(f"Final draft: {state_final_draft.draft_v1[:150]}...")
        
        # Final check
        state_final_check = check_evidence(state_final_draft)
        print(f"Final evidence OK: {state_final_check.evidence_ok}")
        
        print("\n=== LOOP COMPLETED ===")
        print(f"Total retrieval attempts: {state_final_check.budget.retrieval_attempts}")
        print(f"Loop was necessary: True")
    else:
        print("\n=== NO LOOP NEEDED ===")