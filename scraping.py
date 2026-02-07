# scraping data BMKG dengan session dan retry
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time

# Setup session dengan retry
def create_session():
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })
    
    return session

session = create_session()

# =====================================
# BMKG memiliki data publik dalam format XML
# Ini lebih mudah diakses daripada website utama
# =====================================

print("=" * 60)
print("BMKG Public Weather Data API")
print("=" * 60)

# URL data cuaca publik BMKG (format XML)
# Dokumentasi: https://data.bmkg.go.id/prakiraan-cuaca/
weather_urls = {
    'DKI Jakarta': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml',
    'Jawa Barat': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml',
    'Jawa Tengah': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml',
    'Jawa Timur': 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml',
}

# Test mengakses data cuaca
for region, url in weather_urls.items():
    print(f"\n📍 {region}")
    try:
        response = session.get(url, timeout=30)
        
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📦 Size: {len(response.content)} bytes")
            
            # Parse XML
            soup = BeautifulSoup(response.content, 'xml')
            
            # Ambil info area
            areas = soup.find_all('area', limit=3)
            for area in areas:
                name = area.get('description', 'Unknown')
                print(f"   🏙️ Area: {name}")
        else:
            print(f"   ❌ Status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Jeda antar request
    time.sleep(1)

print("\n" + "=" * 60)
print("Gempa Terbaru")
print("=" * 60)

# Data gempa terbaru
gempa_url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
try:
    response = session.get(gempa_url, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        gempa = data.get('Infogempa', {}).get('gempa', {})
        
        print(f"🕐 Waktu: {gempa.get('Tanggal', '')} {gempa.get('Jam', '')}")
        print(f"📍 Lokasi: {gempa.get('Wilayah', '')}")
        print(f"📊 Magnitude: {gempa.get('Magnitude', '')}")
        print(f"📏 Kedalaman: {gempa.get('Kedalaman', '')}")
        print(f"🌊 Potensi: {gempa.get('Potensi', '')}")
    else:
        print(f"❌ Status: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Selesai!")

