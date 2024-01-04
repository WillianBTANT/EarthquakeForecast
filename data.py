import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    earthquake_rows = soup.find_all("tr")

    data = []
    for row in earthquake_rows:
        columns = row.find_all("td")
        if columns:
            magnitude = columns[0].text.strip()
            time = columns[1].text.strip()
            time_parts = time.split()  # Splitting 'time' by spaces
            date_part = time_parts[0]  # Extracting the date part
            time_part = time_parts[1]  # Extracting the time part
            latitude = columns[2].text.strip()
            longitude = columns[3].text.strip()
            depth = columns[4].text.strip()
            location = columns[5].text.strip()
            data.append([magnitude, date_part, time_part, latitude, longitude, depth, location])

    return data


def scrape_all_pages(base_url, total_pages):
    all_data = []

    for page_num in range(1, total_pages + 1):
        url = f"{base_url}&page={page_num}"
        print(f"Scraping page {page_num} - {url}")
        page_data = scrape_page(url)
        all_data.extend(page_data)

    return all_data

base_url = "https://www.ceic.ac.cn/speedsearch?time=6&&page=1"
total_pages = 51  # Adjust this based on the total number of pages

all_data = scrape_all_pages(base_url, total_pages)

with open('dz.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["震级", "日期", "时间", "纬度", "经度", "深度", "地点"])
    writer.writerows(all_data)

print("数据已保存到 dz.csv 文件中")


def main():
    return None