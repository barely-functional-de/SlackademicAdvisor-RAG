import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, exceptions

from llm.utils.helpers.index_document_helper import (
    index_documents
)

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

load_dotenv()

@data_exporter
def export_data(es_client_status, documents, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    if es_client_status:
        INDEX_NAME = os.getenv('INDEX_NAME')
        ELASTIC_URL = os.getenv('ELASTIC_URL')
        es_client = Elasticsearch(ELASTIC_URL)
        # for doc in documents:
        #     print(doc['id'], type(doc['chunk']))
        index_pass_fail = index_documents(es_client, documents, INDEX_NAME)
        if index_pass_fail['failed_indexes'] != 0:
            raise Exception("Failed to lead all the indexes successfully. BLock halted")

    else:
        # Raise an exception to stop the block execution
        raise Exception("Failed to create Elasticsearch client. Block execution halted.")

