import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import os


def create_pro_map():
    # 1. Veriyi yükle
    durak_df = pd.read_csv(r'C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_durak_final.csv')

    print(f"🌍 {len(durak_df)} durak haritaya işleniyor...")

    # 2. İstanbul merkezli interaktif harita oluştur
    # 'CartoDB positron' sade ve profesyonel bir görünüm sağlar
    m = folium.Map(location=[41.0082, 28.9784], zoom_start=11, tiles='CartoDB positron')

    # 3. ISI HARİTASI (Yoğunluk analizi için)
    heat_data = [[row['latitude'], row['longitude']] for index, row in durak_df.iterrows()]
    HeatMap(heat_data, name="Durak Yoğunluğu", radius=15).add_to(m)

    # 4. DURAK KÜMELENMESİ (Cluster)
    # Binlerce noktayı tek tek basıp haritayı kasmıyoruz, yaklaştıkça açılan kümeler yapıyoruz
    marker_cluster = MarkerCluster(name="Durak Detayları").add_to(m)

    for idx, row in durak_df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            popup=f"Durak: {row.get('ADI', 'İsimsiz')}",
            color='blue',
            fill=True
        ).add_to(marker_cluster)

    # 5. Katman Kontrolü Ekle (Kullanıcı ısı haritasını kapatıp açabilsin)
    folium.LayerControl().add_to(m)

    # 6. Kaydet
    output_path = 'visualizations/istanbul_ulasim_interaktif_harita.html'
    m.save(output_path)
    print(f"✅ Harita hazır! Şuradan açabilirsin:\n{os.path.abspath(output_path)}")


if __name__ == "__main__":
    create_pro_map()