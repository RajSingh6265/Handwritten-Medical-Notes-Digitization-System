#!/usr/bin/env python3
"""
Simple Keyword Search Demo for Medical Notes
"""
from app.faiss_db import FAISSVectorDB

def keyword_search_demo():
    """Run a simple keyword search demo"""
    print("🏥 Medical Notes Keyword Search")
    print("="*50)
    
    # Load database
    vector_db = FAISSVectorDB()
    print(f"📊 Database loaded with {len(vector_db.documents)} documents\n")
    
    while True:
        # Get search query
        query = input("🔍 Enter keyword to search (or 'quit' to exit): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not query:
            print("❌ Please enter a search term.\n")
            continue
        
        # Perform keyword search
        print(f"\n🔍 Searching for: '{query}'...")
        results = vector_db.keyword_search(query, k=10)
        
        if not results:
            print("❌ No results found.\n")
        else:
            print(f"📋 Found {len(results)} results:\n")
            
            for i, result in enumerate(results, 1):
                print(f"--- Result {i} (Score: {result['score']:.3f}) ---")
                print(f"📄 File: {result['metadata']['filename']}")
                print(f"📝 Text: {result['text']}")
                
                # Show medical entities if available
                if 'entities' in result['metadata'] and result['metadata']['entities']:
                    print("🏥 Medical Entities:")
                    for entity in result['metadata']['entities'][:3]:
                        print(f"   • {entity['text']} ({entity['category']})")
                
                print()
        
        print("="*50)

if __name__ == "__main__":
    keyword_search_demo()