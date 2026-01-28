# TP5/test_graph_minimal.py
import uuid

from TP5.load_test_emails import load_all_emails
from TP5.agent.state import AgentState
from TP5.agent.graph_minimal import build_graph

if __name__ == "__main__":
    emails = load_all_emails()
    e = emails[0]  # E01 - test principal

    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
    )

    app = build_graph()
    out = app.invoke(state)

    print("=== DECISION ===")
    print(out["decision"].model_dump_json(indent=2))
    print("\n=== DRAFT_V1 ===")
    print(out["draft_v1"])   # TODO: afficher draft_v1
    print("\n=== ACTIONS ===")
    print(out["actions"])   # TODO: afficher actions
    print("\n=== EVIDENCE ===")
    print(f"Number of evidence docs: {len(out['evidence'])}")
    for i, evidence in enumerate(out["evidence"][:3]):  # Show first 3
        print(f"Doc {i+1}: {evidence.doc_type} - {evidence.source}")
        print(f"  Snippet: {evidence.snippet[:100]}...")
        print(f"  Score: {evidence.score}")
    print("\n=== RETRIEVAL_SPEC ===")
    if "retrieval_spec" in out and out["retrieval_spec"]:
        print(f"Query: {out['retrieval_spec'].query}")
        print(f"K: {out['retrieval_spec'].k}")
    else:
        print("No retrieval performed")
