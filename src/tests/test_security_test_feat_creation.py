from utils.security_test_feat_creation import security_test_feat_creation
import pandas as pd
from pytest import raises

def test_wrong_parameters():
    # Test if the function raises an error when the df is not a dataframe
    with raises(TypeError):
        security_test_feat_creation("raw_text")

    with raises(TypeError):
        security_test_feat_creation(123)

    with raises(TypeError):
        security_test_feat_creation(False)

    with raises(TypeError):
        security_test_feat_creation(None)