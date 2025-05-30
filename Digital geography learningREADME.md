#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
from matplotlib.lines import Line2D

# Rastgele sayı üreteci için sabit değer ayarla (tekrarlanabilirlik için)
random.seed(42)
np.random.seed(42)

# Harita başlığı ve boyutu
plt.figure(figsize=(16, 12))
plt.title("Günün Dijital Coğrafi Öğrenme Ağı", fontsize=20, fontweight='bold')

# Ağ oluştur
G = nx.Graph()

# Düğüm türleri ve özellikleri
node_types = {
    'university': {'shape': 's', 'color': 'blue', 'size': 500, 'label': 'Üniversite'},
    'school': {'shape': 's', 'color': 'skyblue', 'size': 300, 'label': 'Okul'},
    'online_platform': {'shape': 'h', 'color': 'dodgerblue', 'size': 400, 'label': 'Çevrimiçi Platform'},
    'student': {'shape': 'o', 'color': 'green', 'size': 100, 'label': 'Öğrenci'},
    'teacher': {'shape': '^', 'color': 'forestgreen', 'size': 200, 'label': 'Öğretmen'},
    'researcher': {'shape': 'd', 'color': 'limegreen', 'size': 250, 'label': 'Araştırmacı'},
    'digital_library': {'shape': '*', 'color': 'purple', 'size': 350, 'label': 'Dijital Kütüphane'},
    'open_resource': {'shape': 'p', 'color': 'mediumpurple', 'size': 300, 'label': 'Açık Kaynak'},
    'research_center': {'shape': 's', 'color': 'darkviolet', 'size': 450, 'label': 'Araştırma Merkezi'},
    'internet_hub': {'shape': 'o', 'color': 'orange', 'size': 350, 'label': 'İnternet Erişim Merkezi'},
    'mobile_point': {'shape': '^', 'color': 'darkorange', 'size': 250, 'label': 'Mobil Öğrenme Noktası'}
}

# Coğrafi bölgeler (x, y koordinat aralıkları)
regions = {
    'europe': {'x': (-10, 10), 'y': (0, 10), 'label': 'Avrupa'},
    'north_america': {'x': (-30, -10), 'y': (0, 10), 'label': 'Kuzey Amerika'},
    'asia': {'x': (10, 30), 'y': (0, 10), 'label': 'Asya'},
    'africa': {'x': (-5, 15), 'y': (-10, 0), 'label': 'Afrika'},
    'south_america': {'x': (-30, -10), 'y': (-10, 0), 'label': 'Güney Amerika'},
    'oceania': {'x': (15, 30), 'y': (-10, 0), 'label': 'Okyanusya'},
    'virtual': {'x': (-5, 5), 'y': (-5, 5), 'label': 'Sanal Alan'}
}

# Bağlantı türleri
edge_types = {
    'info_flow': {'style': '-', 'color': 'blue', 'width': 1.5, 'label': 'Bilgi Akışı'},
    'communication': {'style': '--', 'color': 'green', 'width': 1.0, 'label': 'İletişim'},
    'collaboration': {'style': ':', 'color': 'purple', 'width': 2.0, 'label': 'İşbirliği'},
    'data_sharing': {'style': '-.', 'color': 'orange', 'width': 1.2, 'label': 'Veri Paylaşımı'}
}

