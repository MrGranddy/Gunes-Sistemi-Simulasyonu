import pygame
import math

yer_cekimi_sabiti = 6.67408 * 1.e-11  # metre^3 / (kilogram * saniye^2)

gunesin_kutlesi = 1.989 * 1.e30  # kilogram
dunyanin_kutlesi = 5.972 * 1.e24  # kilogram
jupiterin_kutlesi = 1.898 * 1.e27
marsin_kutlesi = 6.39 * 1.e23
venusun_kutlesi = 4.867 * 1.e24
merkurun_kutlesi = 3.285 * 1.e23
ayin_kutlesi = 7.34767309 * 1.e22
saturnun_kutlesi = 5.683 * 1.e26

dunyanin_capi = 6.371 * 1.e3  # metre
gunesin_capi = 6.957 * 1.e8  #  metre
jupiterin_capi = 6.9911 * 1.e4
marsin_capi = 3.390 * 1.e3
venusun_capi = 6.052 * 1.e3
merkurun_capi = 2.440 * 1.e3
ayin_capi = 1.737 * 1.e3
saturnun_capi = 5.8232 * 1.e3

dunya_gunes_uzaklik = 1.521 * 1.e11  # metre
jupiterin_gunes_uzaklik = 7.785 * 1.e11
mars_gunes_uzaklik = 2.279 * 1.e11
venus_gunes_uzaklik = 1.082 * 1.e11
merkur_gunes_uzaklik = 5.791 * 1.e10
ay_gunes_uzaklik = dunya_gunes_uzaklik + 3.844 * 1.e5
saturn_gunes_uzaklik = 1.429 * 1.e12

ayrik_zaman = 5000  # saniye

oran = 3.e9  # Bu oran sistemi ekrana sığdırmak için kullanılacak
cap_oran = 0.25e1  # Bu oran cisimlerin çaplarını ekrana sığdırmak için kullanılacak

arkaplan_rengi = (20, 20, 20)
(en, boy) = (1000, 1000)

ekran = pygame.display.set_mode((en, boy))
pygame.display.set_caption("Gunes Sistemi Simulasyonu")
ekran.fill(arkaplan_rengi)

cisimler = []


class Gokcismi:

    def __init__(self, isim, kutle, cap, gunesten_uzaklik, renk):
        self.isim = isim
        self.kutle = kutle
        self.cap = cap
        self.gunesten_uzaklik = gunesten_uzaklik
        self.renk = renk
        self.koordinatlar = [-gunesten_uzaklik, 0]
        if gunesten_uzaklik == 0:
            self.hiz = [0, 0]
        else:
            self.hiz = [
                0, -(yer_cekimi_sabiti * gunesin_kutlesi / gunesten_uzaklik)**(0.5)]

    def yercekimi_etki(self, cisim):
        konum_fark_vektoru = (cisim.koordinatlar[
                              0] - self.koordinatlar[0], cisim.koordinatlar[1] - self.koordinatlar[1])
        uzaklik_kare = konum_fark_vektoru[0]**2 + konum_fark_vektoru[1]**2
        if uzaklik_kare < 1.e-1:
            return (0, 0)
        birim_konum_fark_vektoru = (konum_fark_vektoru[
                                    0] / uzaklik_kare**(0.5), konum_fark_vektoru[1] / uzaklik_kare**(0.5))
        kuvvet_buyuklugu = yer_cekimi_sabiti * self.kutle * cisim.kutle / uzaklik_kare
        kuvvet = (kuvvet_buyuklugu * birim_konum_fark_vektoru[
                  0], kuvvet_buyuklugu * birim_konum_fark_vektoru[1])
        return kuvvet

    def hizi_degistir(self, kopya_cisimler):
        for cisim in kopya_cisimler:
            if cisim != self:
                kuvvet = self.yercekimi_etki(cisim)
                self.hiz[0] += (kuvvet[0] / self.kutle) * ayrik_zaman
                self.hiz[1] += (kuvvet[1] / self.kutle) * ayrik_zaman

    def hizi_uygula(self):
        self.koordinatlar[0] += self.hiz[0] * ayrik_zaman
        self.koordinatlar[1] += self.hiz[1] * ayrik_zaman

def tum_cisimlere_kuvvet_etki(cisimler):
    kopya_cisimler = list(cisimler)
    for i in range(len(cisimler)):
        cisimler[i].hizi_degistir(kopya_cisimler)

def tum_cisimleri_hareket_ettir(cisimler):
    for i in range(len(cisimler)):
        cisimler[i].hizi_uygula()

def tum_cisimleri_cizdir(cisimler, referans_cisim):
    for i in range(len(cisimler)):

        yeni_koordinatlar = (cisimler[i].koordinatlar[0] - referans_cisim.koordinatlar[0],
                                cisimler[i].koordinatlar[1] - referans_cisim.koordinatlar[1])
        yeni_koordinatlar = (yeni_koordinatlar[0] / oran, yeni_koordinatlar[1] / oran)
        yeni_koordinatlar = (int(yeni_koordinatlar[0] + en / 2), int(boy / 2 - yeni_koordinatlar[1]))
        yeni_cap = int(math.log(cisimler[i].cap) / cap_oran)
        pygame.draw.circle(
            ekran, cisimler[i].renk, yeni_koordinatlar, yeni_cap)

dunya = Gokcismi('Dunya', dunyanin_kutlesi, dunyanin_capi,
                 dunya_gunes_uzaklik, (0, 0, 255))
gunes = Gokcismi('Gunes', gunesin_kutlesi, gunesin_capi, 0, (255, 255, 0))
jupiter = Gokcismi('Jupiter', jupiterin_kutlesi, jupiterin_capi,
                   jupiterin_gunes_uzaklik, (255, 180, 180))
mars = Gokcismi('Mars', marsin_kutlesi, marsin_capi,
                mars_gunes_uzaklik, (200, 0, 0))
venus = Gokcismi('Venus', venusun_kutlesi, venusun_capi,
                 venus_gunes_uzaklik, (230, 150, 150))
merkur = Gokcismi('Merkus', merkurun_kutlesi, merkurun_capi,
                  merkur_gunes_uzaklik, (150, 150, 150))
ay = Gokcismi('Ay', ayin_kutlesi, ayin_capi, ay_gunes_uzaklik, (80, 80, 80))
saturn = Gokcismi('Saturn', saturnun_kutlesi, saturnun_capi,
                  saturn_gunes_uzaklik, (230, 200, 200))

#karadelik = Gokcismi('Karadelik', gunesin_kutlesi * 1, merkurun_capi, dunya_gunes_uzaklik * 1.2, (255, 255, 255))

cisimler += [gunes, dunya, jupiter, mars, venus, merkur]#, saturn]#, karadelik]

running = True
while running:
    tum_cisimleri_hareket_ettir(cisimler)
    tum_cisimlere_kuvvet_etki(cisimler)

    ekran.fill(arkaplan_rengi)
    tum_cisimleri_cizdir(cisimler, gunes) # Baska gezegenlere göre çizdirmek için referans cismi değiştir!
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
