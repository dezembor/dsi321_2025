import pandas as pd
from nltk.corpus import stopwords
import nltk
import os

# โหลด stopwords ภาษาอังกฤษ
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# รายชื่อบริษัท/เว็บไซต์/องค์กรที่ต้องลบ
remove_words = [
    "BBC", "DW", "ResearchGate", "Dezeen", "HowStuffWorks",
    "Power Line Magazine", "ET EnergyWorld", "trend", "promoting", "about", "About", "and", "use"
]

# ฟังก์ชันลบคำที่เป็นชื่อองค์กร
def remove_companies(text):
    for word in remove_words:
        # ลบทั้งแบบคำเดี่ยวและท้ายประโยค
        text = re.sub(rf"\b{re.escape(word)}\b", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()  # ลบช่องว่างซ้ำ

# โหลดข่าว
df = pd.read_csv("data/scrap_data.csv")

# ลบ missing
df = df.dropna(subset=["title", "keyword"])

# เตรียม list สำหรับเก็บผลลัพธ์
filtered_rows = []

for _, row in df.iterrows():
    title = str(row["title"])
    keyword = row["keyword"]
    
    words = title.split()
    filtered = [word for word in words if word.lower() not in stop_words and word.isalpha()]
    filtered_title = " ".join(filtered)
    
    filtered_rows.append({
        "cleaned_title": filtered_title,
        "keyword": keyword
    })

# สร้าง DataFrame ใหม่
filtered_df = pd.DataFrame(filtered_rows)

# บันทึกไฟล์ใหม่
output_path = "data/filtered_by_topic.csv"
filtered_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✅ บันทึกไฟล์ {output_path} เรียบร้อยแล้ว (ลบ stop words และแยกตาม topic)")

