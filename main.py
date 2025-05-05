import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

def duckduckgo_search(query, num_results=10, max_pages=10):
    # จัดเตรียมคำค้นหาเป็น URL-safe
    query = urllib.parse.quote_plus(query)
    results = []
    seen_links = set()  # ใช้ set สำหรับเก็บ link ที่เจอแล้ว

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
                
                # ตรวจสอบว่า link นี้ซ้ำหรือยัง
                if link not in seen_links:
                    seen_links.add(link)  # ถ้ายังไม่เคยเก็บ link นี้ ก็ให้เพิ่มเข้าไป
                    results.append((title, link))  # เพิ่มผลลัพธ์ที่ไม่ซ้ำ

            print(f"Page {page} results retrieved.")
        else:
            print(f"Error on page {page}: {response.status_code}")
            break


    return results

# กำหนดหัวข้อการค้นหาหลายหัวข้อ
topics = [
    "Life Cycle Assessment of Alternative Construction Materials: Comparing the environmental impact from production to disposal.",
    "Physical and Mechanical Properties of Compressed Earth Blocks: Investigating strength, thermal conductivity, and durability.",
    "The Potential of Bamboo as a Structural Construction Material: Design considerations, limitations, and development pathways.",
    "Applications of Concrete Mixed with Recycled Materials: Challenges and opportunities for practical use.",
    "Thermal Insulation from Natural Materials: Efficiency and cost-effectiveness compared to synthetic options.",
    "Developing Construction Materials from Agricultural Waste: Such as rice husks, straw, and sugarcane bagasse.",
    "Bio-based Construction Materials: Trends and emerging innovations in the industry.",
    "The Use of 3D Printing with Alternative Construction Materials: Feasibility and limitations.",
    "Designing Energy-Efficient Buildings with Alternative Construction Materials: Case studies and analysis.",
    "Standards and Regulations for Alternative Construction Materials: Issues and approaches to standardization.",
    "Adoption and Acceptance of Alternative Construction Materials in Thailand: Influencing factors and promotion strategies.",
    "The Economic Impact of Using Alternative Construction Materials on Local Communities: Job creation and income generation.",
    "Promoting Alternative Construction Materials for Sustainable Development: The role of government and the private sector.",
    "Consumer Awareness and Understanding of Alternative Construction Materials: Surveys and analysis.",
    "Opportunities and Challenges in the Production of Alternative Construction Materials in Thailand: Competition and innovation.",
    "Developing Alternative Construction Materials with Enhanced Properties: Such as carbon dioxide absorption.",
    "Improving the Properties of Alternative Construction Materials with New Technologies: Nanotechnology, composite materials.",
    "Research and Development of Alternative Construction Materials from Local Resources: Adding value and reducing costs.",
    "Integrating Alternative Construction Materials into the Circular Economy Concept: Waste reduction and reuse.",
    "Building Networks and Collaboration for the Development of Alternative Construction Materials: Among researchers, manufacturers, and users."
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
