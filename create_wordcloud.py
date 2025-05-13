import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# โหลดไฟล์ที่ลบ stopwords และชื่อบริษัทแล้ว
df = pd.read_csv("data/filtered_by_topic.csv")

# รวมข้อความทั้งหมดจากคอลัมน์ cleaned_title
all_text = " ".join(df["cleaned_title"].dropna().astype(str))

# สร้าง Word Cloud
wordcloud = WordCloud(
    width=1000,
    height=600,
    background_color='white',
    max_words=200,
    colormap='viridis',      # เปลี่ยนโทนสีได้ตามต้องการ เช่น 'plasma', 'inferno', 'cividis'
    collocations=False       # ปิดการรวมคำซ้ำ (เช่น "New York")
).generate(all_text)

# แสดงผล
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Construction Material Topics", fontsize=16)
plt.show()
