import feedparser
import csv
from datetime import datetime
import os
from prefect import task, flow

# คำค้นหาหลายคำที่เกี่ยวกับ alternative construction materials
search_keywords = [
    "construction materials",
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

@task
def create_data_folder_and_csv(csv_path: str):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(csv_path)
    if not file_exists:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "link", "published", "fetched_at", "keyword"])
    return file_exists

@task
def load_existing_links(csv_path: str):
    existing_links = set()
    if os.path.isfile(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames and "link" in reader.fieldnames:
                for row in reader:
                    existing_links.add(row["link"])
    return existing_links

@task
def scrape_and_save(csv_path: str, keyword: str, existing_links: set):
    new_entries = 0
    rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}"
    feed = feedparser.parse(rss_url)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
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
    return new_entries

@flow
def scrape_news_flow():
    csv_path = os.path.join("data", "scrap_data.csv")
    create_data_folder_and_csv(csv_path)
    existing_links = load_existing_links(csv_path)

    total_new_entries = 0
    for keyword in search_keywords:
        new_entries = scrape_and_save(csv_path, keyword, existing_links)
        total_new_entries += new_entries

    print(f"✅ ดึงข่าวใหม่ {total_new_entries} รายการจาก {len(search_keywords)} คำค้นและบันทึกลง scrap_data.csv แล้ว")

if __name__ == "__main__":
    scrape_news_flow()
