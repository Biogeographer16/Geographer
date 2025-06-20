# Gerekli kütüphanelerin yüklenmesi
!pip install cartopy matplotlib pandas numpy requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
import requests
from io import StringIO

# NASA FIRMS VIIRS veri kaynağı (Son 24 saat)
VIIRS_URL = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_24h.csv"

# Basit ve temiz yangın haritası oluşturma (düzeltilmiş)
def create_clean_fire_map():
    # Veriyi indir
    try:
        response = requests.get(VIIRS_URL, timeout=30)
        df = pd.read_csv(StringIO(response.text))
        print(f"{len(df)} yangın noktası yüklendi.")
    except:
        print("Gerçek veri indirilemedi, örnek veri kullanılıyor.")
        df = pd.DataFrame({
            'latitude': np.random.uniform(-55, 70, 500),
            'longitude': np.random.uniform(-180, 180, 500),
            'confidence': np.random.choice(['high', 'nominal', 'low'], 500, p=[0.6, 0.3, 0.1]),
            'bright_ti4': np.random.randint(300, 500, 500)
        })

    # Haritayı oluştur
    plt.figure(figsize=(15, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()

    # Minimalist arkaplan
    ax.add_feature(cfeature.OCEAN, facecolor='#f0f8ff')  # Açık mavi
    ax.add_feature(cfeature.LAND, facecolor='#f5f5f5')    # Açık gri
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='#999999')

    # Yangın noktalarını çiz
    colors = {
        'high': '#e41a1c',    # Kırmızı
        'nominal': '#ff7f00',  # Turuncu
        'low': '#ffff33'       # Sarı
    }

    # Lejant için boş scatter plotlar oluştur
    for conf, color in colors.items():
        df_conf = df[df['confidence'].str.lower() == conf.lower()]
        if not df_conf.empty:
            ax.scatter(
                df_conf['longitude'],
                df_conf['latitude'],
                color=color,
                s=8,  # Sabit küçük boyut
                alpha=0.7,
                edgecolors='none',
                transform=ccrs.PlateCarree()
            )

    # 1. LEJANT (Harita içinde, sağ üst köşede)
    legend_labels = ['High risk', 'Moderate risk', 'Low risk']
    legend_colors = [colors['high'], colors['nominal'], colors['low']]

    # Lejant öğeleri
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                  markersize=8, label=label)
        for color, label in zip(legend_colors, legend_labels)
    ]

    # Lejantı haritanın içine yerleştir - Harita içinde ölçek çubuğunun bir üstüne ekle
    legend = ax.legend(
        handles=legend_elements,
        loc='center left',
        frameon=True,
        framealpha=0.9,
        fontsize=10,
        title='Wildfire Risk Stages',
        title_fontsize=11
    )
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('#cccccc')


    # 3. ÖLÇEK ÇUBUĞU - Harita içinde, sol altta
    # 2000 km'lik ölçek çubuğu (ekvatorda yaklaşık 18 derece)
    scale_length_deg = 18  # Ekvatorda 2000 km ≈ 18 derece

    # Ölçek çubuğunun başlangıç noktası (sol altta)
    start_lon, start_lat = -170, -55

    # Ölçek çizgisi
    ax.plot([start_lon, start_lon + scale_length_deg],
            [start_lat, start_lat],
            color='black', linewidth=2,
            transform=ccrs.PlateCarree())

    # Ölçek uçlarındaki dikey çizgiler
    for lon in [start_lon, start_lon + scale_length_deg]:
        ax.plot([lon, lon],
                [start_lat - 1, start_lat + 1],
                color='black', linewidth=2,
                transform=ccrs.PlateCarree())

    # Ölçek etiketi
    ax.text(start_lon + scale_length_deg/2,
            start_lat - 3,
            '2000 km',
            ha='center', va='top',
            fontsize=10, weight='bold',
            transform=ccrs.PlateCarree(),
            path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])

    # 4. BAŞLIK VE KAYNAK
    plt.title('Global wildfire distribution - last 24 hours', fontsize=16, pad=20)

    # Kaynak bilgisi (küçük ve sade)
    plt.figtext(0.5, 0.01, "Source: NASA FIRMS | Data: last 24 hours",
                ha="center", fontsize=9, color='#666666')

    # Haritayı kaydet ve göster
    plt.savefig('global_fires_fixed.png', bbox_inches='tight', dpi=150, transparent=True)
    plt.show()
    print("Harita oluşturuldu: global_fires_fixed.png")

# Haritayı oluştur
create_clean_fire_map()
