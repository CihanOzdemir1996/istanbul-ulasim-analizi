import geopandas as gpd
import pandas as pd
from pathlib import Path
import os


def load_and_process_geojson():
    print("\n🚀 ANALİZ BAŞLIYOR...")

    # 1. DOSYA YOLUNU SABİTLEYELİM
    # Senin bilgisayarındaki tam adresi buraya manuel olarak tanımlıyoruz.
    # Bu en garantili yöntemdir.
    data_dir = Path(r"C:\Users\cihan\PycharmProjects\PythonProject3\data")

    hat_path = data_dir / "iett_hat.geojson"
    durak_path = data_dir / "iett_durak.geojson"

    processed_data = []

    # 2. DOSYALARI İŞLE
    files_to_process = [("HAT", hat_path), ("DURAK", durak_path)]

    for label, file_path in files_to_process:
        if file_path.exists():
            print(f"✅ {label} dosyası bulundu: {file_path.name}")
            try:
                df = gpd.read_file(file_path)

                # Koordinat hesaplama (Hata önleyici)
                df['latitude'] = df.geometry.centroid.y
                df['longitude'] = df.geometry.centroid.x

                if 'geometry' in df.columns:
                    df = df.drop(columns=['geometry'])

                processed_data.append((label, df))
                print(f"✅ {label} verisi işlendi. Satır: {len(df)}")

            except Exception as e:
                print(f"❌ {label} işlenirken hata: {e}")
        else:
            print(f"❌ {label} bulunamadı!")
            print(f"   Bakılan Adres: {file_path}")

    # 3. KAYIT
    if processed_data:
        for label, df in processed_data:
            output_path = data_dir / f"iett_{label.lower()}_processed.csv"
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"💾 Kaydedildi: {output_path.name}")
        print("\n🎉 ANALİZ BAŞARIYLA TAMAMLANDI!")
    else:
        print("\n⚠️ HATA: Dosyalar hala bulunamıyor. Lütfen klasör ismini kontrol et.")


if __name__ == "__main__":
    load_and_process_geojson()