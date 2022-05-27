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
from utils.country_n_cat_featuring import add_country_and_cat_feats
from utils.metadata_extraction import extract_metadata
from utils.pii_extraction import pii_extraction
from utils.security_test_feat_creation import security_test_feat_creation
import pandas as pd
from pathlib import Path
import swifter

opt = docopt(__doc__)
def main(input_path, input_path_country, output_path):
    path = Path(output_path)
    path.mkdir(parents=True, exist_ok=True)

    #############
    # READ DATA #
    #############
    df = pd.read_excel(input_path, "Core_Endpoint", usecols="A:S")
    df.rename(
        columns={
            "security_test_result (FALSE=Passed; TRUE=Failed)": "security_test_result"
        },
        inplace=True,
    )
    orignial_df = df.drop_duplicates()
    # make a copy of the dataframe
    df = orignial_df.copy()

    ########################
    # ADD PII FII FEATURES #
    ########################
    # WARNING: This function takes 30+ mins to run
    # so consider reading it from the processed file
    path_to_pii = output_path + "/df_pii.xlsx"
    pii_path = Path(path_to_pii)
    if not pii_path.is_file():    # delete the file if you want to run it again
        print("Extracting PII and FII features...")
        df["is_pii"] = df["sample_response"].swifter(pii_extraction, 
            args=("pii", 0.5,)).astype(bool)
        df["is_fii"] = df["sample_response"].swifter(pii_extraction, 
            args=("fii", 0.5,)).astype(bool)
        # save df with pii and fii
        df.to_excel(output_path + "/df_pii.xlsx", index=False)
    else:
        df = pd.read_excel(output_path + "/df_pii.xlsx")


    #############################################
    # ADD COUNTRY SCORE AND CATEGORIES FEATURES #
    #############################################
    df = add_country_and_cat_feats(df, input_path_country)
    df.to_excel(output_path + "/df_country_score.xlsx", index=False)


    ##############################
    # ADD SECURITY TEST FEATURES #
    ##############################
    df = security_test_feat_creation(df)
    df.to_excel(output_path + "/df_security.xlsx", index=False)

    #########################
    # ADD METADATA FEATURES #
    #########################
    df = extract_metadata(df)
    df.to_excel(output_path + "/df_metadata.xlsx", index=False)

    ###################
    # ADD RISK LABELS #
    ###################
    # read risk_labeled.xlsx
    df_risk_labeled = pd.read_excel("data/processed/risk_labeled.xlsx")
    # merge df and df_risk_labeled
    df = df.merge(df_risk_labeled, how="left", on="api_endpoint_id")
    df.to_excel(output_path + "/df_full.xlsx", index=False)

    # make a copy of orignial_df, select only api_endpoint_id and security_test_category
    df_security_test = orignial_df[["api_endpoint_id", "security_test_category"]].copy()
    # merge df and df_security_test
    df = df.merge(df_security_test, how="left", on="api_endpoint_id")
    df.to_excel(output_path + "/df_full_security.xlsx", index=False)

    
    ############################
    # SPLIT TRAIN AND SET DATA #
    ############################
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=123)
    train_df.to_csv(output_path + "/train.csv", index=False)
    test_df.to_csv(output_path + "/test.csv", index=False)

if __name__ == "__main__":
    main(opt["--input_path"], opt["--input_path_country"], opt["--output_path"])
