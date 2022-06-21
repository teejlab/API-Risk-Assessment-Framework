# API-Risk-Assessment-Framework
A framework for quantifying API risks.

## Proposal

Our [proposal](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/docs/report_book/_build/pdf/book.pdf) can be found via this link.

## Contributing

| Contributors         | Github                |
|----------------------|-----------------------|
| Anupriya Srivastava  | \@Anupriya-Sri        |
| Harry Chan           | \@harryyikhchan       |
| Jacqueline Chong     | \@Jacq4nn             |
| Son Chau             | \@SonQBChau           |

## Environment set up
You can install all the dependencies you need using conda:
```
# Create and activate the environment
conda env create -f env.yml
conda activate api-risk

# Install Presidio python package
pip install presidio_analyzer

# Presidio analyzer requires a spaCy language model
python -m spacy download en_core_web_lg
```