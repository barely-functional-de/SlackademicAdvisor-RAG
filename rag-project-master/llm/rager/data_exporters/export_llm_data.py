from typing import Dict, List, Tuple, Union

import numpy as np
from elasticsearch import Elasticsearch

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def elasticsearch(
    documents: List[Dict[str, Union[Dict, List[int], np.ndarray, str]]], *args, **kwargs,
):
    """
    Exports document data to an Elasticsearch database.
    """

    connection_string = kwargs.get('connection_string', 'http://localhost:9300')
    index_name = kwargs.get('index_name', 'documents')
    number_of_shards = kwargs.get('number_of_shards', 1)
    number_of_replicas = kwargs.get('number_of_replicas', 0)
    dimensions = kwargs.get('dimensions')

    if dimensions is None and len(documents) > 0:
        document = documents[0]
        dimensions = len(document.get('embedding') or [])

    es_client = Elasticsearch(connection_string)

    print(f'Connecting to Elasticsearch at {connection_string}')
    print(f"connection_string: {connection_string}\nindex_name:{index_name}\ndimensions:{dimensions}")

    index_settings = {
        "settings": {
            "number_of_shards": number_of_shards,
            "number_of_replicas": number_of_replicas,
        },
        "mappings": {
            "properties": {
                "chunk": {"type": "text"},
                "document_id": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": dimensions}
            }
        }
    }

    # Check if the index exists, and create it if it doesn't
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, body=index_settings)
        print('Index created with properties:')
        print(json.dumps(index_settings, indent=2))
    else:
        print(f'Index {index_name} already exists')

    # print('Embedding dimensions:', dimensions)

    # count = len(documents)
    # print(f'Indexing {count} documents to Elasticsearch index {index_name}')
    # for idx, document in enumerate(documents):
    #     if idx % 100 == 0:
    #         print(f'{idx + 1}/{count}')

    #     if isinstance(document['embedding'], np.ndarray):
    #         document['embedding'] = document['embedding'].tolist()

    #     es_client.index(index=index_name, document=document)

    # return [[d['embedding'] for d in documents[:10]]]