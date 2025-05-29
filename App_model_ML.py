import streamlit as st
from modules.chatbot_logic import chatbot_response
from modules.ui_components import render_chat

st.set_page_config(page_title="Chatbot Tư Vấn Điện Thoại", page_icon="📱", layout="centered")

st.markdown("<h1 style='text-align:center;color:#4B8BBE;'>🤖 Chatbot Tư Vấn Điện Thoại</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555;'>Hãy nhập câu hỏi của bạn về điện thoại, mình sẽ giúp bạn nhé!</p>", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []
if 'prev_intent' not in st.session_state:
    st.session_state.prev_intent = None
if 'prev_text' not in st.session_state:
    st.session_state.prev_text = None

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

scroll_script = """
<script>
const chatBox = window.parent.document.querySelector('section.main > div.element-container');
if(chatBox) { chatBox.scrollTop = chatBox.scrollHeight; }
</script>
"""
st.components.v1.html(scroll_script)
