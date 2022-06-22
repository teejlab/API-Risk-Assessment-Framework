# 4. Data Product and Results

The above is the method and technique employed to respond to the objective of the project: to quantify the risk of the endpoints of each API based on security and data sovereignty markers. To ensure that TeejLab can use our result and deploy an additional column titled “Endpoint Security” on their platform, the following data product will be handed over.

## 4.1 Data Pipeline

The data product will include scripts for the preprocessing and machine learning pipeline. The process is documented with the expectation that Teejlab can reproduce the results with minimal guidance. The data product is accompanied with a Jupyter notebook for how to interpret the results. To elaborate further, the processed data sets will be the output of the preprocessing pipeline, while the model and prediction will be the output of the machine learning pipeline.

This pipeline is modular, making it easy for TeejLab to add new scripts and commands as the domain knowledge evolves. Our pipeline also offers TeejLab the ability to schedule different aspects of the pipeline to be run distinctly or as a whole.

## 4.2 Auxiliary Script

In addition, we converted TeejLab’s rules into a script to automatically label the risk class of each data point at the request of Teejlab. The script will look for specific words or phrases within the API content and label it based on the rule. If or when the domain knowledge changes, TeejLab will be able to adjust the rules accordingly.

With this said, both the preprocessing pipeline and the API risk label script will need to be rerun should a new training dataset be used.

## 4.3 Improvements

To be able to integrate with Teejlab’s existing software, the interface has to be user-friendly and easy to maintain. Also, it must be scalable for future growth. Due to time constraints and limited resources, this integration would need to be conducted by TeejLab’s team.

There are other areas of improvement regarding our model. For instance, we can leverage machine learning tools to create a model or script that is able to be constantly updated and adjusted based on the new data. However, as this project is at the conception stage of this domain, our model will serve as a starting point for TeejLab to further enhance it as domain knowledge broadens.
