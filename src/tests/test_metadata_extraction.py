from utils.metadata_extraction import extract_metadata
import pandas as pd
from pytest import raises

def test_wrong_parameters():
    # Test if the function raises an error when the df is not a dataframe
    with raises(TypeError):
        extract_metadata("raw_text")

    with raises(TypeError):
        extract_metadata(123)

    with raises(TypeError):
        extract_metadata(False)

    with raises(TypeError):
        extract_metadata(None)