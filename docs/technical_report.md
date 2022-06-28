# Technical Report

### Capstone Partners: TeejLab and UBC Saunder
### Mentor(s): Gittu George and Gene Lee
### Contributors:
- Anupriya Srivastava
- Harry Chan
- Jacqueline Chong
- Son Chau


## Introduction
APIs have been present for decades and are set to grow exponentially, in part due to regulations (in public health or finance) or by industry interoperability (in telecommunications) or disruption (in media or retail) (Wang and McLarty 2021). As a cybersecurity company focused on API management at a global scale, TeejLab aims to tackle this key industry challenge of quantifying business risk at the API level. A manual inspection or a rules-based approach is insufficient to accurately capture various aspects of risk, such as security, legal, similarity, and data sovereignty. It is time and labour intensive to inspect every feature and assign a risk label to an API endpoint, let alone quantities of API endpoint in the range of thousands or millions. This process is also static, and would require constant revision to the rules as domain knowledge increases. In addition to those listed previously, the legal aspect is related to the level of protection for users for data use and distribution. Similarity aspect refers to how much user data APIs in the same category are requesting, where one that is requesting for too much data is deemed as less secure.
</br>
</br>

## Scope of Project
Based on the dataset provided and time limitation, our team has narrowed the scope to focus on creating a machine learning pipeline to quantify the risk of the endpoints of each API based on security and data sovereignty markers. More specifically, our project aims to create a well-annotated python script for each stage - (1) data pre-processing and feature engineering, and (2) machine learning.
</br>
</br>

## Scope of Report
In this report, we aim to guide you through the thought process behind the decisions that we made, namely choice of data augmentation, featuring engineering techniques and machine learning algorithms.
</br>
</br>

## Thought Process
### Data Augmentation
From the 1841 rows of HTTP request provided, there were only four rows labelled as high risk, which is insufficient for the machine learning models to learn how to predict this class effectively.Reason being, the training model will read too much into the four instances that are labelled as high risk. The training model will remember the patterns. Please refer to the [eda notebook](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/notebooks/eda/eda.ipynb) for more details. 

In order to maintain this project as a multi-class classification problem, we need to find a tool to create a balanced data set for all the three classes. 

We have attempted these approaches:
- Synthetic Data generation
- Bootstrapping
- Oversampling (SMOTE)

For Synthetic Data generation, while it is able to generate new numerical data, the nature of the technique did not allow us to generate columns for text data, such as response data and response metadata. For Bootstrapping, while it was easy to implement, and the overall data size did increase, the underlying distribution and imbalance in Risk labels was not handled. 

Hence, we used the `imblearn` package for Oversampling. It was a technique that generated new data by ‘clustering’ the data points based on the risk labels and generating new samples based on their ‘neighbours’ information. This technique gave a balanced dataset with sufficient representation of High risk class for further modeling.
</br>
</br>

### Feature Engineering
From the 18 variables provided to us by TeejLab, most of the rows were categorical or text features. As such, in order to draw out more information, it was essential for us to extract and/or engineer several features - (1) PII and FII extraction, (2) quantify exposure frequency, (3) quantify risk associated with server location, and (4) imputation of security test. All the relevant code can be found in [this document](https://github.com/teejlab/API-Risk-Assessment-Framework/tree/main/src/utils).
</br>
</br>

### Supervised Learning
We attempted the following algorithms:
- Logistic Regression
- Tree-based Models: Decision Tree, Random Forest, XGBoost, CatBoost
- K-Nearest Neighbors (KNN) and Support Vector Machines (SVM).

The process of testing each algorithm can be found in these two notebooks: (1) [Logistic Regression, KNN, SVM](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/notebooks/ml/1_logisticregression_knn_svn.ipynb) and (2) [Tree-based Models](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/notebooks/ml/2_treebasedmodels.ipynb).

Ultimately, we chose to use Logistic Regression as it offered us high interpretability and its performance was on par with more complex models.

In addition to selecting the models, we also reduced the dimensionality of the features. From 53 features, we were able to reduce the number of features required to eight. The team attempted several algorithms, namely
- Recursive Feature Elimination (RFE)
- Recursive Feature Elimination with Cross-validation (RFECV)
- SelectFromModel().

In the end, we used RFE as it was the most consistent and resulted in a great dimensionality reduction. RFECV selected different quantities and selection of features each time, while SelectFromModel() only reduced the dimensionality by one. The process of testing each algorithm can be found in this [notebook](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/notebooks/ml/3_feature_selection.ipynb).

## Results
The main scoring metric is Recall, with an acceptance criteria of more than 0.9. We understood that it is critical to correctly identify the High Risk classes, while also ensuring that not too many Low and Medium risk labels are incorrectly classified as High Risk. 

The team has managed to optimise the final model which has a recall score of 0.99 on the validation set. Results can be found in this [notebook](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/notebooks/ml/1_logisticregression_knn_svn.ipynb).

## Room for improvement
The team understands that API Risk Assessment is a completely novel field, and there is no ground truth to the current risk labels. As such, the team set out to investigate the validity of the risk labels. This exploration can be found in this [notebook](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/notebooks/eda/eda-clustering.ipynb). 

We hope that through this notebook and particularly though the clustering that we have performed TeejLab will be able to use their domain knowledge to make sense of the clusters found. 
