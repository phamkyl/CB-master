import joblib
import json
import pandas as pd

model = joblib.load("data/intent_classifier.pkl")
vectorizer = joblib.load("data/tfidf_vectorizer.pkl")

with open("data/intent_answers.json", "r", encoding="utf-8") as f:
    intent_answers = json.load(f)

phones_df = pd.read_csv("data/dienthoai_renamed (1).csv")
