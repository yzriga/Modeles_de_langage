# TP5/test_loop_forced.py - Forcer la boucle en simulant citations invalides
import uuid

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState
from TP5.agent.graph_minimal import build_graph

if __name__ == "__main__":
    emails = load_all_emails()
    e = emails[8]  # E09 - tentative prompt injection (plus complexe)

    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )

    print(f"=== TESTING EMAIL {e['email_id']} ===")
    print(f"Subject: {e['subject']}")
    print(f"Body: {e['body'][:150]}...")

    app = build_graph()
    out = app.invoke(state)

    print("\n=== FINAL RESULT ===")
    print(f"Decision intent: {out['decision'].intent}")
    print(f"Retrieval attempts: {out['budget'].retrieval_attempts}")
    print(f"Evidence count: {len(out['evidence'])}")
    print(f"Evidence OK: {out.get('evidence_ok', 'N/A')}")
    print(f"Last draft had valid citations: {out.get('last_draft_had_valid_citations', 'N/A')}")
    print(f"Final query: {out['decision'].retrieval_query}")
    
    if out['draft_v1']:
        print(f"Draft: {out['draft_v1'][:200]}...")
    else:
        print("No draft generated")
        
    print(f"Actions: {len(out['actions'])} actions")
    print(f"Errors: {len(out['errors'])} errors")