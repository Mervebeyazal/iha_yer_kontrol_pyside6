import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from arayuz.ana_pencere import AnaPencere


class GorevTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        # Ana pencereyi de oluşturarak import/klasör yapısını kontrol ediyoruz.
        self.pencere = AnaPencere()
        self.sayfa = self.pencere.gorev_sayfasi

    def tearDown(self):
        self.pencere.close()
        self.pencere.deleteLater()
        self.app.processEvents()

    def ekle(self, enlem):
        self.sayfa.enlem_kutusu.setValue(enlem)
        self.sayfa.rota_noktasi_ekle()

    def secim_kapali(self):
        self.assertIsNone(self.sayfa.secili_nokta_indeksi)
        for dugme in (self.sayfa.nokta_guncelle_butonu,
                      self.sayfa.nokta_sil_butonu,
                      self.sayfa.yukari_butonu,
                      self.sayfa.asagi_butonu):
            self.assertFalse(dugme.isEnabled())

    def test_ekle_guncelle_sil(self):
        self.secim_kapali()
        self.ekle(41)
        self.ekle(42)
        self.sayfa.rota_tablosu.selectRow(0)
        self.sayfa.irtifa_kutusu.setValue(85)
        self.sayfa.secili_noktayi_guncelle()
        self.assertEqual(self.sayfa.rota_noktalari[0].irtifa, 85)
        self.assertEqual(len(self.sayfa.rota_noktalari), 2)
        self.sayfa.secili_noktayi_sil()
        self.assertEqual(self.sayfa.rota_noktalari[0].enlem, 42)
        self.assertEqual(self.sayfa.rota_tablosu.rowCount(), 1)
        self.secim_kapali()

    def test_tasima_ve_secim_temizleme(self):
        for enlem in (41, 42, 43):
            self.ekle(enlem)
        self.sayfa.rota_tablosu.selectRow(2)
        self.assertFalse(self.sayfa.asagi_butonu.isEnabled())
        self.sayfa.secili_noktayi_tasi(-1)
        self.assertEqual([p.enlem for p in self.sayfa.rota_noktalari], [41, 43, 42])
        self.assertEqual(self.sayfa.secili_nokta_indeksi, 1)
        self.assertEqual(self.sayfa.enlem_kutusu.value(), 43)
        self.ekle(44)
        self.secim_kapali()

    def test_sinir_ve_son_noktayi_silme(self):
        self.ekle(41)
        self.sayfa.rota_tablosu.selectRow(0)
        self.assertFalse(self.sayfa.yukari_butonu.isEnabled())
        self.assertFalse(self.sayfa.asagi_butonu.isEnabled())
        self.sayfa.secili_noktayi_tasi(-1)
        self.assertEqual(len(self.sayfa.rota_noktalari), 1)
        self.sayfa.secili_noktayi_sil()
        self.assertEqual(self.sayfa.rota_tablosu.rowCount(), 0)
        self.secim_kapali()

    def test_kaydet_iptal_ve_hata(self):
        self.ekle(41)
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as klasor:
            yol = Path(klasor) / 'görev.json'
            with patch('arayuz.gorev_sayfasi.QFileDialog.getSaveFileName', return_value=(str(yol), '')):
                self.sayfa.kaydet_butonu.click()
            veri = json.loads(yol.read_text(encoding='utf-8'))
            self.assertEqual(veri['surum'], 1)
            self.assertEqual(veri['rota_noktalari'][0]['enlem'], 41)
            with patch('arayuz.gorev_sayfasi.QFileDialog.getSaveFileName', return_value=('', '')), patch('arayuz.gorev_sayfasi.gorevi_kaydet') as kaydet:
                self.sayfa.gorevi_dosyaya_kaydet()
                kaydet.assert_not_called()
            with patch('arayuz.gorev_sayfasi.QFileDialog.getSaveFileName', return_value=(str(yol), '')), patch('arayuz.gorev_sayfasi.gorevi_kaydet', side_effect=OSError('Disk hatası')), patch('arayuz.gorev_sayfasi.QMessageBox.warning') as uyari:
                self.sayfa.gorevi_dosyaya_kaydet()
                uyari.assert_called_once()

    def test_yazma_hatasinda_eski_dosya_korunur(self):
        from servisler.gorev_dosyasi import gorevi_kaydet
        self.ekle(41)
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as klasor:
            yol = Path(klasor) / 'gorev.json'
            yol.write_text('önceki içerik', encoding='utf-8')
            with patch('servisler.gorev_dosyasi.os.replace', side_effect=OSError('Yazma hatası')):
                with self.assertRaises(OSError):
                    gorevi_kaydet(yol, self.sayfa.rota_noktalari)
            self.assertEqual(yol.read_text(encoding='utf-8'), 'önceki içerik')
            self.assertEqual(list(Path(klasor).iterdir()), [yol])


if __name__ == '__main__':
    unittest.main()
