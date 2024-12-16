from __future__ import annotations
from .Kniha import Kniha
from .Ctenar import Ctenar
import csv
import datetime


class Knihovna:
    def __init__(self, nazev: str):
        self.nazev = nazev
        self.knihy: list[Kniha] = []
        self.ctenari: list[Ctenar] = []
        self.vypujcene_knihy: dict[str, tuple[Ctenar, datetime.date]] = {}

    def kniha_existuje(funkce):
        def wrapper(self, isbn: str, *args, **kwargs):
            if not any(kniha.isbn == isbn for kniha in self.knihy):
                raise ValueError(f"Kniha s ISBN {isbn} neexistuje.")
            return funkce(self, isbn, *args, **kwargs)
        return wrapper
        
        
    @classmethod
    def z_csv(cls, soubor: str) -> Knihovna:
        with open(soubor, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            prvni_radek = next(reader)
            nazev_knihovny = prvni_radek[0].split(":")[1].strip()  # Očekává "Knihovna:<název>"
            knihovna = cls(nazev_knihovny)
            for radek in reader:
                if radek[0] == "kniha":
                    knihovna.pridej_knihu(Kniha(radek[1], radek[2], int(radek[3]), radek[4]))
                elif radek[0] == "ctenar":
                    knihovna.registruj_ctenare(Ctenar(radek[5], radek[6]))
        return knihovna
       

    def pridej_knihu(self, kniha: Kniha):
        self.knihy.append(kniha)
        

    @kniha_existuje
    def odeber_knihu(self, isbn: str):
        self.knihy = [k for k in self.knihy if k.isbn != isbn]

    def vyhledej_knihu(self, klicova_slovo: str = "", isbn: str = ""):
         if isbn:
            return [k for k in self.knihy if k.isbn == isbn]
         return [k for k in self.knihy if klicova_slovo.lower() in k.nazev.lower() or klicova_slovo.lower() in k.autor.lower()]

    def registruj_ctenare(self, ctenar: Ctenar):
        self.ctenari.append(ctenar)

    def zrus_registraci_ctenare(self, ctenar: Ctenar):
         self.ctenari = [c for c in self.ctenari if c != ctenar]

    def vyhledej_ctenare(self, klicova_slovo: str = "", cislo_prukazky: int = None):
        if cislo_prukazky is not None:
            return [c for c in self.ctenari if c.cislo_prukazky == cislo_prukazky]
        return [c for c in self.ctenari if klicova_slovo.lower() in c.jmeno.lower() or klicova_slovo.lower() in c.prijmeni.lower()]

    @kniha_existuje
    def vypujc_knihu(self, isbn: str, ctenar: Ctenar):
        if isbn in self.vypujcene_knihy:
            raise ValueError(f"Kniha s ISBN {isbn} je již vypůjčena.")
        self.vypujcene_knihy[isbn] = (ctenar, datetime.date.today())

    @kniha_existuje
    def vrat_knihu(self, isbn: str, ctenar: Ctenar):
        if isbn not in self.vypujcene_knihy or self.vypujcene_knihy[isbn][0] != ctenar:
            raise ValueError(f"Kniha s ISBN {isbn} není vypůjčena tímto čtenářem.")
        del self.vypujcene_knihy[isbn]

    def __str__(self) -> str:
        knihy_str = ", ".join(kniha.nazev for kniha in self.knihy)
        ctenari_str = ", ".join(f"{c.jmeno} {c.prijmeni}" for c in self.ctenari)
        return f"Knihovna {self.nazev}\nKnihy: {knihy_str}\nČtenáři: {ctenari_str}"
