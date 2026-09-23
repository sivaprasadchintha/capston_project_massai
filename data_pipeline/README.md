# Module 1 – Data Pipeline

## Overview

This module implements an **end-to-end data engineering pipeline** using the public **BooksToScrape** website.

The pipeline performs the following steps:

1. Scrapes book data from the website.
2. Cleans and transforms the collected data.
3. Converts GBP prices into INR.
4. Stores the cleaned data in a normalized SQLite database.
5. Executes SQL queries for analysis.
6. Performs equivalent analysis using Pandas.
7. Verifies that the SQL and Pandas results are consistent.

### Pipeline Flow

```text
BooksToScrape
      │
      ▼
   Scraping
      │
      ▼
Data Cleaning
      │
      ▼
Transformation
      │
      ├── GBP → INR
      ├── Rating → Integer
      └── Availability → Boolean
      │
      ▼
SQLite Database
      │
      ├── SQL Analysis
      │
      └── Pandas Verification
      │
      ▼
   Final Results
```

---

## Technologies Used

| Technology    | Purpose                              |
| ------------- | ------------------------------------ |
| Python        | Main programming language            |
| Requests      | Sending HTTP requests to the website |
| BeautifulSoup | Parsing HTML content                 |
| Pandas        | Data processing and verification     |
| SQLite3       | Database storage and SQL analysis    |

---

## Project Structure

```text
data_pipeline/
│
├── scraper.py              # Scrapes book data from BooksToScrape
├── cleaner.py              # Cleans and transforms scraped data
├── database.py              # Creates and populates SQLite database
├── queries.py               # Executes SQL queries
├── main.py                  # Runs the complete pipeline
├── books_data.db                 # SQLite database
├── sql_query_results.txt    # SQL query outputs
└── README.md                # Project documentation
```

---

## Data Source

The data is collected from the public website:

**BooksToScrape**

https://books.toscrape.com/

The pipeline collects books from the following categories:

* Travel
* Mystery
* Historical Fiction
* Sequential Art

### Dataset Size

A total of **144 books** are collected from the selected categories.

---

## Data Collected

For each book, the following information is extracted:

| Field        | Description                            |
| ------------ | -------------------------------------- |
| Title        | Name of the book                       |
| Price        | Original book price in GBP             |
| Star Rating  | Book rating from 1 to 5                |
| Availability | Whether the book is currently in stock |
| Category     | Category to which the book belongs     |

---

## Data Cleaning and Transformation

After scraping, the raw data is cleaned and transformed before being stored in the database.

### Price Cleaning

The original price contains the `£` currency symbol.

Example:

```text
£51.77
```

is converted to:

```text
51.77
```

The cleaned value is stored as a floating-point number in the `price_gbp` column.

---

### Rating Conversion

The website represents ratings as text such as:

```text
One
Two
Three
Four
Five
```

These values are converted into integers:

```text
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5
```

The resulting value is stored in the `rating` column.

---

### Availability Conversion

Availability information is converted into a Boolean-style value.

```text
In stock → 1
Not in stock → 0
```

The resulting value is stored in the `in_stock` column.

---

## Currency Conversion

Book prices are converted from GBP to INR using the fixed exchange rate specified in the assignment.

```text
1 GBP = 105.50 INR
```

The INR price is calculated as:

```text
price_inr = price_gbp × 105.50
```

### Example

If:

```text
price_gbp = 20.00
```

then:

```text
price_inr = 20.00 × 105.50
          = 2110.00 INR
```

A fixed exchange rate is used, so the pipeline does **not require an external currency API**.

---

## Handling Parsing Errors

The pipeline is designed to handle invalid or missing numeric values without crashing.

If a numeric value cannot be parsed:

1. The invalid value is converted to `NaN`.
2. Median imputation is applied.
3. The cleaned dataset continues through the pipeline.

This provides basic robustness against unexpected or malformed values in the scraped data.

---

# Database Design

The cleaned data is stored in a **normalized SQLite database** named:

```text
books_data.db
```

The database contains two main tables:

```text
categories
     │
     │ 1-to-many
     ▼
  books
```

The `categories` table stores unique categories, while the `books` table stores individual book records.

---

## Table: `categories`

The `categories` table contains the unique book categories.

| Column          | Type                | Description                        |
| --------------- | ------------------- | ---------------------------------- |
| `category_id`   | INTEGER PRIMARY KEY | Unique identifier for the category |
| `category_name` | TEXT UNIQUE         | Name of the category               |

