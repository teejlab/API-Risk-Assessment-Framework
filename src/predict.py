"""
This script trains ML model on the pre-processed train data.
The train files must be named X_train.csv and y_train.csv

Usage: predict.py --model_path=<model_path> --test_path=<test_path> --save_path=<save_path>

Options:
--model_path=<model_path>            The path to the model
--test_path=<test_path>              The path to the test csv files.
--save_path=<save_path>              The folder to save the model results to

Example:
python src/predict.py --model_path=data/model/model.joblib --test_path=data/processed/test_essentials.xlsx --save_path=data/processed/
"""

from docopt import docopt
from pathlib import Path
import pandas as pd
import numpy as np
from joblib import dump, load

opt = docopt(__doc__)

def load_model(path):
    """
    Loads the .joblib file at the given path.
    Parameters
    -----------
    path : string
        The path to the .joblib file containing the model.
    Returns
    -----------
    The loaded model object
    """
    print(f'Loading model from {path}...')
    return load(path)


def main(model_path, test_path, save_path):
    pipe_lr_tuned = load_model(model_path)

    # X, y split for test-set
    test_df = pd.read_excel(test_path)
    X_test, y_test = test_df.drop(columns=["Risk_Label"]), test_df["Risk_Label"]
    X_testselect = X_test[['is_pii', 'is_fii', 'authentication_processed', 'Information & Science',
                           'x0_Broken Authentication', 'x0_Missing', 'server', 'metadata_fields_count']]
    print(f'Predicting on test set...')
    y_pred = pipe_lr_tuned.predict(X_testselect)
    # put the predicted labels in a dataframe
    test_df['Risk_Label'] = y_pred

    # save the test data with the predicted labels
    test_df.to_excel(save_path + 'test_predicted.xlsx', index=False)
    print(f'Test data saved to {save_path}test_predicted.xlsx')


if __name__ == "__main__":
    main(opt["--model_path"], opt["--test_path"], opt["--save_path"])
