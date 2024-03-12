
from tkinter import messagebox, Tk, Text, Label, Button, END
from time import time
from threading import Thread as thr
from importlib import util  
from subprocess import check_call


kütüphane_listesi = []

def Kütüphane_kontrol(Kütüphane_adı):
    spec = util.find_spec(Kütüphane_adı)
    if spec is None: 
        try:
            check_call(['pip', 'install', Kütüphane_adı])
            kütüphane_listesi.append(f"{Kütüphane_adı} kütüphanesi indirildi \n")
        except Exception as e:
            print("Hata:", e)
    else:
        kütüphane_listesi.append(f"{Kütüphane_adı} kütüphanesi zaten yüklü.  \n")
def thread_kütüphane():
    Kütüphaneler = ["requests", "beautifulsoup4", "google"]  # + , "speedtest-cli"
    for kütüphane in Kütüphaneler:
        Kütüphane_kontrol(kütüphane)
thr(target=thread_kütüphane).start()


print(kütüphane_listesi)
from urllib.parse import urlparse
from googlesearch import search
from requests import get, RequestException
from bs4 import BeautifulSoup as BS4
class WikipediaSearch:
    def __init__(self):
        self.pencere = Tk()
        self.pencere.title("One Click Search")
        self.pencere.geometry("700x450")
        self.pencere.resizable(height=False, width=False)

        self.giris_label = Label(text="Metin Giriş:", font=("Arial", 13, "bold"), cursor="star")
        self.giris_label.place(x=300, y=20, height=20)

        self.giris_metni = Text(font=("Arial", 13, "bold"), bg="brown", fg="white")
        self.giris_metni.place(x=100, y=40, width=500, height=50)
        self.giris_metni.insert(END, "Metin Giriş:")

        self.arama_sonucu_text = Text(font=("Arial", 13), bg="lightgrey", wrap="word", cursor="plus")
        self.arama_sonucu_text.place(x=50, y=110, width=600, height=250)

        self.buton = Button(text="Tara", font=("Times", 13, "bold"), command=self.basla)
        self.buton.place(x=300, y=370, width=50)

        self.gecen_sure_label = Label(text="İşlem Süresi: ....", font=("Arial", 10, "bold"))
        self.gecen_sure_label.place(x=50, y=380)

    def hata_kayit(self, hata):
        messagebox.showerror("Hata", hata)

    def thread_fonksiyonu(self, fonksiyon, *args, **kwargs):
        try:
            thr(target=fonksiyon, args=args, kwargs=kwargs).start()
        except Exception as thri:
            self.hata_kayit(f"İşlem Parçacığında Sorun Oluştu: {thri}")

    def wikipedia_makalesi_al(self, sorgu, dil='tr',  min_cümle_sayısı=10):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        arama_sonuçları = search(sorgu + " wikipedia",  lang=dil, )
        link, içerik, cümle_sayısı = None, "", 0
        for l in arama_sonuçları:
            parsed_url = urlparse(l)
            if parsed_url.netloc == f'{dil}.wikipedia.org':
                link = l
                break
        if not link:
            return None
        try:
            cevap = get(link, headers=headers, verify=True)
            cevap.raise_for_status()
            soup = BS4(cevap.content, "html.parser")
            içerik_bölümü = soup.find("div", {"id": "bodyContent"})
            if içerik_bölümü:
                paragraflar = içerik_bölümü.find_all("p")
                for p in paragraflar:
                    paragraf = p.text.strip()
                    if paragraf and cümle_sayısı < min_cümle_sayısı:
                        içerik += paragraf + "\n"
                        cümle_sayısı += len(paragraf.split("."))
                return içerik
        except RequestException as req_f:
            self.hata_kayit(f"Wikipedia İçeriği Alınırken Hata Oluştu: {req_f}")
        return None

    def ana_fonksiyon(self):
        def main():
            try:
                baslangic_zamani = time()
                sorgu = self.giris_metni.get(1.0, END)
                if sorgu[:12] == "Metin Giriş:":
                    sorgu = sorgu[12:]
                içerik = self.wikipedia_makalesi_al(sorgu)
                if içerik:
                    self.arama_sonucu_text.delete("1.0", END)
                    self.arama_sonucu_text.insert(END, f"Arama Sonucu:\n{içerik}\n")
                    self.gecen_sure_label.config(text=f"İşlem Süresi: {round(time() - baslangic_zamani, 2)} saniye")
            except Exception as main_f:
                self.hata_kayit(f"Ana Programda Bir Sorun Oluştu: {main_f}")

        self.buton.config(command=lambda: self.thread_fonksiyonu(main))

    def basla(self):
        self.ana_fonksiyon()
        self.pencere.mainloop()

if __name__ == "__main__":
    wp_search = WikipediaSearch()
    wp_search.basla()
