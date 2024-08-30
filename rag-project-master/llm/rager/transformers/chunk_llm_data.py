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
   # Check if 'data' contains the 'empty': 'True' marker
    is_data_empty = data.shape[0] == 1 and data.iloc[0].to_dict() == {'empty': 'True'}
    
    # Check if 'data_2' contains the 'empty': 'True' marker
    is_data_2_empty = data_2.shape[0] == 1 and data_2.iloc[0].to_dict() == {'empty': 'True'}
    
    # Raise an error if both DataFrames contain the 'empty': 'True' marker
    if is_data_empty and is_data_2_empty:
        raise ValueError("No new data available in both dataframes.")

    # Process the data if it does not contain the 'empty': 'True' marker
    if not is_data_empty:
        llm_faq_df = data[['id', 'question', 'answer', 'course']]
    else:
        llm_faq_df = pd.DataFrame()  # Assign empty DataFrame if 'data' contains 'empty': 'True'

    if not is_data_2_empty:
        llm_channel_df = data_2[['id', 'question', 'answer']]
        llm_channel_df['course'] = 'llm-zoomcamp'
    else:
        llm_channel_df = pd.DataFrame()  # Assign empty DataFrame if 'data_2' contains 'empty': 'True'

    # Combine the DataFrames
    combined_df = pd.concat([llm_faq_df, llm_channel_df], ignore_index=True)
    
    # Apply function to create chunks (Assuming `create_chunk` is defined elsewhere)
    combined_df['chunk'] = combined_df.apply(create_chunk, axis=1)
    
    # Convert to dictionary format
    combined_df_dict = combined_df.to_dict(orient='records')




    return [combined_df_dict]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'