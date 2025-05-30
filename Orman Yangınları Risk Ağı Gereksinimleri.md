# Orman Yangınları Risk Ağı Gereksinimleri

Orman yangınları risk ağı, yangın riskini etkileyen faktörleri, erken uyarı sistemlerini, müdahale birimlerini ve bunlar arasındaki ilişkileri temsil eden bir yapıdır. Bu harita için temel gereksinimler:

## Temel Bileşenler
1. **Düğümler (Nodes)**: 
   - Risk Faktörleri (sıcaklık, nem, rüzgar, bitki örtüsü, topografya)
   - İzleme İstasyonları (meteoroloji, uydu, kamera sistemleri)
   - Müdahale Birimleri (itfaiye, orman yangın ekipleri, hava araçları)
   - Yerleşim Yerleri (köyler, şehirler, kritik tesisler)
   - Karar Verme Merkezleri (yönetim birimleri, kriz merkezleri)
   - Su Kaynakları (göller, barajlar, yangın havuzları)

2. **Bağlantılar (Connections)**:
   - Veri Akışı (sensörlerden izleme merkezlerine)
   - Uyarı Sinyalleri (izleme merkezlerinden müdahale birimlerine)
   - Müdahale Rotaları (birimlerden yangın bölgelerine)
   - Risk Etki İlişkileri (faktörlerden risk seviyelerine)
   - Koordinasyon Hatları (birimler arası iletişim)

3. **Risk Seviyeleri**:
   - Düşük Risk Bölgeleri
   - Orta Risk Bölgeleri
   - Yüksek Risk Bölgeleri
   - Kritik Risk Bölgeleri

## Görsel Gereksinimler
1. **Renk Kodlaması**:
   - Risk seviyeleri için kademeli renk skalası (yeşil-sarı-turuncu-kırmızı)
   - Düğüm türleri için farklı renkler
   - Bağlantı türleri için farklı çizgi stilleri
   - Aktivite yoğunluğunu gösteren renk tonları

2. **Simgeler ve Semboller**:
   - Risk faktörleri için tanımlayıcı simgeler
   - İzleme istasyonları için özel semboller
   - Müdahale birimleri için ayırt edici işaretler
   - Su kaynakları için mavi semboller

3. **Coğrafi Özellikler**:
   - Topografya ve kabartma gösterimi
   - Orman alanlarının belirgin gösterimi
   - İdari sınırların (il/ilçe) belirgin gösterimi
   - Ölçek çubuğu ve yön oku

## Fonksiyonel Gereksinimler
1. **Ağ Yapısı**:
   - Merkezi ve dağıtık izleme sistemleri
   - Hiyerarşik müdahale organizasyonu
   - Çok katmanlı risk değerlendirme sistemi

2. **Dinamik Özellikler**:
   - Zamanla değişen risk seviyeleri
   - Mevsimsel faktörlerin etkisi
   - Müdahale kapasitesinin değişimi
   - Gerçek zamanlı veri akışı

3. **Bursa Özelinde Gereksinimler**:
   - Bursa orman köylerinin belirgin gösterimi
   - Yangına duyarlı bölgelerin vurgulanması
   - İl ve ilçe idari sınırlarının belirgin gösterimi
   - Coğrafi harita formatında (kroki değil) gösterim

Bu gereksinimler doğrultusunda, orman yangınları risk ağını temsil eden görsel bir harita oluşturulacaktır.
