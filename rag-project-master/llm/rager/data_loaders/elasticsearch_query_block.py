import os
from tqdm.auto import tqdm
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

load_dotenv()

# openai.api_key = os.getenv('OPENAI_API_KEY')
ELASTIC_URL = os.getenv('ELASTIC_URL')
INDEX_NAME = os.getenv('INDEX_NAME')
MODEL_NAME = os.getenv('MODEL_NAME')
model = SentenceTransformer(MODEL_NAME)

es_client = Elasticsearch(ELASTIC_URL)


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    search_term = "How to create saturn cloud account?"
    vector_search_term = model.encode(search_term)

    query = {
    "field": "question_answer_vector",
    "query_vector": vector_search_term,
    "k": 3,
    "num_candidates": 10000, 
    }

    res = es_client.search(index=INDEX_NAME, knn=query, source=["id", "answer", "question", "course"])
    
    results = res["hits"]["hits"]

    for result in results:
        print(result)



    return [res["hits"]["hits"]]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'