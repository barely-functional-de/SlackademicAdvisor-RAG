import pandas as pd
from llm.utils.helpers.load_faq_helpers import (
    load_json,
    generate_id,
    add_id_column,
    read_metadata,
    update_metadata,
    filter_new_entries
)

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
    filename = kwargs['faq_data_path']
    faq_metadata_file = kwargs['faq_metadata_file']
    data = load_json(filename)
    data_with_ids = add_id_column(data)
    new_entries = filter_new_entries(data_with_ids, faq_metadata_file)
    if new_entries:
        print(f"{len(new_entries)} new entries")
        new_entries_df = pd.DataFrame(new_entries)
        update_metadata(new_entries, faq_metadata_file)
    else:
        # raise Exception('No new entry to FAQ file added')
        new_entries_df = pd.DataFrame([{'empty': 'True'}])

    return new_entries_df



# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'