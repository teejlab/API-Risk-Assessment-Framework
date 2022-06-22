# 3. Data Science Methods

## 3.1 Available Data

The dataset provided by TeejLab contains around 2,000 observations of Hypertext Transfer Protocol (HTTP) Requests via third-party APIs. Each row of data represents the full HTTP request made by TeejLab Services to the third-party API endpoint, which are also annotated with the level of severity (i.e. High, Medium, Low). The overview of the datasets is shown in {ref}`Table 1 <table-1>` and the detailed description of the dataset is introduced in {ref}`Table 2 <table-2>`. There are 17 features, five of which are to identify the API, eight are categorical variables, three are text variables, one is binary and the target is an ordinal variable.

```{table} : The statistical summary of the dataset
:name: table-1

| **Label**  | **Number of the samples** |
|--------|-----------------------|
| High   | 4                     |
| Medium | 876                   |
| Low    | 961                   |
| Total  | 1,841                 |
```

&nbsp;

```{table} : The detailed description of the columns in the dataset
:name: table-2
| **Column**                 | **Type**        | **Description**                                            |
|------------------------|-------------|--------------------------------------------------------|
| api_endpoint_id        | Categorical | Unique id of API Endpoint                              |
| api_id                 | Categorical | Unique id of API Service                               |
| api_vendor_id          | Categorical | Unique id of API Vendor                                |
| api_vendor             | Categorical | Name of API Vendor                                     |
| api                    | Categorical | Name of API                                            |
| category               | Categorical | Category of API                                        |
| usage_base             | Categorical | Type of the pricing model of API                       |
| sample_response        | Text        | Sample HTTP Response in JSON format                    |
| authentication         | Categorical | Authentication method used (e.g. OAuth2.0, Path, None) |
| security_test_category | Categorical | Category of security vulnerability test                |
| security_test_result   | Binary      | Result of security vulnerability test                  |
| server_location        | Categorical | Location of server host                                |
| hosting_isp            | Categorical | Internet service provider (ISP) that runs  website     |
| server_name            | Categorical | Name and the version of web server used in API         |
| response_metadata      | Categorical | API Response Header                                    |
| hosting_city           | Text        | Location of web hosting                                |
| Risk label             | Ordinal     | Severity level of risk (target label)                  |
```

## 3.2 Summary of the Exploratory Data Analysis (EDA)

We identified two key issues after performing EDA. The first was insufficient data points for high-risk labels (See {ref}`Figure 1 <risk_label-fig>` below). This will result in the training model reading too much into the four instances that are labelled as high risk. The training model will remember the patterns. To tackle this, we used Synthetic Minority Oversampling Technique (SMOTE) to generate more new samples.


```{figure} images/risk_label.jpg
---
height: 150px
name: risk_label-fig
---
Histogram of the Risk Label highlighting severe class imbalance
```

The second issue was that there might be some features hidden from the raw data. Feature engineering techniques are necessary to augment the value of existing data and improve the performance of our machine learning models. For example, we used NLP techniques to analyze the unstructured data such as API header and get the metadata fields to count (See {ref}`Figure 2 <metadata_field_counts-fig>` below).

```{figure} images/metadata_field_counts.jpg
---
height: 150px
name: metadata_field_counts-fig
---
Histogram of Metadata Fields Count, a feature extracted from the text column “API response”
```

## 3.3  Data Augmentation

A major challenge was the imbalanced nature of data, particularly with regard to the class of interest (High Risk). We had only four observations of the High Risk API class in our training set which was insufficient for the models to learn how to predict this class effectively. We attempted these approaches:

- Synthetic Data generation
- Bootstrapping
- Oversampling (SMOTE)

For Synthetic Data generation, while it is able to generate new numerical data, the nature of the technique did not allow us to generate columns for text data, such as response data and response metadata. For Bootstrapping, while it was easy to implement, and the overall data size did increase, the underlying distribution and imbalance in Risk labels was not handled.

Hence, we used the `imblearn` package for Oversampling. It was a technique that generated new data by ‘clustering’ the data points based on the risk labels and generating new samples based on their ‘neighbours’ information. This technique gave a balanced dataset with sufficient representation of High risk class for further modeling (Figure 3).

## 3.4 Evaluation Metric and Acceptance Criteria

