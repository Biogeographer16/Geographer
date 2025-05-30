#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as PathEffects

# Rastgele sayı üreteci için sabit değer ayarla (tekrarlanabilirlik için)
random.seed(42)
np.random.seed(42)

# Harita başlığı ve boyutu
plt.figure(figsize=(16, 12))
plt.title("Çalışma Alanı Orman Yangını Risk Bölgeleri", fontsize=20, fontweight='bold')

# Ağ oluştur
G = nx.Graph()

# Düğüm türleri ve özellikleri
node_types = {
    # Risk Faktörleri
    'temperature': {'shape': 'o', 'color': 'red', 'size': 300, 'label': 'Sıcaklık'},
    'humidity': {'shape': 'o', 'color': 'blue', 'size': 300, 'label': 'Nem'},
    'wind': {'shape': '^', 'color': 'gray', 'size': 300, 'label': 'Rüzgar'},
    'vegetation': {'shape': 's', 'color': 'green', 'size': 300, 'label': 'Bitki Örtüsü'},
    'topography': {'shape': 'd', 'color': 'brown', 'size': 300, 'label': 'Topografya'},
    
    # İzleme İstasyonları
    'meteo_station': {'shape': '*', 'color': 'dodgerblue', 'size': 350, 'label': 'Meteoroloji İstasyonu'},
    'satellite': {'shape': 'h', 'color': 'skyblue', 'size': 350, 'label': 'Uydu İzleme Noktası'},
    'camera': {'shape': '^', 'color': 'deepskyblue', 'size': 250, 'label': 'Kamera Sistemi'},
    'sensor': {'shape': 'o', 'color': 'lightblue', 'size': 150, 'label': 'Sensör Ağı'},
    
    # Müdahale Birimleri
    'fire_station': {'shape': 's', 'color': 'orange', 'size': 350, 'label': 'İtfaiye İstasyonu'},
    'forest_team': {'shape': '^', 'color': 'darkorange', 'size': 300, 'label': 'Orman Yangın Ekibi'},
    'air_base': {'shape': 'd', 'color': 'orangered', 'size': 350, 'label': 'Hava Araçları Üssü'},
    'emergency': {'shape': '*', 'color': 'coral', 'size': 300, 'label': 'Acil Durum Merkezi'},
    
    # Yerleşim Yerleri
    'village': {'shape': 'o', 'color': 'black', 'size': 100, 'label': 'Köy'},
    'city': {'shape': 'o', 'color': 'black', 'size': 250, 'label': 'Şehir'},
    'critical_facility': {'shape': 's', 'color': 'black', 'size': 200, 'label': 'Kritik Tesis'},
    
    # Karar Verme Merkezleri
    'management': {'shape': 's', 'color': 'purple', 'size': 300, 'label': 'Yönetim Birimi'},
    'crisis_center': {'shape': '*', 'color': 'darkviolet', 'size': 350, 'label': 'Kriz Merkezi'},
    'coordination': {'shape': '^', 'color': 'mediumpurple', 'size': 300, 'label': 'Koordinasyon Merkezi'},
    
    # Su Kaynakları
    'lake': {'shape': 'o', 'color': 'lightblue', 'size': 400, 'label': 'Göl/Baraj'},
    'fire_pool': {'shape': 's', 'color': 'lightblue', 'size': 200, 'label': 'Yangın Havuzu'}
}

# Bölgeler (x, y koordinat aralıkları)
regions = {
    'bursa_center': {'x': (-5, 5), 'y': (0, 10), 'label': 'Bursa Merkez', 'risk': 'medium'},
    'uludag': {'x': (0, 10), 'y': (-5, 5), 'label': 'Uludağ Bölgesi', 'risk': 'high'},
    'iznik': {'x': (10, 20), 'y': (0, 10), 'label': 'İznik Bölgesi', 'risk': 'medium'},
    'mudanya': {'x': (-15, -5), 'y': (0, 10), 'label': 'Mudanya Bölgesi', 'risk': 'low'},
    'karacabey': {'x': (-25, -15), 'y': (-5, 5), 'label': 'Karacabey Bölgesi', 'risk': 'medium'},
    'yenisehir': {'x': (5, 15), 'y': (-15, -5), 'label': 'Yenişehir Bölgesi', 'risk': 'critical'},
    'inegol': {'x': (-5, 5), 'y': (-15, -5), 'label': 'İnegöl Bölgesi', 'risk': 'high'}
}

