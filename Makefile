# Author: Son Chau
# Date: 2022-06-23
# Description: Makefile for the project

# Compile the program
all: book.html

# Preprocessing the data	
data/processed/preprocessed_train.xlsx data/processed/preprocessed_test.xlsx: data/raw/RiskClassification_Data_Endpoints_V4_Shared1.xlsx
	python src/preprocessing.py --endpoint_path=data/raw/RiskClassification_Data_Endpoints_V4_Shared1.xlsx --country_path=data/raw/nri_2021_dataset.xlsx --risk_rules_path=data/raw/RiskRules.xlsx --output_path=data/processed/ --split_data=True

# Create model
models/model.joblib: data/processed/preprocessed_train.xlsx
	python src/create_model.py --train_path=data/processed/preprocessed_train.xlsx --create_save_path=data/model/

# Predict data
data/processed/df_predicted.xlxs: data/processed/preprocessed_test.xlsx
	python src/predict.py --model_path=models/model.joblib --predict_path=data/processed/preprocessed_test.xlsx --predict_save_path=data/processed/

# Generate the report in PDF
# book.pdf : histogram_categorical.png
# 	jupyter-book build docs/report_book/ --builder pdfhtml

# Generate report in HTML
book.html: data/processed/df_predicted.xlxs
	jupyter-book build docs/report_book/

# Clean the data
clean:
	rm -rf data/processed/*
	rm -rf models/*
	rm -rf docs/report_book/_build/*