"""
This script trains ML model on the pre-processed train data.
The train files must be named X_train.csv and y_train.csv

Usage: ml_model.py --train_path=<train_path> --save_path=<save_path>

Options:
--train_path=<train_path>            The path to the training csv files.
--save_path=<save_path>             The folder to save the model results to

Example:
python src/ml_model.py --train_path=data/processed/preprocessed_train.xlsx --save_path=data/model/
"""

from docopt import docopt
from pathlib import Path
import pandas as pd
import numpy as np
from joblib import dump, load

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import make_pipeline

from imblearn.over_sampling import SMOTE

opt = docopt(__doc__)

# Smote function
def create_smote(X, y, k_neighbors):
    oversample = SMOTE(k_neighbors = k_neighbors)
    X, y = oversample.fit_resample(X, y)
    return X, y

def main(train_path, save_path):
    print(f'Training model...')
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
    X_select = X_train[[
        'is_pii', 
        'is_fii', 
        'authentication_processed', 
        'Information & Science',
        'x0_Broken Authentication', 
        'x0_Missing', 
        'server', 
        'metadata_fields_count']]
    pipe_lr_tuned = make_pipeline(
        StandardScaler(), LogisticRegression(C=100.0, solver='liblinear'))

    pipe_lr_tuned.fit(X_select, y_train)
    
    # Save the model
    dump(pipe_lr_tuned, f"{path}/{path.name}.joblib")
    print(f'Model saved to {path}/{path.name}.joblib')

if __name__ == "__main__":
    main(opt["--train_path"], opt["--save_path"])