# Risk seviyeleri ve renkleri
risk_levels = {
    'low': {'color': '#8BC34A', 'alpha': 0.3, 'label': 'Düşük Risk'},
    'medium': {'color': '#FFEB3B', 'alpha': 0.4, 'label': 'Orta Risk'},
    'high': {'color': '#FF9800', 'alpha': 0.5, 'label': 'Yüksek Risk'},
    'critical': {'color': '#F44336', 'alpha': 0.6, 'label': 'Kritik Risk'}
}

# Bağlantı türleri
edge_types = {
    'data_flow': {'style': '-', 'color': 'blue', 'width': 1.5, 'label': 'Veri Akışı'},
    'alert': {'style': '--', 'color': 'red', 'width': 2.0, 'label': 'Acil Uyarı'},
    'routine_alert': {'style': '--', 'color': 'orange', 'width': 1.0, 'label': 'Rutin Uyarı'},
    'ground_response': {'style': '-', 'color': 'orange', 'width': 2.0, 'label': 'Kara Müdahalesi'},
    'air_response': {'style': ':', 'color': 'orange', 'width': 2.0, 'label': 'Hava Müdahalesi'},
    'high_impact': {'style': '-', 'color': 'red', 'width': 2.0, 'label': 'Yüksek Etki'},
    'medium_impact': {'style': '-', 'color': 'orange', 'width': 1.5, 'label': 'Orta Etki'},
    'low_impact': {'style': '-', 'color': 'yellow', 'width': 1.0, 'label': 'Düşük Etki'},
    'coordination': {'style': ':', 'color': 'purple', 'width': 1.5, 'label': 'Koordinasyon'},
    'hierarchical': {'style': '-', 'color': 'purple', 'width': 1.0, 'label': 'Hiyerarşik İletişim'}
}

