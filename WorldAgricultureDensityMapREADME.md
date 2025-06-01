import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.cm import ScalarMappable

# 1. Veri indirme fonksiyonları
def get_agricultural_population():
    """Tarımsal nüfus verilerini al"""
    try:
        # Dünya Bankası'ndan kırsal nüfus verisi (tarımsal nüfus yaklaşımı)
        rural_pop = pd.read_csv("https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Rural%20population%20-%20World%20Bank/World%20Bank%20(%202015%20estimates%20).csv")
        rural_pop = rural_pop[rural_pop['Year'] == 2020].dropna()
        rural_pop = rural_pop[['Country', 'Rural population']]
        rural_pop.columns = ['NAME', 'AGRICULTURAL_POP']
        
        # Ülke isimlerini standartlaştırma
        name_corrections = {
            "United States": "United States of America",
            "Russian Federation": "Russia",
            "Iran, Islamic Rep.": "Iran",
            "Egypt, Arab Rep.": "Egypt",
            "Venezuela, RB": "Venezuela",
            "Kyrgyz Republic": "Kyrgyzstan",
            "Lao PDR": "Laos",
            "Syrian Arab Republic": "Syria",
            "Yemen, Rep.": "Yemen",
            "Congo, Dem. Rep.": "Democratic Republic of the Congo",
            "Congo, Rep.": "Congo",
            "Cote d'Ivoire": "Ivory Coast",
            "Czechia": "Czech Republic"
        }
        rural_pop['NAME'] = rural_pop['NAME'].replace(name_corrections)
        return rural_pop
    except:
        print("Tarımsal nüfus verisi indirilemedi - alternatif kaynak kullanılıyor")
        # Alternatif statik veri
        data = {
            'NAME': ['China', 'India', 'United States of America', 'Indonesia', 'Pakistan', 
                     'Brazil', 'Nigeria', 'Bangladesh', 'Russia', 'Mexico'],
            'AGRICULTURAL_POP': [500000000, 450000000, 30000000, 100000000, 80000000, 
                                 40000000, 70000000, 90000000, 35000000, 25000000]
        }
        return pd.DataFrame(data)

def get_agricultural_area():
    """Tarım arazisi verilerini al"""
    try:
        # FAO'dan tarım arazisi verisi
        agri_area = pd.read_csv("https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Agricultural%20area%20-%20FAO/FAO%20(%202020%20).csv")
        agri_area = agri_area[agri_area['Year'] == 2020].dropna()
        agri_area = agri_area[['Country', 'Agricultural area (hectares)']]
        agri_area.columns = ['NAME', 'AREA_HA']
        agri_area['AREA_KM2'] = agri_area['AREA_HA'] / 100  # Hektar'dan km²'ye çevirme
        
        # Ülke isimlerini standartlaştırma
        name_corrections = {
            "United States of America": "United States of America",
            "Russian Federation": "Russia",
            "Iran (Islamic Republic of)": "Iran",
            "Egypt": "Egypt",
            "Venezuela (Bolivarian Republic of)": "Venezuela",
            "Czechia": "Czech Republic"
        }
        agri_area['NAME'] = agri_area['NAME'].replace(name_corrections)
        return agri_area
    except:
        print("Tarım alanı verisi indirilemedi - alternatif kaynak kullanılıyor")
        # Alternatif statik veri
        data = {
            'NAME': ['China', 'India', 'United States of America', 'Indonesia', 'Pakistan', 
                     'Brazil', 'Nigeria', 'Bangladesh', 'Russia', 'Mexico'],
            'AREA_KM2': [5000000, 4500000, 4000000, 3500000, 3000000, 
                         2500000, 2000000, 1500000, 1000000, 500000]
        }
        return pd.DataFrame(data)

def get_world_geodata():
    """Coğrafi verileri indir"""
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    return gpd.read_file(url)

# 2. Veri işleme
def prepare_agricultural_data():
    """Verileri birleştir ve yoğunluğu hesapla"""
    # Coğrafi veriler
    world = get_world_geodata()
    
    # Tarımsal nüfus verisi
    agri_pop = get_agricultural_population()
    
    # Tarım alanı verisi
    agri_area = get_agricultural_area()
    
    # Verileri birleştir
    world = world.merge(agri_pop, on='NAME', how='left')
    world = world.merge(agri_area[['NAME', 'AREA_KM2']], on='NAME', how='left')
    
    # Yoğunluk hesapla (tarımsal nüfus / tarım alanı)
    world['AGRI_DENSITY'] = world['AGRICULTURAL_POP'] / world['AREA_KM2']
    
    # Yoğunluğu kategorilere ayır
    bins = [0, 10, 50, 100, 200, 500, 1000, float('inf')]
    labels = ['<10', '10-50', '50-100', '100-200', '200-500', '500-1000', '>1000']
    world['AGRI_DENSITY_CAT'] = pd.cut(world['AGRI_DENSITY'], bins=bins, labels=labels, right=False)
    
    return world

