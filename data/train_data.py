import csv
import random
from itertools import product

# Cấu trúc intent
intents = {
    "camera_question": {
        "templates": [
            "Camera của điện thoại này {how}?",
            "Chụp hình {good} không?",
            "Camera trước là bao nhiêu {unit}?",
            "Máy có hỗ trợ {feature} không?"
        ],
        "variables": {
            "how": ["bao nhiêu MP", "độ phân giải bao nhiêu", "mấy chấm"],
            "good": ["đẹp", "rõ", "sắc nét"],
            "unit": ["megapixel", "MP"],
            "feature": ["quay phim 4K", "chống rung OIS", "chụp đêm"]
        },
        "answer": "Điện thoại này có camera chính 50MP, hỗ trợ quay phim 4K và chụp ảnh chất lượng cao."
    },
    "ram_question": {
        "templates": [
            "Máy có bao nhiêu {ram_unit} RAM?",
            "RAM của điện thoại này là {value}?",
            "Có tùy chọn RAM {value} không?"
        ],
        "variables": {
            "ram_unit": ["GB", "giga"],
            "value": ["8GB", "12GB", "6GB"]
        },
        "answer": "Điện thoại có các tùy chọn RAM từ 6GB đến 12GB, đáp ứng tốt đa nhiệm."
    },
    "battery_question": {
        "templates": [
            "Dung lượng pin {how}?",
            "Pin có {strong} không?",
            "Máy dùng được {how_long}?"
        ],
        "variables": {
            "how": ["bao nhiêu", "là bao nhiêu"],
            "strong": ["trâu", "tốt", "bền"],
            "how_long": ["bao lâu", "mấy tiếng"]
        },
        "answer": "Pin 5000mAh dùng thoải mái cả ngày, hỗ trợ sạc nhanh 33W."
    },
    "chip_question": {
        "templates": [
            "Máy dùng chip gì?",
            "Hiệu năng {how}?",
            "Dùng {brand1} hay {brand2}?"
        ],
        "variables": {
            "how": ["có mạnh không", "chơi game tốt không", "ổn không"],
            "brand1": ["Snapdragon"],
            "brand2": ["MediaTek"]
        },
        "answer": "Máy trang bị chip Snapdragon 8 Gen 1, cho hiệu năng mạnh mẽ khi chơi game và xử lý tác vụ nặng."
    },
    "storage_question": {
        "templates": [
            "Máy có bộ nhớ trong bao nhiêu?",
            "Lưu trữ được {how_much} không?",
            "Có hỗ trợ thẻ nhớ không?"
        ],
        "variables": {
            "how_much": ["nhiều", "nhiều ảnh", "nhiều video"]
        },
        "answer": "Bộ nhớ trong từ 128GB đến 512GB, có hỗ trợ mở rộng bằng thẻ nhớ."
    },
    "greeting": {
        "phrases": ["Xin chào", "Chào shop", "Hello", "Shop ơi"],
        "answer": ""
    },
    "goodbye": {
        "phrases": ["Cảm ơn nhé", "Tạm biệt", "Hẹn gặp lại", "Bye shop"],
        "answer": "Cảm ơn bạn đã ghé shop! Chúc bạn một ngày tuyệt vời và hẹn gặp lại nhé!"
    },
    "price_request": {
        "phrases": ["Máy này giá bao nhiêu?", "Giá điện thoại là bao nhiêu vậy?", "Bao nhiêu tiền?"],
        "answer": ""
    },
    "brand_question": {
        "phrases": ["Có điện thoại Samsung không?", "Bên mình bán iPhone chứ?", "Có máy Xiaomi không?"],
        "answer": ""
    }
}

# Hàm sinh câu từ template
def generate_sentences(template, variables, max_count=50):
    var_keys = list(variables.keys())
    var_values = [variables[key] for key in var_keys]
    combinations = list(product(*var_values))
    random.shuffle(combinations)
    sentences = []
    for combo in combinations[:max_count]:
        filled = template
        for key, value in zip(var_keys, combo):
            filled = filled.replace("{" + key + "}", value)
        sentences.append(filled)
    return sentences

# Tạo dữ liệu
data = []
for label, content in intents.items():
    if "templates" in content:
        for template in content["templates"]:
            sentences = generate_sentences(template, content["variables"], max_count=60)
            for text in sentences:
                data.append({"text": text, "label": label, "answer": content["answer"]})
    elif "phrases" in content:
        # Nhân bản nhẹ mỗi câu phrase cho đủ số lượng
        for phrase in content["phrases"]:
            for _ in range(25):  # nhân 25 lần mỗi câu
                data.append({"text": phrase, "label": label, "answer": content["answer"]})

# Xáo trộn và cắt đúng 2000 dòng
random.shuffle(data)
data = data[:2000]

# Ghi ra file
with open("intent_data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "label", "answer"])
    writer.writeheader()
    writer.writerows(data)

print(f"✅ Đã sinh {len(data)} dòng và lưu vào intent_data.csv")
