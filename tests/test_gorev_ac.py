import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox
from arayuz.gorev_sayfasi import GorevSayfasi
from modeller.rota_noktasi import RotaNoktasi
from servisler.gorev_dosyasi import gorevi_ac, gorevi_kaydet


class GorevAcTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.gecici = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.yol = Path(self.gecici.name) / 'gorev.json'
        self.sayfa = GorevSayfasi()

    def tearDown(self):
        self.sayfa.deleteLater()
        self.app.processEvents()
        self.gecici.cleanup()

    def test_kaydet_ac_ve_bos_gorev(self):
        noktalar = [RotaNoktasi(41, 29, 50, 'WAYPOINT'), RotaNoktasi(42, 30, 60, 'LAND')]
        gorevi_kaydet(self.yol, noktalar)
        self.assertEqual(gorevi_ac(self.yol), noktalar)
        gorevi_kaydet(self.yol, [])
        self.assertEqual(gorevi_ac(self.yol), [])

    def test_hatali_alanlar(self):
        for alan, deger in [('enlem', 91), ('boylam', -181), ('irtifa', 1001),
                            ('enlem', True), ('irtifa', float('nan')), ('enlem', '41'),
                            ('komut', 'UNKNOWN')]:
            with self.subTest(alan=alan, deger=deger):
                bilgi = dict(enlem=41, boylam=29, irtifa=50, komut='WAYPOINT')
                bilgi[alan] = deger
                self.yol.write_text(json.dumps({'surum': 1, 'rota_noktalari': [bilgi]}))
                with self.assertRaises(ValueError):
                    gorevi_ac(self.yol)
        for veri in [{'surum': 2, 'rota_noktalari': []}, [], {'surum': 1, 'rota_noktalari': 'yanlis'}]:
            self.yol.write_text(json.dumps(veri))
            with self.assertRaises(ValueError):
                gorevi_ac(self.yol)

    def test_arayuz_onay_ret_ve_kabul(self):
        self.sayfa.rota_noktasi_ekle()
        eski = self.sayfa.rota_noktalari.copy()
        yeni = [RotaNoktasi(41, 29, 50, 'TAKEOFF')]
        gorevi_kaydet(self.yol, yeni)
        with patch('arayuz.gorev_sayfasi.QFileDialog.getOpenFileName', return_value=(str(self.yol), '')):
            with patch('arayuz.gorev_sayfasi.QMessageBox.question', return_value=QMessageBox.StandardButton.No):
                self.sayfa.gorevi_dosyadan_ac()
                self.assertEqual(self.sayfa.rota_noktalari, eski)
            with patch('arayuz.gorev_sayfasi.QMessageBox.question', return_value=QMessageBox.StandardButton.Yes):
                self.sayfa.ac_butonu.click()
                self.assertEqual(self.sayfa.rota_noktalari, yeni)
                self.assertEqual(self.sayfa.rota_tablosu.rowCount(), 1)
                self.assertIsNone(self.sayfa.secili_nokta_indeksi)

    def test_bozuk_dosya_ve_iptal_rotayi_korur(self):
        self.sayfa.rota_noktasi_ekle()
        eski = self.sayfa.rota_noktalari.copy()
        self.yol.write_text('{bozuk')
        with patch('arayuz.gorev_sayfasi.QFileDialog.getOpenFileName', return_value=(str(self.yol), '')), patch('arayuz.gorev_sayfasi.QMessageBox.warning') as uyari:
            self.sayfa.gorevi_dosyadan_ac()
            uyari.assert_called_once()
        self.assertEqual(self.sayfa.rota_noktalari, eski)
        with patch('arayuz.gorev_sayfasi.QFileDialog.getOpenFileName', return_value=('', '')), patch('arayuz.gorev_sayfasi.gorevi_ac') as ac:
            self.sayfa.gorevi_dosyadan_ac()
            ac.assert_not_called()
