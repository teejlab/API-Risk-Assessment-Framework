"""
Extract fields from the response_metadata column (along with parameters).
Replace the string value with recomended binary value for risk factor.
Imputation of missing values with low risk factor.

Usage: preprocessing_metadata.py --file_path=<file_path> --rule_path=<rule_path> --output_path=<output_path>
 
Options:
--file_path=<file_path>                    Path to input data
--rule_path=<rule_path>                    Path to input data
--output_path=<output_path>                Path for preprocessed file to be saved

Example:
python src/utils/based_rules_classifier.py --file_path=data/processed/df_pii.xlsx --rule_path=data/raw/RiskClassification_Data_Endpoints_V2.xlsx --output_path=data/processed/
"""


from docopt import docopt
import pandas as pd
from pathlib import Path

# write the rule to classify the Risk_Label based on rule_df


def classify_risk(row, rule_df):
    '''
    Classify the risk based on the rule_df

    Parameters:
    -----------
    row: pandas.Series
        The row of the dataframe to be classified
    rule_df: pandas.DataFrame
        The rule_df contains the rule to classify the risk

    Returns:
    --------
    pandas.Series
        The row of the dataframe with the risk label
    '''
    if not isinstance(row, pd.Series):
        raise TypeError("`type` should be a valid Pandas Series")
    if not isinstance(rule_df, pd.DataFrame):
        raise TypeError("`rule_df` should be a pandas DataFrame")

    # remove api_endpoint_id from row series
    row = row.drop(labels=["api_endpoint_id"])
    # loop through each row in rule_df
    for i in range(len(rule_df)):
        row_copy = rule_df.iloc[i]
        # drop the column "Risk_Label"
        row_copy = row_copy.drop(["Risk_Label"])
        if row_copy['server_location'] == 'Anywhere':
            row_copy['server_location'] = row['server_location']
        if row_copy['security_test_category'] == 'All Tests Performed/Available':
            row_copy['security_test_category'] = row['security_test_category']
        # check if the row is the same with any row in rule_df
        if row_copy.equals(row):
            # return the value in column "Risk_Label"
            return rule_df.iloc[i]["Risk_Label"]
    return "Low Risk"


def main():
    '''
    This function classify the risk based on the rule_df
    '''
    # parse arguments
    args = docopt(__doc__)
    # assign args to variables
    file_path = args['--file_path']
    rule_path = args['--rule_path']
    output_path = args['--output_path']
    path = Path(output_path)
    path.mkdir(parents=True, exist_ok=True)

    # read risk rules
    rule_df = pd.read_excel(rule_path, sheet_name="RiskRules")
    # drop the first column vendor_api_category since we not using it
    rule_df = rule_df.iloc[:, 1:]
    # fill the empty values with "None"
    rule_df = rule_df.fillna("None")
    # remove duplicates
    rule_df = rule_df.drop_duplicates()
    # change server_location to Amaricas to Americas
    # rule_df["server_location"] = rule_df["server_location"].replace("Amaricas", "Americas")
  
    # read the data with fii and pii
    df = pd.read_excel(file_path)
    # make a copy of api_df
    api_df = df.copy()
    # fill the empty values with "None"
    api_df = api_df.fillna("None")
    api_df = api_df[['api_endpoint_id','authentication', 'security_test_category', 'security_test_result','server_location', 'hosting_isp', 'is_pii', 'is_fii']]

    # rename the column "is_pii" to "PII"
    api_df = api_df.rename(columns={"is_pii": "PII"})
    # rename the column "is_fii" to "FII"
    api_df = api_df.rename(columns={"is_fii": "FII"})
    # replace is_pii true to yes and false to no
    api_df["PII"] = api_df["PII"].replace(True, "Yes")
    api_df["PII"] = api_df["PII"].replace(False, "No")
    # replace is_fii true to yes and false to no
    api_df["FII"] = api_df["FII"].replace(True, "Yes")
    api_df["FII"] = api_df["FII"].replace(False, "No")

    # process column authentication from api_df, replace nan and none with "No Authentication"
    api_df["authentication"] = api_df["authentication"].replace(
        "None", "No Authentication")
    # replace all value that not "No Authentication" with "Some Authentication"
    api_df["authentication"].mask(api_df["authentication"] !=
                                "No Authentication", "Some Authentication", inplace=True)

    # process column security_test_category from api_df, replace nan with "No Test Performed/Available"
    api_df["security_test_category"] = api_df["security_test_category"].replace(
        "None", "No Test Performed/Available")
    # replace Injections with "SQL Injection"
    api_df["security_test_category"] = api_df["security_test_category"].replace(
        "Injections", "SQL Injection")
    # replace "Insecure Deserialization" with "No Test Performed/Available"
    api_df["security_test_category"] = api_df["security_test_category"].replace(
        "Insecure Deserialization", "No Test Performed/Available")

    # process column security_test_result from api_df, replace false with "Passed"
    api_df["security_test_result"] = api_df["security_test_result"].replace(
        0., "Pass")
    # replace true with "Failed"
    api_df["security_test_result"] = api_df["security_test_result"].replace(
        1., "Fail")
    

    # process column server_location from api_df, replace nan with "Anywhere"
    api_df["server_location"] = api_df["server_location"].replace(
        "None", "Anywhere")
    api_df["server_location"] = api_df["server_location"].replace(
        ["United States", "Canada"], "Americas")
    api_df["server_location"] = api_df["server_location"].replace(
        ["United Kingdom", "Ireland", "Germany", "Spain", 
         "Luxembourg", "Sweden", "France", "Netherlands"], "West Europe")
    # replace everything else with "Others"
    api_df["server_location"] = api_df["server_location"].replace(
        ["India", "Bangladesh", "Japan", "Australia",  "Czechia", "Lithuania", "Singapore"], "Others")
    
    # process column hosting_isp from api_df, replace value with "Anyone"
    api_df["hosting_isp"] = "Anyone"

    # apply the function classify_risk to each row in api_df
    api_df["Risk_Label"] = api_df.apply(classify_risk, axis=1, args=(rule_df,))

    # save api_df to excel
    api_df.to_excel(output_path + "/converted_data_with_risk.xlsx", index=False)

    # convert api_df.value_counts() to dataframe
    # make a deep copy of api_df
    risk_df = api_df.copy()
    api_df.drop(columns=["api_endpoint_id"], inplace=True)
    value_count = api_df.value_counts()
    # print(value_count)
    # save value_count to excel
    value_count.to_excel(output_path + "/risk_rule_count.xlsx")

    # create risk_df on api_df columns "api_endpoint_id" and "Risk_Label"
    # make a copy of api_df
    risk_df = risk_df[["api_endpoint_id", "Risk_Label"]]
    risk_df.to_excel(output_path + "/risk_labeled.xlsx", index=False)

    # merge api_df and df
    df = pd.merge(df, risk_df, on="api_endpoint_id", how="left")
    df.to_excel(output_path + "/original_with_risk.xlsx", index=False)

    # # convert api_df.value_counts() to dataframe
    # api_df.drop(columns=["api_endpoint_id"], inplace=True)
    # value_count = api_df.value_counts()
    # # save value_count to excel
    # value_count.to_excel(output_path + "/risk_rule_count.xlsx", index=False)


if __name__ == "__main__":
    main()
