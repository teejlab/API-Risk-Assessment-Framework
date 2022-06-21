all: book.html

# Preprocessing the data

train.csv: data/raw/RiskClassification_Data_Endpoints_V2.xlsx 
	python src/preprocessing.py --input_path=data/raw/RiskClassification_Data_Endpoints_V2.xlsx --input_path_country=data/raw/nri_2021_dataset.xlsx --output_path=data/processed/

# Perform EDA
histogram_categorical.png : train.csv
	python src/eda.py --train_file=data/processed/train.csv --output_path=docs/report/images/


# Generate the report in PDF
book.pdf : histogram_categorical.png
	jupyter-book build docs/report_book/ --builder pdfhtml

# Generate report in HTML
book.html : book.pdf
	jupyter-book build docs/report_book/

clean:
	rm -rf data/processed/*

	rm -rf docs/report/images/histogram_categorical.png

	rm -rf docs/report_book/_build/*