# İHA Yer Kontrol — PySide6

Sabit kanat İHA için adım adım geliştirilen masaüstü görev planlama uygulaması.

## Kurulum ve çalıştırma

Python 3.10 veya üzeri gerekir. Terminalde proje klasöründeyken:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python main.py
```

## Modüller

- `main.py`: uygulamanın başlangıcı.
- `arayuz/ana_pencere.py`: menü, bağlantı şeridi ve durum çubuğu.
- `arayuz/gorev_sayfasi.py`: nokta formu, tablo ve görev düzenleme.
- `modeller/rota_noktasi.py`: rota noktası veri modeli.
- `servisler/gorev_dosyasi.py`: sürümlü JSON görev kaydı.
- `tests/`: görev düzenleme kontrolleri.

## Mevcut özellikler

Nokta ekleme, fare/klavye ile seçme, güncelleme, silme ve sıralama.
Seçim olmadığında güncelleme, silme ve taşıma düğmeleri kapanır.

“Görevi kaydet” düğmesi listeye uygulanmış noktaları JSON dosyasına yazar.
Dosya yazımı başarısızsa önceki dosya korunur. Bu biçim uygulamaya özeldir;
Mission Planner dosyası değildir. Formdaki uygulanmamış değişiklikler kaydedilmez.
“Görev aç” dosyanın sürümünü, alanlarını, koordinatlarını, komutlarını ve
formun desteklediği irtifa aralığını doğrular. Hatalı dosyada mevcut rota korunur.
Mevcut rota varsa değiştirmeden önce onay istenir. Bilinmeyen alanlar sessizce
atılmaz; dosya reddedilir. Boş görev dosyaları desteklenir.

Harita henüz yer tutucudur. Gerçek uçak bağlantısı ve görev aktarımı
eklenmemiştir. Kaydedilmeyen noktalar uygulama kapanınca kaybolur.
İrtifa aralığı yalnızca form sınırıdır; yarışma veya güvenli uçuş sınırı değildir.

## Kontroller

```powershell
.venv\Scripts\python -m unittest discover -v
```

Testler ekran açmadan Qt üzerinden görev düzenleme akışını kontrol eder.

## GitHub ile çalışma

Her tamamlanan ve kontrol edilen küçük adım ayrı commit olmalı.
Başlamadan önce `git status` ile yerel değişiklikleri kontrol edin. Çalışma
alanı temizken `git pull --ff-only` ile güncellemeleri alın. Yerel değişiklikler
varsa önce inceleyin ve kaydedin; üzerine yazmayın.

`__pycache__`, `.pyc` ve `.venv` dosyaları repoya eklenmez.
