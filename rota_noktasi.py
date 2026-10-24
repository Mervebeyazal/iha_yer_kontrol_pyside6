# dataclass, verileri tutan sınıfları daha kısa yazmamızı sağlar.
from dataclasses import dataclass


@dataclass
class RotaNoktasi:
    # İki nokta, koordinatları farklı olsa bile aynı veri yapısını kullanır.
    enlem: float
    boylam: float
    irtifa: float
    komut: str