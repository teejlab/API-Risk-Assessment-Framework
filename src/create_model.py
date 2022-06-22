"""
This script trains ML model on the pre-processed train data.
The train files must be named X_train.csv and y_train.csv

Usage: create_model.py --train_path=<train_path> --save_path=<save_path>

Options:
--train_path=<train_path>            The path to the training csv files.
--save_path=<save_path>             The folder to save the model results to

Example:
python src/create_model.py --train_path=data/processed/preprocessed_train.xlsx
--save_path=data/model/
"""

from docopt import docopt
from pathlib import Path
import pandas as pd
from joblib import dump
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFE

opt = docopt(__doc__)


# Smote function
def create_smote(X, y, k_neighbors):
    '''
    This function performs SMOTE over-sampling on the training data.
    Parameters
    -----------
    X : pandas.DataFrame
        The training dataframe.
    y : pandas.Series
        The training labels.
    k_neighbors : int
        The number of neighbors to use in the SMOTE algorithm.

    Returns
    -----------
    X_smote : pandas.DataFrame
        The SMOTE-balanced training dataframe.
    y_smote : pandas.Series
        The SMOTE-balanced training labels.
    '''
    oversample = SMOTE(k_neighbors = k_neighbors)
    X, y = oversample.fit_resample(X, y)
    return X, y


def get_features_selection(X_train, y_train):
    '''
    This function performs feature selection using RFE method.
    Parameters
    -----------
    X_train : pandas.DataFrame
        The training dataframe.
    y_train : pandas.Series
        The training labels.

    Returns
    -----------
    select_features : list
        The list of selected features.
    '''
    select_rfe = RFE(LogisticRegression(), n_features_to_select=8)
    pipe_dt_rfe = make_pipeline(
        StandardScaler(), select_rfe, DecisionTreeClassifier(random_state=42))
    pipe_dt_rfe.fit(X_train, y_train)
    rfe_fs = pipe_dt_rfe.named_steps["rfe"].support_
    rfe_selected_feats = X_train.columns[rfe_fs]
    feature_list = list(rfe_selected_feats)
    return feature_list


def main(train_path, save_path):
    '''
    This function trains the model and saves it to the given path.
    Parameters
    -----------
    train_path : string
        The path to the training csv files.
    save_path : string
        The path to the save the model.

    Returns
    -----------
    None
    '''
    print('Training model...')
    path = Path(save_path)
    path.mkdir(parents=True, exist_ok=True)

    #############
    # READ DATA #
    #############
    api_df = pd.read_excel(train_path)

    # X, y split for train-set
    X_train, y_train = api_df.drop(columns=["Risk_Label"]), api_df["Risk_Label"]

    # Balance training data
    X_train, y_train = create_smote(X_train, y_train, 2)

    # Data sub-set of features identified using RFE method
    select_features = get_features_selection(X_train, y_train)
    X_select = X_train[select_features]

    pipe_lr_tuned = make_pipeline(
        StandardScaler(), LogisticRegression(C=100.0, solver='liblinear'))

    pipe_lr_tuned.fit(X_select, y_train)

    # Save the model
    dump(pipe_lr_tuned, f"{path}/{path.name}.joblib")
    print(f'Model saved to {path}/{path.name}.joblib')


if __name__ == "__main__":
    main(opt["--train_path"], opt["--save_path"])
