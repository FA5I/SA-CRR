### Introduction

This repo only implements the SA-CRR code for interest swaps and swaptions as per the The standardised approach for measuring counterparty credit risk exposures document.

For this task I have implemented two main parent classes: `Basel` and `Derivatives`. `Basel` houses functions which calculate the `EAD`. The function which completes the requirement of  this case study is `calc_EAD` which takes in a file name to a JSON file, and returns the EAD value for that transaction.

I followed a test-driven approach to this project, and the `tests.py` file should act as documentation for how to use the 

### Aims

The task is to get a rough understanding of the objectives of the Basel Committee’s Standardised Approach to Counterparty Credit Risk and implement a calculator in Python for some types of trades. 

For the scope of this exercise I limit implementation to only Interest Rate Swaps and Swaptions for which you can find an example calculation on page 22 (Example 1). I have assumed that the netting set is not subject to a margin agreement and there is no exchange of collateral (independent amount/initial margin) at inception.

The code accepts as an input a “netting set” of derivatives data as a JSON file (.json) of data and returns as an output the Exposure of Default (EAD). 

Sample data:

```json
{
  "name": "Derivatives Data",
  "date": "2017-01-17T00:00:00Z",
  "data": [
    {
      "id": "swap_1",
      "date": "2017-01-17T00:00:00Z",
      "asset_class": "ir",
      "currency_code": "USD",
      "end_date": "2019-01-17T00:00:00Z",
      "mtm_dirty": -1500,
      "notional_amount": 10000,
      "payment_type": "fixed",
      "receive_type": "floating",
      "start_date": "2017-01-10T00:00:00Z",
      "type": "vanilla_swap",
      "trade_date": "2017-01-10T00:00:00Z",
      "value_date": "2017-01-16T00:00:00Z"
		}
	]
}
```



### Installation

All simply hit `pip install -r requirements.txt` and Python should install all the required dependencies outlined in `requirements.txt`

### Testing

Simply run `python3 tests.py` to run the full suite of tests in the `tests.py` file.

### What is the Basel Committee trying to achieve with this regulation?

This regulation was designed to be applicable to a wide variety of derivative transactions (margined, unimagined, bilateral, lateral) and is simple to implement.

The alternatives are CEM (Current Exposure Method) and Standardised Method (SM), but this both had a number of shortcomings. First CEM did not differentiate between margined and unmargined transactions. The volatility factor in CEM and SM did not sufficiently reflect volatilities observed in recent stress periods.  CEM netting was too basic to reflect the reality of derivative transactions. SM's definition of a hedging set led to operational difficulties in implementation.

The new approach, Standardised Approach  (SA-CRR) overcomes these limitations, and was designed with this in mind. The SA-CRR seems simpler to implement and has clear documentation.

###  What's the Add-On for?

For each derivative transaction, there are a number of risk factors that fall into five asset classes: interest rate, foreign exchange, credit, equity or commodity. The add-on attempts to take this into account and is based on recent volatility levels per asset class, among other things. The add-on also influences a multiplier, which allows the recognition of excess capital in the transaction. Excess capital reduces risk exposure.
