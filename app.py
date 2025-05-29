import streamlit as st
st.set_page_config(page_title="Chatbot Tư vấn Điện thoại", page_icon="📱", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #333; font-family: Arial, sans-serif;'>📱 Chatbot Tư vấn Điện thoại</h1>",
    unsafe_allow_html=True)
import pandas as pd
import re
from datetime import datetime

# Today's date and time for timestamps (as provided: 05:55 PM +07, May 29, 2025)
current_time = datetime(2025, 5, 29, 17, 55)

# --- Dữ liệu sản phẩm ---
df = pd.read_csv("data/dienthoai_renamed (1).csv")
BRANDS = df["Brand"].unique()

# --- Kiến thức cơ bản về cấu hình ---
KienThucCauHinh = {
    "ram": "💡 RAM (Random Access Memory) giúp điện thoại chạy đa nhiệm mượt mà hơn. RAM 8GB là đủ cho phần lớn các tác vụ, chơi game và làm việc.",
    "pin": "🔋 Dung lượng pin càng lớn (ví dụ 5000mAh) thì thời gian sử dụng càng dài. Tuy nhiên, thời lượng còn phụ thuộc vào tần suất sử dụng và tối ưu hệ thống.",
    "camera": "📷 Độ phân giải camera (MP) cao cho phép chụp ảnh sắc nét hơn, nhưng chất lượng ảnh còn phụ thuộc vào cảm biến, ống kính và phần mềm xử lý.",
    "storage": "💾 Bộ nhớ (storage) là nơi lưu trữ ảnh, ứng dụng, video... 128GB phù hợp người dùng phổ thông, 256GB+ dành cho người chụp ảnh/video nhiều.",
    "brand": "🏷️ Mỗi hãng điện thoại có thế mạnh riêng: Apple tối ưu mượt mà, Samsung nhiều tính năng, Xiaomi giá tốt, Asus hiệu năng cao cho game thủ.",
    "chip": "⚙️ Chip xử lý (CPU) như Snapdragon, Apple A, MediaTek... ảnh hưởng đến hiệu năng tổng thể. Chip mạnh cho trải nghiệm mượt khi chơi game, mở ứng dụng."
}


# --- Trích xuất thông tin người dùng ---
def trich_xuat_thong_tin(text):
    info = {}
    brand_matches = [brand for brand in BRANDS if brand.lower() in text.lower()]
    if brand_matches:
        info["Brand"] = brand_matches
    price_numbers = re.findall(r'(\d{1,3})\s*(triệu|tr)?', text.lower())
    price_ranges = re.findall(r'(\d{1,3})\s*(triệu|tr)?\s*(đến|-|~)\s*(\d{1,3})\s*(triệu|tr)?', text.lower())
    if price_ranges:
        start, _, _, end, _ = price_ranges[0]
        price_from = int(start) * 1_000_000
        price_to = int(end) * 1_000_000
        if price_from > price_to:
            price_from, price_to = price_to, price_from
        info["PriceRange"] = (price_from, price_to)
    elif len(price_numbers) >= 2:
        p_from = int(price_numbers[0][0]) * 1_000_000
        p_to = int(price_numbers[1][0]) * 1_000_000
        if p_from > p_to:
            p_from, p_to = p_to, p_from
        info["PriceRange"] = (p_from, p_to)
    elif price_numbers:
        info["FinalPrice"] = int(price_numbers[0][0]) * 1_000_000
    match_ram = re.search(r'ram\s*(\d+)', text.lower())
    if match_ram:
        info["RAM"] = int(match_ram.group(1))
    match_storage = re.search(r'(?:bộ nhớ|storage)?\s*(\d+)\s*gb', text.lower())
    if match_storage:
        info["Storage"] = int(match_storage.group(1))
    match_camera = re.search(r'camera\s*(\d+)', text.lower())
    if match_camera:
        info["RearCameraResolution"] = int(match_camera.group(1))
    match_battery = re.search(r'(?:pin|battery)\s*(\d+)', text.lower())
    if match_battery:
        info["BatteryCapacity"] = int(match_battery.group(1))
    return info


