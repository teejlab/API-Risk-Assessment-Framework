from docopt import docopt
from numpy import NaN
import pandas as pd


def extract_metadata(df):
    '''
    Extract metadata features from the sample response.

    Parameters:
    -----------
    df: pandas.DataFrame
        The dataframe to be processed

    Returns:
    --------
    pandas.DataFrame
        The dataframe with the metadata features

    '''
    # Check if the df is valid
    if not isinstance(df, pd.DataFrame):
        raise TypeError("`df` should be a valid Pandas DataFrame")

    # fill missing values with {}
    df["response_metadata"] = df["response_metadata"].fillna("{}")
    df["parameters"] = df["parameters"].fillna("{}")

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

    # loop through api_df and add columns in high_risk_security_headers
    for header in high_risk_security_headers:
        df[header] = NaN
    # create new column metadata_fields_count and set to 0
    df["metadata_fields_count"] = 0
    df["parameters_count"] = 0

    # loop through sample_response see the key match with high_risk_security_headers
    for i in range(len(df)):
        meta_count = 0
        sample_response_dict = eval(df['response_metadata'].iloc[i])
        if df['response_metadata'].iloc[i] is not None:
            # convert sample_response to dictionary
            sample_response_dict = eval(df['response_metadata'].iloc[i])
            # loop through sample_response_dict and extract key value
            for key, value in sample_response_dict.items():
                if key.lower() in high_risk_security_headers:
                    df.loc[df.index[i], key.lower()] = value
                    meta_count += 1
        df.loc[df.index[i],"metadata_fields_count"] = meta_count
        df.loc[df.index[i], "parameters_count"] = len(
            eval(df['parameters'].iloc[i]))

    # recommend rule for each high risk security header
    # to make it simple, if the header is not present, it is considered as not secure
    x_frame_options = 'DENY'
    x_xss_protection = '0'
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
    # to find if the recommended rule is present
    for i in range(len(df)):
        # loop through recommend_dict
        for key, value in recommend_dict.items():
            if pd.notnull(df[key].iloc[i]):
                # if the cell contain the value in recommend_dict, then assign the value 0, else assign 1
                # 0 IS GOOD, 1 IS BAD
                df.loc[df.index[i], key] = 0 if value in df[key].iloc[i] else 1

    # loop through each row of api_df
    for i in range(len(df)):
        # loop through should_not_be_present
        for field in should_not_be_present:
            # check if the cell is not NaN
            if not pd.isna(df[field].iloc[i]):
                # if the cell contain value, then assign the value 1
                df.loc[df.index[i], field] = 1
        # loop through good_to_be_present
        for field in good_to_be_present:
            # check if the cell is not NaN
            if not pd.isna(df[field].iloc[i]):
                # if the cell contain value, then assign the value 0
                df.loc[df.index[i], field] = 0

    # Fill the NaN in high_risk_security_headers with 0
    for header in high_risk_security_headers:
        df[header] = df[header].fillna(0)

    df = df.drop_duplicates()

    return df