# SafeX Solutions — Market Basket Analysis

## Project Overview

This project uses **Market Basket Analysis** to identify products that customers frequently purchase together. The goal is to generate useful cross-selling recommendations that can support retail business decisions.

The analysis uses the **Apriori algorithm** to discover association rules and validates the strongest rules on unseen transactions.

## Business Question

**Which products are frequently purchased together, and how can these associations be used to generate cross-selling recommendations?**

## Dataset

* **Dataset:** UCI Online Retail Dataset
* **Original Records:** 541,909
* **Time Period:** December 2010 – December 2011
* **Columns:** 8
* **Source:** UCI Machine Learning Repository

The dataset contains online retail transactions including invoice numbers, products, quantities, prices, dates, and countries.

## Data Preparation

The data preparation process included:

* Converting invoice dates to datetime format
* Standardizing product descriptions
* Removing invalid quantities and prices
* Removing cancelled transactions
* Removing duplicate records
* Removing non-merchandise/service items
* Creating transaction-level product baskets
* Splitting transactions chronologically into training and validation datasets

Valid high-quantity transactions were retained because Market Basket Analysis focuses on whether a product appears in a basket rather than the exact quantity purchased.

## Methodology

The project uses the **Apriori algorithm** to identify frequent product combinations and generate association rules.

Key metrics:

* **Support:** How frequently products occur together in all transactions.
* **Confidence:** How often customers who purchase one product also purchase another.
* **Lift:** How much stronger the relationship is compared with random purchasing.
* **Validation Confidence:** Measures how consistently the rule performs on unseen transactions.

The first 80% of transactions chronologically were used for training and the latest 20% were used for validation.

## Key Findings

Some of the strongest validated associations included:

| Product A             | Product B             | Confidence |   Lift | Validation Confidence |
| --------------------- | --------------------- | ---------: | -----: | --------------------: |
| Pink Regency Teacup   | Green Regency Teacup  |      83.3% | 15.08x |                 79.2% |
| Pink Regency Teacup   | Roses Regency Teacup  |      78.4% | 13.50x |                 76.9% |
| Green Regency Teacup  | Roses Regency Teacup  |      75.7% | 13.04x |                 75.5% |
| Lunch Bag Suki Design | Lunch Bag Black Skull |      44.4% |  6.64x |                 51.8% |

These results show strong purchasing relationships that can be used for targeted cross-selling.

## Interactive Dashboard

A **Streamlit dashboard** was developed to make the results interactive.

The dashboard includes:

### 🛍️ Interactive Cart Simulator

Users can select a product and view related products that can be recommended for cross-selling.

### 📊 Association Rules

Displays discovered association rules along with support, confidence, lift, and validation confidence.

### 💡 Business Implementation

Shows how the results can support:

* E-commerce cross-selling
* Product bundles
* Product placement
* Inventory planning

The dashboard also provides confidence and lift filters so users can focus on stronger associations.

## Technologies Used

* Python
* Pandas
* Matplotlib
* mlxtend
* Streamlit
* Jupyter Notebook / Google Colab
* GitHub

## Project Structure

safex-market-basket-analysis/
│
├── app.py
├── safex_market_basket_recommendations.csv
├── market_basket_analysis.ipynb
├── requirements.txt
└── README.md


## How to Run

Install the required Python packages:

pip install -r requirements.txt

Run the Streamlit dashboard:

streamlit run app.py

The dashboard will open in a web browser.

## Business Value

The analysis can help retailers identify products that naturally go together and use these relationships to improve:

* Cross-selling recommendations
* Promotional bundles
* Product placement decisions
* Inventory planning

## Future Improvements

Possible improvements include:

* Testing additional association-rule thresholds
* Adding customer or country-level analysis
* Integrating real-time transaction data
* Deploying the dashboard online
* Developing personalized recommendations for individual customers

## Internship Deliverable

**SafeX Solutions — Data Science Internship**
**Week 3: Market Basket Analysis**
