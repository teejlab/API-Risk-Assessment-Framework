# author:
# date:
"""Reads train csv data from path, preprocess the data, and save the preprocessed data to path.
Usage: preprocessing.py --input_path=<input_path> --input_path_country=<input_path_country> --output_path=<output_path>
 
Options:
--input_path=<input_path>                    Path to input data
--input_path_country=<input_path_country>    Path to input country metric data
--output_path=<output_path>                  Path for preprocessed file to be saved
"""

from docopt import docopt
from sklearn.model_selection import train_test_split
from utils.pii_extraction import pii_extraction
import os
import pandas as pd
import sys

opt = docopt(__doc__)


def preprocessing(df, country_metric_df):
    """Read the file, and preprocess the data.
    Parameters
    ----------
    df : Pandas Dataframe
        The file to be preprocessed
    Returns
    -------
    preprocessed_df : Pandas Dataframe
        A preprocessed dataframe
    """
    # Rename the columns
    df.rename(
        columns={
            "security_test_result (FALSE=Passed; TRUE=Failed)": "security_test_result",
            "risk_label_Baljeet": "risk_label",
        },
        inplace=True,
    )
    # Merge country_metric data with input data
    df = df.merge(
        country_metric_df, left_on="server_location", right_on="Country", how="left"
    )
    # Drop the columns that are not needed
    df = df.drop(["server_location"], axis=1)
    # Update the rows with duplicates
    df.loc[df["hosting_isp"] == "Amazon.com, Inc.", "hosting_isp"] = "Amazon.com"
    df.loc[
        df["hosting_isp"] == "Amazon Technologies Inc.", "hosting_isp"
    ] = "Amazon.com"
    df.loc[
        df["hosting_isp"] == "Akamai International B.V.", "hosting_isp"
    ] = "Akamai Technologies, Inc."
    df.loc[
        df["hosting_isp"] == "Akamai International, BV", "hosting_isp"
    ] = "Akamai Technologies, Inc."

    # Authentication column
    authentication_list = df.authentication.unique().tolist()
    authentication_mapper = {}
    for variable in authentication_list:
        if variable == "none":
            authentication_mapper[variable] = 0
        else:
            authentication_mapper[variable] = 1
    df['authentication'] = df['authentication'].replace(authentication_mapper)
    
    # Usage Base
    usagebase_list = df.usage_base.unique().tolist()
    usagebase_mapper = {}
    for variable in usagebase_list:
        if variable == "commercial":
            usagebase_mapper[variable] = 0
        else:
            usagebase_mapper[variable] = 1
    df['usage_base'] = df['usage_base'].replace(usagebase_mapper)
    
    # Drop the rows with duplicates
    df = df.drop_duplicates()
    return df


def main(input_path, input_path_country, output_path):
    # Read the file
    df = pd.read_excel(input_path, "Core_Endpoint", usecols="A:R")

    # Read country metric data
    country_metric_df = pd.read_excel(
        input_path_country, "NRI 2021 - results", usecols="B:C", skiprows=1
    )
    # To-be-modified once we decide which metrics to use, presently, just the overall score

    # Add Columns for PII and FII
    df["is_pii"] = df["sample_response"].apply(pii_extraction, args=("pii", 0.5,)).astype(str)
    df["is_fii"] = df["sample_response"].apply(pii_extraction, args=("fii", 0.5,)).astype(str)

    # Preprocess the data
    df = preprocessing(df, country_metric_df)

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
