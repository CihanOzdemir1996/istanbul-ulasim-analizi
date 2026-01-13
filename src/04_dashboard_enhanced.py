"""
İSTANBUL TOPLU TAŞIMA ANALİZİ - GELİŞMİŞ DASHBOARD
İstatistiksel Testler ve EDA Görselleştirmeleri ile

Yazar: Cihan Özdemir
Tarih: 13 Ocak 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="İstanbul Toplu Taşıma Analizi",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3d3d3d;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #262730;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Başlık
st.markdown("""
    <h1 style='text-align: center; color: #667eea;'>
        🚌 İstanbul Toplu Taşıma Analizi
    </h1>
    <p style='text-align: center; color: #a0a0a0; font-size: 18px;'>
        İstatistiksel Testler ve İnteraktif Veri Analizi
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# Veri yükleme fonksiyonu
@st.cache_data
def load_data():
    """Veri yükleme ve ön işleme"""
    try:
        df_durak = pd.read_csv('data/duraklar.csv')
        df_hat = pd.read_csv('data/hatlar.csv')
        return df_durak, df_hat
    except FileNotFoundError:
        st.error("❌ Veri dosyaları bulunamadı! Lütfen data/ klasöründe duraklar.csv ve hatlar.csv dosyalarının olduğundan emin olun.")
        st.stop()

# İstatistiksel testler
@st.cache_data
def perform_statistical_tests(df_durak):
    """İstatistiksel testleri hesapla"""
    
    # İlçe sütununu bul
    ilce_columns = [col for col in df_durak.columns if 'ilce' in col.lower() or 'district' in col.lower()]
    
    if not ilce_columns:
        return None
    
    ilce_col = ilce_columns[0]
    durak_per_ilce = df_durak[ilce_col].value_counts()
    
    # Normallik testi
    shapiro_stat, shapiro_p = stats.shapiro(durak_per_ilce)
    
    # Aykırı değer tespiti (IQR)
    Q1 = durak_per_ilce.quantile(0.25)
    Q3 = durak_per_ilce.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = durak_per_ilce[(durak_per_ilce < lower_bound) | (durak_per_ilce > upper_bound)]
    
    # Çarpıklık ve basıklık
    skewness = durak_per_ilce.skew()
    kurtosis = durak_per_ilce.kurtosis()
    
    return {
        'durak_per_ilce': durak_per_ilce,
        'ilce_col': ilce_col,
        'shapiro_stat': shapiro_stat,
        'shapiro_p': shapiro_p,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers,
        'skewness': skewness,
        'kurtosis': kurtosis,
        'mean': durak_per_ilce.mean(),
        'median': durak_per_ilce.median(),
        'std': durak_per_ilce.std(),
        'min': durak_per_ilce.min(),
        'max': durak_per_ilce.max()
    }

# Veriyi yükle
df_durak, df_hat = load_data()
stats_results = perform_statistical_tests(df_durak)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Kontrol Paneli")
    
    # Logo veya görsel eklenebilir
    st.markdown("---")
    
    # Filtreler
    st.markdown("### 📍 Filtreleme Seçenekleri")
    
    if stats_results and 'ilce_col' in stats_results:
        ilce_col = stats_results['ilce_col']
        ilce_list = sorted(df_durak[ilce_col].unique())
        
        selected_ilceler = st.multiselect(
            "İlçe Seçin:",
            options=ilce_list,
            default=ilce_list[:3] if len(ilce_list) >= 3 else ilce_list
        )
    else:
        selected_ilceler = []
        st.warning("İlçe bilgisi bulunamadı!")
    
    st.markdown("---")
    
    # Veri özeti
    st.markdown("### 📊 Veri Özeti")
    st.metric("Toplam Durak", f"{len(df_durak):,}")
    st.metric("Toplam Hat", f"{len(df_hat):,}")
    if stats_results:
        st.metric("Toplam İlçe", len(stats_results['durak_per_ilce']))
    
    st.markdown("---")
    
    # Hakkında
    with st.expander("ℹ️ Proje Hakkında"):
        st.markdown("""
        **İstanbul Toplu Taşıma Analizi**
        
        Bu dashboard, İBB Açık Veri'den alınan gerçek 
        İETT verilerini analiz eder.
        
        **Özellikler:**
        - İstatistiksel testler
        - Coğrafi görselleştirme
        - İnteraktif filtreler
        - Detaylı EDA
        
        **Geliştirici:** Cihan Özdemir  
        **Tarih:** Ocak 2026
        """)

