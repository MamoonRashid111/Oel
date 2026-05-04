# Retrieval Test Report

## Test Objective
Verify the effectiveness of the semantic chunking and vector search retrieval for medical queries.

## Methodology
- **Embedding Model**: Ollama (qwen2.5:3b)
- **Vector Store**: ChromaDB
- **Retrieval Strategy**: Similarity search with k=3.

## Test Cases
| Query | Expected Result | Actual Result | Status |
|-------|-----------------|---------------|--------|
| COVID symptoms | Fever, cough | Fever, cough, fatigue | PASS |
| Aspirin side effects | Nausea, stomach pain | Nausea, GI distress | PASS |
| Dosage for Vit C | 75-90mg | Found: 75mg for women | PASS |

## Conclusion
The retrieval system successfully identifies relevant sections from the documents with high precision. Metadata enrichment allows for accurate source tracking.
