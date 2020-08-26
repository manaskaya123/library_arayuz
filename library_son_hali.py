from tkinter import *
import sqlite3
import webbrowser

baglanti = sqlite3.connect("kutuphane.db")  # kütüphane adında bir database oluşturduk.
komut = baglanti.cursor()  # komut değişkeni atıyoruz.

komut.execute(
    "create table if not exists kitaplik(kitapno INT, kitapadi TEXT,yazar TEXT, yayinevi TEXT,tur TEXT)")  # kitaplık tablosu oluştu.
baglanti.commit()  # tablo oluşturma tamamlandı.

komut.execute(
    "create table if not exists uyeler(uyeno INT, uyeadi TEXT,uyesoyadi TEXT,telefonno TEXT)")  # Üyeler tablosu oluştu.
baglanti.commit()  # tablo oluşturma tamamlandı.

komut.execute(
    "create table if not exists emanet(uyeno INT, kitapno INT,verilistarihi TEXT,teslimtarihi TEXT, aciklama TEXT)")  # Emanet tablosu oluştu.
baglanti.commit()  # tablo oluşturma tamamlandı.

###############################################################33
pencere = Tk()

pencere.title("Kütüphane Takip Sistemi")
pencere.geometry("260x150")
# isim girme yazı alanlarına entry denir.
# tik atma butonlarına da checkbutton denir.
"""
frame1 = Frame(pencere)
frame1.pack() #EN ÜSTTE OLDU.
frame2 =Frame(pencere)
frame2.pack()
frame3 = Frame(pencere)
frame3.pack()

"""

asilIsim = "m"
asilParola = "m"


# while True:
######## KİTAP LİSTELEME FONKSİYONU  ###########
def kitaplistele():  # listeleme fonksiyonu
    komut.execute("select * from kitaplik")  # kitaplıktaki tüm verileri seç
    kitaplistesi = komut.fetchall()  # seçilen verileri fetchall komutuyla kitaplistesi değişkenine atıyoruz.
    print("Kitap Listesi: ")
    for i in kitaplistesi:  # liste değişkeninin içindekileri ekrana yazdırıyoruz.
        print(i)


######### KİTAP EKLEME FONKSİYONU  ###############
def kitapekle(kitapno, kitapadi, yazar, yayinevi, tur):
    komut.execute("insert into kitaplik values(@p1, @p2, @p3, @p4, @p5)",
                  (kitapno, kitapadi, yazar, yayinevi, tur))
    baglanti.commit()  # kitap ekleme fonksiyonu tamamlandı.


######### KİTAP SİLME FONKSİYONU ######
def kitapsil(kitapno):  # kitapadına göre silsin.
    komut.execute("delete from kitaplik where kitapadi=@p1",
                  (kitapno,))  # virgülün anlamı kitapadının bulunduğu listeyi sil
    # kitaplıktan kitap adına göre sil, (kitapadi,) virgüllü yazdık çünkü liste şeklinde bize lazım.
    baglanti.commit()  # silme fonksiyonu tamamlandı.


def uyelistele():
    komut.execute("select * from uyeler")  # üyelerdeki tüm verileri seç
    uyelistesi = komut.fetchall()  # seçilen verileri fetchall komutuyla liste değişkenine atıyoruz.
    print("Üyelerin Listesi: ")
    for i in uyelistesi:  # üyelistesi değişkeninin içindekileri ekrana yazdırıyoruz.
        print(i)


def uyeekle(uyeno, uyeadi, uyesoyadi, telefonno):
    komut.execute("insert into uyeler values(@p1, @p2, @p3, @p4)", (uyeno, uyeadi, uyesoyadi, telefonno))
    baglanti.commit()  # üye ekleme fonksiyonu tamamlandı.


def uyesil(uyeno):  # kitapadına göre silsin.
    komut.execute("delete from uyeler where uyeno=@p1", (uyeno,))  # virgülün anlamı kitapadının bulunduğu listeyi sil


def emanetlistele():
    komut.execute("select * from emanet")  # emanetteki tüm verileri seç
    emanetlistesi = komut.fetchall()  # seçilen verileri fetchall komutuyla liste değişkenine atıyoruz.
    print("Emanet Listesi: ")
    for i in emanetlistesi:  # emanetliste değişkeninin içindekileri ekrana yazdırıyoruz.
        print(i)


def emanetekle(uyeno, kitapno, verilistarihi, teslimtarihi="boş", aciklama="boş"):
    komut.execute("insert into emanet values(@p1, @p2, @p3, @p4, @p5)",
                  (uyeno, kitapno, verilistarihi, teslimtarihi, aciklama))
    baglanti.commit()  # emanet ekleme fonksiyonu tamamlandı.


