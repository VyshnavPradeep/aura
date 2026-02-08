import requests
url = "http://127.0.0.1:8000/upload/"
files = {"file": open("test_backend.zip", "rb")}
print("Uploading test_backend.zip...")
response = requests.post(url, files=files)
if response.status_code == 200:
    print("\n✅ Upload Successful!\n")
    data = response.json()
    print(f"Project ID: {data['project_id']}")
    print(f"\n--- Detection ---")
    print(f"Language: {data['detection']['language']} (Confidence: {data['detection']['confidence']:.2f})")
    print(f"Framework: {data['detection']['framework']}")
    print(f"Dependencies: {data['detection']['dependencies']}")
    print(f"\n--- Parsing ---")
    print(f"Files Parsed: {data['parsing']['files_parsed']}")
    print(f"Functions: {data['parsing']['total_functions']}")
    print(f"Classes: {data['parsing']['total_classes']}")
    print(f"Lines: {data['parsing']['total_lines']}")
    print(f"\n--- Embeddings ---")
    print(f"Chunks: {data['embeddings']['chunks_created']}")
    print(f"Index Created: {data['embeddings']['index_created']}")
    print("\n--- Full Response ---")
    import json
    print(json.dumps(data, indent=2))
else:
    print(f"❌ Upload Failed! Status: {response.status_code}")
    print(response.text)