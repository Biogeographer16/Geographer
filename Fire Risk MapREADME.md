Yangın Risk Haritası 

# -*- coding: utf-8 -*-
"""
BURSA ORMAN YANGINI TEHLİKE HARİTASI (Harmancık, Dağ Güney, Fideykızık, Çivili)
Tam çalışan versiyon - SyntaxError düzeltildi
"""

import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx

# 1. BÖLGE KOORDİNATLARI
bbox = {
    "min_lon": 29.15,
    "max_lon": 29.35,
    "min_lat": 39.85,
    "max_lat": 40.00
}

# 2. YANGIN RİSK MODELİ OLUŞTURMA
def generate_hazard_data():
    """Simüle edilmiş yangın risk verisi"""
    x = np.linspace(bbox["min_lon"], bbox["max_lon"], 500)
    y = np.linspace(bbox["min_lat"], bbox["max_lat"], 500)
    X, Y = np.meshgrid(x, y)
    
    # Yükseklik modeli (Harmancık Dağı)
    Z = 1000 * np.exp(-((X-29.25)**2 + (Y-39.92)**2) / 0.005)
    
    # Bitki örtüsü (0-1 arası)
    vegetation = 0.7 * np.sin(X*20) + 0.3 * np.cos(Y*20) + 0.5
    
    # Yangın risk skoru (0-1 arası)
    risk = (Z/1000 * 0.4) + ((1-vegetation) * 0.6)
    return X, Y, risk

# 3. HARİTA OLUŞTURMA
X, Y, risk = generate_hazard_data()
fig, ax = plt.subplots(figsize=(12, 10))

# Risk haritası
contour = ax.contourf(X, Y, risk, levels=np.linspace(0, 1, 11), 
                     cmap='RdYlGn_r', alpha=0.7)

# Yerleşim noktaları
settlements = {
    "Harmancık": (29.25, 39.92),
    "Dağ Güney": (29.20, 39.89),
    "Fideykızık": (29.30, 39.88),
    "Çivili": (29.18, 39.90)
}

for name, (lon, lat) in settlements.items():
    ax.plot(lon, lat, 'ro', markersize=8)
    ax.text(lon+0.005, lat+0.005, name, fontsize=9, weight='bold')

# Lejant ve başlık
cbar = fig.colorbar(contour, ax=ax, label='Yangın Risk Skoru')
ax.set_title("BURSA - HARMANCIK BÖLGESİ ORMAN YANGINI TEHLİKE HARİTASI", 
            fontsize=12, pad=15)
ax.set_xlabel("Boylam")
ax.set_ylabel("Enlem")

# Arka plan harita ekleme
try:
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
except Exception as e:
    print("Arka plan harita yüklenemedi:", e)

plt.savefig("bursa_yangin_tehlikesi.png", dpi=300, bbox_inches='tight')
plt.show()
print("Harita başarıyla oluşturuldu: 'bursa_yangin_tehlikesi.png'")


