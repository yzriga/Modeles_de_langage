# TP5/test_rag_allowlist.py
import sys
import time

sys.path.append('/home/zriga/workspace/Modeles_de_langage')

from TP5.agent.tools.rag_tool import rag_search_tool

if __name__ == "__main__":
    print("=== TESTING RAG TOOL ALLOW-LIST ===")
    
    # Test 1: Empty query
    print("\n--- Test 1: Empty query ---")
    result = rag_search_tool("test_run_1", "", k=5)
    print(f"Result for empty query: {len(result)} documents")
    
    # Test 2: k > 10
    print("\n--- Test 2: k > 10 ---")
    result = rag_search_tool("test_run_2", "validation course", k=15)
    print(f"Result for k=15: {len(result)} documents")
    
    # Test 3: Valid query
    print("\n--- Test 3: Valid query ---")
    result = rag_search_tool("test_run_3", "validation course", k=3)
    print(f"Result for valid query: {len(result)} documents")
    
    print("\nCheck the logs to see the error status for invalid requests.")