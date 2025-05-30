Based on Uludag mountain examples:

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.ndimage import gaussian_filter

def uludag_kontur_haritasi():
    # Uludağ merkez koordinatları
    uludag_merkez = (40.0736, 29.2215)

    # Harita sınırları (enlem ve boylam)
    enlem_min, enlem_max = 40.00, 40.15
    boylam_min, boylam_max = 29.10, 29.35

    # Grid oluşturma
    x = np.linspace(boylam_min, boylam_max, 200)
    y = np.linspace(enlem_min, enlem_max, 200)
    X, Y = np.meshgrid(x, y)

    # Yükseklik fonksiyonu (Uludağ için simüle edilmiş)
    def yukseklik(enlem, boylam):
        # Uludağ ana zirve
        uzaklik = np.sqrt((boylam - uludag_merkez[1])*2 + (enlem - uludag_merkez[0])*2)
        ana_zirve = 2543 * np.exp(-(uzaklik/0.03)**2)

        # Diğer tepeler
        zirve2 = 1800 * np.exp(-((boylam-29.18)*2/0.002 + (enlem-40.05)*2/0.003))
        zirve3 = 1600 * np.exp(-((boylam-29.28)*2/0.0015 + (enlem-40.10)*2/0.002))

        # Temel yükseklik
        temel = 500 + 300*(enlem - enlem_min)

        return temel + ana_zirve + zirve2 + zirve3

    # Yükseklik verisini hesapla
    Z = yukseklik(Y, X)

    # Yumuşatma uygula
    Z = gaussian_filter(Z, sigma=1)

    # Kontur haritası oluştur
    plt.figure(figsize=(12, 10))

    # Seviyeleri belirle (her 100 metrede bir)
    seviyeler = np.arange(500, 2600, 100)

    # Kontur çizgileri
    CS = plt.contour(X, Y, Z, levels=seviyeler, colors='black', linewidths=0.5)
    plt.clabel(CS, inline=True, fontsize=8, fmt='%1.0f m')

    # Renkli doldurma
    plt.contourf(X, Y, Z, levels=seviyeler, cmap=cm.terrain)

    # Renk çubuğu
    cbar = plt.colorbar()
    cbar.set_label('Yükseklik (metre)')

    # Önemli noktaları işaretle
    plt.plot(uludag_merkez[1], uludag_merkez[0], '^r', markersize=10, label='Uludağ Zirvesi (2543 m)')
    plt.plot(29.1433, 40.1069, 'sb', markersize=8, label='Sarıalan Kamp (1600 m)')
    plt.plot(29.0278, 40.1936, 'og', markersize=8, label='Teleferik Başlangıç')

    # Harita bilgileri
    plt.title('Uludağ Kontur (Yükselti) Haritası')
    plt.xlabel('Boylam')
    plt.ylabel('Enlem')
    plt.grid(linestyle='--', alpha=0.5)
    plt.legend()

    # Kaydet
    plt.savefig('uludag_kontur_haritasi.png', dpi=300, bbox_inches='tight')
    print("Uludağ kontur haritası 'uludag_kontur_haritasi.png' olarak kaydedildi.")

# 3B Yüzey Görselleştirme
def uludag_3b_harita():
    from mpl_toolkits.mplot3d import Axes3D

    # Uludağ merkez koordinatları
    uludag_merkez = (40.0736, 29.2215)

    # Daha dar bir alan için sınırlar
    enlem_min, enlem_max = 40.04, 40.10
    boylam_min, boylam_max = 29.18, 29.28

    # Grid oluşturma
    x = np.linspace(boylam_min, boylam_max, 100)
    y = np.linspace(enlem_min, enlem_max, 100)
    X, Y = np.meshgrid(x, y)

    # Yükseklik fonksiyonu
    def yukseklik(enlem, boylam):
        uzaklik = np.sqrt((boylam - uludag_merkez[1])*2 + (enlem - uludag_merkez[0])*2)
        return 500 + 2000 * np.exp(-(uzaklik/0.02)**2)

    Z = yukseklik(Y, X)

    # 3B grafik
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Yüzey çizimi
    surf = ax.plot_surface(X, Y, Z, cmap=cm.terrain,
                         rstride=1, cstride=1, alpha=0.8,
                         linewidth=0, antialiased=True)

    # Kontur çizgileri
    ax.contour(X, Y, Z, zdir='z', offset=500, cmap=cm.terrain)

    # Zirveyi işaretle
    ax.scatter([uludag_merkez[1]], [uludag_merkez[0]], [2543],
              color='red', s=100, label='Uludağ Zirvesi')

    # Grafik ayarları
    ax.set_title('Uludağ 3B Yükselti Haritası')
    ax.set_xlabel('Boylam')
    ax.set_ylabel('Enlem')
    ax.set_zlabel('Yükseklik (m)')
    ax.legend()

    # Renk çubuğu
    fig.colorbar(surf, shrink=0.5, aspect=5, label='Yükseklik (m)')

    # Kaydet
    plt.savefig('uludag_3b_harita.png', dpi=300, bbox_inches='tight')
    print("Uludağ 3B haritası 'uludag_3b_harita.png' olarak kaydedildi.")

if _name_ == "_main_":
    uludag_kontur_haritasi()
    uludag_3b_harita()
