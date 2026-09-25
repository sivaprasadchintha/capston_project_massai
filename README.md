# Capstone Zepto Data & AI Platform

An end-to-end capstone project combining **data engineering, analytics/machine learning, and a GenAI/RAG support assistant**.

The project is organized into three independent but complementary modules:

```text
Capstone Zepto Data & AI Platform
│
├── data_pipeline/
│   └── Web scraping → Cleaning → GBP/INR transformation
│       → SQLite → SQL/Pandas analysis
│
├── analytics/
│   └── Titanic EDA → Visualization → ML classification
│       → Imbalance handling → Hyperparameter tuning
│       → Regression → Model persistence
│
└── support_assistant/
    └── Zepto policy documents → Embeddings → ChromaDB
        → LangGraph RAG → FastAPI → Docker
```

---

# Project Modules

| Module | Main Purpose | Primary Technologies |
|---|---|---|
| Module 1 – Data Pipeline | Scrape, clean, transform, store, and analyze book data | Python, Requests, BeautifulSoup, Pandas, SQLite |
| Module 2 – Analytics | Perform EDA and machine-learning analysis on Titanic data | Pandas, Seaborn, Matplotlib, Scikit-learn, SMOTE, Joblib |
| Module 3 – Support Assistant | Answer Zepto policy questions using local RAG | Sentence Transformers, ChromaDB, LangGraph, Pydantic, FastAPI, Docker |

Each module has its own README with module-specific details:

```text
data_pipeline/README.md
analytics/README.md
support_assistant/README.md
```

---

# Overall Architecture

```text
                         CAPSTONE PROJECT
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
      DATA PIPELINE         ANALYTICS       SUPPORT ASSISTANT
             │                  │                  │
             ▼                  ▼                  ▼
    BooksToScrape          Titanic Data       Zepto Policies
             │                  │                  │
             ▼                  ▼                  ▼
        Scraping              EDA             Documents
             │                  │                  │
             ▼                  ▼                  ▼
        Cleaning          Visualization       Embeddings
             │                  │                  │
             ▼                  ▼                  ▼
     GBP → INR            ML Modeling         ChromaDB
             │                  │                  │
             ▼                  ▼                  ▼
         SQLite          Model Evaluation     LangGraph RAG
             │                  │                  │
             ▼                  ▼                  ▼
       SQL/Pandas        best_model.pkl       FastAPI /ask
                                                   │
                                                   ▼
                                                Docker
```

---

# Module 1 – Data Pipeline

## Purpose

The data pipeline collects book information from the public BooksToScrape website, cleans and transforms the data, stores it in a normalized SQLite database, and performs SQL/Pandas analysis.

### Pipeline

```text
BooksToScrape
      ↓
Scraping
      ↓
Data Cleaning
      ↓
Transformation
      ├── GBP → INR
      ├── Rating → Integer
      └── Availability → Boolean-style value
      ↓
SQLite Database
      ↓
SQL Analysis
      ↓
Pandas Verification
```

## Source

```text
https://books.toscrape.com/
```

The selected categories in the current implementation are:

```text
Religion
Music
Sports and Games
Art
History
Thriller
Business
```

The supplied SQLite artifact contains **74 books across 7 categories**.

## Main Files

```text
data_pipeline/
├── scraper.py
├── cleaner.py
├── database.py
├── queries.py
├── main.py
├── books_data.db
├── sql_query_results.txt
└── README.md
```

## Run

```powershell
cd data_pipeline
pip install requests beautifulsoup4 pandas urllib3
python main.py
```

The main outputs are:

```text
books_data.db
sql_query_results.txt
```

For complete implementation details, see:

```text
data_pipeline/README.md
```

---

# Module 2 – Analytics

## Purpose

The analytics module performs exploratory data analysis and machine-learning modeling using the Titanic dataset.

## EDA

`01_eda.ipynb` performs:

- Dataset profiling
- Missing-value analysis
- Rule-based missing-value handling
- Univariate analysis
- Bivariate analysis
- Multivariate analysis
- Correlation analysis
- Survival-rate analysis
- Feature standardization checks

## Machine Learning

