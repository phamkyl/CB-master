import re

KienThucCauHinh = {
    "ram": "💡 RAM (Random Access Memory)...",
    "pin": "🔋 Dung lượng pin...",
    "camera": "📷 Độ phân giải camera...",
    "storage": "💾 Bộ nhớ...",
    "brand": "🏷️ Mỗi hãng điện thoại...",
    "chip": "⚙️ Chip xử lý..."
}

def tra_cuu_kien_thuc(text):
    text_lower = text.lower()

    if "ram" in text_lower:
        if any(kw in text_lower for kw in ["8gb", "8 gb"]) and any(kw in text_lower for kw in ["16gb", "cao hơn", "so sánh"]):
            return "💡 RAM 8GB đủ... RAM 16GB tốt hơn cho đa nhiệm."
        elif any(kw in text_lower for kw in ["như thế nào", "là gì"]):
            return KienThucCauHinh.get("ram")

    if "pin" in text_lower:
        if any(kw in text_lower for kw in ["so sánh", "thời lượng"]):
            return "🔋 Pin dung lượng lớn hơn..."
        elif any(kw in text_lower for kw in ["là gì", "tác dụng"]):
            return KienThucCauHinh.get("pin")

    if "camera" in text_lower:
        if "so sánh" in text_lower:
            return "📷 Camera cao MP ảnh đẹp hơn..."
        elif "là gì" in text_lower:
            return KienThucCauHinh.get("camera")

    for keyword in KienThucCauHinh:
        if re.search(keyword, text_lower):
            return KienThucCauHinh[keyword]

    return None
