# 2. Introduction

## 2.1 Capstone Partner’s Needs

APIs have been present for decades and are set to grow exponentially, in part due to regulations (in public health or finance) or by industry interoperability (in telecommunications) or disruption (in media or retail)  {cite}`wang_mclarty_2021`. As a cybersecurity company focused on API management at a global scale, TeejLab aims to tackle this key industry challenge of ***quantifying business risk at the API level***. A manual inspection or a rules-based approach is insufficient to accurately capture various aspects of risk, such as *security, legal, similarity, and data sovereignty*. Security refers to how vulnerable the endpoint is to attack, such as the exposure of personal identifiable information (PII) or financial identifiable information (FII), and how stringent the hosting countries' bylaws are for privacy policy. *Legal aspect* is related to the level of protection for users for data use and distribution. *Similarity* refers to how much user data APIs in the same category are requesting, where one that is requesting for too much data is deemed as less secure. Finally, data sovereignty refers to governance of data, which is at risk if they fail certain security tests, such as injection attacks, or if the endpoints are accessible to users.

It is time and labour intensive to inspect every feature and assign a risk label to an API endpoint, let alone quantities of API endpoint in the range of thousands or millions. This process is also static, and would require constant revision to the rules as domain knowledge increases.

## 2.2 Scope of Project

Based on the dataset provided and time limitation, our team has narrowed the scope to focus on creating a machine learning pipeline to ***quantify the risk of the endpoints of each API based on security and data sovereignty markers***. More specifically, our project aims to create a well-annotated python script for each stage - (1) data pre-processing and feature engineering, and (2) machine learning.



