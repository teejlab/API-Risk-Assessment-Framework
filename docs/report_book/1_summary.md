# 1. Executive Summary

Application Programming Interface (API) is a set of definitions and protocols for building and integrating application software {cite:p}`red_hat_api_2017`. Due to the heightened focus on data privacy and security, there is an increased risk of using APIs. TeejLab is a research-driven cybersecurity company, aimed at helping organisations with the evolving challenges of the API economy.

Presently, risk is quantified via manual inspection or a rules-based approach. This method is only suitable if we are dealing with few API endpoints and with few features to consider. However, it will prove to be insurmountable and laborious as we scale up the endpoints by several fold, and as we introduce more features - requiring more time and labour to manually label each endpoint. Therefore, we aim to create a machine learning model to quantify risk at each API endpoint based on security and data sovereignty markers.

More tangibly, we created a data pipeline for both preprocessing and machine learning, and documentation on how to use these scripts. This will allow Teejlab to iterate on the present code, add additional security aspects into the machine learning pipeline, and aid in their long-term goal of incorporating an “endpoint security” column on their platform to provide their clientele an additional metric on the API.



