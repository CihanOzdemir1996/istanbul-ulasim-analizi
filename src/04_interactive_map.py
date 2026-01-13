import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import os


def create_istanbul_map():
    print("🌍 İnteraktif harita oluşturuluyor...")

    # 1. Temizlenmiş veriyi yükle
    data_path = r'C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_durak_final.csv'
    df = pd.read_csv(data_path)

    # 2. İstanbul merkezli haritayı başlat
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=11, tiles='CartoDB positron')

    # 3. ISI HARİTASI (Yoğunluk Analizi)
    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=10, name="Durak Yoğunluğu (Heatmap)").add_to(m)

    # 4. KÜMELEME (Binlerce durağı düzenli göstermek için)
    marker_cluster = MarkerCluster(name="Durak Detayları").add_to(m)

    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            popup=f"Durak: {row.get('ADI', 'İsimsiz')}",
            color='royalblue',
            fill=True,
            fill_opacity=0.7
        ).add_to(marker_cluster)

    # 5. Katman Kontrolü
    folium.LayerControl().add_to(m)

    # 6. Kaydet
    output_path = 'visualizations/istanbul_ulasim_haritasi.html'
    m.save(output_path)
    print(f"✅ Harita hazır: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    create_istanbul_map()