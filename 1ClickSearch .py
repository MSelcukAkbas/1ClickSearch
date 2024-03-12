"""
Tamamen Öğrenim amacı ile yapılmış olup performansa önem verilmiştir
--- Hata kayıtları ve Arama geçmişi için dosya yollları ayarlamamıştır
"""
from tkinter import messagebox, scrolledtext, Tk, Frame, Menu, Text, Label, Button, END ,IntVar ,Checkbutton
from time import time as tt , sleep
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
    Kütüphaneler = ["requests", "beautifulsoup4", "google", "speedtest-cli"]
    for kütüphane in Kütüphaneler:
        Kütüphane_kontrol(kütüphane)
thr(target=thread_kütüphane).start()
from speedtest import Speedtest, SpeedtestException
from requests import get, RequestException
from bs4 import BeautifulSoup as BS4
from googlesearch import search
from urllib.parse import urlparse
print(kütüphane_listesi)
def hata_kayit(hata_mesaji):
    """ 
        Foknsiyonlarda meydana gelen hataları kullanıcıya gösterir
        Hatalar için dosyaya yazma işlemini gerçekleştirir.
    """
    with open("hata-kayitlari.txt", "a", encoding="utf-8") as dosya:
        dosya.write(hata_mesaji + "\n")
    messagebox.showerror("Hata", hata_mesaji)

def arama_gecmisi(sorgu):
    """
        Kullanıcıdan alına sorguları "arama-geçmişi" dosyasına kaydeder
    """
    with open("arama-gecmisi.txt", "a", encoding="utf-8") as dosya:
        dosya.write(sorgu + "\n")

def arama_gecmisi_oku():
    """
    Arama geçmişini okuyarak gösterir
    """
    gecmis_pencere = Tk()
    gecmis_pencere.title("Arama Geçmişi")
    gecmis_pencere.geometry("500x500")
    gecmis_pencere.resizable(height=False, width=False)
    text_widget = scrolledtext.ScrolledText(gecmis_pencere, width=58, height=30, wrap="word")
    text_widget.grid(row=1, column=0, columnspan=2, padx=10, pady=10 )
    try:
        with open("arama-gecmisi.txt", 'r', encoding='utf-8') as dosya:
            dosya_icerigi = dosya.read()
            text_widget.delete(1.0, END)
            text_widget.insert(END, dosya_icerigi)
    except FileNotFoundError:
        text_widget.delete(1.0, END)
        text_widget.insert(END, "Dosya bulunamadı.")

def thread_fonksiyonu(fonksiyon, *args, **kwargs):
    try:
        thr(target=fonksiyon, args=args, kwargs=kwargs).start()
    except Exception as hata:
        hata_kayit(f"İşlem Parçacığında Sorun Oluştu: {hata} \n")
    
def net_hizi_al():
    """İnternet hızını ölçer."""
    try:
        test = Speedtest()
        test.get_servers()
        test.get_best_server()
        ping = test.results.ping
        net_hızı_label.config(text=f"İnternet Gecikmesi: {ping}")
    except SpeedtestException as hata:
        pass
        # hata_kayit(f"İnternet Bağlantısında Bir Sorun Oluştu: {hata}") # Genel interneti kontrol eder
    # except Exception as hata:
    #     hata_kayit(f"İnternet Hızı Ölçülürken Bir Hata Alındı: {hata}")

def wikipedia_makalesi_al(sorgu, dil='tr', ):
    """Wikipedia'da verilen sorgu için bağlantı döndürür"""
    arama_sonuclari = search(sorgu + " wikipedia" , lang=dil )
    for link in arama_sonuclari:
        parsed_url = urlparse(link)
        if parsed_url.netloc == f'{dil}.wikipedia.org':
            return link
    return None

