# Başlangıç argümanlarına ve programdan çıkış işlemine erişmek için kullanıyoruz.
import sys

# PySide6 uygulamasının genel işleyişini yöneten sınıfı alıyoruz.
from PySide6.QtWidgets import QApplication

# arayuz klasöründeki ana_pencere.py dosyasından kendi sınıfımızı alıyoruz.
from arayuz.ana_pencere import AnaPencere


# Uygulamayı başlatan adımları tek bir fonksiyonda topluyoruz.
def main():

    # Arayüz uygulamasını oluşturuyoruz.
    # Bir uygulamada yalnızca bir QApplication oluşturmalıyız.
    # sys.argv, program başlatılırken verilen argümanları Qt'ye iletir.
    uygulama = QApplication(sys.argv)

    # Kendi tanımladığımız sınıftan bir pencere oluşturuyoruz.
    # Bu satır, AnaPencere sınıfındaki __init__ metodunu çalıştırır.
    pencere = AnaPencere()

    # Oluşturulan pencere başlangıçta gizlidir; burada görünür yapıyoruz.
    pencere.show()

    # exec(), tıklama ve klavye gibi olayları dinleyen döngüyü başlatır.
    # Uygulama kapandığında döngü biter ve bir çıkış kodu döndürür.
    # sys.exit(), bu kodu işletim sistemine ileterek programı sonlandırır.
    sys.exit(uygulama.exec())


# Bu dosya doğrudan çalıştırıldıysa başlangıç fonksiyonunu çağırıyoruz.
# Başka bir dosya main.py'yi import ederse bu bölüm çalışmaz.
if __name__ == "__main__":
    main()
