# 🚌 İstanbul Toplu Taşıma Analizi

**Data Analyst Portfolio Projesi**

İstanbul Büyükşehir Belediyesi'nin açık verilerini kullanarak İETT otobüs hatlarını analiz eden, interaktif görselleştirmeler ve dashboard içeren bir veri analizi projesi.

---

## 📋 Proje Hakkında

Bu proje, İstanbul'daki toplu taşıma sistemini veri odaklı bir yaklaşımla analiz eder:

- 🚌 Otobüs hatlarının dağılımı
- 📍 Durak yoğunluğu analizi
- 🗺️ Coğrafi görselleştirmeler (Folium harita)
- 📊 İnteraktif dashboard (Streamlit)
- 📈 İstatistiksel analizler

---

## 🎯 Proje Hedefleri

1. **Veri Toplama:** İBB Açık Veri Portalı'ndan İETT verilerini indirme
2. **Veri Temizleme:** Eksik ve hatalı verileri düzeltme
3. **Keşifsel Veri Analizi (EDA):** Veriyi anlama ve görselleştirme
4. **İleri Analiz:** Yoğunluk analizi, trend tespiti
5. **Dashboard:** Streamlit ile interaktif uygulama
6. **Deployment:** Streamlit Cloud'da yayınlama

---

## 📊 Kullanılan Veri Kaynakları

### İBB Açık Veri Portalı
🔗 https://data.ibb.gov.tr

**Gerekli Dataset'ler:**
- İETT Otobüs Hat ve Güzergah Bilgileri
- İETT Durak Bilgileri  
- Toplu Taşıma Kullanım İstatistikleri (opsiyonel)

---

## 🛠️ Teknolojiler

- **Python 3.10+**
- **Pandas** - Veri işleme
- **Plotly** - İnteraktif grafikler
- **Folium** - Harita görselleştirme
- **Streamlit** - Web dashboard
- **Seaborn/Matplotlib** - Statik grafikler

---

## 📥 Kurulum

### 1. Repo'yu Clone'layın:
```bash
git clone https://github.com/[kullanici-adiniz]/istanbul-transport-analysis.git
cd istanbul-transport-analysis
```

### 2. Virtual Environment Oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Kütüphaneleri Yükleyin:
```bash
pip install -r requirements.txt
```

### 4. Veriyi İndirin:
1. https://data.ibb.gov.tr adresine gidin
2. "İETT" araması yapın
3. İlgili CSV dosyalarını indirin
4. `data/` klasörüne koyun

---

## 🚀 Kullanım

### Veri Keşfi:
```bash
python 01_data_exploration.py
```

### Analiz:
```bash
python 02_analysis.py
```

### Dashboard:
```bash
streamlit run 03_dashboard.py
```

---

## 📁 Proje Yapısı

```
istanbul-transport-analysis/
│
├── data/                      # Veri dosyaları (gitignore'da)
│   ├── iett_hatlar.csv
│   ├── iett_duraklar.csv
│   └── iett_yolcu.csv
│
├── notebooks/                 # Jupyter notebooks
│   └── eda_analysis.ipynb
│
├── src/                       # Kaynak kodlar
│   ├── 01_data_exploration.py
│   ├── 02_analysis.py
│   └── 03_dashboard.py
│
├── visualizations/            # Kaydedilen görseller
│   ├── hat_dagilimi.png
│   └── yogunluk_haritasi.html
│
├── requirements.txt           # Python kütüphaneleri
├── README.md                  # Bu dosya
└── .gitignore                # Git ignore
```

---

## 📊 Örnek Analizler

### 1. Hat Dağılımı
İlçelere göre otobüs hattı sayısı analizi

### 2. Durak Yoğunluğu
En fazla durağa sahip bölgelerin tespiti

### 3. Coğrafi Analiz
Folium ile interaktif harita üzerinde duraklar

### 4. Yolcu İstatistikleri
(Eğer veri mevcutsa) Zaman serisi analizi

---

## 🎯 Gelecek Geliştirmeler

- [ ] Gerçek zamanlı otobüs konumu takibi
- [ ] Rota optimizasyonu önerileri
- [ ] Machine Learning ile yolcu tahmini
- [ ] Mobil responsive dashboard

---

## 📝 Lisans

Bu proje eğitim amaçlıdır ve MIT lisansı altındadır.

---

## 👤 İletişim

**Proje Sahibi:** [İsminiz]  
**LinkedIn:** [LinkedIn profiliniz]  
**Email:** [Email adresiniz]

---

## 🙏 Teşekkürler

- İstanbul Büyükşehir Belediyesi - Açık veri sağladığı için
- İBB Açık Veri Portalı ekibi

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
