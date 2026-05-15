# Week 4: Day 3 - Sentiment and Priority Scoring Endpoint
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sent_model = joblib.load(os.path.join(BASE_DIR, "notebooks/models/sentiment_classifier.pkl"))
sent_vectorizer = joblib.load(os.path.join(BASE_DIR, "notebooks/models/tfidf_sentiment.pkl"))

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
priority_map = {"Neutral": 1, "Negative": 2, "Critical": 3}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words]
    return " ".join(words)

@router.post("/predict/sentiment")
def predict_sentiment(complaint: dict):
    text = complaint.get("text", "")
    cleaned = clean_text(text)
    vec = sent_vectorizer.transform([cleaned])
    sentiment = sent_model.predict(vec)[0]
    priority = priority_map.get(sentiment, 1)
    return {
        "input": text,
        "sentiment": sentiment,
        "priority_score": priority,
        "priority_label": "Critical" if priority == 3 else "Needs Attention" if priority == 2 else "Routine"
    }
