# 🏛️ Project 1: AI-Driven Citizen Grievance & Sentiment Analysis System

## 🚧 Project Status
**Ongoing Internship Project - Week 4 In Progress**
This project is part of the Infotact Technical Internship Program. It focuses on analyzing large-scale NYC 311 service request data using Natural Language Processing (NLP) to build an automated complaint routing and urgency scoring pipeline.

---

## 🎯 Objective
Architect an AI-powered NLP system that:
- Automatically ingests citizen feedback
- Categorizes complaints into relevant government departments
- Performs sentiment analysis to prioritize issues based on urgency
- Exposes predictions via a FastAPI REST endpoint

---

## 📂 Dataset
- **Name:** NY 311 Service Requests
- **Source:** Kaggle / NYC Open Data
- **Link:** https://www.kaggle.com/datasets/new-york-city/ny-311-service-requests
- **Size:** 14.69 GB (193,533 rows used after filtering)
- **Columns:** 46 columns → reduced to 8 key columns
- **Key Fields:** Created Date, Agency, Complaint Type, Descriptor, Borough, Department

> Dataset not included in repo due to size. Download from Kaggle and place in `project1_nlp/data/raw/`

---

## ✅ Weekly Progress

### Week 1 - Data Collection, Text Cleaning & EDA ✅
- Loaded 14.5GB dataset efficiently using chunking
- Reduced to 193,533 rows and 8 columns
- Text cleaning: lowercase, stopwords removal, lemmatization
- Generated Word Cloud and Bigram frequency charts
- Department distribution analysis
- All EDA documented in Jupyter Notebook

### Week 2 - Department Categorization ✅
- TF-IDF Vectorization (10,000 features, unigrams + bigrams)
- Logistic Regression classifier for 13 departments
- **Test Accuracy: 98.91%**
- **Macro F1: 0.88**
- Cross-validation Macro F1: 0.8791 ± 0.004
- Models saved: `department_classifier.pkl`, `tfidf_vectorizer.pkl`

### Week 3 - Sentiment Analysis & Urgency Scoring ✅
- Hybrid approach: VADER + Domain Keywords + Logistic Regression
- Urgency labels: Critical 🔴 | Negative 🟡 | Neutral 🟢
- Label distribution: Neutral 68% | Negative 30.3% | Critical 1.7%
- VADER threshold tuning: best threshold at -0.3
- **Test Accuracy: 99.73%**
- **Macro F1: 0.98**
- **Cross-validation Macro F1: 0.9855 ± 0.0077**
- Priority scoring: Neutral→1, Negative→2, Critical→3
- Models saved: `tfidf_sentiment.pkl`, `sentiment_classifier.pkl`

### Week 4 - FastAPI Deployment 🔄

#### Day 1 ✅ - Tue 12 May (Subramani)
- FastAPI + Uvicorn setup and installation
- Created main `main.py` with full application structure
- Implemented `GET /` root endpoint → 200 OK
- Implemented `GET /health` health check endpoint → 200 OK
- Swagger UI docs live at `/docs`
- All endpoints tested and verified locally

#### Day 2 ⏳ - Wed 13 May (Karthik)
- Department classification endpoint `/predict/department`
- Load department models and return predicted department

#### Day 3 ⏳ - Thu 14 May (Riya)
- Sentiment + priority scoring endpoint `/predict/sentiment`
- Load sentiment models and return label + priority score

#### Day 4 ⏳ - Fri 15 May (Subramani + Sadiq)
- Combined `/predict` endpoint integrating all models
- API testing with Postman
- Final integration and documentation

---

## 🛠️ Tech Stack
| Component | Technology |
|---|---|
| Language | Python 3.10 |
| Data Processing | Pandas, NumPy |
| NLP | NLTK, VADER, spaCy |
| ML Models | Scikit-learn (Logistic Regression) |
| Visualization | Matplotlib, Seaborn, WordCloud |
| API | FastAPI, Uvicorn |
| Version Control | Git, GitHub |

---

## 📁 Project Structure
DSML_Project/
├── project1_nlp/
│   ├── app/                          # FastAPI application (Week 4)
│   │   ├── main.py                   # Main FastAPI app
│   │   ├── department_router.py      # Department prediction endpoint
│   │   ├── sentiment_router.py       # Sentiment scoring endpoint
│   │   └── test_api.py               # API testing
│   ├── data/
│   │   ├── raw/                      # Original dataset (gitignored)
│   │   └── processed/                # Cleaned dataset
│   ├── models/                       # Saved .pkl model files
│   │   ├── department_classifier.pkl
│   │   ├── tfidf_vectorizer.pkl
│   │   ├── sentiment_classifier.pkl
│   │   └── tfidf_sentiment.pkl
│   └── notebooks/
│       ├── week1_eda_preprocessing.ipynb
│       ├── week2_department_classifier.ipynb
│       └── week3_sentiment_urgency.ipynb
├── .gitignore
├── README.md
└── requirements.txt

---

## 👥 Team
- **Subramani** — Team Lead | Main App + Integration
- **Karthik** — ML Engineer | Department Classification API
- **Riya** — ML Engineer | Sentiment Scoring API
- **Sadiq** — QA + Docs | API Testing & Documentation
