# author: Harry Chan
# date: 2022-05-04

"""Create eda plots for the provided training data file. Saves the plots as png files in the provided output directory.
Usage: src/eda.py --train_file=<train_file> --output_path=<output_path>

Options:
--train_file=<train_file>    Path (including filename) to training data
--output_path=<output_path>    Path (including filename) of where to locally write the file
"""
  
from docopt import docopt
import altair as alt
import pandas as pd
import os 

opt = docopt(__doc__)

def main(train_file, output_path):
    
    # Read the training data
    train_df = pd.read_csv(train_file)
    # Create the directory if not exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Distribution of target variable
    hist_target = alt.Chart(train_df, title="Histogram of the Risk Label").mark_bar().encode(
        y=alt.Y("risk_label", type="nominal", title="Risk Label"),
        x=alt.X("count()", title="Count")
    )
    hist_target.save(output_path + "/histogram_categorical.png")

if __name__ == "__main__":
  main(opt["--train_file"],  opt["--output_path"])