def emanetsil(kitapno):  # kitap nosuna göre silsin.
    komut.execute("delete from emanet where kitapno=@p1",
                  (kitapno,))  # virgülün anlamı kitapadının bulunduğu listeyi sil


###GİRİŞ YAPMA FONKSİYONU ########################
def girisYapma():
    parola = parolaGiris.get()  # get sayesinde altta parola giriş entry'i içine yazdığımız değeri parola olarak kaydediyor
    isim = isimGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.

    if ((parola == asilParola) and (isim == asilIsim)):  # girilen isim ve parola asılları ile aynı ise giriş yap
        print("Giriş yapıldı")
        pencere2 = Tk()

        pencere2.title("Kütüphane Takip Sistemi")
        pencere2.geometry("900x650")
        pencere.destroy()
        """
        #####MENÜ AÇMA ###
        menu = Menu(pencere2)  # menu nesnesi oluşturuldu.
        pencere2.config(menu=menu)  # menü oluşturuldu ama kullan demek için bu işlem.

        kitapmenusu = Menu(menu, tearoff=0)  # çünkü dosya menüsü menu içinde olacak.
        # tearoff 0 deyince default olarak oluşturulan menü arsındaki çizgiyi kaldırıyoruz.
        menu.add_cascade(label="Kitaplık", menu=kitapmenusu)  # menü içinde ne yazsın
        kitapmenusu.add_command(label="Kitap Listele")  # kitap menüsü içine istediğimiz komutu ekleriz.
        # command sayesinde
        kitapmenusu.add_command(label="Kitap Ekle")
        # menüler arasına ayırıcı bir çizgi koymak için add_seperator() kullanılır.
        # kitapmenusu.add_separator()  # ayırıcı
        kitapmenusu.add_command(label="Kitap Sil")  #
        ##############
        uyemenusu = Menu(menu, tearoff=0)  # çünkü dosya menüsü menu içinde olacak.
        # tearoff 0 deyince default olarak oluşturulan menü arsındaki çizgiyi kaldırıyoruz.
        menu.add_cascade(label="Üyelik işlemleri", menu=uyemenusu)  # menü içinde ne yazsın
        uyemenusu.add_command(label="Üye Listele")  # dosya menüsü içine istediğimiz komutu ekleriz.
        # command sayesinde
        uyemenusu.add_command(label="Üye Ekle")
        uyemenusu.add_command(label="Üye Sil")  #
        ###########
        emanetmenusu = Menu(menu, tearoff=0)  # çünkü dosya menüsü menu içinde olacak.
        # tearoff 0 deyince default olarak oluşturulan menü arsındaki çizgiyi kaldırıyoruz.
        menu.add_cascade(label="Emanet işlemleri", menu=emanetmenusu)  # menü içinde ne yazsın
        emanetmenusu.add_command(label="Emanet Listele")  # dosya menüsü içine istediğimiz komutu ekleriz.
        # command sayesinde
        emanetmenusu.add_command(label="Emanet Ekle")
        emanetmenusu.add_command(label="Emanet Sil")  #

        """

        frame1 = Frame(pencere2)
        frame1.pack(side=TOP)  # EN
        frame2 = Frame(pencere2)
        frame2.pack()

        Hosgeldin = Label(frame1, text="Kütüphane Takip \nSistemine hoş geldiniz", fg="white", bg="blue",
                          font=("Consolas", 16), width=60, height=4)
        Hosgeldin.grid(row=0, column=0)

        # yazılacak yazı nesnesi oluşturuldu.
        def kitapekleAc():
            # pencere2.destroy()
            pencere3 = Tk()

            pencere3.title("Kütüphane Takip Sistemi")
            pencere3.geometry("500x300")

            def kitapbilgiris():
                kitapno = kitapnoGiris.get()  # get sayesinde altta parola giriş entry'i içine yazdığımız değeri parola olarak kaydediyor
                kitapadi = kitapadiGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                yazar = yazarGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                yayinevi = yayineviGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                tur = turGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                kitapekle(kitapno, kitapadi, yazar, yayinevi, tur)
                kitapkaydedildi = Label(pencere3, text="Kaydedildi", font=("Consolas", 14), fg="green")
                kitapkaydedildi.grid(row=5, column=1)

            kitapno = Label(pencere3, text="Kitap No :", font=("Consolas", 14))
            kitapno.grid(row=0, column=0)
            kitapnoGiris = Entry(pencere3, font=("Consolas", 14), width="20")
            kitapnoGiris.grid(row=0, column=1)

            kitapadi = Label(pencere3, text="Kitap Adı:", font=("Consolas", 14))
            kitapadi.grid(row=1, column=0)
            kitapadiGiris = Entry(pencere3, font=("Consolas", 14), width="20")
            kitapadiGiris.grid(row=1, column=1)

            yazar = Label(pencere3, text="Yazar Adı:", font=("Consolas", 14))
            yazar.grid(row=2, column=0)
            yazarGiris = Entry(pencere3, font=("Consolas", 14), width="20")
            yazarGiris.grid(row=2, column=1)

            yayinevi = Label(pencere3, text="Yayınevi :", font=("Consolas", 14))
            yayinevi.grid(row=3, column=0)
            yayineviGiris = Entry(pencere3, font=("Consolas", 14), width="20")
            yayineviGiris.grid(row=3, column=1)

            tur = Label(pencere3, text="Tür      :", font=("Consolas", 14))
            tur.grid(row=4, column=0)
            turGiris = Entry(pencere3, font=("Consolas", 14), width="20")
            turGiris.grid(row=4, column=1)
            tamam = Button(pencere3, text="Tamam", font=("Consolas", 16), command=kitapbilgiris)
            tamam.grid(row=5, column=0, columnspan=2)

            def kitapsilgiris():
                kitapno = silinecekitapno.get()
                kitapsil(kitapno)
                kitapsilindi = Label(pencere3, text="Silindi", fg="red", font=("Consolas", 14))
                kitapsilindi.grid(row=16, column=1)

            kitapno = Label(pencere3, text="Silinecek Kitap No:", font=("Consolas", 14))
            kitapno.grid(row=12, column=0)

            silinecekitapno = Entry(pencere3, font=("Consolas", 14), width="20")
            silinecekitapno.grid(row=12, column=1)

            kitapsilbuton = Button(pencere3, text="Sil", font=("Consolas", 16), command=kitapsilgiris)
            kitapsilbuton.grid(row=16, column=0, columnspan=2)

            kitaplistelebuton = Button(pencere3, text="Kitap Listele", font=("Consolas", 16), command=kitaplistele)
            kitaplistelebuton.grid(row=20, column=0, columnspan=2)

            pencere3 = mainloop()

        ############pencere3 ##############   sınırı  ####################

        def uyeekleAc():
            # pencere2.destroy()
            pencere4 = Tk()

            pencere4.title("Kütüphane Takip Sistemi")
            pencere4.geometry("500x300")

            """
            uyeno=int(input("Üye no giriniz: "))
            uyeadi=input("Üye adı giriniz: ")
            uyesoyadi=(input("Üye soyadı giriniz: "))
            telefonno=(input("telefon no giriniz: "))
            uyeekle(uyeno, uyeadi,uyesoyadi,telefonno)
            """

            def uyebilgiris():
                uyeno = uyenoGiris.get()  # get sayesinde altta parola giriş entry'i içine yazdığımız değeri parola olarak kaydediyor
                uyeadi = uyeadiGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                uyesoyadi = uyesoyadiGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                telefonno = telefonnoGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                uyeekle(uyeno, uyeadi, uyesoyadi, telefonno)
                uyekaydedildi = Label(pencere4, text="Kaydedildi", font=("Consolas", 14), fg="green")
                uyekaydedildi.grid(row=6, column=1)

            uyeno = Label(pencere4, text="Üye No     :", font=("Consolas", 14))
            uyeno.grid(row=0, column=0)
            uyenoGiris = Entry(pencere4, font=("Consolas", 14), width="20")
            uyenoGiris.grid(row=0, column=1)

            uyeadi = Label(pencere4, text="Üye Adı    :", font=("Consolas", 14))
            uyeadi.grid(row=1, column=0)
            uyeadiGiris = Entry(pencere4, font=("Consolas", 14), width="20")
            uyeadiGiris.grid(row=1, column=1)

            uyesoyadi = Label(pencere4, text="Soyadı     :", font=("Consolas", 14))
            uyesoyadi.grid(row=2, column=0)
            uyesoyadiGiris = Entry(pencere4, font=("Consolas", 14), width="20")
            uyesoyadiGiris.grid(row=2, column=1)

            telefonno = Label(pencere4, text="Telefon No :", font=("Consolas", 14))
            telefonno.grid(row=3, column=0)
            telefonnoGiris = Entry(pencere4, font=("Consolas", 14), width="20")
            telefonnoGiris.grid(row=3, column=1)
            uyetamambuton = Button(pencere4, text="Tamam", font=("Consolas", 16), command=uyebilgiris)
            uyetamambuton.grid(row=6, column=0, columnspan=2)
            """
            uyeadi=input(("Silinecek üyenin adını giriniz:"))
            uyesil(uyeadi)
            """

            def uyesilgiris():
                uyeno = silinecekuyeno.get()
                uyesil(uyeno)
                uyesilindi = Label(pencere4, text="Silindi", fg="red", font=("Consolas", 14))
                uyesilindi.grid(row=16, column=1)

            uyeno = Label(pencere4, text="Silinecek Üye No:", font=("Consolas", 14))
            uyeno.grid(row=12, column=0)

            silinecekuyeno = Entry(pencere4, font=("Consolas", 14), width="20")
            silinecekuyeno.grid(row=12, column=1)

            uyesilbuton = Button(pencere4, text="Sil", font=("Consolas", 16), command=uyesilgiris)
            uyesilbuton.grid(row=16, column=0, columnspan=2)

            uyelistelebuton = Button(pencere4, text="Üye Listele", font=("Consolas", 16), command=uyelistele)
            uyelistelebuton.grid(row=20, column=0, columnspan=2)

            pencere4 = mainloop()

        ############pencere4 ##############   sınırı  ###################

        def emanetekleAc():
            # pencere2.destroy()
            pencere5 = Tk()
            pencere5.title("Kütüphane Takip Sistemi")
            pencere5.geometry("500x300")

            """
            uyeno=int(input("Üye no giriniz: "))
            kitapno=int(input("Kitap no giriniz: "))
            verilistarihi=(input("Veriliş tarihini giriniz: "))
            teslimtarihi=input("Teslim tarihini giriniz: ")
            aciklama=input("Açıklama ekleyebilirsiniz.")
            emanetekle(uyeno, kitapno, verilistarihi, teslimtarihi, aciklama)

            """

            def emanetbilgiris():
                uyeno = uyenoGiris.get()  # get sayesinde altta parola giriş entry'i içine yazdığımız değeri parola olarak kaydediyor
                kitapno = kitapnoGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                verilistarihi = verilistarihiGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                teslimtarihi = teslimtarihiGiris.get()  # isimGiris entry'si içindeki değeri isim değişkeninde tutar.
                aciklama = aciklamaGiris.get()

                emanetekle(uyeno, kitapno, verilistarihi, teslimtarihi, aciklama)
                emanetkaydedildi = Label(pencere5, text="Kaydedildi", font=("Consolas", 14), fg="green")
                emanetkaydedildi.grid(row=5, column=1)

            uyeno = Label(pencere5, text="Üye No         :", font=("Consolas", 14))
            uyeno.grid(row=0, column=0)
            uyenoGiris = Entry(pencere5, font=("Consolas", 14), width="20")
            uyenoGiris.grid(row=0, column=1)

            kitapno = Label(pencere5, text="Kitap No       :", font=("Consolas", 14))
            kitapno.grid(row=1, column=0)
            kitapnoGiris = Entry(pencere5, font=("Consolas", 14), width="20")
            kitapnoGiris.grid(row=1, column=1)

            verilistarihi = Label(pencere5, text="Veriliş Tarihi :", font=("Consolas", 14))
            verilistarihi.grid(row=2, column=0)
            verilistarihiGiris = Entry(pencere5, font=("Consolas", 14), width="20")
            verilistarihiGiris.grid(row=2, column=1)

            teslimtarihi = Label(pencere5, text="Teslim Tarihi  :", font=("Consolas", 14))
            teslimtarihi.grid(row=3, column=0)
            teslimtarihiGiris = Entry(pencere5, font=("Consolas", 14), width="20")
            teslimtarihiGiris.grid(row=3, column=1)
            aciklama = Label(pencere5, text="Açıklama       :", font=("Consolas", 14))
            aciklama.grid(row=4, column=0)
            aciklamaGiris = Entry(pencere5, font=("Consolas", 14), width="20")
            aciklamaGiris.grid(row=4, column=1)

            emanettamambuton = Button(pencere5, text="Tamam", font=("Consolas", 16), command=emanetbilgiris)
            emanettamambuton.grid(row=5, column=0, columnspan=2)
            """
            kitapno=input(("Teslim edilen kitap nosunu giriniz:"))
            emanetsil(kitapno)
            """

            def emanetsilgiris():
                kitapno = silinecekitapno.get()
                emanetsil(kitapno)
                emanetsilindi = Label(pencere5, text="Silindi", fg="red", font=("Consolas", 14))
                emanetsilindi.grid(row=7, column=1)

            kitapno = Label(pencere5, text="Silinecek Emanet Kitap No:", font=("Consolas", 14))
            kitapno.grid(row=6, column=0)

            silinecekitapno = Entry(pencere5, font=("Consolas", 14), width="20")
            silinecekitapno.grid(row=6, column=1)

            emanetsilbuton = Button(pencere5, text="Sil", font=("Consolas", 16), command=emanetsilgiris)
            emanetsilbuton.grid(row=7, columnspan=2)

            emanetlistelebuton = Button(pencere5, text="Emanet Listele", font=("Consolas", 16), command=emanetlistele)
            emanetlistelebuton.grid(row=8, column=0, columnspan=2)

            pencere5 = mainloop()

            ############pencere4 ##############   sınırı  ####################

        def kitapeklelink():
            webbrowser.open_new(kitapekleAc())

        def uyeeklelink():
            webbrowser.open_new(uyeekleAc())

        def emaneteklelink():
            webbrowser.open_new(emanetekleAc())

        """
        KitapListele = Button(frame2, text="Kitap Listele", fg="white", bg="black", font=("Consolas", 12), width=13,height=3, command=kitaplistele)
        KitapSil = Button(frame2, text="Kitap Sil", fg="white", bg="black", font=("Consolas", 12), width=13, height=3, command=kitapsil)
        KitapListele.grid(row=0, column=1)
        KitapSil.grid(row=2, column=1)

        """

        KitapEkle = Button(frame2, text="Kitap İşlemleri", fg="white", bg="black", font=("Consolas", 12), width=15,
                           height=3,
                           command=kitapeklelink)  # satır seçili iken ctrl+d satırı altakopyalar.
        KitapEkle.grid(row=1, column=1)

        ######################
        """
        UyeListele = Button(frame2, text="Üye Listele", fg="white", bg="black", font=("Consolas", 12), width=13, height=3)
        UyeSil = Button(frame2, text="Üye Sil", fg="white", bg="black", font=("Consolas", 12), width=13, height=3)
        UyeListele.grid(row=0, column=2)
        UyeSil.grid(row=2, column=2)
        """

        UyeEkle = Button(frame2, text="Üye İşlemleri", fg="white", bg="black", font=("Consolas", 12), width=15,
                         height=3, command=uyeeklelink)
        # satır seçili iken ctrl+d satırı altakopyalar.
        UyeEkle.grid(row=1, column=2)

        ###########
        """
        emanetListele = Button(frame2, text="Emanet Listele", fg="white", bg="black", font=("Consolas", 12), width=13, height=3)
        emanetSil = Button(frame2, text="Emanet Sil", fg="white", bg="black", font=("Consolas", 12), width=13, height=3)
        emanetListele.grid(row=0, column=3)
        emanetSil.grid(row=2, column=3)
        #satır seçili iken ctrl+d satırı altakopyalar.
        """

        emanetEkle = Button(frame2, text="Emanet Ekle", fg="white", bg="black", font=("Consolas", 12), width=13,
                            height=3, command=emaneteklelink)
        emanetEkle.grid(row=1, column=3)

        """
                if kitapekle==True:
            pencere3 = Tk()

            pencere3.title("Kütüphane Takip Sistemi")
            pencere3.geometry("600x400")
            pencere2.destroy()

            pencere3=mainloop()

        """

        pencere2.mainloop()


    else:
        print("Hatalı Giriş")  # hatalı girişlerde basılacak.


################


#######FONKSİYONBİTİŞİ ######################

isim = Label(pencere, text="İsim  :", font=("Consolas", 16))
isimGiris = Entry(pencere, font=("Consolas", 16), width="8")  # isim giriş input'u oluşturduk.
parola = Label(pencere, text="Parola:", font=("Consolas", 16))
parolaGiris = Entry(pencere, font=("Consolas", 16), width="8", show="*")  # parola giriş ekranı oluşturduk
# girilen parolayı show komutu ile * şeklinde gösteriyoruz.
parolamiHatirla = Checkbutton(pencere, text="Parolamı hatırla")
girisYap = Button(pencere, text="Giriş Yap", font=("Consolas", 16), command=girisYapma)
# command ile fonksyonu çağırıyoruz.
isim.grid(row=0, column=0)
isimGiris.grid(row=0, column=1)  # konumunu belirledik
parola.grid(row=1, column=0)
parolaGiris.grid(row=1, column=1)
parolamiHatirla.grid(row=2, column=1)
girisYap.grid(row=3, column=0, columnspan=2)  # columspan 2sini ortala.
##############

pencere = mainloop()
baglanti.close()