# Düğümleri oluştur
nodes = {
    # Risk Faktörleri
    'temp1': {'type': 'temperature', 'region': 'uludag', 'name': 'Uludağ Sıcaklık', 'value': 35},
    'temp2': {'type': 'temperature', 'region': 'yenisehir', 'name': 'Yenişehir Sıcaklık', 'value': 38},
    'temp3': {'type': 'temperature', 'region': 'inegol', 'name': 'İnegöl Sıcaklık', 'value': 36},
    'hum1': {'type': 'humidity', 'region': 'uludag', 'name': 'Uludağ Nem', 'value': 20},
    'hum2': {'type': 'humidity', 'region': 'yenisehir', 'name': 'Yenişehir Nem', 'value': 15},
    'hum3': {'type': 'humidity', 'region': 'mudanya', 'name': 'Mudanya Nem', 'value': 40},
    'wind1': {'type': 'wind', 'region': 'uludag', 'name': 'Uludağ Rüzgar', 'value': 30},
    'wind2': {'type': 'wind', 'region': 'yenisehir', 'name': 'Yenişehir Rüzgar', 'value': 25},
    'veg1': {'type': 'vegetation', 'region': 'uludag', 'name': 'Uludağ Bitki Örtüsü', 'value': 80},
    'veg2': {'type': 'vegetation', 'region': 'yenisehir', 'name': 'Yenişehir Bitki Örtüsü', 'value': 90},
    'veg3': {'type': 'vegetation', 'region': 'inegol', 'name': 'İnegöl Bitki Örtüsü', 'value': 85},
    'topo1': {'type': 'topography', 'region': 'uludag', 'name': 'Uludağ Topografya', 'value': 75},
    'topo2': {'type': 'topography', 'region': 'yenisehir', 'name': 'Yenişehir Topografya', 'value': 40},
    
    # İzleme İstasyonları
    'meteo1': {'type': 'meteo_station', 'region': 'bursa_center', 'name': 'Bursa Meteoroloji'},
    'meteo2': {'type': 'meteo_station', 'region': 'uludag', 'name': 'Uludağ Meteoroloji'},
    'sat1': {'type': 'satellite', 'region': 'bursa_center', 'name': 'Uydu İzleme Merkezi'},
    'cam1': {'type': 'camera', 'region': 'uludag', 'name': 'Uludağ Kamera 1'},
    'cam2': {'type': 'camera', 'region': 'yenisehir', 'name': 'Yenişehir Kamera'},
    'cam3': {'type': 'camera', 'region': 'inegol', 'name': 'İnegöl Kamera'},
    'sens1': {'type': 'sensor', 'region': 'uludag', 'name': 'Uludağ Sensör Ağı 1'},
    'sens2': {'type': 'sensor', 'region': 'uludag', 'name': 'Uludağ Sensör Ağı 2'},
    'sens3': {'type': 'sensor', 'region': 'yenisehir', 'name': 'Yenişehir Sensör Ağı'},
    'sens4': {'type': 'sensor', 'region': 'inegol', 'name': 'İnegöl Sensör Ağı'},
    
    # Müdahale Birimleri
    'fire1': {'type': 'fire_station', 'region': 'bursa_center', 'name': 'Bursa İtfaiye'},
    'fire2': {'type': 'fire_station', 'region': 'inegol', 'name': 'İnegöl İtfaiye'},
    'forest1': {'type': 'forest_team', 'region': 'uludag', 'name': 'Uludağ Orman Ekibi'},
    'forest2': {'type': 'forest_team', 'region': 'yenisehir', 'name': 'Yenişehir Orman Ekibi'},
    'forest3': {'type': 'forest_team', 'region': 'inegol', 'name': 'İnegöl Orman Ekibi'},
    'air1': {'type': 'air_base', 'region': 'bursa_center', 'name': 'Bursa Hava Üssü'},
    'emerg1': {'type': 'emergency', 'region': 'bursa_center', 'name': 'Bursa AFAD'},
    
    # Yerleşim Yerleri
    'village1': {'type': 'village', 'region': 'uludag', 'name': 'Cumalıkızık Köyü'},
    'village2': {'type': 'village', 'region': 'yenisehir', 'name': 'Yenişehir Köyü 1'},
    'village3': {'type': 'village', 'region': 'yenisehir', 'name': 'Yenişehir Köyü 2'},
    'village4': {'type': 'village', 'region': 'inegol', 'name': 'İnegöl Köyü 1'},
    'village5': {'type': 'village', 'region': 'inegol', 'name': 'İnegöl Köyü 2'},
    'city1': {'type': 'city', 'region': 'bursa_center', 'name': 'Bursa'},
    'city2': {'type': 'city', 'region': 'inegol', 'name': 'İnegöl'},
    'facility1': {'type': 'critical_facility', 'region': 'bursa_center', 'name': 'Kritik Tesis 1'},
    
    # Karar Verme Merkezleri
    'mgmt1': {'type': 'management', 'region': 'bursa_center', 'name': 'Bursa Orman Bölge Müdürlüğü'},
    'crisis1': {'type': 'crisis_center', 'region': 'bursa_center', 'name': 'Bursa Kriz Merkezi'},
    'coord1': {'type': 'coordination', 'region': 'bursa_center', 'name': 'Koordinasyon Merkezi'},
    'coord2': {'type': 'coordination', 'region': 'inegol', 'name': 'İnegöl Koordinasyon'},
    
    # Su Kaynakları
    'lake1': {'type': 'lake', 'region': 'iznik', 'name': 'İznik Gölü'},
    'lake2': {'type': 'lake', 'region': 'uludag', 'name': 'Uludağ Barajı'},
    'pool1': {'type': 'fire_pool', 'region': 'uludag', 'name': 'Yangın Havuzu 1'},
    'pool2': {'type': 'fire_pool', 'region': 'yenisehir', 'name': 'Yangın Havuzu 2'},
    'pool3': {'type': 'fire_pool', 'region': 'inegol', 'name': 'Yangın Havuzu 3'}
}

