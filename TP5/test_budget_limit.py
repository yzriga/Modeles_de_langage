# TP5/test_budget_limit.py
import uuid
import sys
import os

sys.path.append('/home/zriga/workspace/Modeles_de_langage')

from TP5.agent.state import AgentState, Budget
from TP5.agent.graph_minimal import build_graph

def create_normal_email():
    """Create a normal email that would need multiple steps"""
    return {
        'email_id': 'budget_test',
        'from': 'student@university.edu',
        'subject': 'Question about course validation',
        'body': 'Hello, I need information about validating my course units. Could you help me understand the process and requirements? Thank you.'
    }

if __name__ == "__main__":
    e = create_normal_email()
    print(f"=== TESTING BUDGET LIMITS ===")
    print(f"Email: {e['subject']}")
    print()

    # Test with very restrictive budget
    state = AgentState(
        run_id=str(uuid.uuid4()),
        email_id=e["email_id"],
        subject=e["subject"],
        sender=e["from"],
        body=e["body"],
        budget=Budget(max_steps=1, max_tool_calls=0, max_retrieval_attempts=0)  # Very restrictive
    )

    print("=== BUDGET LIMITS SET ===")
    print(f"Max steps: {state.budget.max_steps}")
    print(f"Max tool calls: {state.budget.max_tool_calls}")
    print(f"Max retrieval attempts: {state.budget.max_retrieval_attempts}")
    print()

    app = build_graph()
    out = app.invoke(state)

    print("=== FINAL BUDGET USAGE ===")
    print(f"Steps used: {out['budget'].steps_used}/{out['budget'].max_steps}")
    print(f"Tool calls used: {out['budget'].tool_calls_used}/{out['budget'].max_tool_calls}")
    print(f"Retrieval attempts: {out['budget'].retrieval_attempts}/{out['budget'].max_retrieval_attempts}")
    
    print("\n=== DECISION ===")
    print(out["decision"].model_dump_json(indent=2))
    
    print("\n=== FINAL OUTPUT ===")
    print("kind =", out["final_kind"])
    print(out["final_text"])
    
    print("\n=== ERRORS ===")
    if out["errors"]:
        for error in out["errors"]:
            print(f"- {error}")
    else:
        print("No errors")