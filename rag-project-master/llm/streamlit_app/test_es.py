import os
from elasticsearch import Elasticsearch
from assistant import get_answer

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
es_client = Elasticsearch(ELASTIC_URL)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = os.getenv('INDEX_NAME')

# Test connection
try:
    es_client.ping()
    print("Elasticsearch is connected!")
except Exception as e:
    print("Failed to connect to Elasticsearch:", str(e))


def test_get_answer():
    query = "How to create a Saturn account?"
    course = "llm-zoomcamp"
    model_choice = "openai/gpt-3.5-turbo"  # Replace with your model choice

    try:
        print('calling get_answer()')
        result = get_answer(query, course, model_choice)
        print("Result:", result)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    test_get_answer()
