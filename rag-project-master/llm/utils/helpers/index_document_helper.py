from tqdm.auto import tqdm

def index_documents(es_client, documents, model):
    print("Indexing documents...")
    for doc in tqdm(documents):
        chunk = doc["chunk"]
        doc["question_answer_vector"] = model.encode(chunk).tolist()
        es_client.index(index=INDEX_NAME, document=doc)
    print(f"Indexed {len(documents)} documents")