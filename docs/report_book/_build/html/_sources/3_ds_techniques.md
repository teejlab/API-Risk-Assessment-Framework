# 3. Data Science Techniques

## 3.1 Datasets

The dataset provided by TeejLab contains 2,000 observations of HTTP Requests via third-party APIs. Each row of data represents the full HTTP request made by TeejLab Services to the third-party API endpoint, and all HTTP requests are annotated by the level of severity (i.e. High, Medium, Low, No). The overview of the datasets is shown in Table 1 and the detailed description of the dataset is introduced in Table 2.

| Label  | Number of the samples |
|--------|-----------------------|
| High   | 682                   |
| Medium | 52                    |
| Low    | 1,211                 |
| No     | 55                    |
| Total  | 2,000                 |

Table 1: The statistical summary of the Data Endpoints

| Column                 | Type        | Description                                            |
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

Table 2: The detailed description of the columns in the dataset
## 3.2 Data Pre-processing

During our EDA, we found out that multiple entries were identical with the exception of the request header field “Date” (i.e. timestamp of message) in the “metadata_response” column. However, this information is not useful for our analysis. Moreover, there were insufficient samples for certain risk labels after data wrangling (See Figure 1). More data points are required to make any further statistical conclusions.

```{figure} ../../images/histogram_categorical.png
---
height: 150px
name: histogram_categorical-fig
---
Distribution of the Risk Label
```

## 3.3 Feature Engineering

While there are multiple ways for an API to be exploited, we focused on the features that are available to the attacker, which will help us quantify the risk of a possible attack. This information can be found in the “sample_response” and  “response_metadata” column.

In the “sample_response” column, there are two key pieces of information that are critical - PII and FII. These features include  individuals’ names, ID, and bank number, which can be extracted via a NLP package. The greater the number of such information is exposed, the greater the risk.

In the “response_metadata” column, there are several keys to be extracted. Information, such as server software, and X-rate-limits, are vital. While it is difficult to concisely elaborate on the importance of each key that we are going to extract, the intuition is that with more information exposed to the attacker, they will be better able to exploit its vulnerabilities.

```{figure} ../../images/NLP_preprocess.png
---
height: 250px
name: NLP_preprocess-fig
---
Feature engineering on API responses
```


Currently, most rows in “sample_response” contain missing data. As such, while waiting to acquire more data, we will test pre-trained ML models or find a similar corpus to train the model.


## 3.4 Machine Learning Pipeline

Before embarking on machine learning, we will use a 80:20 train-test split. This is to ensure that we do not influence the test data while training the model.

One challenge is the validity of the provided risk labels. We want to be certain that the labels accurately capture the underlying pattern. Thus, we will first employ unsupervised clustering with three components (to mirror the three risk classes) to evaluate if (a)  there are three distinct clusters and (b) if they correspond to the risk labels provided by TeejLab. If a discrepancy is observed, we will engineer and select new features, which are more predictive of the risk category.

Once we have the final input features, we will train supervised classification algorithms. Presently, we are going to train and optimise Random Forest, CatBoot, XGBoost, and Ensemble Models. However, lest the accuracy is less than 80%, we will look out for other Machine Learning or Deep Learning Models.

In this problem, it is very critical to identify the high risk APIs accurately. Hence, we are using Recall as the primary evaluation metric. However, as we want to avoid low risk APIs to show up as high risk, we will also look at f1-score and accuracy.

Based on metrics scores, we will select the best performing model and build an integrated Machine Learning pipeline for predicting risk classification on new data. This pipeline will be used for evaluating performance on the test data.

```{figure} ../../images/ML_Pipeline.jpg
---
height: 500px
name: ML_Pipeline-fig
---
Machine Learning pipeline
```
