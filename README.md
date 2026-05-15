<<<<<<< HEAD
# DSML 311 Service Requests Project

This DSML project predicts whether a 311 service request will close quickly.

The target is:

```text
fast_close = 1 if Closed Date - Created Date <= 48 hours
fast_close = 0 otherwise
```

The model uses only fields that are available when the request is created, such as agency, complaint type, borough, submission channel, zip code, latitude, longitude, and created-date features.

## Dataset

Main dataset:

```text
C:\Users\Sadiqul Islam\Downloads\NY 311 Service Requests\311-service-requests-from-2010-to-present.csv
```

This file is very large, so the code trains on a configurable number of rows instead of loading everything at once.

## Step 1: Install Requirements

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pip install -r requirements.txt
```

## Step 2: Explore the Dataset

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\explore_data.py --rows 100000
```

This prints:

- dataset shape
- missing values
- most common complaint types
- borough counts
- resolution-time summary

## Step 3: Train the Model

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\train_model.py --rows 100000 --fast-close-hours 48
```

Outputs:

```text
models\dsml_311_fast_close_model.joblib
reports\classification_report.txt
reports\confusion_matrix.png
```

## Step 4: Try More Data

After the first run works, increase rows:

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\train_model.py --rows 500000 --fast-close-hours 48
```

## Step 5: Predict New Requests

Create a small CSV with the same feature columns, then run:

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\predict.py --input new_requests.csv --output reports\predictions.csv
```

The output adds:

- `fast_close_prediction`
- `fast_close_probability`

## Step 6: Run the API Locally

Start the FastAPI server:

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Prediction endpoint:

```text
POST http://127.0.0.1:8000/predict
```

Use this JSON body:

```json
{
  "created_date": "2019-12-01T02:04:01.000",
  "agency": "DOT",
  "complaint_type": "Street Condition",
  "descriptor": "Pothole",
  "location_type": "Street",
  "incident_zip": "10001",
  "borough": "MANHATTAN",
  "open_data_channel_type": "ONLINE",
  "latitude": 40.745668482774114,
  "longitude": -73.9877188309367
}
```

Example response:

```json
{
  "fast_close_prediction": 1,
  "fast_close_label": "fast_close",
  "fast_close_probability": 0.977,
  "fast_close_hours": 48.0
}
```

## Step 7: Test in Postman

1. Open Postman.
2. Create a new `POST` request.
3. URL:

```text
http://127.0.0.1:8000/predict
```

4. Go to `Body`.
5. Select `raw`.
6. Select `JSON`.
7. Paste the JSON from `postman_sample_request.json`.
8. Click `Send`.

You should receive `fast_close_prediction`, `fast_close_label`, and `fast_close_probability`.

## Step 8: Deploy on Render

This project includes `render.yaml` and `Procfile`.

Render settings:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

Deploy steps:

1. Push this project to a GitHub repository.
2. Go to Render.
3. Click `New +`.
4. Select `Web Service`.
5. Connect your GitHub repository.
6. Select Python environment.
7. Use the build and start commands above.
8. Click `Deploy Web Service`.

After deploy, test:

```text
https://your-render-app-name.onrender.com/health
https://your-render-app-name.onrender.com/docs
```

Then test this endpoint in Postman:

```text
POST https://your-render-app-name.onrender.com/predict
```

## Project Files

```text
src\config.py          dataset path and column settings
src\explore_data.py    simple EDA script
src\train_model.py     training and evaluation script
src\predict.py         prediction script
src\api.py             DSML FastAPI deployment API
requirements.txt       Python dependencies
models\                saved model output
reports\               reports and charts
```
=======
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
>>>>>>> ab166886d98b852400d06243de458d5cc600cd53
