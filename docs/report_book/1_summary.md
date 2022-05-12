# 1. Executive Summary

Application Programming Interface (API) is a set of definitions and protocols for building and integrating application software {cite}`red_hat_api_2017`. Due to the heightened focus on data privacy and security, there is an increased risk of using APIs. TeejLab is a research-driven cybersecurity company, aimed at helping organisations with the evolving challenges of the API economy.

Our objective is to quantify risk at each API endpoint based on security and data sovereignty markers. Security refers to how vulnerable the endpoint is to attack, such as the exposure of personal identifiable information (PII) or financial identifiable information (FII), and how stringent the hosting countries bylaws are for privacy policy. Data sovereignty refers to governance of data, which is at risk if they fail certain security tests, such as injections, or if the endpoints are accessible to users.

More tangibly, we seek to create a data pipeline, in the form of a python script, along with a risk assessment report. This will allow Teejlab to iterate on the present code, add additional security aspects into the machine learning pipeline, and aid in their long-term goal of incorporating a “API risk” column on their platform to provide their clientele an additional metric on the API.
