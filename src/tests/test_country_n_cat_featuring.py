from utils.country_n_cat_featuring import add_country_and_cat_feats
import pandas as pd
from pytest import raises

def test_wrong_parameters():
    # Test if the function raises an error when the df is not a dataframe
    with raises(TypeError):
        add_country_and_cat_feats("raw_text")

    with raises(TypeError):
        add_country_and_cat_feats(123)

    with raises(TypeError):
        add_country_and_cat_feats(False)

    with raises(TypeError):
        add_country_and_cat_feats(None)