### Example

```text
category_id | category_name
------------|---------------------
1           | Religion
2           | Music
3           | Sports and Games
4           | Art
5           | History
6           | Thriller
7           | Business
```

---

## Table: `books`

The `books` table contains information about individual books.

| Column        | Type                | Description                          |
| ------------- | ------------------- | ------------------------------------ |
| `book_id`     | INTEGER PRIMARY KEY | Unique identifier for the book       |
| `title`       | TEXT                | Book title                           |
| `price_gbp`   | REAL                | Price in GBP                         |
| `price_inr`   | REAL                | Price converted to INR               |
| `rating`      | INTEGER             | Rating from 1 to 5                   |
| `in_stock`    | INTEGER             | Stock status: 1 or 0                 |
| `category_id` | INTEGER             | Foreign key referencing `categories` |

### Relationship

```text
categories
-----------
category_id (PK)
category_name

       │
       │
       │ 1
       │
       │
       │ N
       ▼

books
-----
book_id (PK)
title
price_gbp
price_inr
rating
in_stock
category_id (FK)
```

This design avoids storing the same category name repeatedly for every book.

---

# SQL Analysis

The project demonstrates several SQL concepts using the SQLite database.

The following SQL operations are implemented:

* `SELECT`
* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* `BETWEEN`
* `LEFT JOIN`

These queries are used to retrieve, filter, sort, limit, and combine data from the database.

### Query Results

The generated SQL outputs are saved in:

```text
sql_query_results.txt
```

This file provides a record of the results produced by the SQL analysis.

---

# Pandas Verification

The project also demonstrates how SQL operations can be reproduced using Pandas.

The following Pandas functionality is used:

```python
pd.read_sql()
```

and:

```python
pd.merge()
```

### Verification Process

The project:

1. Executes a `JOIN` query using SQLite.
2. Loads the required database data into Pandas.
3. Reproduces the same join operation using `pd.merge()`.
4. Compares the SQL and Pandas results.
5. Verifies that both approaches produce identical results.

This demonstrates that the same relational operation can be implemented using either SQL or Pandas.

---

# How to Run

## 1. Navigate to the Data Pipeline Directory

```bash
cd data_pipeline
```

---

## 2. Install Dependencies

Install the required Python packages:

```bash
pip install requests beautifulsoup4 pandas urllib3
```

SQLite3 is included with standard Python installations, so a separate installation is generally not required.

---

## 3. Run the Complete Pipeline

The recommended approach is to run:

```bash
python main.py
```

This executes the complete workflow:

```text
Scraping
   ↓
Cleaning
   ↓
Transformation
   ↓
Database Creation
   ↓
SQL Queries
   ↓
Pandas Verification
```

---

## 4. Run Individual Modules

Each module can also be executed separately when required.

### Scraper

```bash
python scraper.py
```

Collects book information from BooksToScrape.

### Cleaner

```bash
python cleaner.py
```

Cleans and transforms the scraped data.

### Database

```bash
python database.py
```

Creates and populates the SQLite database.

### Queries

```bash
python queries.py
```

Executes the SQL analysis queries and generates the query results.

---

# Output Files

After successfully running the pipeline, the following important outputs are generated:

| File                    | Description                                         |
| ----------------------- | --------------------------------------------------- |
| `books_data.db`              | SQLite database containing categories and book data |
| `sql_query_results.txt` | Results generated by the SQL queries                |

---

# Expected Results

The completed pipeline should:

* Successfully scrape **74 books** from the selected categories.
* Clean and transform the scraped values.
* Convert GBP prices into INR using the fixed rate of **105.50 INR per GBP**.
* Store the data in a normalized SQLite database.
* Maintain a relationship between `categories` and `books`.
* Execute the required SQL queries.
* Save SQL query results to `sql_query_results.txt`.
* Reproduce the SQL `JOIN` operation using Pandas.
* Verify that SQL and Pandas results are identical.

---

# Summary

This module demonstrates a complete **ETL-style data engineering workflow**:

```text
Extract
  │
  │  BooksToScrape
  ▼
Transform
  │
  │  Cleaning
  │  Rating conversion
  │  Availability conversion
  │  GBP → INR
  ▼
Load
  │
  │  SQLite
  ▼
Analyze
  │
  ├── SQL
  └── Pandas
```

The project demonstrates practical skills in **web scraping, data cleaning, data transformation, relational database design, SQL querying, and Pandas-based data analysis**.
