# API-Risk-Assessment-Framework
This project quantified the risk of the endpoint of each API based on security and data sovereignty markers. In this repository, we have included a well-annotated python script for (1) the data preprocessing and feature engineering, along with the (2) machine learning pipeline. These can be found in the `src` folder.

This project is part of UBC MDS' capstone project 2022 where the contributors collaborated with TeejLab.

## Proposal

Our proposal can be found [here](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/docs/proposal_book/_build/pdf/book.pdf).

## Final Report
Our final report can be found [here](https://teejlab.github.io/API-Risk-Assessment-Framework/intro.html). 

## Technical Report
For a high level summary of our project and to understand our decision making choices, please refer to the [technical report](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/main/docs/technical_report.md).
We have included links to the relevant scripts and notebooks for easy navigation within the repository. 

## Top-level Directory Layout
    .
    ├── data                    # Data files
    │   ├── preprocessed           # Preprocessed Dataset
    │   └── raw                    # Raw Dataset
    ├── docs                    # Final Proposal and Report
    │   ├── proposal_book          # Final Proposal
    │   └── report_book            # Final Report
    ├── model                   # Model file
    ├── notebooks               # Jupyter Notebook files 
    │   ├── eda                    # Notebooks for EDA
    │   └── ml                     # Notebooks for ML Models
    ├── src                     # Source files
    │   ├── utils                  # Utility Functions
    │   └── test                   # Automated tests
    ├── reference_material      # Reference Materials
    ├── LICENSE                 # LICENSE File
    ├── requirements.txt        # Dependencies for CI/CD Workflow
    ├── Makefile                # Automated Script
    ├── CODE_OF_CONDUCT.md      # Code of Conduct File
    ├── CONTRIBUTING.md         # Contributing File
    ├── env.yml                 # Conda Environment File
    └── README.md               # README

## Usage
1. Clone the repository to your machine.
2. Set up the environment using the instructions below.
3. Template to include new API endpoint can be found in the `data/processed` folder.
4. To use the models directly, please refer to Makefile instructions below.

## Environment set up
You can install all the dependencies you need using conda:
```
# Create and activate the environment
conda env create -f env.yml
conda activate api-risk-env
```

## Makefile
(to be added by Son - including how to run code for each part i.e. rules, preprocessing, predict)
A. To run all scripts (preprocessing, create_model, and predict):
```
```
B. To run ...
C. 
D. ...

## Contributing

| Contributors         | Github                |
|----------------------|-----------------------|
| Anupriya Srivastava  | \@Anupriya-Sri        |
| Harry Chan           | \@harryyikhchan       |
| Jacqueline Chong     | \@Jacq4nn             |
| Son Chau             | \@SonQBChau           |

## License
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/teejlab/API-Risk-Assessment-Framework/blob/readme/LICENSE)