from rag import rag_engine
import os


file_path = r"../data/cv.pdf"  # or "data/cv.pdf" with forward slashes
filename = "cv.pdf"

# Check if file exists before testing
if not os.path.exists(file_path):
    print(f" File not found: {file_path}")
    print(" Make sure to put a PDF in the data/ folder")
    exit()

print(" Starting RAG Engine Test...\n")

# Test 1: Ingestion
print("Ingesting document...")
chunks = rag_engine.ingest_file(file_path, filename, doc_id=1)
print(f" Created {chunks} chunks\n")

# Test 2: Search
print(" Testing search...")
results = rag_engine.search("give the experience of this cv profile and most interesting project  ?", k=3)
print(f" Found {len(results)} results\n")

# Test 3: Generation
print(" Generating answer...")
if results:
    context = "\n\n".join([r['content'] for r in results])
    answer = rag_engine.generate_answer("What is this document about?", context)
    print(f" Answer: {answer}\n")
else:
    print("  No results to generate answer from")

print(" tests completed!")