# Düğümleri grafa ekle ve konumlarını belirle
pos = {}
for node_id, node_data in nodes.items():
    G.add_node(node_id, **node_data)
    region = regions[node_data['region']]
    # Bölge içinde rastgele konum
    x = random.uniform(region['x'][0], region['x'][1])
    y = random.uniform(region['y'][0], region['y'][1])
    pos[node_id] = (x, y)

# Bağlantıları oluştur
connections = [
    # Veri Akışı Bağlantıları
    ('sens1', 'meteo2', 'data_flow'),
    ('sens2', 'meteo2', 'data_flow'),
    ('sens3', 'meteo1', 'data_flow'),
    ('sens4', 'meteo1', 'data_flow'),
    ('meteo1', 'sat1', 'data_flow'),
    ('meteo2', 'sat1', 'data_flow'),
    ('cam1', 'sat1', 'data_flow'),
    ('cam2', 'sat1', 'data_flow'),
    ('cam3', 'sat1', 'data_flow'),
    ('sat1', 'mgmt1', 'data_flow'),
    ('sat1', 'crisis1', 'data_flow'),
    
    # Uyarı Sinyalleri
    ('meteo2', 'crisis1', 'alert'),
    ('sat1', 'crisis1', 'alert'),
    ('crisis1', 'emerg1', 'alert'),
    ('crisis1', 'fire1', 'alert'),
    ('crisis1', 'air1', 'alert'),
    ('meteo1', 'coord1', 'routine_alert'),
    ('coord1', 'forest1', 'routine_alert'),
    ('coord1', 'forest2', 'routine_alert'),
    ('coord1', 'forest3', 'routine_alert'),
    
    # Müdahale Rotaları
    ('fire1', 'village1', 'ground_response'),
    ('fire1', 'village2', 'ground_response'),
    ('fire2', 'village4', 'ground_response'),
    ('fire2', 'village5', 'ground_response'),
    ('forest1', 'village1', 'ground_response'),
    ('forest2', 'village2', 'ground_response'),
    ('forest2', 'village3', 'ground_response'),
    ('forest3', 'village4', 'ground_response'),
    ('forest3', 'village5', 'ground_response'),
    ('air1', 'village1', 'air_response'),
    ('air1', 'village2', 'air_response'),
    ('air1', 'village3', 'air_response'),
    
    # Risk Etki İlişkileri
    ('temp1', 'veg1', 'high_impact'),
    ('temp2', 'veg2', 'high_impact'),
    ('temp3', 'veg3', 'high_impact'),
    ('wind1', 'veg1', 'high_impact'),
    ('wind2', 'veg2', 'high_impact'),
    ('hum1', 'veg1', 'medium_impact'),
    ('hum2', 'veg2', 'medium_impact'),
    ('hum3', 'veg3', 'low_impact'),
    ('topo1', 'veg1', 'medium_impact'),
    ('topo2', 'veg2', 'low_impact'),
    
    # Koordinasyon Hatları
    ('mgmt1', 'coord1', 'hierarchical'),
    ('mgmt1', 'coord2', 'hierarchical'),
    ('crisis1', 'coord1', 'hierarchical'),
    ('crisis1', 'coord2', 'hierarchical'),
    ('coord1', 'coord2', 'coordination'),
    ('emerg1', 'fire1', 'coordination'),
    ('emerg1', 'fire2', 'coordination'),
    ('emerg1', 'air1', 'coordination'),
    ('fire1', 'forest1', 'coordination'),
    ('fire2', 'forest3', 'coordination'),
    
    # Su Kaynakları Bağlantıları
    ('lake1', 'air1', 'ground_response'),
    ('lake2', 'air1', 'ground_response'),
    ('pool1', 'forest1', 'ground_response'),
    ('pool2', 'forest2', 'ground_response'),
    ('pool3', 'forest3', 'ground_response')
]

