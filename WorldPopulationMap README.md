import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.colors import LogNorm
import pandas_datareader as pdr
from datetime import datetime

# 1. Dünya Bankası'ndan güncel nüfus verilerini alma
def get_world_population():
    try:
        # Dünya Bankası veri kaynağı
        population = pdr.get_data_wb('SP.POP.TOTL', start=2024, end=2024)
        population = population.reset_index()
        
        # Veriyi temizleme
        population = population[['country', 'SP.POP.TOTL']]
        population.columns = ['NAME', 'POPULATION']
        population['NAME'] = population['NAME'].str.replace('Cabo Verde', 'Cape Verde')
        population['NAME'] = population['NAME'].str.replace('Egypt, Arab Rep.', 'Egypt')
        population['NAME'] = population['NAME'].str.replace('Gambia, The', 'Gambia')
        population['NAME'] = population['NAME'].str.replace('Iran, Islamic Rep.', 'Iran')
        population['NAME'] = population['NAME'].str.replace('Kyrgyz Republic', 'Kyrgyzstan')
        population['NAME'] = population['NAME'].str.replace('Lao PDR', 'Laos')
        population['NAME'] = population['NAME'].str.replace('Russian Federation', 'Russia')
        population['NAME'] = population['NAME'].str.replace('Slovak Republic', 'Slovakia')
        population['NAME'] = population['NAME'].str.replace('Syrian Arab Republic', 'Syria')
        population['NAME'] = population['NAME'].str.replace('Venezuela, RB', 'Venezuela')
        population['NAME'] = population['NAME'].str.replace('Yemen, Rep.', 'Yemen')
        
        return population
    except:
        # Alternatif statik veri kaynağı
        print("Dünya Bankası API hatası - statik veri kullanılıyor")
        url = "https://raw.githubusercontent.com/datasets/population/main/data/population.csv"
        data = pd.read_csv(url)
        latest_year = data['Year'].max()
        population = data[data['Year'] == latest_year]
        population = population.groupby('Country Name')['Value'].sum().reset_index()
        population.columns = ['NAME', 'POPULATION']
        return population

# 2. Coğrafi verileri indirme
def get_world_geodata():
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    return gpd.read_file(url)

# 3. Verileri birleştirme ve yoğunluk hesaplama
def prepare_data():
    # Coğrafi veriler
    world = get_world_geodata()
    
    # Nüfus verileri
    pop_data = get_world_population()
    
    # Veri birleştirme
    world = world.merge(pop_data, left_on='NAME', right_on='NAME', how='left')
    
    # Alan hesaplama (km²)
    world['AREA_KM2'] = world['geometry'].to_crs('ESRI:54009').area / 10**6
    
    # Nüfus yoğunluğu hesaplama (kişi/km²)
    world['DENSITY'] = world['POPULATION'] / world['AREA_KM2']
    
    # Yoğunluğu kategorilere ayırma
    bins = [0, 10, 50, 100, 250, 500, 1000, 5000, float('inf')]
    labels = ['<10', '10-50', '50-100', '100-250', '250-500', '500-1000', '1000-5000', '>5000']
    world['DENSITY_CAT'] = pd.cut(world['DENSITY'], bins=bins, labels=labels, right=False)
    
    return world

# 4. Haritayı oluşturma
def create_population_density_map(world):
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    
    # Renk paleti
    colors = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594']
    cmap = plt.cm.get_cmap('Blues', len(colors))
    
    # Harita çizimi
    world.plot(
        ax=ax,
        column='DENSITY_CAT',
        categorical=True,
        cmap=cmap,
        edgecolor='black',
        linewidth=0.3,
        missing_kwds={'color': 'lightgrey'},
        legend=True,
        legend_kwds={
            'loc': 'lower left',
            'title': 'Nüfus Yoğunluğu (kişi/km²)',
            'frameon': True,
            'framealpha': 0.8,
            'fontsize': 10
        }
    )
    
    # Arkaplan haritası
    ctx.add_basemap(
        ax,
        source=ctx.providers.CartoDB.Positron,
        crs=world.crs.to_string(),
        alpha=0.8
    )
    
    # Başlık ve etiketler
    plt.title('DÜNYA NÜFUS YOĞUNLUĞU (2024)', fontsize=22, pad=20)
    plt.annotate(
        'Kaynak: Dünya Bankası & Natural Earth',
        xy=(0.1, 0.05),
        xycoords='figure fraction',
        fontsize=10,
        color='#555555'
    )
    
    # En yoğun 10 ülkeyi gösterme
    top10 = world.sort_values('DENSITY', ascending=False).head(10)
    for idx, row in top10.iterrows():
        if not pd.isna(row['DENSITY']):
            plt.annotate(
                text=f"{row['NAME']}: {int(row['DENSITY'])}",
                xy=row['geometry'].centroid.coords[0],
                xytext=(3, 3),
                textcoords="offset points",
                fontsize=9,
                color='darkred',
                weight='bold'
            )
    
    plt.axis('off')
    plt.tight_layout()
    
    # Kaydetme
    plt.savefig('nufus_yogunlugu_haritasi.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Yoğunluk tablosu oluşturma
    density_report = world[['NAME', 'POPULATION', 'AREA_KM2', 'DENSITY', 'DENSITY_CAT']]
    density_report = density_report.sort_values('DENSITY', ascending=False)
    density_report['DENSITY'] = density_report['DENSITY'].round(1)
    density_report = density_report.rename(columns={
        'NAME': 'Ülke',
        'POPULATION': 'Nüfus',
        'AREA_KM2': 'Alan (km²)',
        'DENSITY': 'Yoğunluk (kişi/km²)',
        'DENSITY_CAT': 'Yoğunluk Kategori'
    })
    
    # Tabloyu HTML olarak kaydetme
    density_report.head(20).to_html('nufus_yogunlugu_tablosu.html', index=False)
    print("Nüfus yoğunluğu tablosu oluşturuldu: nufus_yogunlugu_tablosu.html")

# 5. Ana işlem
if __name__ == "__main__":
    print("Veriler indiriliyor ve işleniyor...")
    world_data = prepare_data()
    
    print("Harita oluşturuluyor...")
    create_population_density_map(world_data)
    
    print("İşlem tamamlandı. 'nufus_yogunlugu_haritasi.png' kaydedildi.")
