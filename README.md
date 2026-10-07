# Customer Management System

**Mayank Singh Sadudia | Python, SQLite and business reporting**

My existing Streamlit project for storing customer profiles and orders, with SQL summaries and Matplotlib reports.

## Features

- Add, view and delete customer profiles.
- Add orders and view customer-linked order records.
- Total customer, order and revenue metrics.
- Order distribution pie chart and revenue per customer bar chart.
- SQLite `customers` and `orders` tables, including joins and aggregations.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run main.py
```

The application creates a new `customers.db` locally. Add fictional customer and order records through the interface to explore the reports. The existing local database is not included in the public repository. This is a local portfolio prototype, without authentication or a production deployment.

## Publication preparation

The existing source was retained and the customer-delete table name and parameter tuple were corrected. Customer deletion also removes that customer's orders to avoid orphaned records. Dependency and setup instructions were added. No private customer records are published.

[Portfolio](https://mayanksinghsadudia.github.io/mayank-portfolio/) | [GitHub](https://github.com/Mayanksinghsadudia)
