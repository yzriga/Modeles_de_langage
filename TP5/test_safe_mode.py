# TP5/test_safe_mode.py
import uuid

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState, Decision
from TP5.agent.nodes.draft_reply import draft_reply

if __name__ == "__main__":
    emails = load_all_emails()
    e = emails[0]  # E01

    # Simuler un état avec decision qui needs_retrieval=True mais evidence vide
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )
    
    # Forcer une decision qui demande retrieval mais sans evidence
    state.decision = Decision(
        intent="reply",
        category="admin",
        priority=3,
        risk_level="low",
        needs_retrieval=True,
        retrieval_query="test query",
        rationale="Test case for safe mode"
    )
    
    # Evidence vide - doit déclencher safe mode
    state.evidence = []

    print("=== TESTING SAFE MODE (no evidence) ===")
    result = draft_reply(state)
    print(f"Draft_v1: {result.draft_v1}")
    print(f"Errors: {result.errors}")