Bördübet (Manavgat) Yakıt Yükü haritası

// 1. BÖLGE TANIMI (Manavgat-Bördübet)
var geometry = ee.Geometry.Rectangle([[30.90, 36.70], [31.50, 36.95]]);

// 2. SENTINEL-2 VERİLERİ
var sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR')
  .filterDate('2023-08-01', '2023-08-31')
  .filterBounds(geometry)
  .median()
  .clip(geometry);

// 3. NDVI ve NBR HESAPLA
var ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI');
var nbr = sentinel2.normalizedDifference(['B8', 'B12']).rename('NBR');
var fuelLoad = ndvi.multiply(nbr).rename('Fuel_Load');

// 4. YAKIT YÜKÜ SINIFLARINI %'YE GÖRE TANIMLA (DÜZELTİLDİ)
var percentiles = fuelLoad.reduceRegion({
  reducer: ee.Reducer.percentile([20, 50, 80]),
  geometry: geometry,
  scale: 10,
  maxPixels: 1e13
});

var p20 = ee.Number(percentiles.get('Fuel_Load_p20'));
var p50 = ee.Number(percentiles.get('Fuel_Load_p50'));
var p80 = ee.Number(percentiles.get('Fuel_Load_p80'));

// SINIFLANDIRMA (Parantez hatası düzeltildi)
var fuelClass = fuelLoad
  .where(fuelLoad.lt(p20), 1)     // Düşük (%20 altı)
  .where(fuelLoad.gte(p20).and(fuelLoad.lt(p50)), 2)  // Orta (%20-50)
  .where(fuelLoad.gte(p50).and(fuelLoad.lt(p80)), 3)  // Yüksek (%50-80)
  .where(fuelLoad.gte(p80), 4);                       // Çok Yüksek (%80 üstü)

// 5. ALAN HESAPLAMA (HA) (DÜZELTİLDİ)
var areaStats = fuelClass.reduceRegion({
  reducer: ee.Reducer.frequencyHistogram(),
  geometry: geometry,
  scale: 10,
  maxPixels: 1e13
});

var areas = ee.Dictionary(areaStats.get('Fuel_Load'));
var totalAreaHa = geometry.area().divide(1e4); // Toplam alan hektar

// Konsola yazdır
print('Sınıf Alanları (HA):', areas.map(function(key, val) {
  return ee.Number(val).divide(100); // Piksel başına 100m² → HA'ya çevir
}));
print('Toplam Alan (HA):', totalAreaHa);

// 6. GÖRSELLEŞTİRME
Map.centerObject(geometry, 10);
Map.addLayer(fuelClass, {
  min: 1,
  max: 4,
  palette: ['green', 'yellow', 'orange', 'red']
}, 'Yakıt Yükü (%)');

// 7. LEJAND VE YÖN OKU (DÜZELTİLDİ)
var legend = ui.Panel({
  style: {
    position: 'bottom-right',
    padding: '10px',
    backgroundColor: 'white',
    border: '2px solid black'
  }
});

// Lejand başlık
legend.add(ui.Label('Yakıt Yükü Sınıfları', {fontWeight: 'bold', fontSize: '14px'}));

// Lejand öğeleri
var labels = ['Düşük (<%20)', 'Orta (%20-50)', 'Yüksek (%50-80)', 'Çok Yüksek (>%80)'];
var colors = ['green', 'yellow', 'orange', 'red'];

labels.forEach(function(label, i) {
  var colorBox = ui.Label({
    value: '■',
    style: {color: colors[i], fontSize: '24px', margin: '0 8px'}
  });
  var text = ui.Label(label);
  legend.add(ui.Panel([colorBox, text], 'flow'));
});

// Yön oku
var northArrow = ui.Label({
  value: '▲ N',
  style: {
    position: 'top-left',
    fontSize: '24px',
    fontWeight: 'bold',
    color: 'black',
    margin: '8px'
  }
});
