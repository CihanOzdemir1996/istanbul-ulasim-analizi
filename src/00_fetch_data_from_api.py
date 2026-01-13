"""
İBB AÇIK VERİ API'DEN İETT VERİLERİNİ ÇEKME
"""

import requests
import pandas as pd
import json
from pathlib import Path

print("=" * 70)
print("İBB AÇIK VERİ API - İETT VERİSİ ÇEKME")
print("=" * 70)

# API Base URL
BASE_URL = "https://data.ibb.gov.tr/api/3/action"

def get_iett_datasets():
    """İETT ile ilgili tüm dataset'leri listele"""
    
    print("\n📡 API'ye bağlanıyor...")
    
    try:
        # İETT dataset'lerini ara
        response = requests.get(
            f"{BASE_URL}/package_search",
            params={"q": "iett", "rows": 100},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success']:
                results = data['result']['results']
                print(f"✅ {len(results)} adet İETT dataset'i bulundu!\n")
                
                # Dataset'leri listele
                for i, pkg in enumerate(results, 1):
                    print(f"{i}. {pkg['title']}")
                    print(f"   ID: {pkg['name']}")
                    print(f"   Resources: {len(pkg.get('resources', []))}")
                    print()
                
                return results
            else:
                print("❌ API başarısız yanıt döndü")
                return []
        else:
            print(f"❌ HTTP Hatası: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:
        print("❌ API zaman aşımı! İnternet bağlantınızı kontrol edin.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Bağlantı hatası: {e}")
        return []


def download_resource(resource_url, filename):
    """Bir kaynağı indir"""
    
    print(f"📥 İndiriliyor: {filename}")
    
    try:
        response = requests.get(resource_url, timeout=60)
        
        if response.status_code == 200:
            # Dosyayı kaydet
            output_path = Path("data") / filename
            output_path.parent.mkdir(exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Kaydedildi: {output_path}")
            return str(output_path)
        else:
            print(f"❌ İndirme hatası: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None


def get_dataset_details(dataset_id):
    """Bir dataset'in detaylarını getir"""
    
    try:
        response = requests.get(
            f"{BASE_URL}/package_show",
            params={"id": dataset_id},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                return data['result']
        
        return None
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None


def fetch_iett_data():
    """İETT verilerini çek ve kaydet"""
    
    # Dataset'leri listele
    datasets = get_iett_datasets()
    
    if not datasets:
        print("\n⚠️ Dataset bulunamadı veya API'ye erişilemiyor!")
        print("\nAlternatif çözüm:")
        print("1. https://data.ibb.gov.tr adresine manuel olarak gidin")
        print("2. 'İETT' araması yapın")
        print("3. CSV dosyalarını manuel indirin")
        return
    
    # İlgili dataset'leri bul
    target_keywords = ['durak', 'hat', 'güzergah', 'lokasyon']
    relevant_datasets = []
    
    for ds in datasets:
        title_lower = ds['title'].lower()
        if any(keyword in title_lower for keyword in target_keywords):
            relevant_datasets.append(ds)
    
    print("\n" + "=" * 70)
    print("İLGİLİ DATASET'LER:")
    print("=" * 70)
    
    for i, ds in enumerate(relevant_datasets, 1):
        print(f"\n{i}. {ds['title']}")
        
        # Resources (dosyalar)
        resources = ds.get('resources', [])
        for j, res in enumerate(resources, 1):
            format_type = res.get('format', 'Unknown')
            url = res.get('url', '')
            name = res.get('name', f'resource_{j}')
            
            print(f"   {j}) {name} ({format_type})")
            
            # CSV dosyalarını otomatik indir
            if format_type.upper() in ['CSV', 'JSON', 'GEOJSON']:
                filename = f"iett_{ds['name']}_{j}.{format_type.lower()}"
                download_resource(url, filename)
    
    print("\n" + "=" * 70)
    print("✅ VERİ ÇEKME TAMAMLANDI!")
    print("=" * 70)
    print("\nİndirilen dosyalar 'data/' klasöründe")


if __name__ == "__main__":
    fetch_iett_data()
    
    print("\n📝 SONRAKİ ADIM:")
    print("Eğer veri çekilmediyse:")
    print("1. https://data.ibb.gov.tr adresine gidin")
    print("2. Manuel olarak CSV indirin")
    print("3. data/ klasörüne koyun")
    print("\nVeri çekildiyse:")
    print("python src/01_data_exploration.py")