# --- Phân tích câu hỏi lý thuyết ---
def tra_cuu_kien_thuc(text):
    text_lower = text.lower()
    if "ram" in text_lower:
        if any(kw in text_lower for kw in ["8gb", "8 gb"]) and any(
                kw in text_lower for kw in ["16gb", "16 gb", "cao hơn", "lớn hơn", "so sánh", "khác biệt"]):
            return (
                "💡 RAM 8GB đủ cho đa số tác vụ và chơi game mượt mà. "
                "RAM 16GB hoặc cao hơn giúp đa nhiệm tốt hơn, chuyển đổi ứng dụng nhanh hơn, "
                "phù hợp với người dùng chuyên sâu hoặc chạy các ứng dụng nặng."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "tác dụng", "có tốt không"]):
            return KienThucCauHinh.get("ram")
    if "pin" in text_lower or "battery" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "khác biệt", "khác nhau", "cao hơn", "thời lượng"]):
            return (
                "🔋 Pin dung lượng lớn hơn (ví dụ 5000mAh so với 4000mAh) thường cho thời gian sử dụng dài hơn. "
                "Tuy nhiên, thời lượng pin còn phụ thuộc vào tối ưu phần mềm và cách sử dụng."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "có tốt không"]):
            return KienThucCauHinh.get("pin")
    if "camera" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "khác biệt", "khác nhau", "chất lượng"]):
            return (
                "📷 Camera có độ phân giải cao hơn thường cho ảnh sắc nét hơn, nhưng chất lượng còn phụ thuộc vào cảm biến và phần mềm xử lý ảnh."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "tác dụng", "có tốt không"]):
            return KienThucCauHinh.get("camera")
    if "bộ nhớ" in text_lower or "storage" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "khác biệt", "khác nhau"]):
            return (
                "💾 Bộ nhớ lớn hơn (ví dụ 256GB so với 128GB) cho phép lưu trữ nhiều dữ liệu hơn như ảnh, video và ứng dụng."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "tác dụng", "có tốt không"]):
            return KienThucCauHinh.get("storage")
    if "hãng" in text_lower or "brand" in text_lower:
        return KienThucCauHinh.get("brand")
    if "chip" in text_lower or "cpu" in text_lower:
        return KienThucCauHinh.get("chip")
    cau_hoi_phan_mem = ["so sánh", "khác biệt", "như thế nào", "thế nào", "có tốt không"]
    if any(kw in text_lower for kw in cau_hoi_phan_mem):
        ket_qua = []
        for key in ["ram", "pin", "camera", "storage", "brand", "chip"]:
            if key in text_lower:
                ket_qua.append(KienThucCauHinh[key])
        if ket_qua:
            return "\n\n".join(ket_qua)
    for keyword in KienThucCauHinh:
        if re.search(keyword, text_lower):
            return KienThucCauHinh[keyword]
    return None


# --- Lọc sản phẩm theo tiêu chí ---
def loc_dien_thoai(info, df):
    ket_qua = df.copy()
    if "PriceRange" in info:
        price_from, price_to = info["PriceRange"]
        ket_qua = ket_qua[(ket_qua["FinalPrice"] >= price_from) & (ket_qua["FinalPrice"] <= price_to)]
    elif "FinalPrice" in info:
        price = info["FinalPrice"]
        ket_qua = ket_qua[(ket_qua["FinalPrice"] >= price - 1_000_000) & (ket_qua["FinalPrice"] <= price + 1_000_000)]
    if "Brand" in info:
        ket_qua = ket_qua[ket_qua["Brand"].str.lower().isin([b.lower() for b in info["Brand"]])]
    if "RAM" in info:
        ram = info["RAM"]
        ket_qua = ket_qua[ket_qua["RAM"] >= ram]
    if "Storage" in info:
        storage = info["Storage"]
        ket_qua = ket_qua[ket_qua["Storage"] >= storage]
    if "RearCameraResolution" in info:
        cam = info["RearCameraResolution"]
        ket_qua = ket_qua[ket_qua["RearCameraResolution"] >= cam]
    if "BatteryCapacity" in info:
        pin = info["BatteryCapacity"]
        ket_qua = ket_qua[ket_qua["BatteryCapacity"] >= pin]
    return ket_qua


