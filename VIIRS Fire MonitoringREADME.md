# Requiry libraries
!pip install cartopy matplotlib imageio pandas numpy requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime, timedelta
import imageio
import os
import requests
from io import StringIO
import time

# NASA FIRMS VIIRS data source (recent 24 o'clock)
VIIRS_URL = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_24h.csv"

# VIIRS data analysis
def get_viirs_fire_data():
    try:
        print("VIIRS data dowload...")
        start_time = time.time()
        response = requests.get(VIIRS_URL, timeout=60)
        response.raise_for_status()
        
        # Load data into DataFrame
        df = pd.read_csv(StringIO(response.text))
        download_time = time.time() - start_time
        print(f"Veri indirme süresi: {download_time:.2f}s - {len(df)} yangın noktası bulundu.")
        
        # VIIRS data structure
        print("Mevcut sütunlar:", df.columns.tolist())
        
        # Date/o'lock transformation (VIIRS file)
        if 'acq_date' in df.columns and 'acq_time' in df.columns:
            df['acq_datetime'] = pd.to_datetime(
                df['acq_date'] + ' ' + df['acq_time'].astype(str).str.zfill(4),
                format='%Y-%m-%d %H%M'
            )
        else:
            print("Uyarı: Tarih sütunu bulunamadı. Şimdiki zaman kullanılacak.")
            df['acq_datetime'] = datetime.utcnow()
            
        return df
    
    except Exception as e:
        print(f"VIIRS data error: {e}")
        print("Use a sample data..")
        # Sample data 
        return pd.DataFrame({
            'latitude': [38.0, 34.5, -25.0, 40.0, -35.0, 50.0],
            'longitude': [35.0, 51.5, 134.0, -120.0, 150.0, -100.0],
            'acq_datetime': [datetime.utcnow() - timedelta(hours=i) for i in range(6)],
            'bright_ti4': [350, 420, 380, 310, 290, 400],
            'confidence': ['high', 'nominal', 'high', 'low', 'nominal', 'high']
        })

# Creating a physical map
def create_base_map(ax):
    ax.clear()
    ax.set_global()
    ax.add_feature(cfeature.OCEAN, facecolor='#a6d6ff', zorder=0)
    ax.add_feature(cfeature.LAND, facecolor='#e5e5e5', zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, zorder=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5, zorder=1)
    ax.add_feature(cfeature.LAKES, alpha=0.5, facecolor='#a6d6ff', zorder=0)
    return ax

# Cretaing a fire animation
def create_viirs_fire_animation():
    # Veriyi al
    fire_df = get_viirs_fire_data()
    
    # Set time intervals (3-hour intervals)
    if not fire_df.empty and 'acq_datetime' in fire_df.columns:
        start_time = fire_df['acq_datetime'].min().floor('H')
        end_time = fire_df['acq_datetime'].max().ceil('H')
        time_intervals = pd.date_range(start_time, end_time, freq='3H')
        print(f"{len(time_intervals)} zaman dilimi oluşturuldu.")
    else:
        print("Warning: No time information found. Single frame to be created.")
        time_intervals = [datetime.utcnow()]
    
    # Visualisation settings
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # Build fire frames
    frame_files = []
    total_frames = len(time_intervals)
    
    for i, interval_end in enumerate(time_intervals):
        print(f"\nKare {i+1}/{total_frames} işleniyor...")
        interval_start = interval_end - timedelta(hours=3)
        
        # Filter by time range
        if not fire_df.empty and 'acq_datetime' in fire_df.columns:
            mask = (fire_df['acq_datetime'] >= interval_start) & (fire_df['acq_datetime'] < interval_end)
            df_interval = fire_df.loc[mask].copy()
        else:
            df_interval = fire_df.copy()
        
        # Create the base map
        ax = create_base_map(ax)
        
        # VIIRS fire points
        if not df_interval.empty:
            # Risk colours
            confidence_colors = {
                'high': 'red',
                'nominal': 'orange',
                'low': 'yellow',
                'n': 'orange',  # Alternatif etiket
                'h': 'red',     # Alternatif etiket
                'l': 'yellow'   # Alternatif etiket
            }
            
            # colour assignment
            df_interval['color'] = df_interval['confidence'].str.lower().map(
                lambda x: confidence_colors.get(x, 'yellow')
            )
            
            # VIIRS special parameters
            if 'bright_ti4' in df_interval.columns:
                sizes = df_interval['bright_ti4'] * 0.05  # Parlaklığa göre boyut
            else:
                sizes = 30  # Varsayılan boyut
            
            # Draw fire points
            sc = ax.scatter(
                df_interval['longitude'], 
                df_interval['latitude'],
                c=df_interval['color'],
                s=sizes,
                alpha=0.8,
                edgecolors='black',
                linewidth=0.3,
                transform=ccrs.PlateCarree(),
                zorder=2
            )
            
            # Show the number of fires in the title
            fire_count = len(df_interval)
        else:
            fire_count = 0
        
        # Title and informations
        title = f"NASA VIIRS Global Forest Fire Monitoring\n{interval_end.strftime('%Y-%m-%d %H:%M')} UTC - {fire_count} Fire"
        plt.title(title, fontsize=14, pad=20)
        
        # Lejant ekle
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='High risk'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=8, label='Moderate risk'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=8, label='Low risk')
        ]
        ax.legend(handles=legend_elements, loc='lower left', framealpha=0.9)
        
        # Save frame
        frame_file = f"viirs_frame_{i:03d}.png"
        plt.savefig(frame_file, bbox_inches='tight', dpi=100, transparent=False)
        frame_files.append(frame_file)
        print(f"Çerçeve oluşturuldu: {frame_file} - Yangın Sayısı: {fire_count}")
    
    # GIF create
    if frame_files:
        gif_path = 'viirs_global_fire_animation.gif'
        print("\nGIF oluşturuluyor...")
        
        images = []
        for frame in frame_files:
            images.append(imageio.imread(frame))
        
        imageio.mimsave(gif_path, images, duration=0.7)
        
        # Clear temporary files
        for frame in frame_files:
            if os.path.exists(frame):
                os.remove(frame)
        
        return gif_path
    else:
        return None

# Create and show animation
print("="*50)
print("NASA VIIRS Global Yangın Animasyonu Oluşturuluyor")
print("="*50)
start_time = time.time()

gif_path = create_viirs_fire_animation()
execution_time = time.time() - start_time

if gif_path and os.path.exists(gif_path):
    print(f"\n✔️ Animasyon başarıyla oluşturuldu: {gif_path}")
    print(f"⏱️ Toplam süre: {execution_time:.2f} saniye")
    
    # GIF'i show
    from IPython.display import Image
    display(Image(filename=gif_path))
    
    # Size control
    file_size = os.path.getsize(gif_path) / (1024 * 1024)
    print(f"📁 File control: {file_size:.2f} MB")
