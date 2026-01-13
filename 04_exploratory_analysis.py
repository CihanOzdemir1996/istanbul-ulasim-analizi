import pandas as pd
import numpy as np


def explore_istanbul_data():
    print("\n🔍 VERİ KEŞFİ BAŞLIYOR...")

    # 1. Verileri Yükle
    durak_df = pd.read_csv(r"C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_durak_processed.csv")
    hat_df = pd.read_csv(r"C:\Users\cihan\PycharmProjects\PythonProject3\data\iett_hat_processed.csv")

    datasets = [("DURAK", durak_df), ("HAT", hat_df)]

    for name, df in datasets:
        print(f"\n--- 📊 {name} VERİ SETİ ---")

        # A. Boyut Kontrolü (Shape)
        print(f"Satır Sayısı: {df.shape[0]} | Sütun Sayısı: {df.shape[1]}")

        # B. Veri Tipleri ve Boş Değer Analizi
        print("\nSütun Bilgileri ve Eksik Veriler:")
        info_df = pd.DataFrame({
            'Veri Tipi': df.dtypes,
            'Eksik Değer': df.isnull().sum(),
            'Eksik %': (df.isnull().sum() / len(df) * 100).round(2)
        })
        print(info_df)

        # C. Betimsel İstatistikler (Sayısal Sütunlar)
        print("\nİstatistiksel Özet (Koordinatlar):")
        print(df[['latitude', 'longitude']].describe())

        # D. Benzersiz Değer Kontrolü
        # (Aynı isimde kaç durak var veya kaç farklı hat segmenti var?)
        if 'DURAK_ADI' in df.columns:
            print(f"\nBenzersiz Durak İsmi Sayısı: {df['DURAK_ADI'].nunique()}")


if __name__ == "__main__":
    explore_istanbul_data()