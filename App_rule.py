import streamlit as st
import pandas as pd
import re

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

    # Trích xuất Brand
    brand_matches = [brand for brand in BRANDS if brand.lower() in text.lower()]
    if brand_matches:
        info["Brand"] = brand_matches

    # Cải tiến trích xuất khoảng giá:
    # Tìm tất cả các số liên quan đến giá, rồi xác định khoảng giá
    # Hỗ trợ dạng "khoảng 10 triệu đến 20 triệu", "giá 10-20 triệu", "từ 10 triệu đến 20 triệu"
    price_numbers = re.findall(r'(\d{1,3})\s*(triệu|tr)?', text.lower())
    price_ranges = re.findall(r'(\d{1,3})\s*(triệu|tr)?\s*(đến|-|~)\s*(\d{1,3})\s*(triệu|tr)?', text.lower())

    if price_ranges:
        # Lấy khoảng giá đầu tiên tìm được
        start, _, _, end, _ = price_ranges[0]
        price_from = int(start) * 1_000_000
        price_to = int(end) * 1_000_000
        # Đảm bảo price_from <= price_to
        if price_from > price_to:
            price_from, price_to = price_to, price_from
        info["PriceRange"] = (price_from, price_to)

    elif len(price_numbers) >= 2:
        # Nếu có ít nhất 2 số giá, giả định 2 số đó là khoảng giá
        p_from = int(price_numbers[0][0]) * 1_000_000
        p_to = int(price_numbers[1][0]) * 1_000_000
        if p_from > p_to:
            p_from, p_to = p_to, p_from
        info["PriceRange"] = (p_from, p_to)

    elif price_numbers:
        # Nếu chỉ có 1 giá, coi như giá cố định
        info["FinalPrice"] = int(price_numbers[0][0]) * 1_000_000

    # Các thông số khác
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



# --- Phân tích xem có phải câu hỏi lý thuyết không (cập nhật cải tiến cho câu hỏi RAM) ---
def tra_cuu_kien_thuc(text):
    text_lower = text.lower()

    # Xử lý câu hỏi về RAM (so sánh 8GB với 16GB hoặc cao hơn)
    if "ram" in text_lower:
        if any(kw in text_lower for kw in ["8gb", "8 gb"]) and any(kw in text_lower for kw in ["16gb", "16 gb", "cao hơn", "lớn hơn", "so sánh", "khác biệt"]):
            return (
                "💡 RAM 8GB đủ cho đa số tác vụ và chơi game mượt mà. "
                "RAM 16GB hoặc cao hơn giúp đa nhiệm tốt hơn, chuyển đổi ứng dụng nhanh hơn, "
                "phù hợp với người dùng chuyên sâu hoặc chạy các ứng dụng nặng."
            )
        # Trả lời câu hỏi chung về RAM
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "tác dụng", "có tốt không"]):
            return KienThucCauHinh.get("ram")

    # Xử lý câu hỏi về Pin
    if "pin" in text_lower or "battery" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "khác biệt", "khác nhau", "cao hơn", "thời lượng"]):
            return (
                "🔋 Pin dung lượng lớn hơn (ví dụ 5000mAh so với 4000mAh) thường cho thời gian sử dụng dài hơn. "
                "Tuy nhiên, thời lượng pin còn phụ thuộc vào tối ưu phần mềm và cách sử dụng."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "có tốt không"]):
            return KienThucCauHinh.get("pin")

    # Xử lý câu hỏi về Camera
    if "camera" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "khác biệt", "khác nhau", "chất lượng"]):
            return (
                "📷 Camera có độ phân giải cao hơn thường cho ảnh sắc nét hơn, nhưng chất lượng còn phụ thuộc vào cảm biến và phần mềm xử lý ảnh."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "tác dụng", "có tốt không"]):
            return KienThucCauHinh.get("camera")

    # Xử lý câu hỏi về Storage (bộ nhớ)
    if "bộ nhớ" in text_lower or "storage" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "khác biệt", "khác nhau"]):
            return (
                "💾 Bộ nhớ lớn hơn (ví dụ 256GB so với 128GB) cho phép lưu trữ nhiều dữ liệu hơn như ảnh, video và ứng dụng."
            )
        elif any(kw in text_lower for kw in ["như thế nào", "là gì", "tác dụng", "có tốt không"]):
            return KienThucCauHinh.get("storage")

    # Xử lý câu hỏi về Brand (hãng)
    if "hãng" in text_lower or "brand" in text_lower:
        return KienThucCauHinh.get("brand")

    # Xử lý câu hỏi về Chip (CPU)
    if "chip" in text_lower or "cpu" in text_lower:
        return KienThucCauHinh.get("chip")

    # Nếu phát hiện nhiều từ khóa cùng lúc hỏi tổng quát
    cau_hoi_phan_mem = ["so sánh", "khác biệt", "như thế nào", "thế nào", "có tốt không"]
    if any(kw in text_lower for kw in cau_hoi_phan_mem):
        # Tổng hợp giải thích cho các thành phần phổ biến
        ket_qua = []
        for key in ["ram", "pin", "camera", "storage", "brand", "chip"]:
            if key in text_lower:
                ket_qua.append(KienThucCauHinh[key])
        if ket_qua:
            return "\n\n".join(ket_qua)

    # Mặc định trả lời theo từng từ khóa đơn
    for keyword in KienThucCauHinh:
        if re.search(keyword, text_lower):
            return KienThucCauHinh[keyword]

    return None


# --- Lọc sản phẩm theo tiêu chí ---
# --- Hàm lọc sản phẩm theo tiêu chí ---
def loc_dien_thoai(info, df):
    ket_qua = df.copy()

    if "PriceRange" in info:
        price_from, price_to = info["PriceRange"]
        ket_qua = ket_qua[(ket_qua["FinalPrice"] >= price_from) & (ket_qua["FinalPrice"] <= price_to)]
    elif "FinalPrice" in info:
        price = info["FinalPrice"]
        # Lọc linh hoạt ±1 triệu hoặc theo mức
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



# --- UI Streamlit ---
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

    # Gọi hàm trích xuất thông tin
    thong_tin_moi = trich_xuat_thong_tin(user_input)

    # Gộp thông tin mới với thông tin cũ
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

# Hiển thị lịch sử trò chuyện
st.markdown("## 📜 Lịch sử trò chuyện")
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")

# Nút xóa
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Xóa lịch sử"):
        st.session_state.chat_history = []
with col2:
    if st.button("♻️ Xóa tiêu chí lọc"):
        st.session_state.thong_tin_tich_luy = {}