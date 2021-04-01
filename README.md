### Introduction

This repo only implements the SA-CRR code for interest swaps and swaptions as per the case study requirements.

The code was automatically formatted in line with Pep-8 standards.

For this task I have implemented two main parent classes: `Basel` and `Derivatives`. `Basel` houses functions which calculate the `EAD`. The function which completes the requirement of  this case study is `calc_EAD` which takes in a file name to a JSON file, and returns the EAD value for that transaction.

I followed a test-driven approach to this project, and the `tests.py` file should act as documentation for how to use the 

### Installation

All simply hit `pip install -r requirements.txt` and Python should install all the required dependencies outlined in `requirements.txt`

### Testing

Simply run `python3 tests.py` to run the full suite of tests in the `tests.py` file.

### Question 1:

 In 200 words or less, explain what you think the Basel Committee is trying to achieve with this regulation, pros/cons of this approach and what (if any) is the alternative?*

### Answer:

This regulation was designed to be applicable to a wide variety of derivative transactions (margined, unimagined, bilateral, lateral) and is simple to implement.

The alternatives are CEM (Current Exposure Method) and Standardised Method (SM), but this both had a number of shortcomings. First CEM did not differentiate between margined and unmargined transactions. The volatility factor in CEM and SM did not sufficiently reflect volatilities observed in recent stress periods.  CEM netting was too basic to reflect the reality of derivative transactions. SM's definition of a hedging set led to operational difficulties in implementation.

The new approach, Standardised Approach  (SA-CRR) overcomes these limitations, and was designed with this in mind. The SA-CRR seems simpler to implement and has clear documentation.

 ### Question 2:

In 100 words or less, explain, as you would to your grandmother, what the Add-On is for?

### Answer:

For each derivative transaction, there are a number of risk factors that fall into five asset classes: interest rate, foreign exchange, credit, equity or commodity. The add-on attempts to take this into account and is based on recent volatility levels per asset class, among other things. The add-on also influences a multiplier, which allows the recognition of excess capital in the transaction. Excess capital reduces risk exposure.
