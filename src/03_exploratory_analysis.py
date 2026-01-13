"""
İSTANBUL TOPLU TAŞIMA ANALİZİ
03 - Keşifsel Veri Analizi (EDA)

Bu script ile:
- Veri dağılımını analiz edeceğim
- Normallik testleri yapacağım
- Aykırı değerleri tespit edeceğim
- İstatistiksel görseller oluşturacağım

Yazar: Cihan Özdemir
Tarih: 13 Ocak 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Görselleştirme ayarları
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("=" * 80)
print("İSTANBUL TOPLU TAŞIMA ANALİZİ - KEŞİFSEL VERİ ANALİZİ (EDA)")
print("=" * 80)

# =============================================================================
# VERİ YÜKLEME
# =============================================================================

print("\n📂 Veriler yükleniyor...")

try:
    df_durak = pd.read_csv(r'C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_durak_final.csv')
    df_hat = pd.read_csv(r'C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_hat_final.csv')
    print(f"✅ Durak verisi yüklendi: {len(df_durak):,} satır")
    print(f"✅ Hat verisi yüklendi: {len(df_hat):,} satır")
except FileNotFoundError as e:
    print(f"❌ HATA: {e}")
    print("Lütfen önce veri temizleme script'ini çalıştırın!")
    exit()

# =============================================================================
# 1. GENEL VERİ İNCELEMESİ
# =============================================================================

print("\n" + "=" * 80)
print("1. GENEL VERİ İNCELEMESİ")
print("=" * 80)

print("\n📍 DURAK VERİSİ:")
print(f"Toplam Satır: {len(df_durak):,}")
print(f"Toplam Sütun: {len(df_durak.columns)}")
print(f"Sütunlar: {list(df_durak.columns)}")

print("\n🚌 HAT VERİSİ:")
print(f"Toplam Satır: {len(df_hat):,}")
print(f"Toplam Sütun: {len(df_hat.columns)}")
print(f"Sütunlar: {list(df_hat.columns)}")

# =============================================================================
# 2. İLÇE BAZINDA DAĞILIM ANALİZİ
# =============================================================================

print("\n" + "=" * 80)
print("2. İLÇE BAZINDA DAĞILIM ANALİZİ")
print("=" * 80)

# İlçe sütununu bul
ilce_columns = [col for col in df_durak.columns if 'ilce' in col.lower() or 'district' in col.lower()]

if ilce_columns:
    ilce_col = ilce_columns[0]
    print(f"\n✅ İlçe sütunu bulundu: {ilce_col}")
    
    # İlçe bazında durak sayısı
    durak_per_ilce = df_durak[ilce_col].value_counts()
    
    print(f"\n🏙️ İlçelere Göre Durak Dağılımı (Top 15):")
    print(durak_per_ilce.head(15))
    
    # Tanımlayıcı istatistikler
    print(f"\n📊 Tanımlayıcı İstatistikler:")
    print(f"   • Toplam İlçe Sayısı: {len(durak_per_ilce)}")
    print(f"   • Ortalama Durak/İlçe: {durak_per_ilce.mean():.2f}")
    print(f"   • Medyan: {durak_per_ilce.median():.2f}")
    print(f"   • Standart Sapma: {durak_per_ilce.std():.2f}")
    print(f"   • Minimum: {durak_per_ilce.min()}")
    print(f"   • Maksimum: {durak_per_ilce.max()}")
    
    # Çarpıklık ve basıklık
    skewness = durak_per_ilce.skew()
    kurtosis = durak_per_ilce.kurtosis()
    print(f"\n📐 Dağılım Özellikleri:")
    print(f"   • Çarpıklık (Skewness): {skewness:.4f}")
    if abs(skewness) < 0.5:
        print("     → Yaklaşık simetrik dağılım")
    elif skewness > 0.5:
        print("     → Sağa çarpık (pozitif çarpık)")
    else:
        print("     → Sola çarpık (negatif çarpık)")
    
    print(f"   • Basıklık (Kurtosis): {kurtosis:.4f}")
    if abs(kurtosis) < 0.5:
        print("     → Normal dağılıma yakın")
    elif kurtosis > 0.5:
        print("     → Normal'den daha sivri (leptokurtic)")
    else:
        print("     → Normal'den daha düz (platykurtic)")

else:
    print("⚠️ İlçe sütunu bulunamadı!")
    ilce_col = None

# =============================================================================
# 3. NORMALLİK TESTLERİ
# =============================================================================

print("\n" + "=" * 80)
print("3. NORMALLİK TESTLERİ")
print("=" * 80)

if ilce_col and len(durak_per_ilce) >= 3:
    
    print("\n📈 Shapiro-Wilk Normallik Testi:")
    print("   (H0: Veriler normal dağılıma sahiptir)")
    
    stat, p_value = stats.shapiro(durak_per_ilce)
    
    print(f"\n   Test İstatistiği (W): {stat:.6f}")
    print(f"   P-Value: {p_value:.6f}")
    print(f"   Anlamlılık Seviyesi (α): 0.05")
    
    if p_value > 0.05:
        print(f"\n   ✅ SONUÇ: Dağılım NORMAL (p = {p_value:.6f} > 0.05)")
        print("   → H0 hipotezi reddedilemez")
        print("   → Parametrik testler kullanılabilir (t-test, ANOVA)")
    else:
        print(f"\n   ❌ SONUÇ: Dağılım NORMAL DEĞİL (p = {p_value:.6f} < 0.05)")
        print("   → H0 hipotezi reddedilir")
        print("   → Non-parametrik testler kullanılmalı (Mann-Whitney, Kruskal-Wallis)")
    
    # Kolmogorov-Smirnov testi (alternatif)
    print("\n📈 Kolmogorov-Smirnov Normallik Testi:")
    ks_stat, ks_pvalue = stats.kstest(durak_per_ilce, 'norm', 
                                       args=(durak_per_ilce.mean(), durak_per_ilce.std()))
    print(f"   Test İstatistiği: {ks_stat:.6f}")
    print(f"   P-Value: {ks_pvalue:.6f}")
    
    if ks_pvalue > 0.05:
        print(f"   ✅ SONUÇ: Normal dağılım (p > 0.05)")
    else:
        print(f"   ❌ SONUÇ: Normal dağılım değil (p < 0.05)")

# =============================================================================
# 4. AYKIRI DEĞER ANALİZİ (IQR Yöntemi)
# =============================================================================

print("\n" + "=" * 80)
print("4. AYKIRI DEĞER ANALİZİ (IQR YÖNTEMİ)")
print("=" * 80)

if ilce_col:
    print("\n🔍 IQR (Interquartile Range) Yöntemi ile Aykırı Değer Tespiti:")
    
    Q1 = durak_per_ilce.quantile(0.25)
    Q3 = durak_per_ilce.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"\n   📊 Çeyrekler:")
    print(f"      Q1 (25. yüzdelik): {Q1:.2f}")
    print(f"      Q2 (50. yüzdelik - Medyan): {durak_per_ilce.median():.2f}")
    print(f"      Q3 (75. yüzdelik): {Q3:.2f}")
    print(f"      IQR (Q3 - Q1): {IQR:.2f}")
    
    print(f"\n   🎯 Aykırı Değer Sınırları:")
    print(f"      Alt Sınır: {lower_bound:.2f}")
    print(f"      Üst Sınır: {upper_bound:.2f}")
    
    # Aykırı değerleri bul
    outliers = durak_per_ilce[(durak_per_ilce < lower_bound) | (durak_per_ilce > upper_bound)]
    
    if len(outliers) > 0:
        print(f"\n   ⚠️  {len(outliers)} adet AYKIRI DEĞER bulundu:")
        for ilce, count in outliers.items():
            if count > upper_bound:
                print(f"      • {ilce}: {count} durak (ÜST aykırı değer)")
            else:
                print(f"      • {ilce}: {count} durak (ALT aykırı değer)")
        
        print(f"\n   📌 Aykırı değer oranı: {len(outliers)/len(durak_per_ilce)*100:.2f}%")
    else:
        print("\n   ✅ Aykırı değer BULUNAMADI!")
        print("   → Veri homojen dağılmış")

# =============================================================================
# 5. KORELASYON ANALİZİ
# =============================================================================

print("\n" + "=" * 80)
print("5. KORELASYON ANALİZİ")
print("=" * 80)

if 'latitude' in df_durak.columns and 'longitude' in df_durak.columns:
    print("\n🗺️  Koordinat Korelasyonu:")
    
    corr = df_durak[['latitude', 'longitude']].corr()
    print(corr)
    
    corr_value = corr.iloc[0, 1]
    print(f"\n   Pearson Korelasyon Katsayısı: {corr_value:.4f}")
    
    if abs(corr_value) < 0.3:
        print("   → Zayıf korelasyon")
    elif abs(corr_value) < 0.7:
        print("   → Orta düzey korelasyon")
    else:
        print("   → Güçlü korelasyon")

# =============================================================================
# 6. GÖRSELLEŞTİRMELER
# =============================================================================

print("\n" + "=" * 80)
print("6. GÖRSELLEŞTİRMELER OLUŞTURULUYOR...")
print("=" * 80)

# Output klasörünü oluştur
Path("visualizations").mkdir(exist_ok=True)

if ilce_col:
    
    # GÖRSEL 1: 4'lü Dağılım Analizi
    print("\n📊 Görsel 1/3: Dağılım Analizi Grafikleri...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('İlçelere Göre Durak Sayısı - Dağılım Analizi', 
                 fontsize=18, fontweight='bold', y=1.00)
    
    # 1. Histogram
    axes[0, 0].hist(durak_per_ilce, bins=20, edgecolor='black', 
                    alpha=0.7, color='steelblue')
    axes[0, 0].axvline(durak_per_ilce.mean(), color='red', 
                       linestyle='--', linewidth=2, label=f'Ortalama: {durak_per_ilce.mean():.1f}')
    axes[0, 0].axvline(durak_per_ilce.median(), color='green', 
                       linestyle='--', linewidth=2, label=f'Medyan: {durak_per_ilce.median():.1f}')
    axes[0, 0].set_title('Histogram', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Durak Sayısı')
    axes[0, 0].set_ylabel('Frekans (İlçe Sayısı)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. KDE (Kernel Density Estimate)
    sns.kdeplot(data=durak_per_ilce, ax=axes[0, 1], fill=True, color='steelblue')
    axes[0, 1].axvline(durak_per_ilce.mean(), color='red', 
                       linestyle='--', linewidth=2, label='Ortalama')
    axes[0, 1].axvline(durak_per_ilce.median(), color='green', 
                       linestyle='--', linewidth=2, label='Medyan')
    axes[0, 1].set_title('Kernel Density Estimate (KDE)', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Durak Sayısı')
    axes[0, 1].set_ylabel('Yoğunluk')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Box Plot (Aykırı Değer Gösterimi)
    bp = axes[1, 0].boxplot(durak_per_ilce, vert=True, patch_artist=True,
                             boxprops=dict(facecolor='lightblue', alpha=0.7),
                             medianprops=dict(color='red', linewidth=2),
                             flierprops=dict(marker='o', markerfacecolor='red', 
                                           markersize=8, alpha=0.5))
    axes[1, 0].set_title('Box Plot (Aykırı Değer Gösterimi)', 
                         fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Durak Sayısı')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 4. Q-Q Plot (Normallik Kontrolü)
    stats.probplot(durak_per_ilce, dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title('Q-Q Plot (Normallik Kontrolü)', 
                         fontsize=14, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Normallik testi sonucunu ekle
    if 'p_value' in locals():
        if p_value > 0.05:
            result_text = f"Shapiro-Wilk Test: p={p_value:.4f}\n✅ Normal Dağılım"
            color = 'green'
        else:
            result_text = f"Shapiro-Wilk Test: p={p_value:.4f}\n❌ Normal Değil"
            color = 'red'
        axes[1, 1].text(0.05, 0.95, result_text, transform=axes[1, 1].transAxes,
                        fontsize=11, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('visualizations/01_distribution_analysis.png', dpi=300, bbox_inches='tight')
    print("   ✅ Kaydedildi: visualizations/01_distribution_analysis.png")
    plt.close()
    
    # GÖRSEL 2: Top 15 İlçe Bar Chart
    print("📊 Görsel 2/3: En Fazla Durağa Sahip İlçeler...")
    
    plt.figure(figsize=(14, 8))
    top15 = durak_per_ilce.head(15)
    colors = plt.cm.viridis(np.linspace(0, 1, len(top15)))
    
    bars = plt.bar(range(len(top15)), top15.values, color=colors, 
                   edgecolor='black', linewidth=1.5)
    
    # Değerleri bar'ların üstüne yaz
    for i, (bar, value) in enumerate(zip(bars, top15.values)):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f'{int(value):,}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    plt.xticks(range(len(top15)), top15.index, rotation=45, ha='right', fontsize=11)
    plt.title('En Fazla Durağa Sahip 15 İlçe', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('İlçe', fontsize=12, fontweight='bold')
    plt.ylabel('Durak Sayısı', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Ortalama çizgisi ekle
    plt.axhline(durak_per_ilce.mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Ortalama: {durak_per_ilce.mean():.0f}')
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig('visualizations/02_top15_ilce.png', dpi=300, bbox_inches='tight')
    print("   ✅ Kaydedildi: visualizations/02_top15_ilce.png")
    plt.close()
    
    # GÖRSEL 3: Aykırı Değer Vurgulamalı Grafik
    if 'outliers' in locals() and len(outliers) > 0:
        print("📊 Görsel 3/3: Aykırı Değer Analizi...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Tüm ilçeleri çiz
        normal_ilceler = durak_per_ilce.drop(outliers.index)
        
        # Normal değerler (mavi)
        ax.scatter(range(len(normal_ilceler)), normal_ilceler.values, 
                  color='steelblue', s=100, alpha=0.6, label='Normal Değerler', 
                  edgecolors='black', linewidth=1)
        
        # Aykırı değerler (kırmızı)
        outlier_positions = [list(durak_per_ilce.index).index(idx) for idx in outliers.index]
        ax.scatter(outlier_positions, outliers.values, 
                  color='red', s=200, alpha=0.8, label='Aykırı Değerler', 
                  edgecolors='black', linewidth=2, marker='D')
        
        # Aykırı değer sınırlarını çiz
        ax.axhline(upper_bound, color='orange', linestyle='--', 
                  linewidth=2, label=f'Üst Sınır: {upper_bound:.0f}')
        ax.axhline(lower_bound, color='orange', linestyle='--', 
                  linewidth=2, label=f'Alt Sınır: {lower_bound:.0f}')
        
        # Medyan çizgisi
        ax.axhline(durak_per_ilce.median(), color='green', linestyle='-', 
                  linewidth=2, label=f'Medyan: {durak_per_ilce.median():.0f}')
        
        ax.set_title('Aykırı Değer Analizi (IQR Yöntemi)', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('İlçe Sıralaması', fontsize=12, fontweight='bold')
        ax.set_ylabel('Durak Sayısı', fontsize=12, fontweight='bold')
        ax.legend(fontsize=11, loc='upper right')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        plt.savefig('visualizations/03_outlier_analysis.png', dpi=300, bbox_inches='tight')
        print("   ✅ Kaydedildi: visualizations/03_outlier_analysis.png")
        plt.close()

# =============================================================================
# 7. ÖZET RAPOR
# =============================================================================

print("\n" + "=" * 80)
print("7. ÖZET RAPOR")
print("=" * 80)

summary_report = f"""
📊 İSTANBUL TOPLU TAŞIMA VERİSİ - KEŞİFSEL ANALİZ SONUÇLARI

