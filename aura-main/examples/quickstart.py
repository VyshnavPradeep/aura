import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.advanced_rag import AdvancedRAG
def main():
    print("Advanced RAG - Quick Start\n")
    print("Step 1: Initialize RAG system...")
    rag = AdvancedRAG(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        llm_provider='anthropic'
    )
    print("✓ RAG system initialized\n")
    print("Step 2: Index codebase...")
    project_dir = str(Path(__file__).parent.parent)
    result = rag.index_codebase(
        project_dir=project_dir,
        project_id="quickstart_demo",
        file_extensions=['.py']
    )
    if result['success']:
        print(f"✓ Indexed {result['files_indexed']} files")
        print(f"✓ Created {result['chunks_created']} chunks\n")
    else:
        print(f"✗ Indexing failed: {result['error']}\n")
        return
    print("Step 3: Search for code...")
    queries = [
        "authentication functions",
        "database operations",
        "error handling code"
    ]
    for query in queries:
        print(f"\nSearching: '{query}'")
        search_result = rag.query(
            query=query,
            project_id="quickstart_demo",
            strategy="standard",
            top_k=3
        )
        if search_result['success']:
            print(f"  Found {search_result['results_count']} results:")
            for i, r in enumerate(search_result['results'], 1):
                print(f"    {i}. {r['name']} ({r['chunk_type']}) - {r['file']}")
        else:
            print(f"  Search failed: {search_result.get('error')}")
    print("\n✓ Quick start complete!")
    print("\nNext steps:")
    print("  • Try different strategies: 'multi_query', 'decompose', 'hyde'")
    print("  • Add filters: filters={'chunk_type': 'function'}")
    print("  • Enable reranking: use_reranking=True")
    print("  • See examples/rag_demo.py for advanced usage")
if __name__ == "__main__":
    main()