# Bağlantıları grafa ekle
for source, target, edge_type in connections:
    G.add_edge(source, target, type=edge_type)

# Risk bölgelerini çiz
for region_id, region_data in regions.items():
    x_min, x_max = region_data['x']
    y_min, y_max = region_data['y']
    width = x_max - x_min
    height = y_max - y_min
    risk_level = region_data['risk']
    risk_color = risk_levels[risk_level]['color']
    risk_alpha = risk_levels[risk_level]['alpha']
    
    rect = plt.Rectangle((x_min, y_min), width, height, fill=True, alpha=risk_alpha, 
                        color=risk_color, edgecolor='black', linewidth=0.5)
    plt.gca().add_patch(rect)
    
    # Bölge etiketleri
    text = plt.text(x_min + width/2, y_max + 0.5, region_data['label'], 
                   ha='center', fontsize=10, fontweight='bold')
    text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])

# Topografya katmanını simüle et (kabartma gösterimi)
for i in range(100):
    x = random.uniform(-30, 30)
    y = random.uniform(-20, 20)
    size = random.uniform(0.5, 2)
    alpha = random.uniform(0.05, 0.15)
    plt.scatter(x, y, s=size*50, color='gray', alpha=alpha, edgecolors=None)

# İdari sınırları çiz (Bursa il sınırı)
bursa_border_x = [-25, 20, 20, -25, -25]
bursa_border_y = [-15, -15, 10, 10, -15]
plt.plot(bursa_border_x, bursa_border_y, 'k--', linewidth=2, alpha=0.7)

# İlçe sınırlarını çiz
district_borders = [
    [(-5, -15), (-5, 10)],  # Batı-Doğu ayırıcı
    [(5, -15), (5, 10)],    # Doğu-Batı ayırıcı
    [(-25, 0), (20, 0)],    # Kuzey-Güney ayırıcı
    [(-15, -5), (-15, 10)], # Mudanya-Karacabey ayırıcı
    [(10, 0), (10, 10)]     # İznik ayırıcı
]

for border in district_borders:
    start, end = border
    plt.plot([start[0], end[0]], [start[1], end[1]], 'k--', linewidth=1, alpha=0.5)

# Bağlantıları çiz
for u, v, edge_data in G.edges(data=True):
    edge_type = edge_data['type']
    edge_style = edge_types[edge_type]
    
    x1, y1 = pos[u]
    x2, y2 = pos[v]
    
    # Uzun mesafeli bağlantılar için eğri çizgiler
    if abs(x1 - x2) > 10 or abs(y1 - y2) > 5:
        # Eğri bağlantı için kontrol noktası
        control_x = (x1 + x2) / 2
        control_y = (y1 + y2) / 2 + np.sign(y2 - y1) * 3
        
        # Bezier eğrisi için noktalar
        t = np.linspace(0, 1, 100)
        x = (1-t)**2 * x1 + 2*(1-t)*t * control_x + t**2 * x2
        y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2
        
        plt.plot(x, y, linestyle=edge_style['style'], color=edge_style['color'], 
                linewidth=edge_style['width'], alpha=0.7)
        
        # Ok başı ekle (veri akışı ve uyarı için)
        if edge_type in ['data_flow', 'alert', 'routine_alert']:
            arrow_idx = 80  # Eğrinin sonuna yakın bir nokta
            dx = x[arrow_idx+1] - x[arrow_idx-1]
            dy = y[arrow_idx+1] - y[arrow_idx-1]
            arrow_len = np.sqrt(dx**2 + dy**2)
            dx, dy = dx/arrow_len, dy/arrow_len
            plt.arrow(x[arrow_idx], y[arrow_idx], dx*0.5, dy*0.5, 
                    head_width=0.3, head_length=0.5, fc=edge_style['color'], ec=edge_style['color'])
    else:
        # Kısa mesafeli düz bağlantılar
        plt.plot([x1, x2], [y1, y2], linestyle=edge_style['style'], 
                color=edge_style['color'], linewidth=edge_style['width'], alpha=0.7)
        
        # Ok başı ekle (veri akışı ve uyarı için)
        if edge_type in ['data_flow', 'alert', 'routine_alert']:
            dx = x2 - x1
            dy = y2 - y1
            arrow_len = np.sqrt(dx**2 + dy**2)
            dx, dy = dx/arrow_len, dy/arrow_len
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            plt.arrow(mid_x - dx*0.5, mid_y - dy*0.5, dx, dy, 
                    head_width=0.3, head_length=0.5, fc=edge_style['color'], ec=edge_style['color'])

