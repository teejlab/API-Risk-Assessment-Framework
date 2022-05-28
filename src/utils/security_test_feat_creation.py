# Import dependencies
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import make_pipeline

def security_test_feat_creation(df):
    """
    Create security test features.
    Parameters
    ----------
    df : pandas dataframe
        The text to be analyzed.
    Returns
    -------
    transformed_df : pandas df
        A list containing the extracted PII.
    """
    # SETTING-UP pre-processor variables
    # Define column types
    categorical_features = ["security_test_category"]
    ordinal_features = ["security_test_result"]
    # passthrough_features is the list of columns in df 
    # minus the categorical and ordinal features
    passthrough_features = [
        feature for feature in df.columns 
        if feature not in ordinal_features
    ]
    # Define levels for ordinal encoder
    test_result_levels = [
        0.0,
        0.5,
        1.0
    ]
    # Define transformers
    categorical_transformer = make_pipeline(
        SimpleImputer(strategy="constant", fill_value="Missing"),
        OneHotEncoder(handle_unknown="ignore", sparse=False),
    )
    ordinal_transformer = make_pipeline(
        SimpleImputer(strategy="constant", fill_value=0.5),
        OrdinalEncoder(categories=[test_result_levels], dtype=int)
    )
    # Build preprocessor
    preprocessor = make_column_transformer(
        ("passthrough", passthrough_features),
        (ordinal_transformer, ordinal_features),
        (categorical_transformer, categorical_features),
    )

    # Create security test features
    preprocessor.fit(df)
    transformed = preprocessor.transform(df)

    # Get column names
    ohe_features = list(preprocessor.named_transformers_['pipeline-2'].named_steps['onehotencoder'].get_feature_names())
    feature_names = passthrough_features + ordinal_features + ohe_features

    transformed_df = pd.DataFrame(transformed, columns=feature_names)

    transformed_df = transformed_df.drop_duplicates()
    return transformed_df