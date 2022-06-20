"""Reads train csv data from path, preprocess the data, and save the preprocessed data to path.
Usage: preprocessing.py --endpoint_path=<endpoint_path> --country_path=<country_path> --risk_rules_path=<risk_rules_path> --output_path=<output_path>
 
Options:
--endpoint_path=<endpoint_path>         Path to input data
--country_path=<country_path>           Path to input country metric data
--risk_rules_path=<risk_rules_path>     Path to risk rules
--output_path=<output_path>             Path for preprocessed file to be saved

Example:
python src/preprocessing.py --endpoint_path=data/raw/RiskClassification_Data_Endpoints_V4_Shared1.xlsx --country_path=data/raw/nri_2021_dataset.xlsx --risk_rules_path=data/raw/RiskRules.xlsx --output_path=data/processed/
"""

from docopt import docopt
from sklearn.model_selection import train_test_split
from utils.country_n_cat_featuring import add_country_and_cat_feats
from utils.metadata_extraction import extract_metadata
from utils.pii_extraction import pii_extraction
from utils.risk_labelling import create_risk_label
from utils.security_test_feat_creation import security_test_feat_creation
import pandas as pd
from pathlib import Path
import swifter

opt = docopt(__doc__)


def preprocessing(df, name, output_path, risk_rules_path, country_path):

    ########################
    # ADD PII FII FEATURES #
    ########################
    # WARNING: This function takes 30+ mins to run
    # so consider reading it from the processed file
    path_to_pii = output_path + "/pii_fii_" + name + ".xlsx"
    pii_path = Path(path_to_pii)
    if not pii_path.is_file():    # delete the file if you want to run it again
        print("Extracting PII and FII features. This will take a while...")
        df["is_pii"] = df["sample_response"].swifter.apply(pii_extraction, 
            args=("pii", 0.5,)).astype(bool)
        df["is_fii"] = df["sample_response"].swifter.apply(pii_extraction,
            args=("fii", 0.5,)).astype(bool)
        # save df with pii and fii
        df.to_excel(path_to_pii, index=False)
    else:
        df = pd.read_excel(path_to_pii)

    #############################################
    # ADD COUNTRY SCORE AND CATEGORIES FEATURES #
    #############################################
    print(f'Adding country score and OHE categories features...')
    df = add_country_and_cat_feats(df, country_path)

    ##############################
    # ADD SECURITY TEST FEATURES #
    ##############################
    print(f'Adding security test features...')
    df = security_test_feat_creation(df)

    #########################
    # ADD METADATA FEATURES #
    #########################
    print(f'Adding metadata features...')
    df = extract_metadata(df)

    ###################
    # ADD RISK LABELS #
    ###################
    print(f'Adding risk labels...')
    df = create_risk_label(df, risk_rules_path)
    # drop duplicates
    df = df.drop_duplicates()

    return df
    

def main(endpoint_path, country_path, risk_rules_path, output_path):
    path = Path(output_path)
    path.mkdir(parents=True, exist_ok=True)

    #############
    # READ DATA #
    #############
    df = pd.read_excel(endpoint_path, "Core_Endpoint", usecols="A:S")
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
    # SPLIT TRAIN AND TEST #
    ########################
    train, test = train_test_split(df, test_size=0.3, random_state=42)

    processed_train = preprocessing(train, 'train', output_path, risk_rules_path, country_path)
    processed_test = preprocessing(test, 'test', output_path, risk_rules_path, country_path)

    # save the processed data to excel
    processed_train.to_excel(output_path + "/train.xlsx", index=False)
    processed_test.to_excel(output_path + "/test.xlsx", index=False)

    # save the processed data to excel
    # drop columns : api_endpoint_id, api_id, api_vendor_id, request_id,
    # method, category, parameters, usage_base, sample_response, tagset, server_location,
    # hosting_isp, response_metadata, hosting_city
    columns_to_drop = [
        "api_endpoint_id",
        "api_id",
        "api_vendor_id",
        "request_id",
        "method",
        "category",
        "parameters",
        "usage_base",
        "sample_response",
        "tagset",
        "server_location",
        "hosting_isp",
        "response_metadata",
        "hosting_city",
        "authentication",
        "security_test_category", 
        "security_test_result",
        "server_name",
        "Country",

    ]
    processed_train.drop(columns=columns_to_drop, inplace=True)
    processed_test.drop(columns=columns_to_drop, inplace=True)

    processed_train.to_excel(output_path + "/train_essentials.xlsx", index=False)
    processed_test.to_excel(output_path + "/test_essentials.xlsx", index=False)


   

if __name__ == "__main__":
    main(opt["--endpoint_path"], opt["--country_path"],
         opt["--risk_rules_path"], opt["--output_path"])
