# 🏥 Handwritten Medical Notes Digitization System

A complete pipeline for digitizing handwritten medical notes using AWS Textract and providing intelligent search capabilities through a vector database and REST API.

## 📋 Overview

This project demonstrates a real-world solution for digitizing handwritten medical documents, extracting structured information, and providing fast search capabilities. It combines AWS cloud services with modern AI techniques to create a practical healthcare digitization tool.

## ✨ Features

- **📄 Document Digitization**: Converts handwritten notes to structured text using AWS Textracts
- **🧠 AI-Powered Search**: Semantic search using sentence transformers and FAISS vector database
- **🔍 Keyword Search**: Fast keyword-based document retrieval
- **🏥 Medical Entity Recognition**: Extracts medical terms, conditions, and medications
- **🚀 REST API**: FastAPI-based web service with interactive documentation
- **💻 CLI Interface**: Command-line tools for batch processing and search
- **🔒 Secure**: Environment-based AWS credential management

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Handwritten    │    │ AWS Textract │    │ Text Extraction │
│  Medical Notes  │───▶│   Service    │───▶│   & Cleaning    │
│  (Images/PDFs)  │    └──────────────┘    └─────────────────┘
└─────────────────┘                                 │
                                                    ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Search API    │    │ FAISS Vector│    │Medical Entity   │
│   (FastAPI)     │◀───│   Database   │◀───│  Recognition    │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

- **Cloud Service**: AWS Textract for OCR
- **Vector Database**: FAISS for semantic search
- **Web Framework**: FastAPI for REST API
- **AI/ML**: SentenceTransformers for embeddings
- **Database**: Local file-based storage with JSON metadata
- **Environment**: Python 3.13+ with virtual environment

## 📦 Installation

### Prerequisites
- Python 3.13+
- AWS Account with Textract access
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Handwritten
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   
   Create a `.env` file in the project root:
   ```env
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_REGION=us-east-1
   ```

   Or use AWS CLI:
   ```bash
   aws configure
   ```

## 🚀 Quick Start

### 1. Process Sample Images
```bash
python process_notes.py
```
This will:
- Extract text from all images in `data/images/`
- Store processed data in FAISS vector database
- Generate CSV export of all processed notes

### 2. Start the Web API
```bash
python main.py
```
- API will be available at `http://localhost:8000`
- Interactive documentation at `http://localhost:8000/docs`

### 3. Use CLI Search
```bash
python keyword_search.py
```
Interactive keyword search interface

### 4. Run Full Demo
```bash
python demo.py
```
Complete demo with both semantic and keyword search

## 📚 API Documentation

### Upload and Process Image
```http
POST /upload-image/
Content-Type: multipart/form-data

# Upload a handwritten note image for processing
```

### Search Notes
```http
POST /search/
Content-Type: application/json

{
    "query": "chest pain",
    "k": 5,
    "search_type": "semantic"  // or "keyword"
}
```

### Get Statistics
```http
GET /stats
# Returns database statistics and health info
```

## 📁 Project Structure

```
Handwritten/
├── app/
│   ├── __init__.py
│   ├── textract_service.py    # AWS Textract integration
│   └── faiss_db.py           # Vector database operations
├── data/
│   ├── images/               # Sample handwritten notes
│   └── processed/            # Processed data and indices
├── main.py                   # FastAPI web server
├── process_notes.py          # Batch processing script
├── demo.py                   # Interactive demo
├── keyword_search.py         # CLI search tool
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                # This file
```

## 🔧 Configuration Options

### TextractService Options
- Switch between real AWS Textract and Mock service
- Configure AWS region and credentials
- Adjust confidence thresholds

### FAISS Database Options
- Change embedding model (default: `all-MiniLM-L6-v2`)
- Adjust vector dimensions
- Modify search parameters

### API Configuration
- Custom host and port settings
- CORS configuration
- Rate limiting options

## 📊 Sample Data

The project includes 5 sample handwritten medical note images:
- Patient consultation notes
- Prescription records
- Emergency visit reports
- Routine checkup summaries
- Treatment plans

## 🧪 Testing the System

### Test with Sample Queries

**Keyword Search Examples:**
- `"chest pain"` - Find cardiac-related notes
- `"John Doe"` - Search by patient name
- `"medication"` - Find prescription information
- `"blood pressure"` - Locate vital signs

**Semantic Search Examples:**
- `"heart problems"` - Finds related cardiac issues
- `"breathing difficulties"` - Matches respiratory symptoms
- `"drug prescription"` - Finds medication records

## 🚨 Error Handling

The system includes comprehensive error handling:
- AWS service connection issues
- Invalid image formats
- Missing credentials
- Database corruption recovery
- API request validation

## 🔐 Security Considerations

- **Credentials**: Store AWS credentials in `.env` file (never commit)
- **Data Privacy**: Medical data stays local unless using cloud storage
- **API Security**: Input validation and sanitization
- **Access Control**: Configure AWS IAM permissions properly

## 📈 Performance Optimization

- **Batch Processing**: Process multiple images efficiently
- **Vector Indexing**: FAISS provides sub-second search times
- **Caching**: Embedding models cached for faster processing
- **Memory Management**: Optimized for large document collections

## 🐛 Troubleshooting

### Common Issues

**AWS Textract Subscription Error**
```
SubscriptionRequiredException: The AWS Access Key Id needs a subscription for the service
```
- Ensure AWS account has Textract enabled
- Use `MockTextractService` for development
- Check AWS IAM permissions

**Import Errors**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Empty Search Results**
- Verify documents are processed: `python inspect_db.py`
- Check search keywords match document content
- Try semantic search for better matching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request



## 🙏 Acknowledgments

- AWS Textract for OCR capabilities
- Sentence Transformers for semantic embeddings
- FAISS for efficient vector search
- FastAPI for the web framework



---

**Built with ❤️ for healthcare digitization**
