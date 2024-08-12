import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

load_dotenv()


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Model: Selected model for indexing documents)
    """
    # Specify your data loading logic here
    MODEL_NAME = os.getenv("MODEL_NAME")    
    return [MODEL_NAME, data]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'