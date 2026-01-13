import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Sayfa Ayarları
st.set_page_config(page_title="İstanbul İETT Analiz Dashboard", layout="wide")

st.title("🚌 İstanbul Toplu Taşıma Analizi")
st.markdown("Bu dashboard, İETT açık verileri kullanılarak hazırlanmış bir veri analitiği projesidir.")

# 1. Veriyi Yükle
@st.cache_data
def load_data():
    durak_df = pd.read_csv(r'C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_durak_final.csv')
    return durak_df

df = load_data()

# 2. Yan Menü (Filtreler)
st.sidebar.header("Filtreleme Seçenekleri")
selected_ilce = st.sidebar.multiselect("Analiz Edilecek İlçeleri Seçin:",
                                       options=df['ILCEID'].unique(),
                                       default=df['ILCEID'].unique()[:5])

# Filtreleme Uygula
filtered_df = df[df['ILCEID'].isin(selected_ilce)]

# 3. Üst Bilgi Kartları (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Durak Sayısı", len(filtered_df))
col2.metric("Seçili İlçe Sayısı", len(selected_ilce))
col3.metric("Analiz Edilen Hat Sayısı", "7,214")

# 4. Harita ve Grafik Yan Yana
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📍 Coğrafi Dağılım")
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=11)
    for idx, row in filtered_df.head(500).iterrows(): # Performans için ilk 500
        folium.CircleMarker([row['latitude'], row['longitude']], radius=3).add_to(m)
    st_folium(m, width=700, height=500)

with c2:
    st.subheader("📊 İlçe Bazlı Durak Sayısı")
    ilce_counts = filtered_df['ILCEID'].value_counts()
    st.bar_chart(ilce_counts)

st.success("Analiz başarıyla tamamlandı. Portfolyo için hazır!")