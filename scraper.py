import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from utils import create_session

# Base URL untuk scraping
base_url = "https://sinta.kemdikbud.go.id/google?page="

# Inisialisasi sesi request (jika perlu login)
session = create_session()

# Rentang halaman yang ingin di-scrape (contoh: 5005-5015)
start_page = 5005
end_page = start_page + 10

# Simpan semua hasil scraping
all_data = []

for page in range(start_page, end_page + 1):
    url = base_url + str(page)
    print(f"📄 Scraping halaman {page}...")

    response = session.get(url)
    
    if response.status_code != 200:
        print(f"❌ Gagal mengakses halaman {page}, lanjut ke halaman berikutnya...")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # Temukan semua artikel
    articles = soup.find_all("div", class_="ar-title")

    for article in articles:
        # Judul publikasi
        title_tag = article.find("a")
        title = title_tag.text.strip() if title_tag else "N/A"
        link = title_tag["href"] if title_tag else "N/A"

        # Penulis
        authors_tag = article.find_next("div", class_="ar-meta")
        authors = authors_tag.text.replace("Authors :", "").strip() if authors_tag else "N/A"

        # Tahun publikasi
        year_tag = article.find_next("a", class_="ar-year")
        year = year_tag.text.strip() if year_tag else "N/A"

        # Jumlah sitasi
        cited_tag = article.find_next("a", class_="ar-cited")
        cited = cited_tag.text.replace("cited", "").strip() if cited_tag else "0"

        # Institusi
        institution_tag = article.find_next("a", class_="ar-pub")
        institution = institution_tag.text.strip() if institution_tag else "N/A"

        # Simpan data ke dalam list
        all_data.append({
            "Halaman": page,
            "Judul": title,
            "Tautan": link,
            "Penulis": authors,
            "Tahun": year,
            "Sitasi": cited,
            "Institusi": institution
        })

    # Delay untuk menghindari pemblokiran
    time.sleep(2)

# Konversi ke DataFrame dan simpan ke CSV
df = pd.DataFrame(all_data)
df.to_csv("data/hasil_scraping.csv", index=False)

print("✅ Scraping selesai! Data disimpan dalam data/hasil_scraping.csv")
