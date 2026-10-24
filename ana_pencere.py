
# Görev ekranını artık ayrı dosyadaki sınıftan oluşturacağız.
from arayuz.gorev_sayfasi import GorevSayfasi
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yer Kontrol İstasyonu")
        self.resize(1200, 800)
        # Ana pencereye yerleştireceğimiz bütün bölümlerin içinde bulunacağı merkez bileşeni oluşturuyoruz.
        merkez = QWidget()
        self.setCentralWidget(merkez)

        # Dikey yerleşim: bölümleri yukarıdan aşağıya dizer.
        # Burada üst şerit ve gövde alt alta yerleşecek.
        ana_duzen = QVBoxLayout(merkez)

        # İçeriğin pencere kenarlarına olan uzaklığı.
        ana_duzen.setContentsMargins(12, 12, 12, 12)

        # Bölümler arasındaki boşluk.
        ana_duzen.setSpacing(12)

        # Bölümleri ayrı metotlarla oluşturuyoruz.
        # Böylece bütün kodu __init__ içine yığmamış oluyoruz.
        ust_serit = self.ust_serit_olustur()
        govde = self.govde_olustur()
        ana_duzen.addWidget(ust_serit)

        # stretch=1, kalan dikey alanın gövdeye verilmesini sağlar.
        ana_duzen.addWidget(govde, stretch=1)

        # QMainWindow'un hazır durum çubuğunu kullanıyoruz.
        # Bu çubuk merkez bileşeninin altında görünür.
        self.statusBar().showMessage(
            "Hazır | Uçak bağlantısı yok | Kayıt kapalı"
        )

    def ust_serit_olustur(self):
        # QFrame, ayrı bir panel gibi kullanabildiğimiz bileşendir.
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        # Yatay yerleşim: bileşenleri soldan sağa dizer.
        duzen = QHBoxLayout(panel)

        takim_adi = QLabel("TAKIM ADI")
        duzen.addWidget(takim_adi)

        # Esnek boşluk, sonraki bileşenleri sağ tarafa iter.
        duzen.addStretch()

        self.baglanti_durumu = QLabel("Araç: — | Bağlı değil")
        duzen.addWidget(self.baglanti_durumu)

        self.baglan_butonu = QPushButton("Bağlan")

        # Haberleşme kodunu henüz yazmadığımız için düğmeyi
        # şimdilik devre dışı bırakıyoruz.
        self.baglan_butonu.setEnabled(False)
        self.baglan_butonu.setToolTip(
            "Haberleşme modülü eklendiğinde kullanılacak."
        )

        duzen.addWidget(self.baglan_butonu)

        # Oluşturulan paneli çağıran metoda geri veriyoruz.
        return panel

    def govde_olustur(self):
        govde = QWidget()

        duzen = QHBoxLayout(govde)
        duzen.setContentsMargins(0, 0, 0, 0)
        duzen.setSpacing(12)

        sol_menu = self.sol_menu_olustur()

        # Görev sayfasını oluşturup pencerenin bir özelliği olarak tutuyoruz.
        # Böylece ileride başka metotlardan da ona erişebiliriz.
        self.gorev_sayfasi = GorevSayfasi()

        duzen.addWidget(sol_menu)
        # Görev sayfası, menüden kalan bütün yatay alanı kaplar.
        duzen.addWidget(self.gorev_sayfasi, stretch=1)

        return govde

    def sol_menu_olustur(self):
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        # Menü genişliğini bu aşamada sabit tutuyoruz.
        panel.setFixedWidth(150)

        duzen = QVBoxLayout(panel)

        # Aynı işlemi her menü için tekrar yazmak yerine
        # liste üzerinde döngü kuruyoruz.
        for baslik in [
            "Uçuş",
            "Görev",
            "Haberleşme",
            "Kayıtlar",
            "Ayarlar",
        ]:
            buton = QPushButton(baslik)
            buton.setMinimumHeight(42)

            if baslik == "Görev":
                # Görev düğmesini seçili görünmesi için işaretliyoruz.
                buton.setCheckable(True)
                buton.setChecked(True)
            else:
                # Diğer sayfaları sonraki adımlarda oluşturacağız.
                buton.setEnabled(False)

            duzen.addWidget(buton)

        # Boş alanı menünün altına ekleyerek düğmeleri üstte tutuyoruz.
        duzen.addStretch()

        return panel

    