import pandas as pd
import json

# Đọc dữ liệu training có 3 cột: text, label, answer
df = pd.read_csv("intent_data.csv")

# Tạo dictionary mapping label (intent) → câu trả lời mẫu (answer)
label_to_answer = {}
for label, ans in zip(df['label'], df['answer']):
    if label not in label_to_answer:
        if isinstance(ans, str) and ans.strip():
            label_to_answer[label] = ans.strip()
        else:
            label_to_answer[label] = ""  # Câu trả lời mặc định nếu không có

# Lưu dictionary ra file JSON
with open("intent_answers.json", "w", encoding="utf-8") as f:
    json.dump(label_to_answer, f, ensure_ascii=False, indent=2)
