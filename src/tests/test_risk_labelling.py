from utils.risk_labelling import classify_risk, create_risk_label
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

    # Test if the function raises an error when the df is not a dataframe
    with raises(TypeError):
        create_risk_label("raw_text")

    with raises(TypeError):
        create_risk_label(123)

    with raises(TypeError):
        create_risk_label(False)

    with raises(TypeError):
        create_risk_label(None)