📍 VERİ SETİ:
   • Toplam Durak: {len(df_durak):,}
   • Toplam Hat: {len(df_hat):,}
   • Analiz Edilen İlçe: {len(durak_per_ilce) if ilce_col else 'N/A'}

📈 DAĞILIM İSTATİSTİKLERİ:
   • Ortalama Durak/İlçe: {durak_per_ilce.mean():.2f} if ilce_col else 'N/A'
   • Medyan: {durak_per_ilce.median():.2f} if ilce_col else 'N/A'
   • Standart Sapma: {durak_per_ilce.std():.2f} if ilce_col else 'N/A'
   • Min-Max: {durak_per_ilce.min()}-{durak_per_ilce.max()} if ilce_col else 'N/A'

🔬 NORMALLİK TESTİ:
   • Shapiro-Wilk p-value: {p_value:.6f} if 'p_value' in locals() else 'N/A'
   • Sonuç: {'Normal Dağılım' if 'p_value' in locals() and p_value > 0.05 else 'Normal Değil'}

⚠️  AYKIRI DEĞER:
   • Tespit Edilen: {len(outliers) if 'outliers' in locals() else 0}
   • Oran: {len(outliers)/len(durak_per_ilce)*100:.2f}% if 'outliers' in locals() and len(outliers) > 0 else '0.00%'

