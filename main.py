import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

def duckduckgo_search(query, num_results=10, max_pages=10):
    # จัดเตรียมคำค้นหาเป็น URL-safe
    query = urllib.parse.quote_plus(query)
    results = []

    # การค้นหาหลายหน้า
    for page in range(1, max_pages + 1):
        url = f"https://duckduckgo.com/html/?q={query}&s={(page - 1) * num_results}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # ส่งคำขอไปยัง DuckDuckGo
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # ดึงข้อมูลจากผลลัพธ์ค้นหาของ DuckDuckGo
            for a in soup.find_all('a', class_='result__a'):
                title = a.get_text()
                link = a['href']
                results.append((title, link))

            print(f"Page {page} results retrieved.")
        else:
            print(f"Error on page {page}: {response.status_code}")
            break

        # หยุดเมื่อได้ 1000 records
        if len(results) >= 1000:
            break

    return results

# กำหนดหัวข้อการค้นหาหลายหัวข้อ
topics = [
    "green construction materials",
    "sustainable building materials",
    "eco-friendly construction materials",
    "recycled construction materials",
    "innovative construction materials"
]

# รวบรวมผลลัพธ์จากหลายหัวข้อ
all_results = []

for topic in topics:
    print(f"Searching for: {topic}")
    results = duckduckgo_search(topic, num_results=10, max_pages=10)
    all_results.extend(results)

# บันทึกผลลัพธ์ลงในไฟล์ CSV
with open('duckduckgo_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])  # เขียน header
    for title, link in all_results:
        writer.writerow([title, link])  # เขียนข้อมูลแต่ละแถว

print("ผลลัพธ์ถูกบันทึกลงในไฟล์ 'duckduckgo_results.csv' แล้ว")