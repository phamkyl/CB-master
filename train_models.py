import pandas as pd
from recommender.preprocess import preprocess_data
from recommender.knn_recommender import KNNRecommender
from recommender.rf_recommender import train_rf
from recommender.embedding_model import train_embedding_model
import joblib

if __name__ == "__main__":
    df = pd.read_csv('data/dienthoai_renamed (1).csv')

    # Nếu có nhãn phù hợp (ví dụ điểm đánh giá), thay đổi ở đây
    # y = ...

    # Train & lưu KNN
    X, preprocessor = preprocess_data(df)
    knn = KNNRecommender()
    knn.fit(X, df)
    knn.save()
    joblib.dump(preprocessor, 'models/preprocessor.pkl')
    print("KNN model & preprocessor đã lưu")

    # Train & lưu RF nếu có y
    # rf, preprocessor_rf = train_rf(df, y)

    # Train & lưu embedding model
    train_embedding_model(X, epochs=30)
