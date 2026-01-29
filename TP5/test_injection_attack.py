# TP5/test_injection_attack.py
import uuid
import sys
import os

sys.path.append('/home/zriga/workspace/Modeles_de_langage')

from TP5.agent.state import AgentState
from TP5.agent.graph_minimal import build_graph

def parse_email_file(file_path):
    """Parse a simple email file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    
    # Extract headers
    from_line = next((line for line in lines if line.startswith('From:')), 'unknown@example.com')
    subject_line = next((line for line in lines if line.startswith('Subject:')), 'Subject: No Subject')
    
    # Extract body (everything after the headers)
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '':
            body_start = i + 1
            break
    
    body = '\n'.join(lines[body_start:])
    
    return {
        'email_id': 'injection_test',
        'from': from_line.replace('From:', '').strip(),
        'subject': subject_line.replace('Subject:', '').strip(),
        'body': body.strip()
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_injection_attack.py <email_file>")
        sys.exit(1)
    
    email_file = sys.argv[1]
    if not os.path.exists(email_file):
        print(f"Email file not found: {email_file}")
        sys.exit(1)
    
    e = parse_email_file(email_file)
    print(f"=== TESTING EMAIL: {e['email_id']} ===")
    print(f"From: {e['from']}")
    print(f"Subject: {e['subject']}")
    print(f"Body preview: {e['body'][:100]}...")
    print()

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
    
    print("\n=== BUDGET USAGE ===")
    print(f"Steps used: {out['budget'].steps_used}/{out['budget'].max_steps}")
    print(f"Tool calls used: {out['budget'].tool_calls_used}/{out['budget'].max_tool_calls}")
    print(f"Retrieval attempts: {out['budget'].retrieval_attempts}/{out['budget'].max_retrieval_attempts}")
    
    print("\n=== DRAFT_V1 ===")
    print(out["draft_v1"])
    
    print("\n=== EVIDENCE ===")
    print(f"Number of evidence docs: {len(out['evidence'])}")
    for i, evidence in enumerate(out["evidence"][:3]):  # Show first 3
        print(f"Doc {i+1}: {evidence.doc_type} - {evidence.source}")
        print(f"  Snippet: {evidence.snippet[:100]}...")
    
    print("\n=== RETRIEVAL_SPEC ===")
    if "retrieval_spec" in out and out["retrieval_spec"]:
        print(f"Query: {out['retrieval_spec'].query}")
        print(f"K: {out['retrieval_spec'].k}")
    else:
        print("No retrieval performed")

    print("\n=== FINAL ===")
    print("kind =", out["final_kind"])
    print(out["final_text"])
    
    print("\n=== ERRORS ===")
    if out["errors"]:
        for error in out["errors"]:
            print(f"- {error}")
    else:
        print("No errors")
