import feedparser
import csv
from datetime import datetime
import os

# คำค้นหาหลายคำที่เกี่ยวกับ alternative construction materials
search_keywords = [
     "construction materials",
    "building materials",
    "building materials",
    "building supplies",
    "construction market",
    "construction news",
    "construction chemicals",
    "material shortage",
    "price increase construction",
    "supply chain construction",
    "green building materials",
    "sustainable construction",
]

# สร้างโฟลเดอร์ 'data' ถ้ายังไม่มี
os.makedirs("data", exist_ok=True)
# ชื่อไฟล์ CSV ที่จะบันทึก
csv_path = os.path.join("data", "scrap_data.csv")
file_exists = os.path.isfile(csv_path)

# โหลดลิงก์ที่เคยบันทึกไว้
existing_links = set()
if file_exists:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames and "link" in reader.fieldnames:
            for row in reader:
                existing_links.add(row["link"])
        else:
            print("❌ ไม่พบหรือไม่มี field 'link' ในไฟล์ CSV")

# เตรียมเขียน CSV
new_entries = 0
with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # เขียน header ถ้ายังไม่มีไฟล์
    if not file_exists:
        writer.writerow(["title", "link", "published", "fetched_at", "keyword"])

    for keyword in search_keywords:
        rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}"
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            if entry.link not in existing_links:
                writer.writerow([
                    entry.title,
                    entry.link,
                    entry.published,
                    datetime.now().isoformat(),
                    keyword
                ])
                existing_links.add(entry.link)
                new_entries += 1

print(f"✅ ดึงข่าวใหม่ {new_entries} รายการจาก {len(search_keywords)} คำค้นและบันทึกลง scrap_data.csv แล้ว")

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# โหลด stopwords ของภาษาอังกฤษ (โหลดครั้งแรกเท่านั้น)
nltk.download('stopwords')

# เตรียม stop words
stop_words = set(stopwords.words('english'))

# โหลดไฟล์ข่าว
df = pd.read_csv("data/scrap_data.csv")

# รวม title ของข่าวทั้งหมดเป็นข้อความเดียว
text = " ".join(df["title"].dropna().astype(str))

# ตัด stopwords ออก
filtered_words = [
    word for word in text.split()
    if word.lower() not in stop_words and word.isalpha()
]
filtered_text = " ".join(filtered_words)

# สร้าง WordCloud จากข้อความที่ตัด stopwords แล้ว
wordcloud = WordCloud(
    width=1000,
    height=600,
    background_color='white',
    max_words=200,
    collocations=False
).generate(filtered_text)

# แสดงผล
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud (without Stopwords)", fontsize=16)
plt.show()
