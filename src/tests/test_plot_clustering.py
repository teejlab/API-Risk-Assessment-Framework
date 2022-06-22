from utils.plot_clustering import plot_clustering
import pandas as pd
from pytest import raises


def test_wrong_parameters():
    # Test if the function raises an error when the df is not a dataframe
    with raises(TypeError):
        plot_clustering("raw_text")

    with raises(TypeError):
        plot_clustering(123)

    with raises(TypeError):
        plot_clustering(False)

    with raises(TypeError):
        plot_clustering(None)