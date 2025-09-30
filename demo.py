import sys
import os
sys.path.append('.')

from app.faiss_db import FAISSVectorDB
from app.textract_service import MockTextractService

def run_demo():
    """Run a simple CLI demo"""
    print("🏥 Handwritten Medical Notes Search Demo")
    print("=" * 50)
    
    # Initialize
    vector_db = FAISSVectorDB()
    
    # Show stats
    stats = vector_db.get_stats()
    print(f"📊 Database Stats: {stats['total_documents']} documents indexed")
    print()
    
    while True:
        print("Choose search type:")
        print("1. Semantic Search (AI-powered)")
        print("2. Keyword Search")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "3":
            print("👋 Goodbye!")
            break
        
        if choice not in ["1", "2"]:
            print("❌ Invalid choice. Please try again.")
            continue
        
        query = input("\nEnter your search query: ").strip()
        if not query:
            print("❌ Please enter a valid query.")
            continue
        
        print(f"\n🔍 Searching for: '{query}'...")
        
        if choice == "1":
            results = vector_db.search(query, k=3)
            print("📋 Semantic Search Results:")
        else:
            results = vector_db.keyword_search(query, k=3)
            print("📋 Keyword Search Results:")
        
        if not results:
            print("❌ No results found.")
        else:
            for i, result in enumerate(results, 1):
                print(f"\n--- Result {i} (Score: {result['score']:.3f}) ---")
                print(f"📄 Text: {result['text'][:200]}...")
                if 'entities' in result['metadata']:
                    entities = result['metadata']['entities']
                    if entities:  # Check if entities list is not empty
                        print("🏥 Medical Entities Found:")
                        for entity in entities[:3]:  # Show first 3 entities
                            print(f"   • {entity['text']} ({entity['category']}) - {entity['confidence']*100:.1f}%")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    run_demo()
