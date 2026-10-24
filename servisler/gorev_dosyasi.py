"""Görevi uygulamaya özel, sürümlü JSON biçiminde kaydeder."""
import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path


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
