import streamlit as st
import pandas as pd
from utils.extractor import trich_xuat_thong_tin
from utils.knowledge import tra_cuu_kien_thuc
from utils.filter import loc_dien_thoai

# Load dữ liệu
df = pd.read_csv("data/dienthoai_renamed (1).csv")

st.set_page_config(page_title="Chatbot Tư vấn Điện thoại", page_icon="📱")
st.title("📱 Chatbot Tư vấn Điện thoại Thông minh")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thong_tin_tich_luy" not in st.session_state:
    st.session_state.thong_tin_tich_luy = {}

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Hãy nhập câu hỏi hoặc yêu cầu của bạn:")
    submitted = st.form_submit_button("Gửi")

if submitted and user_input:
    st.session_state.chat_history.append(("👤 Bạn", user_input))

    thong_tin_moi = trich_xuat_thong_tin(user_input, df["Brand"].unique())
    thong_tin_hop_le = st.session_state.thong_tin_tich_luy.copy()

    for key, val in thong_tin_moi.items():
        if key == "Brand":
            old = thong_tin_hop_le.get("Brand", [])
            if not isinstance(old, list):
                old = [old]
            thong_tin_hop_le["Brand"] = list(set(old + val))
        else:
            thong_tin_hop_le[key] = val

    st.session_state.thong_tin_tich_luy = thong_tin_hop_le

    giai_thich = tra_cuu_kien_thuc(user_input)
    if giai_thich:
        st.session_state.chat_history.append(("🤖 Chatbot", giai_thich))
    else:
        ket_qua = loc_dien_thoai(thong_tin_hop_le, df)

        if not ket_qua.empty:
            response = "📱 Dưới đây là một số gợi ý:\n"
            for _, row in ket_qua.iterrows():
                response += f"""- **{row['Product']}** ({row['Brand']})  
📦 Giá: **{row['FinalPrice']//1_000_000} triệu**  
🧠 RAM: {row['RAM']}GB | Bộ nhớ: {row['Storage']}GB  
📷 Camera: {row['RearCameraResolution']}MP | 🔋 Pin: {row['BatteryCapacity']}mAh  
---\n"""
        else:
            response = "❌ Không tìm thấy sản phẩm phù hợp với yêu cầu."
        st.session_state.chat_history.append(("🤖 Chatbot", response))

# Hiển thị lịch sử
st.markdown("## 📜 Lịch sử trò chuyện")
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Xóa lịch sử"):
        st.session_state.chat_history = []
with col2:
    if st.button("♻️ Xóa tiêu chí lọc"):
        st.session_state.thong_tin_tich_luy = {}