# Düğümleri oluştur
nodes = {
    # Eğitim Kurumları
    'uni1': {'type': 'university', 'region': 'europe', 'name': 'Avrupa Üniversitesi'},
    'uni2': {'type': 'university', 'region': 'north_america', 'name': 'Kuzey Amerika Üniversitesi'},
    'uni3': {'type': 'university', 'region': 'asia', 'name': 'Asya Üniversitesi'},
    'school1': {'type': 'school', 'region': 'europe', 'name': 'Avrupa Okulu'},
    'school2': {'type': 'school', 'region': 'north_america', 'name': 'Kuzey Amerika Okulu'},
    'school3': {'type': 'school', 'region': 'asia', 'name': 'Asya Okulu'},
    'school4': {'type': 'school', 'region': 'africa', 'name': 'Afrika Okulu'},
    'online1': {'type': 'online_platform', 'region': 'virtual', 'name': 'Global Öğrenme Platformu'},
    'online2': {'type': 'online_platform', 'region': 'virtual', 'name': 'Dil Öğrenme Platformu'},
    
    # Kullanıcılar
    'student1': {'type': 'student', 'region': 'europe', 'name': 'Avrupa Öğrencisi'},
    'student2': {'type': 'student', 'region': 'north_america', 'name': 'Kuzey Amerika Öğrencisi'},
    'student3': {'type': 'student', 'region': 'asia', 'name': 'Asya Öğrencisi'},
    'student4': {'type': 'student', 'region': 'africa', 'name': 'Afrika Öğrencisi'},
    'student5': {'type': 'student', 'region': 'south_america', 'name': 'Güney Amerika Öğrencisi'},
    'student6': {'type': 'student', 'region': 'oceania', 'name': 'Okyanusya Öğrencisi'},
    'teacher1': {'type': 'teacher', 'region': 'europe', 'name': 'Avrupa Öğretmeni'},
    'teacher2': {'type': 'teacher', 'region': 'north_america', 'name': 'Kuzey Amerika Öğretmeni'},
    'teacher3': {'type': 'teacher', 'region': 'asia', 'name': 'Asya Öğretmeni'},
    'researcher1': {'type': 'researcher', 'region': 'europe', 'name': 'Avrupa Araştırmacısı'},
    'researcher2': {'type': 'researcher', 'region': 'north_america', 'name': 'Kuzey Amerika Araştırmacısı'},
    
    # Kaynaklar
    'library1': {'type': 'digital_library', 'region': 'europe', 'name': 'Avrupa Dijital Kütüphanesi'},
    'library2': {'type': 'digital_library', 'region': 'north_america', 'name': 'Kuzey Amerika Dijital Kütüphanesi'},
    'library3': {'type': 'digital_library', 'region': 'asia', 'name': 'Asya Dijital Kütüphanesi'},
    'open1': {'type': 'open_resource', 'region': 'virtual', 'name': 'Açık Eğitim Kaynağı 1'},
    'open2': {'type': 'open_resource', 'region': 'virtual', 'name': 'Açık Eğitim Kaynağı 2'},
    'research1': {'type': 'research_center', 'region': 'europe', 'name': 'Avrupa Araştırma Merkezi'},
    'research2': {'type': 'research_center', 'region': 'north_america', 'name': 'Kuzey Amerika Araştırma Merkezi'},
    
    # Erişim Noktaları
    'hub1': {'type': 'internet_hub', 'region': 'europe', 'name': 'Avrupa İnternet Merkezi'},
    'hub2': {'type': 'internet_hub', 'region': 'africa', 'name': 'Afrika İnternet Merkezi'},
    'mobile1': {'type': 'mobile_point', 'region': 'africa', 'name': 'Afrika Mobil Öğrenme Noktası'},
    'mobile2': {'type': 'mobile_point', 'region': 'south_america', 'name': 'Güney Amerika Mobil Öğrenme Noktası'}
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
    # Bilgi Akışı Bağlantıları
    ('uni1', 'student1', 'info_flow'),
    ('uni2', 'student2', 'info_flow'),
    ('uni3', 'student3', 'info_flow'),
    ('school1', 'student1', 'info_flow'),
    ('school2', 'student2', 'info_flow'),
    ('school3', 'student3', 'info_flow'),
    ('school4', 'student4', 'info_flow'),
    ('online1', 'student1', 'info_flow'),
    ('online1', 'student2', 'info_flow'),
    ('online1', 'student3', 'info_flow'),
    ('online1', 'student4', 'info_flow'),
    ('online1', 'student5', 'info_flow'),
    ('online1', 'student6', 'info_flow'),
    ('online2', 'student1', 'info_flow'),
    ('online2', 'student3', 'info_flow'),
    ('online2', 'student5', 'info_flow'),
    ('library1', 'student1', 'info_flow'),
    ('library2', 'student2', 'info_flow'),
    ('library3', 'student3', 'info_flow'),
    ('open1', 'student1', 'info_flow'),
    ('open1', 'student2', 'info_flow'),
    ('open1', 'student3', 'info_flow'),
    ('open1', 'student4', 'info_flow'),
    ('open2', 'student5', 'info_flow'),
    ('open2', 'student6', 'info_flow'),
    
    # İletişim Bağlantıları
    ('teacher1', 'student1', 'communication'),
    ('teacher2', 'student2', 'communication'),
    ('teacher3', 'student3', 'communication'),
    ('teacher1', 'teacher2', 'communication'),
    ('teacher2', 'teacher3', 'communication'),
    ('teacher3', 'teacher1', 'communication'),
    ('online1', 'teacher1', 'communication'),
    ('online1', 'teacher2', 'communication'),
    ('online1', 'teacher3', 'communication'),
    
    # İşbirliği Bağlantıları
    ('researcher1', 'researcher2', 'collaboration'),
    ('researcher1', 'uni1', 'collaboration'),
    ('researcher2', 'uni2', 'collaboration'),
    ('research1', 'uni1', 'collaboration'),
    ('research2', 'uni2', 'collaboration'),
    ('research1', 'research2', 'collaboration'),
    ('uni1', 'uni2', 'collaboration'),
    ('uni2', 'uni3', 'collaboration'),
    ('uni3', 'uni1', 'collaboration'),
    
    # Veri Paylaşım Bağlantıları
    ('library1', 'library2', 'data_sharing'),
    ('library2', 'library3', 'data_sharing'),
    ('library3', 'library1', 'data_sharing'),
    ('open1', 'open2', 'data_sharing'),
    ('library1', 'open1', 'data_sharing'),
    ('library2', 'open1', 'data_sharing'),
    ('library3', 'open2', 'data_sharing'),
    ('hub1', 'online1', 'data_sharing'),
    ('hub1', 'online2', 'data_sharing'),
    ('hub2', 'online1', 'data_sharing'),
    ('mobile1', 'student4', 'data_sharing'),
    ('mobile2', 'student5', 'data_sharing'),
    ('hub2', 'mobile1', 'data_sharing'),
    ('hub1', 'uni1', 'data_sharing'),
    ('hub1', 'school1', 'data_sharing'),
]

