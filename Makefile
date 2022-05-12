all: book.html

# Preprocessing the data
train.csv: data/raw/RiskClassification_Data_Endpoints_V1.xlsx 
	python src/preprocessing.py --input_path=data/raw/RiskClassification_Data_Endpoints_V1.xlsx --output_path=data/processed/

# Perform EDA
histogram_categorical.png : train.csv
	python src/eda.py --train_file=data/processed/train.csv --output_path=images/

# Generate the report in PDF
book.pdf : histogram_categorical.png
	jupyter-book build docs/report_book/ --builder pdfhtml

# Generate report in HTML
book.html : book.pdf
	jupyter-book build docs/report_book/

clean:
	rm -rf data/processed/*
	rm -rf images/histogram_categorical.png
	rm -rf docs/report_book/_build/*