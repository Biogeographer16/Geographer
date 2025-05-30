# Orman Yangınları Risk Ağı Harita Yapısı Tasarımı

## Düğüm (Node) Türleri ve Görsel Temsilleri

1. **Risk Faktörleri**
   - Sıcaklık: Kırmızı daireler (büyüklük sıcaklık şiddetini gösterir)
   - Nem: Mavi daireler (büyüklük nem seviyesinin tersini gösterir)
   - Rüzgar: Gri üçgenler (büyüklük rüzgar hızını gösterir)
   - Bitki Örtüsü: Yeşil kareler (koyu yeşil yüksek yanıcı bitki örtüsünü gösterir)
   - Topografya: Kahverengi elmaslar (büyüklük eğim derecesini gösterir)

2. **İzleme İstasyonları**
   - Meteoroloji İstasyonları: Mavi yıldızlar
   - Uydu İzleme Noktaları: Mavi altıgenler
   - Kamera Sistemleri: Mavi üçgenler
   - Sensör Ağları: Mavi küçük daireler

3. **Müdahale Birimleri**
   - İtfaiye İstasyonları: Turuncu kareler
   - Orman Yangın Ekipleri: Turuncu üçgenler
   - Hava Araçları Üsleri: Turuncu elmaslar
   - Acil Durum Merkezleri: Turuncu yıldızlar

4. **Yerleşim Yerleri**
   - Köyler: Siyah küçük daireler
   - Şehirler: Siyah büyük daireler
   - Kritik Tesisler: Siyah kareler

5. **Karar Verme Merkezleri**
   - Yönetim Birimleri: Mor kareler
   - Kriz Merkezleri: Mor yıldızlar
   - Koordinasyon Merkezleri: Mor üçgenler

6. **Su Kaynakları**
   - Göller/Barajlar: Açık mavi daireler
   - Yangın Havuzları: Açık mavi kareler
   - Nehirler: Açık mavi çizgiler

## Bağlantı Türleri ve Stilleri

1. **Veri Akışı**
   - Sensörlerden İzleme Merkezlerine: İnce mavi oklu çizgiler
   - İzleme Merkezlerinden Karar Merkezlerine: Kalın mavi oklu çizgiler
   - Yoğunluk: Çizgi kalınlığı ile temsil edilir

2. **Uyarı Sinyalleri**
   - Acil Uyarılar: Kalın kırmızı kesikli oklu çizgiler
   - Rutin Uyarılar: İnce turuncu kesikli oklu çizgiler

3. **Müdahale Rotaları**
   - Kara Yolu Müdahalesi: Kalın turuncu düz çizgiler
   - Hava Yolu Müdahalesi: Kalın turuncu noktalı çizgiler
   - Alternatif Rotalar: İnce turuncu kesikli çizgiler

4. **Risk Etki İlişkileri**
   - Yüksek Etki: Kalın kırmızı çizgiler
   - Orta Etki: Orta kalınlıkta turuncu çizgiler
   - Düşük Etki: İnce sarı çizgiler

5. **Koordinasyon Hatları**
   - Birimler Arası İletişim: Mor noktalı çizgiler
   - Hiyerarşik İletişim: Mor düz çizgiler

## Risk Seviyeleri ve Coğrafi Katmanlar

1. **Risk Seviyeleri**
   - Düşük Risk: Yeşil tonlu alanlar (şeffaflık: %30)
   - Orta Risk: Sarı tonlu alanlar (şeffaflık: %40)
   - Yüksek Risk: Turuncu tonlu alanlar (şeffaflık: %50)
   - Kritik Risk: Kırmızı tonlu alanlar (şeffaflık: %60)

2. **Coğrafi Katmanlar**
   - Topografya: Kabartma gösterimi (gri tonlarda)
   - Orman Alanları: Yeşil tonlu alanlar
   - Su Kaynakları: Mavi tonlu alanlar
   - İdari Sınırlar: Siyah kesikli çizgiler (il sınırları kalın, ilçe sınırları ince)

3. **Bursa Özelinde Katmanlar**
   - Bursa İl Sınırı: Kalın siyah kesikli çizgi
   - İlçe Sınırları: İnce siyah kesikli çizgiler
   - Orman Köyleri: Siyah küçük daireler (risk bölgelerinde olanlar daha belirgin)
   - Yangına Duyarlı Orman Alanları: Koyu yeşil tonlu alanlar

## Renk Şeması ve Kodlama

1. **Risk Renk Skalası**
   - Düşük Risk: Yeşil (#8BC34A)
   - Orta Risk: Sarı (#FFEB3B)
   - Yüksek Risk: Turuncu (#FF9800)
   - Kritik Risk: Kırmızı (#F44336)

2. **Düğüm Renkleri**
   - Risk Faktörleri: Kırmızı, Mavi, Gri, Yeşil, Kahverengi
   - İzleme İstasyonları: Mavi tonları
   - Müdahale Birimleri: Turuncu tonları
   - Yerleşim Yerleri: Siyah
   - Karar Verme Merkezleri: Mor tonları
   - Su Kaynakları: Açık mavi tonları

3. **Bağlantı Renkleri**
   - Veri Akışı: Mavi
   - Uyarı Sinyalleri: Kırmızı, Turuncu
   - Müdahale Rotaları: Turuncu
   - Risk Etki İlişkileri: Kırmızı, Turuncu, Sarı
   - Koordinasyon Hatları: Mor

## Dinamik Özellikler

1. **Zamansal Değişim**
   - Mevsimsel Risk Değişimi: Renk yoğunluğu değişimi
   - Günlük Risk Değişimi: Düğüm boyutu değişimi

2. **Aktivite Göstergeleri**
   - Aktif İzleme: Yanıp sönen düğümler
   - Devam Eden Müdahale: Kalın, parlak çizgiler
   - Yükselen Risk: Kademeli renk değişimi

3. **Ağ Dinamikleri**
   - Kritik Yollar: Kalın, parlak çizgiler
   - Yeni Uyarılar: Yanıp sönen bağlantılar
   - Müdahale Öncelikleri: Düğüm parlaklığı ile temsil

## Kartografik Özellikler

1. **Harita Bileşenleri**
   - Başlık: "Çalışma Alanı Orman Yangını Risk Bölgeleri"
   - Ölçek Çubuğu: Sağ alt köşede
   - Yön Oku: Sol alt köşede (lejanttan uzak)
   - Lejant: Sağ kenar boyunca

2. **Görsel Hiyerarşi**
   - Risk Bölgeleri: Arka planda
   - Coğrafi Özellikler: Orta katmanda
   - Düğümler ve Bağlantılar: Ön planda

Bu tasarım, orman yangınları risk ağını temsil eden bir harita oluşturmak için kullanılacaktır. Harita, Python ve uygun görselleştirme kütüphaneleri kullanılarak oluşturulacaktır.
