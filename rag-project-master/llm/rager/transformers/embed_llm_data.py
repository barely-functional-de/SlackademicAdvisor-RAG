from typing import List, Tuple, Union

import numpy as np
import spacy

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def spacy_embeddings(
    document_data: List[dict],
    *args,
    **kwargs,
) -> Tuple[str, str, str, List[str], List[Union[float, int]]]:
    """
    Generate embeddings using SpaCy models.

    Args:
        document_data (Tuple[str, str, str, List[str]]):
            Tuple containing document_id, document_content, chunk_text, and tokens.

    Returns:
        Tuple[str, str, str, List[str], List[Union[float, int]]]:
            Tuple containing document_id, document_content, chunk_text, tokens, and embeddings.
    """
    data = []
    for document in document_data:
        document_id = document['document_id']
        #  Load SpaCy model
        nlp = spacy.load('en_core_web_sm')
        tokens = document['tokens']
        # combine tokens back into a string of text
        text = ' '.join(tokens)
        nlp_doc = nlp(text)
        # Average the word vectors in the doc to get a general embedding
        embedding = np.mean([token.vector for token in nlp_doc], axis=0).tolist()
        data.append(
            dict(
                chunk = document['chunk'],
                document_id = document_id,
                embedding = embedding
            )
        )

    return [data]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'