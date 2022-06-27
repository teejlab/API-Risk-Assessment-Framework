"""
This script trains ML model on the pre-processed train data. 
The train files must be named X_train.csv and y_train.csv

Usage: predict.py --model_path=<model_path> --predict_path=<predict_path --predict_save_path=<predict_save_path>

Options:
--model_path=<model_path>                           The path to the model
--predict_path=<predict_path>                       The path to the predict csv files.
--predict_save_path=<predict_save_path>             The folder to save the results to

Example:
python src/predict.py --model_path=models/model.joblib --predict_path=data/processed/preprocessed_test.xlsx --predict_save_path=data/processed/
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


def get_features_selection():
    features = []
    with open('data/processed/features.txt', 'r') as f:
        for line in f:
            features.append(line.strip())
    return features


def main(model_path, predict_path, predict_save_path):
    '''
    This function loads the model and performs predictions on the test data.
    Parameters
    -----------
    model_path : string
        The path to the .joblib file containing the model.
    predict_path : string
        The path to the predict csv files.
    predict_save_path : string
        The folder to save the results to

    Returns
    -----------
    None
    '''
    pipe_lr_tuned = load_model(model_path)
    predict_df = pd.read_excel(predict_path)
    X_test, y_test = predict_df.drop(
        columns=["Risk_Label"]), predict_df["Risk_Label"]

    select_features = get_features_selection()
    X_select = X_test[select_features]
    print('Predicting on test set...')
    y_pred = pipe_lr_tuned.predict(X_select)
    # put the predicted labels in a dataframe
    predict_df['Risk_Label'] = y_pred

    # save the test data with the predicted labels
    predict_df.to_excel(predict_save_path + 'df_predicted.xlsx', index=False)
    print(f'Test data saved to {predict_save_path}df_predicted.xlsx')


if __name__ == "__main__":
    main(opt["--model_path"], opt["--predict_path"],
         opt["--predict_save_path"])
