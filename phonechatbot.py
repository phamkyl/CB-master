import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import google.generativeai as genai

# Streamlit page config
st.set_page_config(page_title="Phone Store Chatbot", layout="wide")

# Load environment variables
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GENAI_API_KEY)

# Load dataset as 'phones_df'
DATA_PATH = "data/dienthoai_renamed (1).csv"
phones_df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else pd.DataFrame()

# Initialize chat history in session with greeting
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {'role': 'assistant', 'text': '👋 Xin chào quý khách! Chào mừng đến với cửa hàng điện thoại. Hãy nhập tên điện thoại bạn muốn tìm hiểu hoặc để tôi gợi ý cho bạn!'}
    ]

# Main interface
st.title("🤖💬 Chatbot Cửa Hàng Điện Thoại")
st.markdown("Bạn có thể hỏi về bất kỳ điện thoại nào trong cửa hàng, mình sẽ tư vấn.")

# Chat input and processing
user_input = st.chat_input("Bạn muốn mua điện thoại nào hoặc có câu hỏi gì?")
if user_input:
    # Append user message before response generation
    st.session_state.chat_history.append({'role': 'user', 'text': user_input})

    # Prepare context: full store data
    context_text = phones_df.to_dict(orient='records')
    prompt = f"""
Bạn là trợ lý bán hàng điện thoại.
Dữ liệu sản phẩm:
{context_text}

Khách hàng hỏi: {user_input}
Hãy tư vấn chi tiết, gợi ý sản phẩm phù hợp.
"""

    # Call Gemini
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    chat = model.start_chat()
    resp = chat.send_message(prompt)
    answer = resp.text

    # Append assistant reply
    st.session_state.chat_history.append({'role': 'assistant', 'text': answer})

# Display chat history
for entry in st.session_state.chat_history:
    st.chat_message(entry['role']).write(entry['text'])
