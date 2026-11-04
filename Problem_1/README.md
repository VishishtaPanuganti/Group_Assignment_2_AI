# AI Group Assignment 2 – Problem 1

## Smart Home Energy Consumption Analysis Using Bayesian Networks

This notebook implements a Bayesian Network to analyse and predict household energy consumption based on weather, day type, occupancy, AC usage, and appliance load.

### Contents
- Construction of the expert Bayesian Network and CPTs.
- Verification of conditional probability distributions.
- Bayesian inference for queries Q1–Q7.
- Conditional independence analysis using d-separation.
- Explaining Away phenomenon.
- Manual calculation of high energy consumption probability.
- Synthetic data generation using ancestral sampling.
- Parameter learning using MLE and Bayesian Estimation (BDeu, ESS = 10).
- Comparison of expert and learned models for 500, 5,000 and 20,000 samples.
- Visualization and comparative error analysis.

### Technologies Used
- Python
- Jupyter Notebook
- pgmpy
- NumPy
- Pandas
- Matplotlib
- NetworkX

### How to Run
1. Install the required libraries:
   ```bash
   pip install pgmpy pandas numpy matplotlib networkx
   ```
2. Open `Problem_1.ipynb` in Jupyter Notebook or Google Colab.
3. Run all cells sequentially to reproduce the results and visualizations.