`02_modeling.ipynb` performs:

- Feature/target preparation
- Leakage prevention
- Stratified train/test split
- Numeric scaling
- Categorical encoding
- Logistic Regression
- Decision Tree
- Random Forest
- Confusion matrices
- ROC/AUC comparison
- Class-imbalance comparison
- SMOTE
- Random Forest hyperparameter tuning with GridSearchCV
- Out-of-Bag evaluation
- Linear Regression
- MAE, RMSE, R² and Adjusted R²
- Model persistence using Joblib

## Main Files

```text
analytics/
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── eda_visualizations.py
├── titanic.csv
├── best_model.pkl
├── charts/
└── README.md
```

## Run

```powershell
cd analytics
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn joblib jupyter
jupyter notebook
```

Run:

```text
01_eda.ipynb
```

first, followed by:

```text
02_modeling.ipynb
```

For complete analytics documentation, see:

```text
analytics/README.md
```

---

# Module 3 – Support Assistant

## Purpose

The support assistant is an offline-first Zepto policy question-answering service using Retrieval-Augmented Generation (RAG).

It uses:

```text
Zepto policy documents
       ↓
Sentence Transformer embeddings
       ↓
ChromaDB
       ↓
Top-3 cosine-similarity retrieval
       ↓
LangGraph workflow
       ↓
AnswerResponse
       ↓
FastAPI /ask
```

## RAG Architecture

```text
8 policy documents
       │
       ▼
    ingest.py
       │
       ▼
all-MiniLM-L6-v2
       │
       ▼
Persistent ChromaDB
       │
       │
User question
       │
       ▼
classify_intent
       │
       ├── policy_question
       │        │
       │        ▼
       │   retrieve_and_answer
       │        │
       │        ▼
       │   ChromaDB top-3
       │        │
       │        ▼
       │      Answer
       │
       └── general_question
                │
                ▼
          direct_answer
```

## Main Files

```text
support_assistant/
├── docs/
│   ├── doc_01.txt
│   ├── ...
│   └── doc_08.txt
├── chroma_db/
├── config.py
├── ingest.py
├── retrieval.py
├── prompts.py
├── policy_keywords.py
├── rag.py
├── main.py
├── verify.py
├── run_examples.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Local Setup

```powershell
cd support_assistant
pip install -r requirements.txt
```

The graded baseline uses:

```env
MOCK_LLM=1
```

Build the vector store:

```powershell
python ingest.py
```

Verify the RAG setup:

```powershell
python verify.py
```

Run examples:

```powershell
python run_examples.py
```

---

# FastAPI

Start the support assistant locally:

```powershell
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## API Endpoint

```text
POST /ask
```

Example request:

```json
{
  "query": "How long do I have to report a damaged item?"
}
```

The response follows:

```json
{
  "answer": "string",
  "sources": ["chunk_id"],
  "confidence": 1.0
}
```

For a policy question, `sources` should contain retrieved document/chunk IDs.

For a general out-of-domain question, the baseline returns an empty `sources` list.

---

# Docker

The support assistant includes:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

The Dockerfile uses:

```text
python:3.11-slim
```

and exposes:

```text
7860
```

## Build the Image

From the `support_assistant` directory:

```powershell
docker build -t support_assistant .
```

## Run the Container

```powershell
docker run --rm -p 7860:7860 support_assistant
```

Then open:

```text
http://localhost:7860/docs
```

## Docker Compose

Alternatively:

```powershell
docker compose up --build
```

The API is available at:

```text
http://localhost:7860/docs
```

Stop it with:

```powershell
docker compose down
```

The Docker baseline uses:

```text
MOCK_LLM=1
```

so the required grading path does not depend on an external LLM provider.

---

# End-to-End Testing

A recommended project verification sequence is:

```text
1. Data Pipeline
       │
       ├── python main.py
       └── verify books_data.db / SQL results
       │
       ▼
2. Analytics
       │
       ├── run 01_eda.ipynb
       ├── run 02_modeling.ipynb
       └── verify charts/ and best_model.pkl
       │
       ▼
3. Support Assistant
       │
       ├── python ingest.py
       ├── python verify.py
       └── python run_examples.py
       │
       ▼
4. FastAPI
       │
       └── POST /ask
       │
       ▼
5. Docker
       │
       ├── docker build
       ├── docker run
       └── test /docs and POST /ask
```

