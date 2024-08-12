import os
from dotenv import load_dotenv

from llm.utils.helpers.setup_elasticsearch_helper import (
    setup_elasticsearch
)


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

load_dotenv()

@data_exporter
def export_data(*args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    INDEX_NAME = os.getenv('INDEX_NAME')
    ELASTIC_URL = os.getenv('ELASTIC_URL')
    es_client = setup_elasticsearch(INDEX_NAME, ELASTIC_URL)

    # Check if the index already exists
    index_exists = es_client.indices.exists(index=INDEX_NAME)
    # Specify your data exporting logic here
    return {"status": "success" if index_exists else "failure"}