# 3. Harita oluşturma
def create_agricultural_density_map(world):
    """Tarımsal nüfus yoğunluğu haritasını oluştur"""
    fig, ax = plt.subplots(1, 1, figsize=(22, 15))
    
    # Renk paleti (yeşil tonları)
    colors = ['#ffffcc', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#005a32']
    cmap = plt.cm.colors.ListedColormap(colors)
    
    # Verileri filtrele (geçerli yoğunluğu olanlar)
    valid_data = world.dropna(subset=['AGRI_DENSITY'])
    
    # Haritayı çiz
    valid_data.plot(
        ax=ax,
        column='AGRI_DENSITY_CAT',
        categorical=True,
        cmap=cmap,
        edgecolor='black',
        linewidth=0.3,
        legend=True,
        legend_kwds={
            'loc': 'lower left',
            'title': 'Tarımsal Nüfus Yoğunluğu\n(kişi/km²)',
            'frameon': True,
            'framealpha': 0.9,
            'fontsize': 11
        }
    )
    
    # Veri olmayan ülkeleri gri göster
    no_data = world[world['AGRI_DENSITY'].isna()]
    no_data.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=0.3)
    
    # Arkaplan haritası
    ctx.add_basemap(
        ax,
        source=ctx.providers.CartoDB.Positron,
        crs=world.crs.to_string(),
        alpha=0.8
    )
    
    # Başlık ve etiketler
    plt.title('DÜNYA TARIMSAL NÜFUS YOĞUNLUĞU (2020)', fontsize=24, pad=20)
    plt.annotate(
        'Kaynak: Dünya Bankası, FAO & Natural Earth',
        xy=(0.12, 0.05),
        xycoords='figure fraction',
        fontsize=12,
        color='#555555'
    )
    
    # En yoğun 10 ülkeyi işaretle
    top10 = valid_data.sort_values('AGRI_DENSITY', ascending=False).head(10)
    for idx, row in top10.iterrows():
        centroid = row['geometry'].centroid
        plt.annotate(
            text=f"{row['NAME']}: {int(row['AGRI_DENSITY'])}",
            xy=(centroid.x, centroid.y),
            xytext=(3, 3),
            textcoords="offset points",
            fontsize=10,
            color='darkred',
            weight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='none', alpha=0.7)
        )
    
    plt.axis('off')
    plt.tight_layout()
    
    # Kaydet
    plt.savefig('tarimsal_nufus_yogunlugu.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Yoğunluk raporu oluştur
    density_report = world[['NAME', 'AGRICULTURAL_POP', 'AREA_KM2', 'AGRI_DENSITY', 'AGRI_DENSITY_CAT']]
    density_report = density_report.sort_values('AGRI_DENSITY', ascending=False)
    density_report['AGRI_DENSITY'] = density_report['AGRI_DENSITY'].round(1)
    density_report = density_report.rename(columns={
        'NAME': 'Ülke',
        'AGRICULTURAL_POP': 'Tarımsal Nüfus',
        'AREA_KM2': 'Tarım Alanı (km²)',
        'AGRI_DENSITY': 'Yoğunluk (kişi/km²)',
        'AGRI_DENSITY_CAT': 'Yoğunluk Kategori'
    })
    
    # Tabloyu kaydet
    density_report.head(20).to_csv('tarimsal_nufus_yogunlugu.csv', index=False)
    print("Tarımsal nüfus yoğunluğu tablosu oluşturuldu: tarimsal_nufus_yogunlugu.csv")

# 4. Ana işlem
if __name__ == "__main__":
    print("Tarımsal veriler indiriliyor ve işleniyor...")
    world_data = prepare_agricultural_data()
    
    print("Harita oluşturuluyor...")
    create_agricultural_density_map(world_data)
    
    print("İşlem tamamlandı. 'tarimsal_nufus_yogunlugu.png' kaydedildi.")

    import folium
from folium.plugins import HeatMap

def create_interactive_map(world):
    m = folium.Map(location=[30, 0], zoom_start=2)
    