---

# Suggested API Test Cases

## Policy Question

```json
{
  "query": "How long do I have to report a damaged item?"
}
```

Expected behavior:

```text
Policy question
      ↓
RAG retrieval
      ↓
Relevant Zepto policy source
      ↓
Grounded answer
```

## Delivery Policy

```json
{
  "query": "What is the delivery fee for orders below INR 149?"
}
```

Expected behavior:

```text
Policy question
      ↓
Retrieve relevant document
      ↓
Answer with source IDs
```

## General Question

```json
{
  "query": "What is the capital of India?"
}
```

Expected baseline behavior:

```text
General question
      ↓
No policy retrieval
      ↓
"I can only answer questions about Zepto policies right now."
      ↓
sources = []
```

---

# Project Requirements by Module

## Data Engineering

The project demonstrates:

- Web scraping
- HTML parsing
- Data cleaning
- Data transformation
- Currency conversion
- Relational database design
- Primary and foreign keys
- SQL querying
- Pandas analysis
- SQL/Pandas result verification

## Analytics / Machine Learning

The project demonstrates:

- Exploratory data analysis
- Missing-value handling
- Data visualization
- Feature preprocessing
- Target-leakage prevention
- Stratified train/test split
- Classification
- Model evaluation
- ROC/AUC
- Class imbalance
- SMOTE
- Hyperparameter tuning
- Cross-validation
- Out-of-Bag evaluation
- Regression
- Model persistence

## GenAI / RAG

The project demonstrates:

- Document ingestion
- Local embeddings
- Vector search
- ChromaDB
- Cosine similarity
- Top-3 retrieval
- Structured prompting
- LangGraph
- Typed state
- Conditional routing
- Pydantic validation
- FastAPI
- Docker

---

# Repository Structure

The intended repository-level structure is:

```text
Capstone Zepto Data & AI Platform/
│
├── data_pipeline/
│   ├── scraper.py
│   ├── cleaner.py
│   ├── database.py
│   ├── queries.py
│   ├── main.py
│   ├── books_data.db
│   ├── sql_query_results.txt
│   └── README.md
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── eda_visualizations.py
│   ├── titanic.csv
│   ├── best_model.pkl
│   ├── charts/
│   └── README.md
│
├── support_assistant/
│   ├── docs/
│   ├── chroma_db/
│   ├── config.py
│   ├── ingest.py
│   ├── retrieval.py
│   ├── prompts.py
│   ├── policy_keywords.py
│   ├── rag.py
│   ├── main.py
│   ├── verify.py
│   ├── run_examples.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
│
└── README.md
```

---

# Important Notes

### Data Pipeline

The current database artifact contains:

```text
7 categories
74 books
```

The category set is:

```text
Religion
Music
Sports and Games
Art
History
Thriller
Business
```

The module README contains the detailed pipeline documentation.

### Analytics

The analytics workflow is notebook-based. Run EDA before modeling because `02_modeling.ipynb` consumes the local `titanic.csv`.

### Support Assistant

The current Docker configuration builds the local vector index during image construction:

```text
Docker build
    ↓
pip install requirements
    ↓
copy project
    ↓
python ingest.py
    ↓
ChromaDB created
    ↓
FastAPI starts
```

The baseline uses `MOCK_LLM=1`, while the optional real-LLM path can use Groq according to the support-assistant module configuration.

---

# Overall Project Outcome

This capstone combines three practical layers:

```text
DATA
 │
 ├── Scrape and store structured information
 │
 ▼
ANALYTICS
 │
 ├── Explore data
 ├── Build ML models
 └── Evaluate and persist models
 │
 ▼
AI APPLICATION
 │
 ├── Retrieve policy knowledge
 ├── Generate grounded responses
 ├── Expose API
 └── Containerize application
```

The result is a complete project demonstrating **data engineering + analytics/machine learning + retrieval-augmented AI application development**.
