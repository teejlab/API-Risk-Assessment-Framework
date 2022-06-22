# all: book.html
all: data/processed/df_predicted.xlxs

# Preprocessing the data	
data/processed/preprocessed_train.xlsx data/processed/preprocessed_test.xlsx: data/raw/RiskClassification_Data_Endpoints_V4_Shared1.xlsx
	python src/preprocessing.py --endpoint_path=data/raw/RiskClassification_Data_Endpoints_V4_Shared1.xlsx --country_path=data/raw/nri_2021_dataset.xlsx --risk_rules_path=data/raw/RiskRules.xlsx --output_path=data/processed/ --split_data=True

# Perform EDA
# histogram_categorical.png : train.csv
# 	python src/eda.py --train_file=data/processed/train.csv --output_path=docs/report/images/

# Create model
data/model/model.joblib: data/processed/preprocessed_train.xlsx
	python src/create_model.py --train_path=data/processed/preprocessed_train.xlsx --save_path=data/model/

# Predict data
data/processed/df_predicted.xlxs: data/processed/preprocessed_test.xlsx
	python src/predict.py --model_path=data/model/model.joblib --predict_path=data/processed/preprocessed_test.xlsx --save_path=data/processed/

# Generate the report in PDF
# book.pdf : histogram_categorical.png
# 	jupyter-book build docs/report_book/ --builder pdfhtml

# Generate report in HTML
# book.html : book.pdf
# 	jupyter-book build docs/report_book/

clean:
	rm -rf data/processed/*
	rm -rf data/model/*
	rm -rf docs/report_book/_build/*