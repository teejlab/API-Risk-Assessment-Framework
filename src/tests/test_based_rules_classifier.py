from utils.based_rules_classifier import classify_risk
import pandas as pd
from pytest import raises

def test_wrong_parameters():
    # Test if the function raises an error when the df is not a dataframe
    with raises(TypeError):
        classify_risk("raw_text")

    with raises(TypeError):
        classify_risk(123)

    with raises(TypeError):
        classify_risk(False)

    with raises(TypeError):
        classify_risk(None)