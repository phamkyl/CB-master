from .model_loader import model, vectorizer, intent_answers, phones_df

def chatbot_response(text, prev_intent=None, prev_text=None):
    X = vectorizer.transform([text])
    intent = model.predict(X)[0]

    if len(text.strip()) < 5 and prev_text:
        combined_text = prev_text + " " + text
        X_combined = vectorizer.transform([combined_text])
        intent = model.predict(X_combined)[0]

    if intent == "brand_question":
        brand_keywords = ["samsung", "apple", "xiaomi", "oppo", "vivo"]
        text_lower = text.lower()
        brand_filter = None
        for b in brand_keywords:
            if b in text_lower:
                brand_filter = b.capitalize()
                break
        if brand_filter:
            filtered = phones_df[phones_df["Brand"] == brand_filter]
            if filtered.empty:
                return f"Xin lỗi, hiện tại không có điện thoại {brand_filter} trong kho.", intent
            else:
                results = filtered.head(3)
                resp = f"Mình tìm thấy các điện thoại {brand_filter}:\n"
                for _, row in results.iterrows():
                    resp += f"- {row['Product']} (Giá: {row['FinalPrice']:,} VND)\n"
                return resp, intent
        else:
            return "Bạn muốn tìm điện thoại của hãng nào vậy?", intent

    answer = intent_answers.get(intent, "")
    if answer:
        return answer, intent
    else:
        return "Xin lỗi, mình chưa hiểu câu hỏi của bạn. Bạn có thể hỏi lại được không?", intent
