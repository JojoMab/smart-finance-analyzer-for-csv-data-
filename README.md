# Smart Finance Analyzer

Smart Finance Analyzer is an interactive Python CLI for analyzing personal finance data from CSV files. The program reads transactions, calculates income, expenses, monthly balances and a simple forecast, then creates a structured financial report.

## GitHub Description

Interactive Python finance analyzer for CSV transactions with monthly balances, category analysis and forecasting.

## Recruiter Snapshot

- Topic: financial data, CSV processing, reporting and simple forecasting
- Technology: Python standard library, interactive CLI, text report
- Input: realistic sample transactions in `transactions.csv`
- Output: full financial report in the terminal and as a text file
- Focus: clean data validation, structured analysis and traceable results

## Features

- load and validate transactions from CSV files
- calculate total income, total expenses and net surplus
- rank expenses by category
- create monthly balances
- forecast the next month
- handle missing files, missing columns and invalid amounts
- save the report automatically

## Quick Start

Run the project from the repository root:

```bash
python3 main.py
```

Confirm the default values with Enter:

```txt
Enter CSV file name [transactions.csv]:
Enter report file name [report.txt]:
```

Expected terminal output:

```txt
Smart Finance Analyzer starting...
[1/5] Loading transactions from CSV...
✓ 132 transactions loaded.
[2/5] Calculating financial summary...
✓ Income: 37140.00 EUR | Expenses: 20870.00 EUR | Surplus: 16270.00 EUR
[3/5] Analyzing expense categories...
✓ 12 categories found: Rent, Groceries, Leisure, Savings, Insurance, Mobility, Internet, Clothing, Phone, Education, Gifts, Health
[4/5] Calculating monthly balances and forecast...
✓ 12 months analyzed. Forecast: 1355.83 EUR
```

## Examples

The example outputs are versioned intentionally so recruiters can inspect the result directly on GitHub without running the project locally:

- [Terminal output](examples/terminal_output.txt)

The terminal output shows the interactive input, key financial KPIs and successful report creation.

## Input Format

The CSV file needs these columns:

```csv
month,type,amount,category
January,income,2850.00,Salary
January,expense,820.00,Rent
January,expense,345.00,Groceries
```

`type` must be either `income` or `expense`.

## Outputs

The generated report contains:

- financial summary with income, expenses and net surplus
- category analysis with percentages
- monthly balances
- next-month forecast
- note on whether a positive financial buffer is expected

By default, the report is saved as `report.txt`. This file is generated and not versioned.

## Project Structure

```txt
.
├── main.py
├── transactions.csv
├── examples/
│   ├── README.md
│   └── terminal_output.txt
└── README.md
```

## Technical Goals

- no external dependencies
- clear Python functions
- robust CSV validation
- traceable calculation steps
- simple terminal usage

## Portfolio Relevance

This project demonstrates clean foundational data processing with Python: CSV import, validation, aggregation, report generation and simple forecasting. The realistic sample transactions make the result easy for recruiters to understand without running the project.
