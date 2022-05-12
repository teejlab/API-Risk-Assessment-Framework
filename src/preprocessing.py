# author: Harry Chan
# date: 2022-05-04
"""Reads train csv data from path, preprocess the data, and save the preprocessed data to path.
Usage: preprocessing.py --input_path=<input_path> --output_path=<output_path>
 
Options:
--input_path=<input_path>     Path to input data
--output_path=<output_path>   Path for preprocessed file to be saved
"""

from docopt import docopt
from sklearn.model_selection import train_test_split
import os
import pandas as pd
import sys

opt = docopt(__doc__)


def preprocessing(df):
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
    df.rename(columns={
        'security_test_result (FALSE=Passed; TRUE=Failed)': 'security_test_result',
        'risk_label_Baljeet': 'risk_label'
    }, inplace=True)
    # Drop the columns that are not needed
    df = df.drop(['response_metadata'], axis=1)  # To-be-modifited
    # Update the rows with duplicates
    df.loc[df['hosting_isp'] == 'Amazon Technologies Inc.',
           'hosting_isp'] = 'Amazon.com, Inc.'
    # Drop the rows with duplicates
    df = df.drop_duplicates()
    return df


def main(input_path, output_path):
    # Read the file
    df = pd.read_excel(input_path, "Core_Endpoint", usecols="A:R")

    # Preprocess the data
    df = preprocessing(df)

    # Output the preprocessed dataframe to a csv file
    try:
        df.to_csv(output_path + "/train.csv", index=False)
    except:
        os.makedirs(os.path.dirname(output_path))
        df.to_csv(output_path + "/train.csv", index=False)

    # Split the data into training and testing sets
    # train_df, test_df = train_test_split(df, test_size=0.3, random_state=123)
    # try:
    #     train_df.to_csv(output_path + "/train.csv", index=False)
    #     test_df.to_csv(output_path + "/test.csv", index=False)
    # except:
    #     os.makedirs(os.path.dirname(output_path))
    #     train_df.to_csv(output_path + "/train.csv", index=False)
    #     test_df.to_csv(output_path + "/test.csv", index=False)


if __name__ == "__main__":
    main(opt["--input_path"], opt["--output_path"])