# Ana içerik - Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Harita & Genel Bakış",
    "📊 İstatistiksel Testler", 
    "📈 Detaylı EDA",
    "📋 Ham Veri"
])

# ============================================================================
# TAB 1: HARİTA & GENEL BAKIŞ
# ============================================================================

with tab1:
    
    # KPI Kartları
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filtered_durak = df_durak[df_durak[ilce_col].isin(selected_ilceler)] if selected_ilceler and stats_results else df_durak
        st.metric(
            "📍 Toplam Durak",
            f"{len(filtered_durak):,}",
            delta=f"{len(selected_ilceler)} ilçe" if selected_ilceler else "Tüm ilçeler"
        )
    
    with col2:
        st.metric(
            "🚌 Toplam Hat",
            f"{len(df_hat):,}",
            delta=None
        )
    
    with col3:
        if stats_results:
            st.metric(
                "📊 Ortalama Durak/İlçe",
                f"{stats_results['mean']:.0f}",
                delta=f"±{stats_results['std']:.0f}"
            )
    
    with col4:
        if stats_results:
            outlier_count = len(stats_results['outliers'])
            st.metric(
                "⚠️ Aykırı Değer",
                outlier_count,
                delta="Tespit edildi" if outlier_count > 0 else "Yok",
                delta_color="inverse" if outlier_count > 0 else "normal"
            )
    
    st.markdown("---")
    
    # Harita ve Grafik
    col_map, col_chart = st.columns([2, 1])
    
    with col_map:
        st.markdown("### 🗺️ Coğrafi Dağılım")
        
        # Folium haritası
        istanbul_center = [41.0082, 28.9784]
        m = folium.Map(
            location=istanbul_center,
            zoom_start=11,
            tiles='OpenStreetMap'
        )
        
        # Durakları ekle
        if 'latitude' in filtered_durak.columns and 'longitude' in filtered_durak.columns:
            for idx, row in filtered_durak.iterrows():
                if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                    if row['latitude'] != 0 and row['longitude'] != 0:
                        folium.CircleMarker(
                            location=[row['latitude'], row['longitude']],
                            radius=2,
                            color='blue',
                            fill=True,
                            fillColor='blue',
                            fillOpacity=0.6,
                            popup=f"Durak ID: {row.get('ID', 'N/A')}"
                        ).add_to(m)
        
        st_folium(m, width=700, height=500)
    
    with col_chart:
        st.markdown("### 📊 İlçe Bazlı Dağılım")
        
        if stats_results and selected_ilceler:
            selected_data = stats_results['durak_per_ilce'][selected_ilceler]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=selected_data.index,
                    y=selected_data.values,
                    marker=dict(
                        color=selected_data.values,
                        colorscale='Viridis',
                        showscale=False
                    ),
                    text=selected_data.values,
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                title="Seçili İlçelerdeki Durak Sayısı",
                xaxis_title="İlçe",
                yaxis_title="Durak Sayısı",
                template="plotly_dark",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: İSTATİSTİKSEL TESTLER
# ============================================================================

