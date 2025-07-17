#!/usr/bin/env python3
"""Test script for Docker-based document processing system."""

import requests
import json
import os
import time
from pathlib import Path

def test_api_health():
    """Test if the API is responding."""
    try:
        response = requests.get("http://localhost:8000/")
        return response.status_code == 200
    except:
        return False

def test_database_connections():
    """Test database connections."""
    try:
        response = requests.get("http://localhost:8000/api/health/databases")
        return response.status_code == 200
    except:
        return False

def upload_test_file(file_path: str, file_type: str):
    """Upload a test file."""
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'file_type': file_type}
            response = requests.post(
                "http://localhost:8000/api/ingestion/upload",
                files=files,
                data=data
            )
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, str(e)

def query_processed_data(query: str):
    """Query the processed data."""
    try:
        response = requests.post(
            "http://localhost:8000/api/knowledge/search",
            json={"query": query, "limit": 5}
        )
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, str(e)

def main():
    """Run comprehensive tests."""
    print("🐳 Testing Docker-based Document Processing System")
    print("=" * 60)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    for i in range(30):
        if test_api_health():
            print("✅ API is responding")
            break
        time.sleep(2)
    else:
        print("❌ API failed to respond after 60 seconds")
        return
    
    # Test database connections
    print("\n🔍 Testing database connections...")
    if test_database_connections():
        print("✅ Database connections successful")
    else:
        print("❌ Database connection failed")
    
    # Create test files
    print("\n📁 Creating test files...")
    test_data_dir = Path("test_data")
    test_data_dir.mkdir(exist_ok=True)
    
    test_files = {
        "test_data/sample.json": {
            "title": "Sample Document",
            "content": "This is a test JSON document with sample data.",
            "metadata": {"source": "test", "created": "2023-01-01"}
        },
        "test_data/sample.csv": "name,value,category\nItem1,100,A\nItem2,200,B\nItem3,300,C",
        "test_data/sample.md": "# Test Document\n\nThis is a **test** markdown document.\n\n## Features\n- Item 1\n- Item 2",
        "test_data/sample.txt": "This is a plain text document for testing the system."
    }
    
    for file_path, content in test_files.items():
        with open(file_path, 'w') as f:
            if file_path.endswith('.json'):
                json.dump(content, f)
            else:
                f.write(content)
    
    # Test file uploads
    print("\n📤 Testing file uploads...")
    uploaded_files = []
    
    for file_path in test_files.keys():
        file_type = file_path.split('.')[-1]
        success, result = upload_test_file(file_path, file_type)
        
        if success:
            print(f"✅ Uploaded {file_path}")
            uploaded_files.append(result)
        else:
            print(f"❌ Failed to upload {file_path}: {result}")
    
    # Wait for processing
    print("\n⏳ Waiting for document processing...")
    time.sleep(10)
    
    # Test queries
    print("\n🔍 Testing search queries...")
    test_queries = [
        "What is the content about?",
        "Find information about items and values",
        "What are the key features mentioned?",
        "Show me test data"
    ]
    
    for query in test_queries:
        success, result = query_processed_data(query)
        
        if success:
            print(f"✅ Query '{query}': Found {len(result.get('results', []))} results")
        else:
            print(f"❌ Query '{query}' failed: {result}")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main() 