# Düğümleri çiz
for node_id in G.nodes():
    node_data = G.nodes[node_id]
    node_type = node_data['type']
    node_style = node_types[node_type]
    
    x, y = pos[node_id]
    
    # Risk faktörleri için boyut değişimi
    size = node_style['size']
    if node_type in ['temperature', 'humidity', 'wind', 'vegetation', 'topography'] and 'value' in node_data:
        size = node_style['size'] * (0.5 + node_data['value'] / 100)
    
    # Düğüm çiz
    plt.scatter(x, y, s=size, c=node_style['color'], 
               marker=node_style['shape'], edgecolors='black', linewidths=1, alpha=0.9)
    
    # Önemli düğümler için etiket ekle
    if node_type in ['city', 'fire_station', 'air_base', 'crisis_center', 'lake']:
        text = plt.text(x, y-0.5, node_data['name'], ha='center', va='top', fontsize=8)
        text.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='white')])

# Ölçek çubuğu ekle
plt.plot([-28, -23], [-18, -18], 'k-', linewidth=2)
plt.text(-25.5, -18.5, '5 km', ha='center', fontsize=8)

# Yön oku ekle
arrow_x, arrow_y = -28, -16
plt.arrow(arrow_x, arrow_y, 0, 1, head_width=0.3, head_length=0.5, fc='k', ec='k')
plt.text(arrow_x, arrow_y+2, 'K', ha='center', fontsize=10, fontweight='bold')

# Lejant için öğeler
node_legend_elements = []
for node_type, style in list(node_types.items())[:10]:  # İlk 10 düğüm türü
    node_legend_elements.append(
        plt.Line2D([0], [0], marker=style['shape'], color='w', markerfacecolor=style['color'],
                  markersize=10, label=style['label'])
    )

edge_legend_elements = []
for edge_type, style in list(edge_types.items())[:6]:  # İlk 6 bağlantı türü
    edge_legend_elements.append(
        Line2D([0], [0], color=style['color'], linestyle=style['style'], 
              linewidth=style['width'], label=style['label'])
    )

risk_legend_elements = []
for risk_level, style in risk_levels.items():
    risk_legend_elements.append(
        mpatches.Patch(color=style['color'], alpha=style['alpha'], 
                      label=style['label'])
    )

# Lejantları ekle
plt.legend(handles=node_legend_elements, title="Düğüm Türleri", 
          loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
plt.legend(handles=edge_legend_elements, title="Bağlantı Türleri", 
          loc='upper left', bbox_to_anchor=(1.01, 0.7), borderaxespad=0)
plt.legend(handles=risk_legend_elements, title="Risk Seviyeleri", 
          loc='upper left', bbox_to_anchor=(1.01, 0.4), borderaxespad=0)

# Eksen sınırlarını ayarla
plt.xlim(-30, 30)
plt.ylim(-20, 15)

# Eksen etiketlerini kaldır
plt.xticks([])
plt.yticks([])

# Alt bilgi ekle
plt.figtext(0.5, 0.01, "Orman Yangını Risk Ağı - Bursa İli Örneği", 
           ha="center", fontsize=10, style='italic')

# Haritayı kaydet
plt.tight_layout()
plt.savefig('/home/ubuntu/orman_yangini_risk_agi/orman_yangini_risk_agi.png', dpi=300, bbox_inches='tight')
plt.savefig('/home/ubuntu/orman_yangini_risk_agi/orman_yangini_risk_agi.svg', format='svg', bbox_inches='tight')

print("Orman Yangını Risk Ağı haritası başarıyla oluşturuldu.")
