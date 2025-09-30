import os
import glob
from app.textract_service import MockTextractService
from app.faiss_db import FAISSVectorDB
import pandas as pd

def process_all_images():
    """Process all images in the data/images directory"""
    
    # Initialize services
    # Try us-east-1 region which has full Textract support
    textract_service = MockTextractService()
    vector_db = FAISSVectorDB()
    
    # Get all image files
    image_files = glob.glob("data/images/*.png") + glob.glob("data/images/*.jpg") + glob.glob("data/images/*.jpeg")
    
    processed_data = []
    
    print(f"Found {len(image_files)} images to process...")
    
    for image_path in image_files:
        print(f"Processing: {image_path}")
        
        # Extract text
        result = textract_service.extract_text_from_image(image_path)
        
        if result['success']:
            # Extract medical entities
            entities = textract_service.extract_medical_entities(result['text'])
            
            # Add to vector database
            metadata = {
                'filename': os.path.basename(image_path),
                'confidence': result['confidence'],
                'entities': entities,
                'processing_timestamp': str(pd.Timestamp.now())
            }
            
            doc_id = vector_db.add_document(result['text'], metadata)
            
            processed_data.append({
                'document_id': doc_id,
                'filename': os.path.basename(image_path),
                'text': result['text'],
                'confidence': result['confidence'],
                'entities': entities
            })
            
            print(f"✅ Processed {os.path.basename(image_path)}")
        else:
            print(f"❌ Failed to process {image_path}: {result.get('error')}")
    
    # Save the vector database
    vector_db.save_index()
    
    # Save processed data as CSV
    if processed_data:
        df = pd.DataFrame(processed_data)
        df.to_csv("data/processed/processed_notes.csv", index=False)
        print(f"✅ Saved {len(processed_data)} processed notes to CSV")
    
    print(f"✅ Processing complete! {len(processed_data)} documents added to vector database")
    return processed_data

if __name__ == "__main__":
    import pandas as pd
    process_all_images()
