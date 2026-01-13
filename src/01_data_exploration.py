"""
İSTANBUL TOPLU TAŞIMA ANALİZİ
Data Analyst Portfolio Projesi

Amaç: İETT otobüs verilerini analiz edip interaktif dashboard oluşturmak
Yazar: [İsminiz]
Tarih: 2026-01-13
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Görselleştirme ayarları
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 70)
print("İSTANBUL TOPLU TAŞIMA ANALİZİ - VERİ YÜKLEME")
print("=" * 70)

# =============================================================================
# ADIM 1: VERİYİ YÜKLE
# =============================================================================

def load_data():
    """
    İETT verilerini yükle
    
    Not: İBB Açık Veri'den indirdiğiniz CSV dosyalarının yolunu güncelleyin
    """
    
    print("\n📂 Veri yükleniyor...")
    
    try:
        # Hat bilgileri
        # df_hatlar = pd.read_csv('iett_hatlar.csv', encoding='utf-8')
        # print(f"✅ Hat bilgileri yüklendi: {df_hatlar.shape}")
        
        # Durak bilgileri
        # df_duraklar = pd.read_csv('iett_duraklar.csv', encoding='utf-8')
        # print(f"✅ Durak bilgileri yüklendi: {df_duraklar.shape}")
        
        # Yolcu istatistikleri (eğer varsa)
        # df_yolcu = pd.read_csv('iett_yolcu.csv', encoding='utf-8')
        # print(f"✅ Yolcu istatistikleri yüklendi: {df_yolcu.shape}")
        
        print("\n⚠️  Henüz veri yüklenMEdi!")
        print("Lütfen İBB Açık Veri'den CSV dosyalarını indirin ve yukarıdaki")
        print("satırların comment'ini kaldırın (# işaretini silin)")
        
        return None, None, None
        
    except FileNotFoundError as e:
        print(f"\n❌ HATA: Dosya bulunamadı - {e}")
        print("\nÇözüm:")
        print("1. https://data.ibb.gov.tr adresine gidin")
        print("2. 'İETT' araması yapın")
        print("3. CSV dosyalarını indirin")
        print("4. Bu script ile aynı klasöre koyun")
        return None, None, None


# =============================================================================
# ADIM 2: VERİYİ KEŞFET (EDA - Exploratory Data Analysis)
# =============================================================================

def explore_data(df, dataset_name):
    """
    Dataset'in genel özelliklerini göster
    """
    
    if df is None:
        return
    
    print("\n" + "=" * 70)
    print(f"📊 {dataset_name.upper()} - VERİ KEŞFİ")
    print("=" * 70)
    
    # Boyut
    print(f"\n📏 Boyut: {df.shape[0]:,} satır × {df.shape[1]} sütun")
    
    # İlk 5 satır
    print(f"\n👀 İlk 5 Satır:")
    print(df.head())
    
    # Sütun bilgileri
    print(f"\n📋 Sütun Bilgileri:")
    print(df.info())
    
    # Eksik değerler
    print(f"\n❓ Eksik Değerler:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        missing_df = pd.DataFrame({
            'Sütun': missing.index,
            'Eksik Sayısı': missing.values,
            'Yüzde (%)': (missing.values / len(df) * 100).round(2)
        })
        print(missing_df[missing_df['Eksik Sayısı'] > 0])
    else:
        print("✅ Eksik değer yok!")
    
    # Sayısal sütunlar için istatistikler
    if len(df.select_dtypes(include=[np.number]).columns) > 0:
        print(f"\n📈 İstatistiksel Özet:")
        print(df.describe())


# =============================================================================
# ADIM 3: ÖRNEK ANALİZLER (Veri geldiğinde kullanılacak)
# =============================================================================

def analyze_hat_dagilimi(df_hatlar):
    """
    Hat dağılımını analiz et
    """
    if df_hatlar is None:
        return
    
    print("\n" + "=" * 70)
    print("🚌 HAT DAĞILIMI ANALİZİ")
    print("=" * 70)
    
    # İlçelere göre hat sayısı (eğer ilçe sütunu varsa)
    if 'ilce' in df_hatlar.columns:
        ilce_dagilim = df_hatlar['ilce'].value_counts().head(10)
        print("\n📍 En Fazla Hat Olan 10 İlçe:")
        print(ilce_dagilim)
        
        # Görselleştirme
        fig = px.bar(
            x=ilce_dagilim.index,
            y=ilce_dagilim.values,
            title="İlçelere Göre Hat Sayısı (Top 10)",
            labels={'x': 'İlçe', 'y': 'Hat Sayısı'},
            color=ilce_dagilim.values,
            color_continuous_scale='Viridis'
        )
        fig.show()


def analyze_durak_yogunlugu(df_duraklar):
    """
    Durak yoğunluğunu analiz et
    """
    if df_duraklar is None:
        return
    
    print("\n" + "=" * 70)
    print("📍 DURAK YOĞUNLUĞU ANALİZİ")
    print("=" * 70)
    
    # İlçelere göre durak sayısı
    if 'ilce' in df_duraklar.columns:
        durak_dagilim = df_duraklar['ilce'].value_counts().head(10)
        print("\n📍 En Fazla Durak Olan 10 İlçe:")
        print(durak_dagilim)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    
    print("\n🚀 Analiz başlıyor...\n")
    
    # Veriyi yükle
    df_hatlar, df_duraklar, df_yolcu = load_data()
    
    # Her dataset için keşif yap
    if df_hatlar is not None:
        explore_data(df_hatlar, "Hat Bilgileri")
        analyze_hat_dagilimi(df_hatlar)
    
    if df_duraklar is not None:
        explore_data(df_duraklar, "Durak Bilgileri")
        analyze_durak_yogunlugu(df_duraklar)
    
    if df_yolcu is not None:
        explore_data(df_yolcu, "Yolcu İstatistikleri")
    
    print("\n" + "=" * 70)
    print("✅ ANALİZ TAMAMLANDI!")
    print("=" * 70)
    
    print("\n📝 SONRAKI ADIMLAR:")
    print("1. İBB Açık Veri'den CSV dosyalarını indirin")
    print("2. Bu script'in bulunduğu klasöre koyun")
    print("3. load_data() fonksiyonundaki comment'leri kaldırın")
    print("4. Script'i tekrar çalıştırın")
    print("\n🎯 Sonra: Harita görselleştirme ve dashboard!")
