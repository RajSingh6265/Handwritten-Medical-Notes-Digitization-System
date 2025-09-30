from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List, Dict, Optional
from pydantic import BaseModel
import uvicorn
import pandas as pd

from app.textract_service import MockTextractService  # Use TextractService for real AWS
from app.faiss_db import FAISSVectorDB

app = FastAPI(title="Handwritten Notes Digitization API", version="1.0.0")

# Initialize services
textract_service = MockTextractService()  # Switch to TextractService() when you have AWS credentials
vector_db = FAISSVectorDB()

class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 5
    search_type: Optional[str] = "semantic"  # "semantic" or "keyword"

class SearchResponse(BaseModel):
    results: List[Dict]
    total_found: int
    query: str

@app.get("/")
async def root():
    return {"message": "Handwritten Notes Digitization API", "status": "running"}

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    stats = vector_db.get_stats()
    return {"database_stats": stats}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """Upload and process a handwritten note image"""
    try:
        # Save uploaded file
        upload_dir = "data/images"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text using Textract
        extraction_result = textract_service.extract_text_from_image(file_path)
        
        if not extraction_result['success']:
            raise HTTPException(status_code=500, detail=f"Text extraction failed: {extraction_result.get('error')}")
        
        # Extract medical entities
        entities = textract_service.extract_medical_entities(extraction_result['text'])
        
        # Add to vector database
        metadata = {
            'filename': file.filename,
            'confidence': extraction_result['confidence'],
            'entities': entities,
            'upload_timestamp': str(pd.Timestamp.now())
        }
        
        doc_id = vector_db.add_document(extraction_result['text'], metadata)
        vector_db.save_index()
        
        return {
            "success": True,
            "document_id": doc_id,
            "extracted_text": extraction_result['text'],
            "confidence": extraction_result['confidence'],
            "entities": entities
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/", response_model=SearchResponse)
async def search_notes(request: SearchRequest):
    """Search through digitized notes"""
    try:
        if request.search_type == "keyword":
            results = vector_db.keyword_search(request.query, request.k)
        else:
            results = vector_db.search(request.query, request.k)
        
        return SearchResponse(
            results=results,
            total_found=len(results),
            query=request.query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/keyword/{keyword}")
async def search_by_keyword(keyword: str, k: int = 5):
    """Quick keyword search endpoint"""
    try:
        results = vector_db.keyword_search(keyword, k)
        return {"results": results, "total_found": len(results), "keyword": keyword}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

