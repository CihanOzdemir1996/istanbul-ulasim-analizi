import pandas as pd
from pathlib import Path


def clean_transport_data():
    # 1. Dosya yollarını belirle
    base_path = Path(r"C:\Users\cihan\PycharmProjects\PythonProject3\data")
    hat_file = base_path / "iett_hat_processed.csv"
    durak_file = base_path / "iett_durak_processed.csv"

    # 2. Verileri yükle
    hat_df = pd.read_csv(hat_file)
    durak_df = pd.read_csv(durak_file)

    print(f"🧹 Temizlik öncesi hat sayısı: {len(hat_df)}")

    # 3. HATALARI TEMİZLE (Kritik Adım)
    # İstanbul 40 derece kuzey enleminin altındaysa hatalıdır (0 olanları atar)
    hat_df_clean = hat_df[hat_df['latitude'] > 40].copy()

    # Duraklarda da benzer bir hata olma ihtimaline karşı filtre uygulayalım
    durak_df_clean = durak_df[durak_df['latitude'] > 40].copy()

    print(f"✅ Temizlik sonrası hat sayısı: {len(hat_df_clean)}")
    print(f"🗑️ Silinen hatalı satır sayısı: {len(hat_df) - len(hat_df_clean)}")

    # 4. TEMİZ VERİLERİ YENİ İSİMLE KAYDET
    # Üzerine yazmıyoruz ki orijinal işlenmiş verimiz yedekte kalsın
    hat_df_clean.to_csv(base_path / "iett_hat_final.csv", index=False)
    durak_df_clean.to_csv(base_path / "iett_durak_final.csv", index=False)

    print("\n🚀 Temiz veriler 'iett_..._final.csv' olarak kaydedildi. Artık testlere hazırız!")


if __name__ == "__main__":
    clean_transport_data()