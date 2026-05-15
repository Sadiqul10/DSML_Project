# Week 4: Day 2 - Department Classification Endpoint
from fastapi import APIRouter
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

router = APIRouter()

# Load models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dept_model = joblib.load(os.path.join(BASE_DIR, "notebooks/models/department_classifier.pkl"))
dept_vectorizer = joblib.load(os.path.join(BASE_DIR, "notebooks/models/tfidf_vectorizer.pkl"))

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words]
    return " ".join(words)

@router.post("/predict/department")
def predict_department(complaint: dict):
    text = complaint.get("text", "")
    cleaned = clean_text(text)
    vec = dept_vectorizer.transform([cleaned])
    department = dept_model.predict(vec)[0]
    return {
        "input": text,
        "predicted_department": department
    }