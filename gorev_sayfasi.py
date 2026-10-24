from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QFormLayout,
    QDoubleSpinBox,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
)

# Verileri tutan sınıfımız; arayüz kodundan ayrı.
from modeller.rota_noktasi import RotaNoktasi


class GorevSayfasi(QWidget):
    def __init__(self):
        super().__init__()

        # Noktaların asıl veri kaynağı bu listedir.
        self.rota_noktalari = []

        # None: Henüz hiçbir nokta seçilmedi.
        self.secili_nokta_indeksi = None

        # Solda çalışma alanı, sağda veri giriş paneli.
        ana_duzen = QHBoxLayout(self)
        ana_duzen.setContentsMargins(0, 0, 0, 0)
        ana_duzen.setSpacing(12)

        calisma_alani = self.calisma_alani_olustur()
        sag_panel = self.sag_panel_olustur()

        # Pencere genişlediğinde ek alanı çalışma alanı alır.
        ana_duzen.addWidget(calisma_alani, stretch=1)
        ana_duzen.addWidget(sag_panel)

    def calisma_alani_olustur(self):
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        duzen = QVBoxLayout(panel)
        duzen.addWidget(QLabel("GÖREV / ROTA PLANLAMA"))

        # Gerçek harita eklenene kadar geçici yer tutucu.
        self.harita_yer_tutucu = QLabel(
            "Harita ve rota alanı\n\n"
            "Rota noktaları burada gösterilecek."
        )
        self.harita_yer_tutucu.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        duzen.addWidget(self.harita_yer_tutucu, stretch=1)
        duzen.addWidget(QLabel("ROTA NOKTALARI"))

        # Başlangıçta sıfır satır ve beş sütun var.
        self.rota_tablosu = QTableWidget(0, 5)
        self.rota_tablosu.setHorizontalHeaderLabels([
            "No",
            "Komut",
            "Enlem (°)",
            "Boylam (°)",
            "İrtifa (m)",
        ])

        # Numaraları kendi sütunumuzda gösteriyoruz.
        self.rota_tablosu.verticalHeader().setVisible(False)

        # Hücre yerine satır seçilsin.
        self.rota_tablosu.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Aynı anda yalnızca bir nokta seçilebilsin.
        self.rota_tablosu.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        # Değişiklikler sağdaki formdan yapılacak.
        self.rota_tablosu.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Sütunlar mevcut genişliği paylaşsın.
        self.rota_tablosu.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Değiştirebilirsin: tablonun yüksekliği.
        self.rota_tablosu.setFixedHeight(220)

        # Seçim değişince formu güncelliyoruz.
        # Bu sinyal fareyle ve klavyeyle yapılan seçimleri kapsar.
        self.rota_tablosu.itemSelectionChanged.connect(
            self.rota_noktasi_sec
        )

        duzen.addWidget(self.rota_tablosu)

        return panel

    def sag_panel_olustur(self):
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        # Değiştirebilirsin: sağ panelin genişliği.
        panel.setFixedWidth(300)

        duzen = QVBoxLayout(panel)
        duzen.setSpacing(12)
        duzen.addWidget(QLabel("ROTA NOKTASI BİLGİLERİ"))

        # Solda alan adları, sağda giriş kutuları.
        form = QFormLayout()
        form.setSpacing(10)

        # İlk metin ekranda görünür; ikinci metin veride saklanır.
        self.komut_kutusu = QComboBox()
        self.komut_kutusu.addItem("Rota noktası", "WAYPOINT")
        self.komut_kutusu.addItem("Kalkış", "TAKEOFF")
        self.komut_kutusu.addItem("İniş", "LAND")
        form.addRow("Komut:", self.komut_kutusu)

        self.enlem_kutusu = QDoubleSpinBox()
        self.enlem_kutusu.setDecimals(7)
        self.enlem_kutusu.setRange(-90.0, 90.0)
        self.enlem_kutusu.setSingleStep(0.00001)
        self.enlem_kutusu.setSuffix(" °")
        form.addRow("Enlem:", self.enlem_kutusu)

        self.boylam_kutusu = QDoubleSpinBox()
        self.boylam_kutusu.setDecimals(7)
        self.boylam_kutusu.setRange(-180.0, 180.0)
        self.boylam_kutusu.setSingleStep(0.00001)
        self.boylam_kutusu.setSuffix(" °")
        form.addRow("Boylam:", self.boylam_kutusu)

        self.irtifa_kutusu = QDoubleSpinBox()
        self.irtifa_kutusu.setDecimals(1)

        # Bu aralık yalnızca prototipin veri giriş sınırıdır.
        self.irtifa_kutusu.setRange(0.0, 1000.0)

        # Değiştirebilirsin: artış miktarı ve başlangıç değeri.
        self.irtifa_kutusu.setSingleStep(5.0)
        self.irtifa_kutusu.setValue(50.0)
        self.irtifa_kutusu.setSuffix(" m")
        form.addRow("İrtifa:", self.irtifa_kutusu)

        referans = QLabel(
            "HOME konumuna göre\n"
            "(HOME henüz ayarlanmadı)"
        )
        referans.setWordWrap(True)
        form.addRow("Referans:", referans)

        duzen.addLayout(form)

        # Önce düğmeleri oluşturuyoruz.
        self.nokta_ekle_butonu = QPushButton(
            "Rotaya nokta ekle"
        )
        self.nokta_guncelle_butonu = QPushButton(
            "Seçili noktayı güncelle"
        )
        self.nokta_sil_butonu = QPushButton(
            "Seçili noktayı sil"
        )

        # Düğmeleri ancak oluşturduktan sonra kullanabiliriz.
        # Başlangıçta seçili nokta bulunmuyor.
        self.nokta_guncelle_butonu.setEnabled(False)
        self.nokta_sil_butonu.setEnabled(False)

        # Tıklama sinyallerini ilgili metotlara bağlıyoruz.
        self.nokta_ekle_butonu.clicked.connect(
            self.rota_noktasi_ekle
        )
        self.nokta_guncelle_butonu.clicked.connect(
            self.secili_noktayi_guncelle
        )
        self.nokta_sil_butonu.clicked.connect(
            self.secili_noktayi_sil
        )

        duzen.addWidget(self.nokta_ekle_butonu)
        duzen.addWidget(self.nokta_guncelle_butonu)
        duzen.addWidget(self.nokta_sil_butonu)
         # İki düğmeyi yan yana yerleştireceğiz.
        sira_duzeni = QHBoxLayout()

        self.yukari_butonu = QPushButton("↑ Yukarı")
        self.asagi_butonu = QPushButton("↓ Aşağı")

        # Başlangıçta seçili nokta yok.
        self.yukari_butonu.setEnabled(False)
        self.asagi_butonu.setEnabled(False)

        # lambda, tıklama gerçekleştiğinde metodu
        # belirlediğimiz yön değeriyle çağırmamızı sağlar.
        self.yukari_butonu.clicked.connect(
            lambda: self.secili_noktayi_tasi(-1)
        )
        self.asagi_butonu.clicked.connect(
            lambda: self.secili_noktayi_tasi(1)
        )

        sira_duzeni.addWidget(self.yukari_butonu)
        sira_duzeni.addWidget(self.asagi_butonu)

        duzen.addLayout(sira_duzeni)

        self.form_sonucu = QLabel(
            "Henüz rota noktası eklenmedi."
        )
        self.form_sonucu.setWordWrap(True)

        duzen.addWidget(self.form_sonucu)
        duzen.addStretch()

        return panel

    def rota_noktasi_ekle(self):
        # Formdaki değerlerden yeni bir nokta oluşturuyoruz.
        yeni_nokta = RotaNoktasi(
            enlem=self.enlem_kutusu.value(),
            boylam=self.boylam_kutusu.value(),
            irtifa=self.irtifa_kutusu.value(),
            komut=self.komut_kutusu.currentData(),
        )

        # append: listenin sonuna yeni eleman ekler.
        self.rota_noktalari.append(yeni_nokta)

        self.rota_tablosunu_guncelle()
        self.nokta_secimini_temizle()

        self.form_sonucu.setText(
            f"{len(self.rota_noktalari)}. nokta eklendi.\n\n"
            f"Toplam nokta: {len(self.rota_noktalari)}\n"
            "Henüz dosyaya kaydedilmedi."
        )

    def rota_tablosunu_guncelle(self):
        # Tabloyu yeniden doldururken geçici seçim değişimleri olur.
        # Bu sırada seçim metodunun çalışmasını engelliyoruz.
        onceki_sinyal_durumu = self.rota_tablosu.blockSignals(True)

        try:
            self.rota_tablosu.setRowCount(
                len(self.rota_noktalari)
            )

            # enumerate, her noktanın indeksini de verir.
            for satir, nokta in enumerate(self.rota_noktalari):
                hucreler = [
                    str(satir + 1),
                    nokta.komut,
                    f"{nokta.enlem:.7f}",
                    f"{nokta.boylam:.7f}",
                    f"{nokta.irtifa:.1f}",
                ]

                for sutun, metin in enumerate(hucreler):
                    self.rota_tablosu.setItem(
                        satir,
                        sutun,
                        QTableWidgetItem(metin),
                    )
        finally:
            # İşlem bitince sinyalleri önceki durumuna döndürüyoruz.
            self.rota_tablosu.blockSignals(
                onceki_sinyal_durumu
            )

    def rota_noktasi_sec(self):
        # Tabloda seçili olan satırları öğreniyoruz.
        secili_satirlar = (
            self.rota_tablosu.selectionModel().selectedRows()
        )

        if not secili_satirlar:
            self.nokta_secimini_temizle()
            return

        satir = secili_satirlar[0].row()

        if not 0 <= satir < len(self.rota_noktalari):
            self.nokta_secimini_temizle()
            return

        self.secili_nokta_indeksi = satir
        secili_nokta = self.rota_noktalari[satir]

        # Seçilen noktanın bilgilerini forma getiriyoruz.
        self.enlem_kutusu.setValue(secili_nokta.enlem)
        self.boylam_kutusu.setValue(secili_nokta.boylam)
        self.irtifa_kutusu.setValue(secili_nokta.irtifa)

        komut_indeksi = self.komut_kutusu.findData(
            secili_nokta.komut
        )

        if komut_indeksi != -1:
            self.komut_kutusu.setCurrentIndex(komut_indeksi)

        # Artık işlem yapılabilecek bir nokta seçili.
        self.nokta_guncelle_butonu.setEnabled(True)
        self.nokta_sil_butonu.setEnabled(True)

        self.form_sonucu.setText(
            f"{satir + 1}. nokta seçildi.\n\n"
            "Değerleri değiştirip güncelleme düğmesine basabilirsin."
        )
        # Seçilen noktanın sırasına göre taşıma düğmelerini ayarla.
        self.sira_butonlarini_guncelle()

    def secili_noktayi_guncelle(self):
        indeks = self.secili_nokta_indeksi

        if indeks is None:
            return

        if not 0 <= indeks < len(self.rota_noktalari):
            return

        # Yeni eleman eklemiyoruz; mevcut elemanı değiştiriyoruz.
        self.rota_noktalari[indeks] = RotaNoktasi(
            enlem=self.enlem_kutusu.value(),
            boylam=self.boylam_kutusu.value(),
            irtifa=self.irtifa_kutusu.value(),
            komut=self.komut_kutusu.currentData(),
        )

        self.rota_tablosunu_guncelle()

        # Güncellenen noktayı yeniden seçip formu eşitliyoruz.
        self.rota_tablosu.selectRow(indeks)
        self.rota_noktasi_sec()

        self.form_sonucu.setText(
            f"{indeks + 1}. nokta güncellendi.\n\n"
            f"Toplam nokta: {len(self.rota_noktalari)}\n"
            "Henüz dosyaya kaydedilmedi."
        )

    def secili_noktayi_sil(self):
        indeks = self.secili_nokta_indeksi

        if indeks is None:
            return

        if not 0 <= indeks < len(self.rota_noktalari):
            return

        silinen_numara = indeks + 1

        # Belirtilen indeksteki noktayı listeden çıkarıyoruz.
        self.rota_noktalari.pop(indeks)

        self.rota_tablosunu_guncelle()
        self.nokta_secimini_temizle()

        self.form_sonucu.setText(
            f"{silinen_numara}. nokta silindi.\n\n"
            f"Kalan nokta: {len(self.rota_noktalari)}\n"
            "Formdaki değerler yeni nokta eklemek için korundu.\n"
            "Henüz dosyaya kaydedilmedi."
        )

    def nokta_secimini_temizle(self):
        # Seçim temizleme işleminin tekrar seçim sinyali
        # oluşturmasını engelliyoruz.
        onceki_sinyal_durumu = self.rota_tablosu.blockSignals(True)

        try:
            self.rota_tablosu.clearSelection()
            self.rota_tablosu.setCurrentCell(-1, -1)
        finally:
            self.rota_tablosu.blockSignals(
                onceki_sinyal_durumu
            )

        self.secili_nokta_indeksi = None

        # Yeniden bir nokta seçilene kadar kapalı kalırlar.
        self.nokta_guncelle_butonu.setEnabled(False)
        self.nokta_sil_butonu.setEnabled(False)
    def sira_butonlarini_guncelle(self):
        indeks = self.secili_nokta_indeksi

        # Seçim yoksa iki düğme de kapalı.
        if indeks is None:
            self.yukari_butonu.setEnabled(False)
            self.asagi_butonu.setEnabled(False)
            return

        # İlk nokta daha yukarı taşınamaz.
        self.yukari_butonu.setEnabled(indeks > 0)

        # Son nokta daha aşağı taşınamaz.
        self.asagi_butonu.setEnabled(
            indeks < len(self.rota_noktalari) - 1
        )
    def secili_noktayi_tasi(self, yon):
        # Yalnızca bir sıra yukarı veya aşağı taşımayı destekliyoruz.
        if yon not in (-1, 1):
            return

        eski_indeks = self.secili_nokta_indeksi

        if eski_indeks is None:
            return

        if not 0 <= eski_indeks < len(self.rota_noktalari):
            return

        yeni_indeks = eski_indeks + yon

        # Listenin başından veya sonundan dışarı çıkmayı önlüyoruz.
        if not 0 <= yeni_indeks < len(self.rota_noktalari):
            return

        # Seçili noktayla komşusunun yerini değiştiriyoruz.
        # Sağdaki iki değer önce okunur, sonra soldakilere atanır.
        (
            self.rota_noktalari[eski_indeks],
            self.rota_noktalari[yeni_indeks],
        ) = (
            self.rota_noktalari[yeni_indeks],
            self.rota_noktalari[eski_indeks],
        )

        # Taşınan noktanın yeni yerini takip ediyoruz.
        self.secili_nokta_indeksi = yeni_indeks

        self.rota_tablosunu_guncelle()

        # Aynı nokta yeni sırasında seçili kalsın.
        self.rota_tablosu.selectRow(yeni_indeks)

        # Formu ve düğmeleri yeni seçime göre eşitliyoruz.
        self.rota_noktasi_sec()

        self.form_sonucu.setText(
            f"{eski_indeks + 1}. sıradaki nokta "
            f"{yeni_indeks + 1}. sıraya taşındı.\n\n"
            "Koordinatlar değişmedi; rota sırası değişti.\n"
            "Henüz dosyaya kaydedilmedi."
        )