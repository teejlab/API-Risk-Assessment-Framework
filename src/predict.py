"""
This script trains ML model on the pre-processed train data.
The train files must be named X_train.csv and y_train.csv

Usage: predict.py --model_path=<model_path> --predict_path=<predict_path> --save_path=<save_path>

Options:
--model_path=<model_path>            The path to the model
--predict_path=<predict_path>        The path to the predict csv files.
--save_path=<save_path>              The folder to save the model results to

Example:
python src/predict.py --model_path=data/model/model.joblib --predict_path=data/processed/preprocessed_test.xlsx --save_path=data/processed/
"""

from docopt import docopt
import pandas as pd
from joblib import load

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


def main(model_path, predict_path, save_path):
    pipe_lr_tuned = load_model(model_path)
    predict_df = pd.read_excel(predict_path)
    X_test, y_test = predict_df.drop(
        columns=["Risk_Label"]), predict_df["Risk_Label"]
    X_testselect = X_test[[
        'is_pii', 
        'is_fii', 
        'authentication_processed', 
        'Information & Science',
        'x0_Broken Authentication', 
        'x0_Missing', 
        'server', 
        'metadata_fields_count']]
    print(f'Predicting on test set...')
    y_pred = pipe_lr_tuned.predict(X_testselect)
    # put the predicted labels in a dataframe
    predict_df['Risk_Label'] = y_pred

    # save the test data with the predicted labels
    predict_df.to_excel(save_path + 'test_predicted.xlsx', index=False)
    print(f'Test data saved to {save_path}test_predicted.xlsx')


if __name__ == "__main__":
    main(opt["--model_path"], opt["--predict_path"], opt["--save_path"])
