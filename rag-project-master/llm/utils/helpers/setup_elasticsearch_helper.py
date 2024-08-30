import os
from elasticsearch import Elasticsearch, exceptions
from dotenv import load_dotenv

load_dotenv()

def setup_elasticsearch(INDEX_NAME, ELASTIC_URL):
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)
    

    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "answer": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"},
                "id": {"type": "keyword"},
                "question_answer_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    # Check if the index already exists
    if es_client.indices.exists(index=INDEX_NAME):
        # es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
        # es_client.indices.create(index=INDEX_NAME, body=index_settings)
        print(f"Elasticsearch index '{INDEX_NAME}' already exists")
    else:
        es_client.indices.create(index=INDEX_NAME, body=index_settings)
        print(f"Elasticsearch index '{INDEX_NAME}' created")
    
    return es_client
