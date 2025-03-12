import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Buat sesi request agar bisa login (jika perlu)
def create_session():
    session = requests.Session()
    login_url = "https://example.com/login"  # Sesuaikan dengan URL login
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = session.post(login_url, data=payload)
    
    if response.status_code == 200:
        print("✅ Login berhasil!")
    else:
        print("❌ Login gagal, periksa kredensial Anda.")
    
    return session
