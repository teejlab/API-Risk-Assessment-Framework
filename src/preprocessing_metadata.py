"""
Extract fields from the response_metadata column (along with parameters).
Replace the string value with recomended binary value for risk factor.
Imputation of missing values with low risk factor.

Usage: preprocessing_metadata.py --input_path=<input_path> --output_path=<output_path>
 
Options:
--input_path=<input_path>                    Path to input data
--output_path=<output_path>                  Path for preprocessed file to be saved

Example:
python src/preprocessing_metadata.py --input_path=data/raw/RiskClassification_Data_Endpoints_V2.xlsx --output_path=data/processed/
"""

from docopt import docopt
import pandas as pd
from pathlib import Path

def main():
    # parse arguments
    args = docopt(__doc__)
    # assign args to variables
    input_path = args['--input_path']
    output_path = args['--output_path']

    # Read the excel file
    api_df = pd.read_excel(input_path, "Core_Endpoint", usecols="A:R")
    # rename column "security_test_result (FALSE=Passed; TRUE=Failed)" to "security_test_result"
    api_df.rename(columns={
                'security_test_result (FALSE=Passed; TRUE=Failed)': 'security_test_result'}, inplace=True)
    # get only api_id, parameters and response_metadata columns
    api_df = api_df[['api_id', 'parameters', 'response_metadata']]
    
    # get a list of all response_metadata
    metadata_list = api_df['response_metadata'].tolist()
    # get a list of all parameters
    parameters_list = api_df['parameters'].tolist()
    # replace nan with empty string
    metadata_list = [str(x) if pd.notnull(x) else '{}' for x in metadata_list]
    parameters_list = [str(x) if pd.notnull(x) else '{}' for x in parameters_list]

    key_set = set()  # make sure there is no duplicate key
    # loop through each response_metadata and extract key value
    for i in range(len(metadata_list)):
        if metadata_list[i] is not None:
            # convert metadata_list[i] to dictionary
            metadata_dict = eval(metadata_list[i])
            # loop through metadata_dict and extract key value
            for key, value in metadata_dict.items():
                key_set.add(key.lower())
    
    # list of columns that have high risk security
    high_risk_security_headers = [
        'x-frame-options',
        'x-xss-protection',
        'strict-transport-security',
        'expect-ct',
        'referrer-policy',
        'content-type',
        'set-cookie',
        'access-control-allow-origin',
        'server',
        'x-powered-by',
        'x-aspnet-version',
        'x-ratelimit-limit'
    ]

    metadata_count_df = pd.DataFrame(columns=['metadata_fields_count'])
    parameters_count_df = pd.DataFrame(columns=['parameters_count'])
    for i in range(len(metadata_list)):
        metadata_fields_count = 0  # keep track of how many fields in each API
        parameters_count = 0  # keep track of how many parameters in each API
        if metadata_list[i] is not None:
            metadata_dict = eval(metadata_list[i])
            # loop through metadata_dict and extract key value
            for key, value in metadata_dict.items():
                key = key.lower()
                if key in high_risk_security_headers:
                    api_df.loc[i, key] = value
                    metadata_fields_count += 1
        metadata_count_df.loc[i, 'metadata_fields_count'] = metadata_fields_count
        # repeat for parameters
        if parameters_list[i] is not None:
            parameters_dict = eval(parameters_list[i])
            parameters_count = len(parameters_dict)
        parameters_count_df.loc[i, 'parameters_count'] = parameters_count
    api_df = api_df.assign(metadata_fields_count=metadata_count_df)
    api_df = api_df.assign(parameters_count=parameters_count_df)


    # recommend rule for each high risk security header
    # to make it simple, if the header is not present, it is considered as not secure
    x_frame_options = 'DENY'
    x_xss_protection = '0'
    content_security_policy = '0'
    strict_transport_security = 'includeSubDomains'
    expect_ct = 'max-age'
    referrer_policy = 'strict-origin-when-cross-origin'
    content_type = 'charset'
    set_cookie = 'Secure'
    access_control_allow_origin = 'https'
    # make a dictionary to store the recommended rule
    recommend_dict = {
        'x-frame-options': x_frame_options,
        'x-xss-protection': x_xss_protection,
        'strict-transport-security': strict_transport_security,
        'expect-ct': expect_ct,
        'referrer-policy': referrer_policy,
        'content-type': content_type,
        'set-cookie': set_cookie,
        'access-control-allow-origin': access_control_allow_origin
    }

    # the following headers are not recommended
    should_not_be_present = ['server',
                            'x-powered-by',
                            'x-aspnet-version']
    good_to_be_present = ['x-ratelimit-limit']

    # loop through each row of api_df
    for i in range(len(api_df)):
        # loop through recommend_dict
        for key, value in recommend_dict.items():
            # check if the cell is not NaN
            if not pd.isna(api_df.loc[i, key]):
                # if the cell contain the value in recommend_dict, then assign the value 0, else assign 1
                api_df.loc[i, key] = 0 if value in api_df.loc[i, key] else 1
    
    # loop through each row of api_df
    for i in range(len(api_df)):
        # loop through should_not_be_present
        for field in should_not_be_present:
            # check if the cell is not NaN
            if not pd.isna(api_df.loc[i, field]):
                # if the cell contain value, then assign the value 1
                api_df.loc[i, field] = 1
        # loop through good_to_be_present
        for field in good_to_be_present:
            # check if the cell is not NaN
            if not pd.isna(api_df.loc[i, field]):
                # if the cell contain value, then assign the value 0
                api_df.loc[i, field] = 0
    
    # replace NaN value with 0
    api_df = api_df.fillna(0)
    
    # save api_df to excel
    path = Path(output_path)
    path.mkdir(parents=True, exist_ok=True)
    api_df.to_excel(output_path + "/metadata.xlsx", index=False)
    api_df.to_csv(output_path + "/metadata.csv", index=False)
        

if __name__ == "__main__":
    main()
