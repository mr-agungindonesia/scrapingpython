print("Hello, World!"  
      )

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
