import streamlit as st

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