def wikipedia_icerigi_al(link, min_cumle_sayisi=10):
    """Verilen Wikipedia makalesinden içerik alır"""
    if Dahafazla_degisken.get() == 1:
        min_cumle_sayisi=30
    if not link:
        return None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    try:
        cevap = get(link, headers=headers, verify=True)
        cevap.raise_for_status()
        soup = BS4(cevap.content, "html.parser")
        icerik_bolumu = soup.find("div", {"id": "bodyContent"})
        if icerik_bolumu:
            paragraflar = icerik_bolumu.find_all("p")
            icerik, cumle_sayisi = "", 0
            for p in paragraflar:
                paragraf = p.text.strip()
                if paragraf:
                    if cumle_sayisi >= min_cumle_sayisi:
                        break
                    icerik += paragraf + "\n"
                    cumle_sayisi += len(paragraf.split("."))
            return icerik
    except RequestException as hata:
        hata_kayit(f"Wikipedia İçeriği Alınırken Hata Oluştu: {hata}")
    return None

def icerik_olustur(sorgu):
    """Wikipedia makalesinden içerik oluşturur"""
    wikipedia_baglantisi = wikipedia_makalesi_al(sorgu)
    icerik = wikipedia_icerigi_al(wikipedia_baglantisi)
    return icerik

def ana_program():
    """Ana programı içeren fonksiyon."""
    try:
        baslangic_zamani = tt()
        sorgu = giris_metni.get(1.0, END)
        if sorgu[:12] == "Metin Giriş:":
            sorgu = sorgu[12:]
        arama_gecmisi(sorgu)
        icerik = icerik_olustur(sorgu)
        if icerik:
            arama_sonucu_text.delete("1.0", END)
            arama_sonucu_text.insert(END, f"Arama Sonucu:\n{icerik}\n")
            gecen_sure_label.config(text=f"İşlem Süresi: {round(tt() - baslangic_zamani, 3)} saniye")
    except Exception as hata:
        hata_kayit(f"Ana Programda Bir Sorun Oluştu: {hata}")
    finally:
        thread_fonksiyonu(net_hizi_al)


def cikis():
    """Programı kapatır."""
    try:
        pencere.destroy()
    except Exception as hata:
        hata_kayit(f"Program Kapatmaya Çalışırken Sorun Oluştu: {hata}")


########        
pencere = Tk()
pencere.title("1Click Search ")
pencere.geometry("700x450")
pencere.resizable(height=False, width=False)
cerceve1 = Frame(pencere,bg="grey", cursor="star")
###
cerceve1.pack(side = "top", fill="both", expand=True)
###
menü_cubugu = Menu(cerceve1)
pencere.config(menu=menü_cubugu)
###
giris_label = Label(cerceve1,text="Metin Giriş:", font="Arial 13 bold", fg="black")
giris_label.place(x=300, y=20, height=20)
###
giris_metni = Text(cerceve1,font="Arial 13 bold", bg="brown", fg="white") 
giris_metni.place(x=100, y=40, width=500, height=50)
giris_metni.insert(END, "Metin Giriş:")
###
arama_sonucu_text = Text(cerceve1,font="Arial 13", bg="lightgrey", wrap="word")
arama_sonucu_text.place(x=50, y=110, width=600, height=250)
###
buton = Button(cerceve1,text="Tara", font="Times 13 bold", bg="black", fg="white", command=lambda: thread_fonksiyonu(ana_program))
buton.place(x=300, y=370, width=50)
###
gecen_sure_label = Label(cerceve1,text="İşlem Süresi: ....", font="Arial 10 bold", fg="black")
gecen_sure_label.place(x=50, y=380)
###
net_hızı_label = Label(cerceve1,text="İnternet Gecikmesi: ....", font="Arial 10 bold")
net_hızı_label.place(x=50, y=410)
###
Dahafazla_degisken = IntVar()
oto_yenileme_label = Label(pencere, justify ="center", text="Daha Fazla",font="Arial 8 bold").place(x=430, y=410)
Dahafazla = Checkbutton(pencere, variable=Dahafazla_degisken, justify="center", font="Times 13 bold").place(x=450, y=375)
###
menü_cubugu.add_command(label="Geçmiş",command=arama_gecmisi_oku )
menü_cubugu.add_command(label="Güvenli Kapat",command=cikis )
###
thread_fonksiyonu(net_hizi_al)
###
pencere.mainloop()