✅ OLUŞTURULAN GÖRSELLER:
   1. visualizations/01_distribution_analysis.png
   2. visualizations/02_top15_ilce.png
   3. visualizations/03_outlier_analysis.png (varsa)
"""

print(summary_report)

# Raporu dosyaya kaydet
with open('visualizations/EDA_SUMMARY_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(summary_report)

print("\n💾 Özet rapor kaydedildi: visualizations/EDA_SUMMARY_REPORT.txt")

print("\n" + "=" * 80)
print("✅ KEŞİFSEL VERİ ANALİZİ TAMAMLANDI!")
print("=" * 80)

print("\n🎯 SONRAKİ ADIMLAR:")
print("   1. ✅ Veriler analiz edildi")
print("   2. ✅ Dağılım özellikleri belirlendi")
print("   3. ✅ İstatistiksel testler yapıldı")
print("   4. ✅ Görselleştirmeler oluşturuldu")
print("   5. ⏭️  Şimdi: Detaylı harita ve dashboard!")

print("\n📝 NOT: Portfolio'da EDA bölümünü şöyle anlatabilirsiniz:")
print('"15,316 durak ve 7,215 hat verisini analiz ettim. Shapiro-Wilk')
print('normallik testi ve IQR yöntemiyle aykırı değer tespiti yaptım.')
print('Sonuçları görselleştirerek veri kalitesini raporladım."')
