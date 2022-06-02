
import pandas as pd
from pathlib import Path

def classify_risk(row, rule_df):
    """
    Check if the row is the same with any row in rule_df
    """
    # remove api_endpoint_id from row series
    row = row.drop(labels=["api_endpoint_id"])
    # loop through each row in rule_df
    for i in range(len(rule_df)):
        rule_copy = rule_df.iloc[i]
        # drop the column "Risk_Label"
        rule_copy = rule_copy.drop(["Risk_Label"])
        if rule_copy['server_location'] == 'Anywhere':
            rule_copy['server_location'] = row['server_location']
        if rule_copy['security_test_category'] == 'All Tests Performed/Available':
            rule_copy['security_test_category'] = row['security_test_category']
        # check if the row is the same with any row in rule_df
        if row.equals(rule_copy):
            # return the value in column "Risk_Label"
            return rule_df.iloc[i]["Risk_Label"]
    return "Low"


def create_risk_label(df, risk_rules_path):
    # read risk rules
    rule_df = pd.read_excel(risk_rules_path, sheet_name="RiskRules")
    # drop the first column vendor_api_category since we not using it
    rule_df = rule_df.iloc[:, 1:]
    # fill the empty values with "None"
    rule_df = rule_df.fillna("None")
    # remove duplicates
    rule_df = rule_df.drop_duplicates()
    # change server_location from Amaricas to Americas
    # rule_df["server_location"] = rule_df["server_location"].replace(
    #     "Amaricas", "Americas")

    # # read the data with fii and pii
    # original_df = pd.read_excel(path_to_pii)
    # original_df = original_df.drop_duplicates()
    # # make a copy of api_df
    api_df = df.copy()
    # fill the empty values with "None"
    api_df = api_df.fillna("None")
    api_df = api_df[['api_endpoint_id', 'authentication', 'security_test_category',
                     'security_test_result', 'server_location', 'hosting_isp', 'is_pii', 'is_fii']]

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
        "SQL Injection", "Injections")
    # replace "Insecure Deserialization" with "No Test Performed/Available"
    api_df["security_test_category"] = api_df["security_test_category"].replace(
        "Insecure Deserialization", "All Tests Performed/Available")

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

    # create risk_df on api_df columns "api_endpoint_id" and "Risk_Label"
    # make a copy of api_df
    risk_df = api_df[["api_endpoint_id", "Risk_Label"]]

    # to avoid unexpected behavior, we need to drop the duplicates
    risk_df = risk_df.drop_duplicates()

    # merge df and df_risk_labeled
    # df = df.merge(risk_df, how="left", on="api_endpoint_id")
    df_full = pd.merge(df, risk_df, left_index=True, right_index=True)

    return df_full

