import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

def duckduckgo_search(query, num_results=10, max_pages=10):
    query = urllib.parse.quote_plus(query)
    results = []
    seen_links = set()  # สำหรับตรวจสอบลิงก์ซ้ำ

    for page in range(1, max_pages + 1):
        url = f"https://duckduckgo.com/html/?q={query}&s={(page - 1) * num_results}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.find_all('a', class_='result__a'):
                title = a.get_text()
                link = a['href']
                if link not in seen_links:
                    seen_links.add(link)
                    results.append((title, link))

            print(f"Page {page} results retrieved.")
        else:
            print(f"Error on page {page}: {response.status_code}")
            break

        if len(results) >= 1000:
            break

    return results

topics = [
    "green construction materials",
    "sustainable building materials",
    "eco-friendly construction materials",
    "recycled construction materials",
    "innovative construction materials"
]

all_results = []
seen_links_all = set()  # ตรวจสอบลิงก์ซ้ำรวมจากทุกหัวข้อ

for topic in topics:
    print(f"Searching for: {topic}")
    results = duckduckgo_search(topic, num_results=10, max_pages=10)
    for title, link in results:
        if link not in seen_links_all:
            seen_links_all.add(link)
            all_results.append((title, link))

# บันทึกผลลัพธ์ลงในไฟล์ CSV
with open('duckduckgo_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])
    for title, link in all_results:
        writer.writerow([title, link])

print("ผลลัพธ์ถูกบันทึกลงในไฟล์ 'duckduckgo_results.csv' แล้ว")