with tab2:
    
    if not stats_results:
        st.warning("İstatistiksel testler için yeterli veri bulunamadı!")
    else:
        st.markdown("## 🔬 İstatistiksel Test Sonuçları")
        st.markdown("Veri kalitesi ve dağılım özellikleri hakkında detaylı bilgiler")
        
        # Normallik Testi Kartı
        col1, col2, col3 = st.columns(3)
        
        with col1:
            is_normal = stats_results['shapiro_p'] > 0.05
            card_class = "success-card" if is_normal else "warning-card"
            
            st.markdown(f"""
                <div class='{card_class}'>
                    <h3>📈 Normallik Testi</h3>
                    <p><b>Shapiro-Wilk Test</b></p>
                    <p>Test İstatistiği: {stats_results['shapiro_stat']:.6f}</p>
                    <p>P-Value: {stats_results['shapiro_p']:.6f}</p>
                    <h4>{'✅ Normal Dağılım' if is_normal else '❌ Normal Değil'}</h4>
                    <small>α = 0.05 anlamlılık seviyesi</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            outlier_count = len(stats_results['outliers'])
            outlier_ratio = (outlier_count / len(stats_results['durak_per_ilce'])) * 100
            
            st.markdown(f"""
                <div class='{"warning-card" if outlier_count > 0 else "success-card"}'>
                    <h3>⚠️ Aykırı Değer Analizi</h3>
                    <p><b>IQR Yöntemi</b></p>
                    <p>Tespit Edilen: {outlier_count} adet</p>
                    <p>Oran: %{outlier_ratio:.2f}</p>
                    <p>Alt Sınır: {stats_results['lower_bound']:.0f}</p>
                    <p>Üst Sınır: {stats_results['upper_bound']:.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            skew_status = "Simetrik" if abs(stats_results['skewness']) < 0.5 else ("Sağa Çarpık" if stats_results['skewness'] > 0 else "Sola Çarpık")
            
            st.markdown(f"""
                <div class='stat-card'>
                    <h3>📐 Dağılım Özellikleri</h3>
                    <p><b>Çarpıklık (Skewness)</b></p>
                    <p>Değer: {stats_results['skewness']:.4f}</p>
                    <p>Durum: {skew_status}</p>
                    <p><b>Basıklık (Kurtosis)</b></p>
                    <p>Değer: {stats_results['kurtosis']:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detaylı İstatistikler
        st.markdown("### 📊 Tanımlayıcı İstatistikler")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Merkezi Eğilim Ölçüleri")
            stats_df = pd.DataFrame({
                'İstatistik': ['Ortalama', 'Medyan', 'Mod'],
                'Değer': [
                    f"{stats_results['mean']:.2f}",
                    f"{stats_results['median']:.2f}",
                    f"{stats_results['durak_per_ilce'].mode()[0]:.0f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Yayılım Ölçüleri")
            spread_df = pd.DataFrame({
                'İstatistik': ['Standart Sapma', 'Varyans', 'Minimum', 'Maksimum', 'Aralık'],
                'Değer': [
                    f"{stats_results['std']:.2f}",
                    f"{stats_results['std']**2:.2f}",
                    f"{stats_results['min']:.0f}",
                    f"{stats_results['max']:.0f}",
                    f"{stats_results['max'] - stats_results['min']:.0f}"
                ]
            })
            st.dataframe(spread_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Test Yorumları
        with st.expander("📖 Test Sonuçlarının Yorumlanması"):
            st.markdown(f"""
            ### Normallik Testi (Shapiro-Wilk)
            
            **Sonuç:** {'Veriler normal dağılıma sahip ✅' if is_normal else 'Veriler normal dağılıma sahip değil ❌'}
            
            **Ne Anlama Geliyor?**
            - P-value = {stats_results['shapiro_p']:.6f}
            - {'P > 0.05 olduğu için H0 hipotezi reddedilemez.' if is_normal else 'P < 0.05 olduğu için H0 hipotezi reddedilir.'}
            - {'Parametrik testler (t-test, ANOVA) kullanılabilir.' if is_normal else 'Non-parametrik testler (Mann-Whitney, Kruskal-Wallis) kullanılmalıdır.'}
            
            ### Aykırı Değer Analizi (IQR)
            
            **Sonuç:** {outlier_count} adet aykırı değer tespit edildi
            
            **IQR Sınırları:**
            - Q1 (25%): {stats_results['Q1']:.0f}
            - Q3 (75%): {stats_results['Q3']:.0f}
            - IQR: {stats_results['IQR']:.0f}
            - Alt Sınır: {stats_results['lower_bound']:.0f}
            - Üst Sınır: {stats_results['upper_bound']:.0f}
            
            **Aykırı Değerler:**
            {f"Bu ilçeler aykırı değer: {', '.join([f'{idx} ({val})' for idx, val in stats_results['outliers'].items()])}" if outlier_count > 0 else "Aykırı değer bulunamadı ✅"}
            
            ### Çarpıklık Analizi
            
            **Skewness:** {stats_results['skewness']:.4f} → {skew_status}
            
            - |Skewness| < 0.5: Yaklaşık simetrik
            - Skewness > 0.5: Sağa çarpık (uzun sağ kuyruk)
            - Skewness < -0.5: Sola çarpık (uzun sol kuyruk)
            """)

# ============================================================================
# TAB 3: DETAYLI EDA
# ============================================================================

with tab3:
    
    st.markdown("## 📈 Keşifsel Veri Analizi (EDA)")
    
    if not stats_results:
        st.warning("EDA için yeterli veri bulunamadı!")
    else:
        # Görsel yükleme denemeleri
        viz_path = Path("visualizations")
        
        # 4'lü dağılım grafiği
        st.markdown("### 📊 Dağılım Analizi")
        
        dist_plot = viz_path / "01_distribution_analysis.png"
        if dist_plot.exists():
            img = Image.open(dist_plot)
            st.image(img, use_container_width=True, caption="Histogram, KDE, Box Plot ve Q-Q Plot ile dağılım analizi")
        else:
            # Canlı grafik oluştur
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.patch.set_facecolor('#0e1117')
            
            data = stats_results['durak_per_ilce']
            
            # Histogram
            axes[0, 0].hist(data, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
            axes[0, 0].axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Ortalama: {data.mean():.1f}')
            axes[0, 0].axvline(data.median(), color='green', linestyle='--', linewidth=2, label=f'Medyan: {data.median():.1f}')
            axes[0, 0].set_title('Histogram', color='white', fontsize=12)
            axes[0, 0].set_facecolor('#262730')
            axes[0, 0].legend()
            axes[0, 0].tick_params(colors='white')
            
            # KDE
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(data)
            x_range = np.linspace(data.min(), data.max(), 100)
            axes[0, 1].plot(x_range, kde(x_range), color='steelblue', linewidth=2)
            axes[0, 1].fill_between(x_range, kde(x_range), alpha=0.3, color='steelblue')
            axes[0, 1].set_title('KDE (Kernel Density)', color='white', fontsize=12)
            axes[0, 1].set_facecolor('#262730')
            axes[0, 1].tick_params(colors='white')
            
            # Box Plot
            bp = axes[1, 0].boxplot(data, vert=True, patch_artist=True)
            bp['boxes'][0].set_facecolor('lightblue')
            axes[1, 0].set_title('Box Plot', color='white', fontsize=12)
            axes[1, 0].set_facecolor('#262730')
            axes[1, 0].tick_params(colors='white')
            
            # Q-Q Plot
            stats.probplot(data, dist="norm", plot=axes[1, 1])
            axes[1, 1].set_title('Q-Q Plot', color='white', fontsize=12)
            axes[1, 1].set_facecolor('#262730')
            axes[1, 1].tick_params(colors='white')
            axes[1, 1].get_lines()[0].set_markerfacecolor('steelblue')
            axes[1, 1].get_lines()[1].set_color('red')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("---")
        
        # Top İlçeler
        st.markdown("### 🏆 En Fazla Durağa Sahip İlçeler")
        
        top_plot = viz_path / "02_top15_ilce.png"
        if top_plot.exists():
            img = Image.open(top_plot)
            st.image(img, use_container_width=True, caption="Top 15 İlçe - Durak Sayısı")
        else:
            # Canlı grafik
            top15 = stats_results['durak_per_ilce'].head(15)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=top15.index,
                    y=top15.values,
                    marker=dict(
                        color=top15.values,
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Durak Sayısı")
                    ),
                    text=top15.values,
                    textposition='outside'
                )
            ])
            
            fig.add_hline(
                y=stats_results['mean'],
                line_dash="dash",
                line_color="red",
                annotation_text=f"Ortalama: {stats_results['mean']:.0f}",
                annotation_position="right"
            )
            
            fig.update_layout(
                title="En Fazla Durağa Sahip 15 İlçe",
                xaxis_title="İlçe",
                yaxis_title="Durak Sayısı",
                template="plotly_dark",
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Aykırı Değer Analizi
        if len(stats_results['outliers']) > 0:
            st.markdown("### ⚠️ Aykırı Değer Görselleştirmesi")
            
            outlier_plot = viz_path / "03_outlier_analysis.png"
            if outlier_plot.exists():
                img = Image.open(outlier_plot)
                st.image(img, use_container_width=True, caption="Aykırı Değer Analizi (IQR Yöntemi)")
            else:
                # Canlı grafik
                all_data = stats_results['durak_per_ilce']
                normal_data = all_data.drop(stats_results['outliers'].index)
                
                fig = go.Figure()
                
                # Normal değerler
                fig.add_trace(go.Scatter(
                    x=list(range(len(normal_data))),
                    y=normal_data.values,
                    mode='markers',
                    name='Normal Değerler',
                    marker=dict(size=8, color='steelblue')
                ))
                
                # Aykırı değerler
                outlier_positions = [list(all_data.index).index(idx) for idx in stats_results['outliers'].index]
                fig.add_trace(go.Scatter(
                    x=outlier_positions,
                    y=stats_results['outliers'].values,
                    mode='markers',
                    name='Aykırı Değerler',
                    marker=dict(size=12, color='red', symbol='diamond')
                ))
                
                # Sınır çizgileri
                fig.add_hline(y=stats_results['upper_bound'], line_dash="dash", line_color="orange", 
                             annotation_text=f"Üst Sınır: {stats_results['upper_bound']:.0f}")
                fig.add_hline(y=stats_results['lower_bound'], line_dash="dash", line_color="orange",
                             annotation_text=f"Alt Sınır: {stats_results['lower_bound']:.0f}")
                fig.add_hline(y=stats_results['median'], line_dash="solid", line_color="green",
                             annotation_text=f"Medyan: {stats_results['median']:.0f}")
                
                fig.update_layout(
                    title="Aykırı Değer Analizi (IQR Yöntemi)",
                    xaxis_title="İlçe Sırası",
                    yaxis_title="Durak Sayısı",
                    template="plotly_dark",
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: HAM VERİ
# ============================================================================

with tab4:
    
    st.markdown("## 📋 Ham Veri Görüntüleme")
    
    data_type = st.radio("Veri Tipi Seçin:", ["Durak Verisi", "Hat Verisi"], horizontal=True)
    
    if data_type == "Durak Verisi":
        st.markdown(f"### 📍 Durak Verisi ({len(df_durak):,} satır)")
        
        # Filtreleme
        if selected_ilceler and stats_results:
            filtered = df_durak[df_durak[stats_results['ilce_col']].isin(selected_ilceler)]
            st.dataframe(filtered, use_container_width=True, height=400)
            
            # İndirme
            csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Filtrelenmiş Veriyi İndir (CSV)",
                data=csv,
                file_name='istanbul_duraklar_filtered.csv',
                mime='text/csv'
            )
        else:
            st.dataframe(df_durak, use_container_width=True, height=400)
            
            csv = df_durak.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tüm Veriyi İndir (CSV)",
                data=csv,
                file_name='istanbul_duraklar.csv',
                mime='text/csv'
            )
    
    else:
        st.markdown(f"### 🚌 Hat Verisi ({len(df_hat):,} satır)")
        st.dataframe(df_hat, use_container_width=True, height=400)
        
        csv = df_hat.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Hat Verisini İndir (CSV)",
            data=csv,
            file_name='istanbul_hatlar.csv',
            mime='text/csv'
        )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚌 İstanbul Toplu Taşıma Analizi | 📊 Data Analytics Portfolio Project</p>
        <p>Geliştirici: Cihan Özdemir | 📅 Ocak 2026</p>
        <p><small>Veri Kaynağı: İBB Açık Veri Portalı</small></p>
    </div>
    """, unsafe_allow_html=True)