Yangın yerleşim haritası
# -*- coding: utf-8 -*-
"""
BURSA TUTUŞMA RİSK HARİTASI (Flammap Tarzı - Tek Parça Kod)
1. Çalıştırmadan önce: pip install numpy matplotlib contextily
2. PNG çıktısı: bursa_tutusma_riski.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import contextily as ctx

# 1. FLAMMAP TARZI RENK PALETİ
flammap_renkleri = [
    (0.0, '#FFFFFF'),  # Beyaz (Düşük risk)
    (0.2, '#00FF00'),  # Yeşil (Orman)
    (0.4, '#FFFF00'),  # Sarı (Çalılık)
    (0.6, '#FFA500'),  # Turuncu (Kuru ot)
    (0.8, '#FF0000'),  # Kırmızı (Yüksek risk)
    (1.0, '#800080')   # Mor (Aşırı risk)
]
palet = LinearSegmentedColormap.from_list('flammap', flammap_renkleri)

# 2. TUTUŞMA RİSK MODELİ
def risk_hesapla():
    """Bölge için simüle edilmiş risk matrisi"""
    x = np.linspace(29.15, 29.35, 500)  # Boylam
    y = np.linspace(39.85, 40.00, 500)  # Enlem
    X, Y = np.meshgrid(x, y)
    
    # Ana risk faktörleri
    yukseklik = 800 * np.exp(-((X-29.22)**2 + (Y-39.90)**2)/0.004)
    bitki_ortusu = 0.6 * np.sin(X*15)**2 + 0.4 * np.cos(Y*18)**2
    ruzgar_etkisi = 0.5 * (X - 29.15)/0.2
    
    # Bileşik risk indeksi (0-1 arası)
    risk = 0.4*(yukseklik/1000) + 0.3*(1-bitki_ortusu) + 0.3*ruzgar_etkisi
    return np.clip(risk, 0, 1), X, Y

# 3. HARİTA OLUŞTURMA
def harita_uret():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    
    # Veri hesapla
    risk, X, Y = risk_hesapla()
    
    # Görselleştirme
    im = ax.imshow(risk, extent=[29.15, 29.35, 39.85, 40.00],
                  cmap=palet, alpha=0.9, origin='lower', vmin=0, vmax=1)
    
    # Yerleşim noktaları
    yerlesimler = {
        "HARMANCIK": (29.25, 39.92),
        "DAĞ GÜNEY": (29.20, 39.89),
        "FİDEYKIZIK": (29.30, 39.88),
        "ÇİVİLİ": (29.18, 39.90)
    }
    for isim, (lon, lat) in yerlesimler.items():
        ax.plot(lon, lat, 'o', color='black', markersize=8, markeredgewidth=1)
        ax.text(lon+0.005, lat+0.005, isim, fontsize=10, weight='bold',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Lejant
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, label='TUTUŞMA RİSK İNDEKSİ')
    cbar.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    cbar.set_ticklabels(['ÇOK DÜŞÜK', 'DÜŞÜK', 'ORTA', 'YÜKSEK', 'ÇOK YÜKSEK', 'AŞIRI'])
    
    # Başlık ve etiketler
    ax.set_title("BURSA - HARMANCIK BÖLGESİ TUTUŞMA RİSK HARİTASI\n(Flammap Modeli)",
                fontsize=14, weight='bold', pad=20)
    ax.set_xlabel("BOYLAM (°)", fontsize=10)
    ax.set_ylabel("ENLEM (°)", fontsize=10)
    
    # Arka plan harita (OpenStreetMap)
    try:
        ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik,
                       attribution="(C) OpenStreetMap Contributors")
    except Exception as e:
        print(f"Arka plan harita hatası: {str(e)}")
    
    # PNG olarak kaydet
    cikti_dosya = "bursa_tutusma_riski.png"
    plt.savefig(cikti_dosya, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"\n✓ Harita başarıyla oluşturuldu: {cikti_dosya}")

# 4. ÇALIŞTIRMA
if __name__ == "__main__":
    harita_uret()
    import os
print("Dosya yolu:", os.path.abspath("bursa_tutusma_riski.png"))


# bursa_flammap_garantili.py
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap

# 1. Basit veri oluşturma
x = np.linspace(29.15, 29.35, 100)
y = np.linspace(39.85, 40.00, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X*10) + np.cos(Y*10)

# 2. Grafik oluşturma
plt.figure(figsize=(10,8))
plt.contourf(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar(label='Risk İndeksi')

# 3. Kesin kayıt yolu
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
output_path = os.path.join(desktop_path, 'BURSA_TUTUSMA_RISK.png')

plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

# 4. Sonuç kontrolü
if os.path.exists(output_path):
    print(f"✓ Harita BAŞARIYLA kaydedildi:\n{output_path}")
    os.startfile(output_path)  # Dosyayı otomatik aç
else:
    print("❌ Hata: Dosya oluşturulamadı. Yazma izinlerini kontrol edin.")
# bursa_yangin_riski_son.py
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap

# 1. AYARLAR
YERLESIMLER = {
    "HARMANCIK": (29.25, 39.92),
    "DAĞ GÜNEY": (29.20, 39.89),
    "FİDEYKIZIK": (29.30, 39.88),
    "ÇİVİLİ": (29.18, 39.90)
}
PALET = [(0,'white'), (0.2,'green'), (0.4,'yellow'), (0.6,'orange'), (0.8,'red'), (1,'purple')]

# 2. HARİTA OLUŞTURMA
def harita_uret():
    # Veri oluştur
    x = np.linspace(29.15, 29.35, 500)
    y = np.linspace(39.85, 40.00, 500)
    X, Y = np.meshgrid(x, y)
    risk = np.sin(X*10)**2 + np.cos(Y*10)**2 * 0.7  # Simüle risk verisi
    
    # Çizim
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.contourf(X, Y, risk, levels=20, cmap=LinearSegmentedColormap.from_list('flammap', PALET))
    
    # Yerleşimleri işaretle
    for name, (lon, lat) in YERLESIMLER.items():
        plt.plot(lon, lat, 'o', color='black', markersize=8)
        plt.text(lon+0.005, lat+0.005, name, fontsize=10, weight='bold',
                bbox=dict(facecolor='white', alpha=0.8))
    
    # Lejant
    plt.colorbar(label='Tutuşma Riski (0-1)')
    plt.title("BURSA - HARMANCIK BÖLGESİ YANGIN RİSK HARİTASI")

    # 3. KAYDETME (Mevcut dizine)
    kayit_yolu = os.path.join(os.getcwd(), "BURSA_YANGIN_RISK.png")
    plt.savefig(kayit_yolu, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Kontrol
    if os.path.exists(kayit_yolu):
        print(f"✓ Harita başarıyla kaydedildi:\n{kayit_yolu}")
        # Windows'ta otomatik aç
        if os.name == 'nt':
            os.startfile(kayit_yolu)
    else:
        print("❌ Hata: Dosya oluşturulamadı!")

# ÇALIŞTIR
if __name__ == "__main__":
    harita_uret()
