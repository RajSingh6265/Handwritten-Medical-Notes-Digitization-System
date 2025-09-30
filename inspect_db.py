#!/usr/bin/env python3
"""
Quick script to inspect the FAISS database content
"""
from app.faiss_db import FAISSVectorDB

def inspect_database():
    # Load the database
    vector_db = FAISSVectorDB()
    
    print(f"📊 Database has {len(vector_db.documents)} documents")
    print("="*50)
    
    # Show each document
    for i, (doc, meta) in enumerate(zip(vector_db.documents, vector_db.metadata)):
        print(f"\n📄 Document {i+1}:")
        print(f"Text: {doc[:200]}...")
        print(f"Metadata: {meta}")
        print("-" * 30)

if __name__ == "__main__":
    inspect_database()