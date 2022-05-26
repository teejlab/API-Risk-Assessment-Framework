# author:
# date:
"""Reads train csv data from path, preprocess the data, and save the preprocessed data to path.
Usage: preprocessing.py --input_path=<input_path> --input_path_country=<input_path_country> --output_path=<output_path>
 
Options:
--input_path=<input_path>                    Path to input data
--input_path_country=<input_path_country>    Path to input country metric data
--output_path=<output_path>                  Path for preprocessed file to be saved

Example:
python src/preprocessing.py --input_path=data/raw/RiskClassification_Data_Endpoints_V4_Shared1.xlsx --input_path_country=data/raw/nri_2021_dataset.xlsx --output_path=data/processed/
"""

from docopt import docopt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from utils.add_country_and_cat_feats import add_country_and_cat_feats
from utils.metadata_extraction import extract_metadata
from utils.pii_extraction import pii_extraction
from utils.security_test_feat_creation import security_test_feat_creation
import os
import pandas as pd
import sys
import re

opt = docopt(__doc__)
def main(input_path, input_path_country, output_path):
    # Read the file
    df = pd.read_excel(input_path, "Core_Endpoint", usecols="A:S")
    # Rename the columns
    df.rename(
        columns={
            "security_test_result (FALSE=Passed; TRUE=Failed)": "security_test_result"
        },
        inplace=True,
    )

    # Add Columns for PII and FII
    df["is_pii"] = df["sample_response"].apply(pii_extraction, args=("pii", 0.5,)).astype(bool)
    df["is_fii"] = df["sample_response"].apply(pii_extraction, args=("fii", 0.5,)).astype(bool)

    # save df with pii and fii
    df.to_excel(output_path + "/df_fii_pii.xlsx", index=False)

    # Add country score and OHE categories
    df = add_country_and_cat_feats(df, input_path_country)
    df.to_excel(output_path + "/df_country_score.xlsx", index=False)


    # Add Security test features
    df = security_test_feat_creation(df)
    df.to_excel(output_path + "/df_security.xlsx", index=False)

    df = extract_metadata(df)

    df.to_excel(output_path + "/df_metadata.xlsx", index=False)

    # Split the data into training and testing sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)
    try:
        train_df.to_csv(output_path + "/train.csv", index=False)
        test_df.to_csv(output_path + "/test.csv", index=False)
    except:
        os.makedirs(os.path.dirname(output_path))
        train_df.to_csv(output_path + "/train.csv", index=False)
        test_df.to_csv(output_path + "/test.csv", index=False)


if __name__ == "__main__":
    main(opt["--input_path"], opt["--input_path_country"], opt["--output_path"])
