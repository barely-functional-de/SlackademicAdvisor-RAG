import os
from tqdm.auto import tqdm
from elasticsearch import Elasticsearch, exceptions
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

def index_documents(es_client, documents, index_name):
    print("Indexing documents...")

    es_client = Elasticsearch(os.getenv("ELASTIC_URL"))  # Use ELASTIC_URL from environment variables
    MODEL_NAME = os.getenv('MODEL_NAME')
    model = SentenceTransformer(MODEL_NAME)
    
    successful_indexes = 0
    failed_indexes = 0

    for doc in tqdm(documents):
        # Ensure 'chunk' is a string
        chunk = doc["chunk"]
        if chunk is None:
            chunk = ""
        
        # Encode the chunk into a vector
        try:
            encoded_vector = model.encode(chunk).tolist()
            doc["question_answer_vector"] = encoded_vector

            try:
                response = es_client.index(index=index_name, id=doc['id'], document=doc)
                # Check if the document was successfully indexed
                if response.get('result') in ['created', 'updated']:
                    successful_indexes += 1
                else:
                    failed_indexes += 1
                    print(f"Failed to index document: {doc}")
            except exceptions.ElasticsearchException as e:
                failed_indexes += 1
                print(f"Exception occurred while indexing document: {doc}. Error: {e}")

        except Exception as e:
            failed_indexes += 1
            print(f"Error encoding document chunk: {chunk}. Error: {e}")
    
    print(f"Indexed {successful_indexes} documents successfully.")
    if failed_indexes > 0:
        print(f"Failed to index {failed_indexes} documents.")

    return {
        "successful_indexes": successful_indexes,
        "failed_indexes": failed_indexes,
    }
