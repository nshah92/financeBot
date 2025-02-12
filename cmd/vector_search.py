import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
from sklearn.preprocessing import normalize
import faiss
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')

def generate_embeddings(text_list):
    return np.array(model.encode(text_list))

def create_faiss_index(embeddings):
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

def save_faiss_index(index, file_path):
    faiss.write_index(index, file_path)

def load_faiss_index(file_path):
    return faiss.read_index(file_path) if os.path.exists(file_path) else None

def search_faiss(index, texts, query_embedding, top_k=1, threshold=0.0):
    D, I = index.search(query_embedding, k=top_k)

    results = []
    for idx, i in enumerate(I[0]):
        if 0 <= i < len(texts):
            similarity_score = float(D[0][idx])

            if similarity_score >= threshold:
                results.append({
                    "text": texts[i][:300], 
                    "document_index": int(i), 
                    "score": similarity_score
                })

    if not results:
        results.append({"text": "I'm sorry, but I couldn't find any relevant financial data for your query.", "document_index": "N/A", "score": 0.0})

    return results