import asyncio
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.advanced_rag import AdvancedRAG
from config import get_rag_config
import os
def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
def print_result(result, index, show_details=True):
    print(f"\n[Result {index + 1}]")
    print(f"  Name: {result.get('name', 'N/A')}")
    print(f"  Type: {result.get('chunk_type', 'N/A')}")
    print(f"  File: {result.get('file', 'N/A')} (Line {result.get('line', 'N/A')})")
    if 'fused_score' in result:
        print(f"  Score: {result['fused_score']:.3f} (reranked)")
    elif 'combined_score' in result:
        print(f"  Score: {result['combined_score']:.3f}")
    if show_details and 'context' in result:
        context = result['context'][:150]
        print(f"  Context: {context}...")
    if 'parent_chunk' in result:
        print(f"  Parent: {result['parent_chunk']['name']} ({result['parent_chunk']['type']})")
async def demo_basic_indexing():
    print_separator("DEMO 1: Indexing a Codebase")
    rag = AdvancedRAG(
        api_key=os.getenv('GEMINI_API_KEY'),
        llm_provider='gemini'
    )
    project_dir = str(Path(__file__).parent.parent)
    print(f"\nIndexing project directory: {project_dir}")
    print("This will:")
    print("  1. Scan for Python files")
    print("  2. Create hierarchical chunks (classes → methods)")
    print("  3. Generate embeddings")
    print("  4. Build FAISS + BM25 indices")
    result = rag.index_codebase(
        project_dir=project_dir,
        project_id="demo_project",
        file_extensions=['.py'],
        exclude_dirs=['venv', '__pycache__', 'tests']
    )
    if result['success']:
        print("\n✓ Indexing successful!")
        print(f"  Files indexed: {result['files_indexed']}")
        print(f"  Chunks created: {result['chunks_created']}")
        print(f"  Embeddings dimension: {result['embeddings_dimension']}")
        print(f"  BM25 enabled: {result['bm25_enabled']}")
        print(f"  Features: {', '.join(result['features'])}")
    else:
        print(f"\n✗ Indexing failed: {result.get('error')}")
    return rag
async def demo_standard_search(rag):
    print_separator("DEMO 2: Standard Hybrid Search")
    query = "authentication and password validation"
    print(f"\nQuery: '{query}'")
    print("Strategy: standard (direct hybrid search - fastest)")
    result = rag.query(
        query=query,
        project_id="demo_project",
        strategy="standard",
        top_k=3,
        use_reranking=True,
        include_context=True
    )
    if result['success']:
        print(f"\n✓ Found {result['results_count']} results")
        for i, r in enumerate(result['results']):
            print_result(r, i)
    else:
        print(f"\n✗ Search failed: {result.get('error')}")
async def demo_multi_query_search(rag):
    print_separator("DEMO 3: Multi-Query Search")
    query = "find database connection handling"
    print(f"\nOriginal query: '{query}'")
    print("Strategy: multi_query (generates 3 variations)")
    result = rag.query(
        query=query,
        project_id="demo_project",
        strategy="multi_query",
        top_k=3,
        use_reranking=True
    )
    if result['success']:
        print(f"\nQuery variations used:")
        for i, q in enumerate(result.get('queries_used', []), 1):
            print(f"  {i}. {q}")
        print(f"\n✓ Found {result['results_count']} results (combined from all queries)")
        for i, r in enumerate(result['results']):
            print_result(r, i, show_details=False)
    else:
        print(f"\n✗ Search failed: {result.get('error')}")
async def demo_decompose_search(rag):
    print_separator("DEMO 4: Query Decomposition")
    query = "find async database operations with error handling and logging"
    print(f"\nComplex query: '{query}'")
    print("Strategy: decompose (breaks into sub-queries)")
    result = rag.query(
        query=query,
        project_id="demo_project",
        strategy="decompose",
        top_k=5,
        use_reranking=True
    )
    if result['success']:
        print(f"\nSub-queries generated:")
        for i, q in enumerate(result.get('queries_used', []), 1):
            print(f"  {i}. {q}")
        print(f"\n✓ Found {result['results_count']} results")
        for i, r in enumerate(result['results'][:3]):
            print_result(r, i, show_details=False)
    else:
        print(f"\n✗ Search failed: {result.get('error')}")
