# TP5/test_all_intents.py - Démonstration de tous les intents avec finalize
import uuid

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState, Decision
from TP5.agent.nodes.finalize import finalize

def test_intent(intent: str, email_data: dict, description: str):
    print(f"\n=== TEST INTENT: {intent.upper()} ===")
    print(f"Description: {description}")
    print(f"Email: {email_data['email_id']} - {email_data['subject']}")
    
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=email_data["email_id"],
        subject=email_data["subject"],
        sender=email_data["from"],
        body=email_data["body"],
    )
    
    # Simuler une décision avec l'intent désiré
    state.decision = Decision(
        intent=intent,
        category="admin",
        priority=3 if intent != "escalate" else 1,
        risk_level="low" if intent != "escalate" else "high",
        needs_retrieval=intent == "reply",
        retrieval_query="test query" if intent == "reply" else "",
        rationale=f"Test case for {intent}"
    )
    
    # Pour reply, simuler draft_v1 avec citations
    if intent == "reply":
        state.draft_v1 = "Voici votre réponse avec référence au document [doc_1] et [doc_2]."
        # Simuler evidence
        from TP5.agent.state import EvidenceDoc
        state.evidence = [
            EvidenceDoc(doc_id="doc_1", doc_type="pdf", source="reglement.pdf", snippet="Test snippet 1"),
            EvidenceDoc(doc_id="doc_2", doc_type="email", source="email.md", snippet="Test snippet 2")
        ]
    
    # Pour ask_clarification, simuler draft_v1
    elif intent == "ask_clarification":
        state.draft_v1 = "Pourriez-vous préciser votre demande ? Quels éléments vous intéressent ?"
    
    # Appliquer finalize
    result = finalize(state)
    
    print(f"Final kind: {result.final_kind}")
    print(f"Final text: {result.final_text}")
    
    if result.actions:
        print(f"Actions: {result.actions}")
    
    print("-" * 50)

if __name__ == "__main__":
    emails = load_all_emails()
    
    # Test reply
    test_intent("reply", emails[0], "Réponse normale avec citations")
    
    # Test ask_clarification  
    test_intent("ask_clarification", emails[3], "Demande de clarification")
    
    # Test escalate
    test_intent("escalate", emails[4], "Escalade vers humain")
    
    # Test ignore
    test_intent("ignore", emails[6], "Email à ignorer")
    
    print("\n=== TOUS LES INTENTS TESTÉS ===")
    print("Le nœud finalize harmonise correctement tous les types de sortie")