# Bağlantıları grafa ekle
for source, target, edge_type in connections:
    G.add_edge(source, target, type=edge_type)

# Coğrafi bölgeleri çiz
for region_id, region_data in regions.items():
    x_min, x_max = region_data['x']
    y_min, y_max = region_data['y']
    width = x_max - x_min
    height = y_max - y_min
    
    # Sanal alan için farklı stil
    if region_id == 'virtual':
        circle = plt.Circle((0, 0), 5, fill=True, alpha=0.1, color='lightgray', linestyle='--')
        plt.gca().add_patch(circle)
        plt.text(0, 5.5, region_data['label'], ha='center', fontsize=12, fontweight='bold')
    else:
        rect = plt.Rectangle((x_min, y_min), width, height, fill=True, alpha=0.1, 
                            color=plt.cm.tab10(list(regions.keys()).index(region_id) % 10))
        plt.gca().add_patch(rect)
        plt.text(x_min + width/2, y_max + 0.5, region_data['label'], ha='center', fontsize=12, fontweight='bold')

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
        control_y = (y1 + y2) / 2 + np.sign(y2 - y1) * 5
        
        # Bezier eğrisi için noktalar
        t = np.linspace(0, 1, 100)
        x = (1-t)**2 * x1 + 2*(1-t)*t * control_x + t**2 * x2
        y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2
        
        plt.plot(x, y, linestyle=edge_style['style'], color=edge_style['color'], 
                linewidth=edge_style['width'], alpha=0.7)
        
        # Ok başı ekle (bilgi akışı için)
        if edge_type == 'info_flow':
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
        
        # Ok başı ekle (bilgi akışı için)
        if edge_type == 'info_flow':
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
    
    # Düğüm çiz
    plt.scatter(x, y, s=node_style['size'], c=node_style['color'], 
               marker=node_style['shape'], edgecolors='black', linewidths=1, alpha=0.9)
    
    # Önemli düğümler için etiket ekle
    if node_type in ['university', 'research_center', 'online_platform']:
        plt.text(x, y-0.5, node_data['name'], ha='center', va='top', fontsize=8)

# Lejant için öğeler
node_legend_elements = []
for node_type, style in node_types.items():
    node_legend_elements.append(
        plt.Line2D([0], [0], marker=style['shape'], color='w', markerfacecolor=style['color'],
                  markersize=10, label=style['label'])
    )

edge_legend_elements = []
for edge_type, style in edge_types.items():
    edge_legend_elements.append(
        Line2D([0], [0], color=style['color'], linestyle=style['style'], 
              linewidth=style['width'], label=style['label'])
    )

# Lejantları ekle
plt.legend(handles=node_legend_elements, title="Düğüm Türleri", 
          loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
plt.legend(handles=edge_legend_elements, title="Bağlantı Türleri", 
          loc='upper left', bbox_to_anchor=(1.01, 0.6), borderaxespad=0)

# Eksen sınırlarını ayarla
plt.xlim(-35, 35)
plt.ylim(-15, 15)

# Eksen etiketlerini kaldır
plt.xticks([])
plt.yticks([])

# Alt bilgi ekle
plt.figtext(0.5, 0.01, "Dijital Coğrafi Öğrenme Ağı - Küresel Eğitim Bağlantıları", 
           ha="center", fontsize=10, style='italic')

# Haritayı kaydet
plt.tight_layout()
plt.savefig('/home/ubuntu/dijital_cografi_harita/dijital_cografi_ogrenme_agi.png', dpi=300, bbox_inches='tight')
plt.savefig('/home/ubuntu/dijital_cografi_harita/dijital_cografi_ogrenme_agi.svg', format='svg', bbox_inches='tight')

print("Dijital Coğrafi Öğrenme Ağı haritası başarıyla oluşturuldu.")