# --- Custom CSS for User-Friendly Interface ---
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.chat-container {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 15px;
    height: 60vh;
    overflow-y: auto;
    margin-bottom: 20px;
    box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
}
.chat-message {
    margin: 8px 0;
    display: flex;
    align-items: flex-start;
}
.chat-message.user {
    justify-content: flex-end;
}
.chat-message.bot {
    justify-content: flex-start;
}
.chat-bubble {
    max-width: 75%;
    padding: 10px 15px;
    border-radius: 15px;
    line-height: 1.4;
    word-wrap: break-word;
    font-size: 16px;
    font-family: 'Arial', sans-serif;
}
.chat-bubble.user {
    background-color: #4a90e2;
    color: white;
    border-bottom-right-radius: 4px;
}
.chat-bubble.bot {
    background-color: #f1f1f1;
    color: #333;
    border-bottom-left-radius: 4px;
}
.sender {
    font-size: 0.85em;
    color: #888;
    margin-bottom: 3px;
}
.timestamp {
    font-size: 0.75em;
    color: #aaa;
    margin-top: 3px;
    text-align: right;
}
.input-container {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    border-radius: 30px;
    padding: 10px 15px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.stTextInput > div > div > input {
    border: none !important;
    background-color: transparent !important;
    font-size: 16px;
    font-family: 'Arial', sans-serif;
}
.stButton > button {
    border-radius: 30px;
    background-color: #4a90e2;
    color: white;
    margin-left: 10px;
    padding: 8px 20px;
    font-size: 16px;
    transition: background-color 0.2s;
}
.stButton > button:hover {
    background-color: #357abd;
}
.clear-button {
    background-color: #ff6b6b !important;
    color: white !important;
    border-radius: 30px !important;
    padding: 8px 20px !important;
    font-size: 16px !important;
    transition: background-color 0.2s;
}
.clear-button:hover {
    background-color: #e55a5a !important;
}
.product-card {
    background-color: #fafafa;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
    border: 1px solid #e8e8e8;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    font-size: 15px;
}
.auto-scroll {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    min-height: 100%;
}
.stApp {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# --- UI Streamlit ---


# Initialize session state
if "chat_history" not in st.session_state:
    # Initialize with prior conversation history
    st.session_state.chat_history = [
        ("user", "Initial code submission for chatbot (Streamlit code for phone consultation)", "17:55"),
        ("bot", """
        <div class='product-card'>
            <strong>Improved Chatbot UI</strong><br>
            📦 Enhanced with chat bubbles, product cards, and scrollable chat history.<br>
            🧠 Modern design resembling Messenger/Zalo.<br>
            📷 Includes custom CSS for styling.<br>
            🔋 Fully functional with previous logic preserved.
        </div>
        """, "17:55"),
        ("user", "dựng lại để lịch sử đoạn chat phía trên và trong khung chat có thể nhìn thấy được",
         "17:55"),
        ("user", "viết theo kiểu giao diện này nà", "17:55"),
        ("user",
         "sửa lại cho thân thiện với dễ dùng hơn. phần khung chat ở phía dưới câu trả lời và phía trên là đoạn lịch sử , câu trả lời hỏi của khách hàng và hệ thống",
         "17:55"),
    ]
if "thong_tin_tich_luy" not in st.session_state:
    st.session_state.thong_tin_tich_luy = {}

# Display chat history
st.markdown("<h3 style='color: #333; font-family: Arial, sans-serif;'>💬 Lịch sử trò chuyện</h3>",
            unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="chat-container"><div class="auto-scroll">', unsafe_allow_html=True)
    for sender, msg, timestamp in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f"""
            <div class='chat-message user'>
                <div>
                    <div class='sender'>👤 Bạn</div>
                    <div class='chat-bubble user'>{msg}</div>
                    <div class='timestamp'>{timestamp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message bot'>
                <div>
                    <div class='sender'>🤖 Chatbot</div>
                    <div class='chat-bubble bot'>{msg}</div>
                    <div class='timestamp'>{timestamp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# Auto-scroll to bottom
st.markdown("""
<script>
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
</script>
""", unsafe_allow_html=True)

# Chat input form (below the chat history)
st.markdown("<h3 style='color: #333; font-family: Arial, sans-serif;'>💬 Trò chuyện với Chatbot</h3>",
            unsafe_allow_html=True)
with st.container():
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input("Nhập câu hỏi hoặc yêu cầu của bạn:",
                                       placeholder="Ví dụ: Tìm điện thoại Samsung giá 10-15 triệu, RAM 8GB...",
                                       label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Gửi")

# Process user input
if submitted and user_input:
    # Add user message with timestamp
    timestamp = current_time.strftime("%H:%M")
    st.session_state.chat_history.append(("user", user_input, timestamp))

    # Check if it's a knowledge-based question
    kien_thuc = tra_cuu_kien_thuc(user_input)
    if kien_thuc:
        st.session_state.chat_history.append(("bot", kien_thuc, timestamp))
    else:
        # Extract information and filter products
        thong_tin_moi = trich_xuat_thong_tin(user_input)
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
        ket_qua = loc_dien_thoai(thong_tin_hop_le, df)

        if not ket_qua.empty:
            response = []
            for _, row in ket_qua.head(5).iterrows():
                product_info = f"""
                <div class='product-card'>
                    <strong>{row['Product']} ({row['Brand']})</strong><br>
                    📦 Giá: <strong>{row['FinalPrice'] // 1_000_000} triệu</strong><br>
                    🧠 RAM: {row['RAM']}GB | 💾 Bộ nhớ: {row['Storage']}GB<br>
                    📷 Camera: {row['RearCameraResolution']}MP | 🔋 Pin: {row['BatteryCapacity']}mAh
                </div>
                """
                response.append(product_info)
            st.session_state.chat_history.append(("bot", "".join(response), timestamp))
        else:
            st.session_state.chat_history.append(("bot", "❌ Không tìm thấy sản phẩm phù hợp với yêu cầu.", timestamp))

    # Rerun to update the UI
    st.experimental_rerun()

# Clear buttons (below the input form)
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Xóa lịch sử", key="clear_history", help="Xóa toàn bộ lịch sử trò chuyện"):
        st.session_state.chat_history = []
        st.experimental_rerun()
with col2:
    if st.button("♻️ Xóa tiêu chí lọc", key="clear_filters", help="Xóa các tiêu chí tìm kiếm đã lưu"):
        st.session_state.thong_tin_tich_luy = {}
        st.experimental_rerun()