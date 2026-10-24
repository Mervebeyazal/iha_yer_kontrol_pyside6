"""Görevi uygulamaya özel, sürümlü JSON biçiminde kaydeder."""
import json
import os
import tempfile
import math
from dataclasses import asdict
from pathlib import Path
from modeller.rota_noktasi import RotaNoktasi


def gorevi_ac(dosya_yolu):
    # Henüz arayüzdeki listeye dokunmuyoruz: önce dosyanın tamamını okuyoruz.
    with open(dosya_yolu, encoding='utf-8') as dosya:
        veri = json.load(dosya)
    if not isinstance(veri, dict) or set(veri) != {'surum', 'rota_noktalari'}:
        raise ValueError('Görev dosyasının alanları geçersiz.')
    if type(veri['surum']) is not int or veri['surum'] != 1:
        raise ValueError('Bu görev dosyası sürümü desteklenmiyor.')
    if not isinstance(veri['rota_noktalari'], list):
        raise ValueError('Rota noktaları bir liste olmalı.')
    noktalar = []
    for sira, bilgi in enumerate(veri['rota_noktalari'], start=1):
        if not isinstance(bilgi, dict) or set(bilgi) != {'enlem', 'boylam', 'irtifa', 'komut'}:
            raise ValueError(f'{sira}. noktanın alanları geçersiz.')
        for alan, alt, ust in [('enlem', -90, 90), ('boylam', -180, 180), ('irtifa', 0, 1000)]:
            deger = bilgi[alan]
            # bool, Python'da int alt türüdür; burada sayı olarak kabul etmiyoruz.
            if type(deger) not in (int, float) or not math.isfinite(deger) or not alt <= deger <= ust:
                raise ValueError(f'{sira}. nokta: {alan} değeri geçersiz.')
        if bilgi['komut'] not in ('WAYPOINT', 'TAKEOFF', 'LAND'):
            raise ValueError(f'{sira}. noktanın komutu desteklenmiyor.')
        noktalar.append(RotaNoktasi(**bilgi))
    # Yalnızca bütün noktalar geçerliyse listeyi çağıran yere veriyoruz.
    return noktalar


def gorevi_kaydet(dosya_yolu, rota_noktalari):
    # Önce tüm veriyi metne çeviriyoruz; hatalı veri mevcut dosyayı bozmasın.
    veri = {
        'surum': 1,
        'rota_noktalari': [asdict(nokta) for nokta in rota_noktalari],
    }
    metin = json.dumps(veri, ensure_ascii=False, indent=4, allow_nan=False)
    hedef = Path(dosya_yolu)
    gecici_yol = None
    try:
        # Aynı klasörde geçici dosyaya yazıyoruz. Yazma tamamlanmadan
        # kullanıcının önceki görev dosyasına dokunmuyoruz.
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', dir=hedef.parent,
            prefix='.gorev-', suffix='.tmp', delete=False,
        ) as dosya:
            gecici_yol = Path(dosya.name)
            dosya.write(metin)
            dosya.flush()
            os.fsync(dosya.fileno())
        # Tamamlanan dosyayı hedefe atomik olarak taşıyoruz.
        os.replace(gecici_yol, hedef)
    finally:
        if gecici_yol is not None and gecici_yol.exists():
            gecici_yol.unlink()
