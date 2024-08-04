import pandas as pd
from llm.utils.helpers.chunk_helpers import create_chunk

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    # Combine the DataFrames
    llm_faq_df = data[['id', 'Question', 'Answer', 'Course']]
    llm_channel_df = data_2[['id', 'Question', 'Answer', 'Course']]
    llm_channel_df['Course'] = 'llm-zoomcamp'
    combined_df = pd.concat([llm_faq_df, llm_channel_df], ignore_index=True)
    # Apply function to create chunks
    combined_df['Chunk'] = combined_df.apply(create_chunk, axis=1)

    return combined_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'