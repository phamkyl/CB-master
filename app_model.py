import streamlit as st
import joblib
import json
import pandas as pd

model = joblib.load("data/intent_classifier.pkl")
vectorizer = joblib.load("data/tfidf_vectorizer.pkl")

with open("data/intent_answers.json", "r", encoding="utf-8") as f:
    intent_answers = json.load(f)

phones_df = pd.read_csv("data/dienthoai_renamed (1).csv")

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

# --- Giao diện thân thiện hơn ---
st.set_page_config(page_title="Chatbot Tư Vấn Điện Thoại", page_icon="📱", layout="centered")

st.markdown("<h1 style='text-align:center;color:#4B8BBE;'>🤖 Chatbot Tư Vấn Điện Thoại</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555;'>Hãy nhập câu hỏi của bạn về điện thoại, mình sẽ giúp bạn nhé!</p>", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []
if 'prev_intent' not in st.session_state:
    st.session_state.prev_intent = None
if 'prev_text' not in st.session_state:
    st.session_state.prev_text = None

def render_chat():
    for i, (speaker, text) in enumerate(st.session_state.history):
        if speaker == "Bạn":
            st.markdown(
                f"""
                <div style="
                    background-color:#DCF8C6;
                    padding:10px 15px;
                    border-radius:15px 15px 15px 0;
                    max-width:70%;
                    margin-left:auto;
                    margin-bottom:8px;
                    font-size:16px;
                    ">
                    <strong>Bạn:</strong><br>{text}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div style="
                    background-color:#E8E8E8;
                    padding:10px 15px;
                    border-radius:15px 15px 0 15px;
                    max-width:70%;
                    margin-right:auto;
                    margin-bottom:8px;
                    font-size:16px;
                    ">
                    <strong>Chatbot:</strong><br>{text}
                </div>
                """, unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Nhập câu hỏi của bạn...", placeholder="Ví dụ: Máy có camera bao nhiêu MP?", key="input")
    submitted = st.form_submit_button("Gửi")

    if submitted and user_input.strip():
        response, intent = chatbot_response(user_input, st.session_state.prev_intent, st.session_state.prev_text)
        st.session_state.history.append(("Bạn", user_input))
        st.session_state.history.append(("Chatbot", response))

        st.session_state.prev_intent = intent
        st.session_state.prev_text = user_input

render_chat()

# Scroll tự động xuống cuối chat
scroll_script = """
<script>
const chatBox = window.parent.document.querySelector('section.main > div.element-container');
if(chatBox) { chatBox.scrollTop = chatBox.scrollHeight; }
</script>
"""
st.components.v1.html(scroll_script)
