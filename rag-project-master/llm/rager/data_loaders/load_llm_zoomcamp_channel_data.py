import pandas as pd
from llm.utils.helpers.load_channel_helpers import (
    read_json_files,
    process_messages,
    create_dataframe,
    load_existing_metadata,
    update_metadata,
    scan_for_new_files
)
# from llm.rager.data_loaders import load_helpers 

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    metadata_file = kwargs['metadata_file']
    data_path = kwargs['data_path']
    processed_files = load_existing_metadata(metadata_file)
    print(f'processed files: {processed_files}')
    new_files = scan_for_new_files(data_path, processed_files)
    
    if not new_files:
        print("No new files to process.")
        return pd.DataFrame()
    if new_files:
        print(f'new_files: {new_files}')
    
    data = read_json_files(new_files)
    ids, questions, question_askers, question_timestamps, answers, answered_by, answer_timestamps = process_messages(data)
    df = create_dataframe(ids, questions, question_askers, question_timestamps, answers, answered_by, answer_timestamps)
    
    processed_files.extend(new_files)
    update_metadata(processed_files, metadata_file)


    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'