async def demo_hyde_search(rag):
    print_separator("DEMO 5: HyDE Search")
    query = "how to validate user input"
    print(f"\nQuery: '{query}'")
    print("Strategy: hyde (generates hypothetical answer first)")
    result = rag.query(
        query=query,
        project_id="demo_project",
        strategy="hyde",
        top_k=3,
        use_reranking=True
    )
    if result['success']:
        queries_used = result.get('queries_used', [])
        if len(queries_used) > 1:
            print(f"\nHypothetical document generated:")
            print(f"  {queries_used[1][:200]}...")
        print(f"\n✓ Found {result['results_count']} results")
        for i, r in enumerate(result['results']):
            print_result(r, i, show_details=False)
    else:
        print(f"\n✗ Search failed: {result.get('error')}")
async def demo_filtered_search(rag):
    print_separator("DEMO 6: Filtered Search")
    query = "code analysis functions"
    print(f"\nQuery: '{query}'")
    print("Filter: Only 'function' type chunks (not classes or methods)")
    result = rag.query(
        query=query,
        project_id="demo_project",
        strategy="standard",
        top_k=5,
        filters={'chunk_type': 'function'},
        use_reranking=False
    )
    if result['success']:
        print(f"\n✓ Found {result['results_count']} functions")
        for i, r in enumerate(result['results']):
            print_result(r, i, show_details=False)
            assert r.get('chunk_type') == 'function', "All results should be functions"
    else:
        print(f"\n✗ Search failed: {result.get('error')}")
async def demo_context_enrichment(rag):
    print_separator("DEMO 7: Context Enrichment")
    query = "analyze method"
    print(f"\nQuery: '{query}'")
    print("Context enrichment: Show parent class for methods")
    result = rag.query(
        query=query,
        project_id="demo_project",
        strategy="standard",
        top_k=3,
        filters={'chunk_type': 'method'},
        include_context=True
    )
    if result['success']:
        print(f"\n✓ Found {result['results_count']} methods with context")
        for i, r in enumerate(result['results']):
            print(f"\n[Result {i + 1}]")
            print(f"  Method: {r.get('name', 'N/A')}")
            print(f"  File: {r.get('file', 'N/A')}")
            if 'parent_chunk' in r:
                parent = r['parent_chunk']
                print(f"  Parent Class: {parent.get('name', 'N/A')}")
                print(f"  Class Context: {parent.get('context', 'N/A')[:100]}...")
            else:
                print("  No parent context (standalone function)")
    else:
        print(f"\n✗ Search failed: {result.get('error')}")
async def demo_statistics(rag):
    print_separator("DEMO 8: Project Statistics")
    stats = rag.get_statistics("demo_project")
    if 'error' not in stats:
        print("\n✓ Project statistics:")
        print(f"  Total chunks: {stats['total_chunks']}")
        print(f"  Hierarchical structure: {stats['has_hierarchical_structure']}")
        print(f"  Has relationships: {stats['has_relationships']}")
        print(f"\n  Chunk type distribution:")
        for chunk_type, count in stats['chunk_types'].items():
            print(f"    {chunk_type}: {count}")
    else:
        print(f"\n✗ Failed to get statistics: {stats['error']}")
async def main():
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "ADVANCED RAG SYSTEM DEMO" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    try:
        if not os.getenv('GEMINI_API_KEY'):
            print("\n⚠ WARNING: No LLM API key found.")
            print("  Multi-query, decompose, and HyDE strategies will use fallbacks.")
            print("  Set GEMINI_API_KEY for full functionality.\n")
        rag = await demo_basic_indexing()
        await demo_standard_search(rag)
        await demo_multi_query_search(rag)
        await demo_decompose_search(rag)
        await demo_hyde_search(rag)
        await demo_filtered_search(rag)
        await demo_context_enrichment(rag)
        await demo_statistics(rag)
        print_separator("DEMO COMPLETE")
        print("\n✓ All demos completed successfully!")
        print("\nKey Takeaways:")
        print("  • Standard search: Fastest, good for simple queries")
        print("  • Multi-query: Better recall, finds more relevant results")
        print("  • Decompose: Best for complex multi-part questions")
        print("  • HyDE: Excellent for 'how to' and conceptual queries")
        print("  • Filtering: Narrows results to specific code types")
        print("  • Context enrichment: Provides full picture with parent/child")
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
if __name__ == "__main__":
    asyncio.run(main())