As per our discussion with the partner, we understood that it is critical to correctly identify the High Risk classes, while also ensuring that not too many Low and Medium risk labels are incorrectly classified as High Risk.

Thus, we selected Recall as the primary evaluation metric to optimize the models and to maximize the correct identification of High Risk labels. We also considered f1-score as the secondary evaluation metric to ensure that not too many data points were incorrectly classified.

It was agreed that Acceptance Criteria would be: Recall >= 0.9.

## 3.5 Feature Engineering

As mentioned above, the dataset consists of 17 variables, which include identity numbers, strings and text. Based on our domain understanding, it is essential to extract and/or engineer several features - (1) PII and FII extraction, (2) quantify exposure frequency, (3) quantify risk associated with server location, and (4) imputation of security test.

PII and FII are crucial pieces of personal and financial information that can be used to identify, contact or even locate an individual or enterprises (Impervia 2021). It is imperative that they are transmitted and stored securely. The team attempted several techniques to extract this information, including Amazon’s Comprehend, PyPi’s piianalyzer package, and Microsoft’s PresidioAnalyzer. However, PresidioAnalyzer was ultimately chosen as it had high accuracy, was transferable between both PII and FII and was cost-free. By using PresidioAnalyzer on the “sample_response” column and defining the pieces of information to pick up on for PII and FII (See Appendix A), we created two binary columns of whether PII and/or FII is exposed by the API endpoint (Figure 4).

Second, we had to quantify the exposure of sensitive information and its frequency. This sensitive information was present in two columns - “parameter” and “response_metadata”. The former refer to request data while the latter refer to HTTP response headers. To quantify exposure, we counted the number of keys exposed per API endpoint (See Figure 5 below). In addition, there were specific security response headers, that if exposed, could lead to a security breach. As such, we extracted 12 security response keys, and engineered twelve additional binary columns (present or absent) (Figure 5). See Appendix A for the list and description of the 12 keys.

Third, we had to quantify the risk associated with the server location. Other than ensuring high loading speeding if they are situated near the user, the infrastructure, technology and the governance associated with the country could also impact the API’s security. As a proxy, our team has used the Network Readiness Index (Network Readiness Index 2021). It is an annual index that quantifies the impact of digital technology.

Finally, API exposes application logic and sensitive data, and has unique vulnerabilities and security risk. Ideally, each endpoint would contain all five security tests which TeejLab deems as crucial. However, it would be unreasonable for third parties such as TeejLab to request for a temporary shutdown of these API. Based on our discussion with TeejLab, we determined that should a test not be present, it would be deemed as low risk as there was no concern warranting a request for a security test. To capture the subtle difference between a test that passed and a test that was missing, we assigned a value of 0.5 to denote that the specific test was missing, 0 to denote that specific test was employed and passed, and 1 to denote that specific test was employed and failed (Figure 6).

## 3.6 Supervised Learning

As the risk labels (target column) were provided by TeejLab, we approached this problem as a Supervised Machine Learning task. We attempted the following algorithms:

- Logistic Regression
- Tree-based Models: Decision Tree, Random Forest, XGBoost, CatBoost
- K-Nearest Neighbors (KNN) and Support Vector Machines (SVM)

For each of these models, they were initially trained using the processed data set without any feature engineering. However, the maximum recall value was 0.75. Hyperparameter optimization did not lead to any significant improvement in performance of models. At this stage, Logistic Regression was selected for integration into the prediction pipeline. This is due to its high interpretability and its performance was on par with more complex models.

To improve the scores, we review the information being captured by the input features. We transformed all the existing columns and created new features as per Section 3.5. The final features resulted in improvement in model performance by more than 20% (a high recall score of 0.99), which exceeded the partner’s expectations.

However, the process of feature engineering caused an increase in dimensionality to 53. Recursive Feature Elimination (RFE) was employed to select the most important features instead of RFE with Cross Validation (RFECV) or SelectFromModel() which is a feature selection method based on feature importance. This was because it was the most consistent and resulted in a great dimensionality reduction. RFECV selected different quantities and selection of features each time, while SelectFromModel() only reduced the dimensionality by one. The RFE model identified eight variables that gave the same high performance level while reducing the dimensionality. The improvement of the Recall score is provided in Figure 7.