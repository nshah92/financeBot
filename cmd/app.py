from flask import Flask, request, jsonify, render_template
import vector_search
import graph_search
import pickle
import numpy as np
from py2neo import Graph, Node

app = Flask(__name__)

def load_index(index_path):
    return vector_search.load_faiss_index(index_path)

def load_texts(text_path):
    with open(text_path, "rb") as f:
        return pickle.load(f)

pdf_index = load_index("generated/pdf_index.bin")
pdf_texts = load_texts("generated/pdf_texts.pkl")
pptx_index = load_index("generated/pptx_index.bin")
pptx_texts = load_texts("generated/pptx_texts.pkl")
csv_index = load_index("generated/csv_index.bin")
csv_texts = load_texts("generated/csv_texts.pkl")

graph = Graph("bolt://localhost:7687", auth=("neo4j", "admin123"))

@app.route('/api/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query')

    query_embedding = vector_search.generate_embeddings([user_query])
    
    pdf_results = vector_search.search_faiss(pdf_index, pdf_texts, query_embedding)
    pptx_results = vector_search.search_faiss(pptx_index, pptx_texts, query_embedding)
    csv_results = vector_search.search_faiss(csv_index, csv_texts, query_embedding)

    neo4j_results = []
    neo4j_results = graph_search.search_neo4j(user_query)

    results = pdf_results + neo4j_results + pptx_results + csv_results

    for result in results:
        if isinstance(result.get("document_index"), (np.int64, np.int32)):
            result["document_index"] = int(result["document_index"])

    ranked_results = rank_results(user_query, results)  

    return jsonify({"response": ranked_results})

def rank_results(query, results):
    for result in results:
        if "score" not in result:  
            result["score"] = 0.0
    
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results[:10]

@app.route('/')
def index():
    return "Welcome to the Financial Chatbot API! Use POST /api/chat for queries."

if __name__ == '__main__':
    app.run(debug=True)
