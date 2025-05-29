import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dữ liệu
df = pd.read_csv("intent_data.csv")
texts = df['text'].astype(str)
labels = df['label'].astype(str)

# Vector hóa văn bản bằng TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(texts)
y = labels

# Tách train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Mô hình Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Dự đoán và đánh giá
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)

# In và lưu đánh giá vào file
print("🔍 Kết quả đánh giá:\n")
print(report)

with open("evaluation_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

# Lưu mô hình và vectorizer
joblib.dump(model, "intent_classifier.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("✅ Đã huấn luyện và lưu mô hình vào 'intent_classifier.pkl'")
print("✅ Báo cáo đánh giá đã lưu vào 'evaluation_report.txt'")
