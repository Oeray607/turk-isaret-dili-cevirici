import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from cumle_olusturucu import DilMotoru 

#  GÖRÜNÜM AYARLARI 
ctk.set_appearance_mode("Dark")

ctk.set_default_color_theme("dark-blue") 

class IsaretDiliUygulamasi(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arayuz Kismi")
        self.geometry("1300x720") 
        self.resizable(False, False)

        # MODELİ YÜKLEME
        try:
            self.model = load_model('action.h5')
        except Exception as e:
            print(f"action.h5 bulunamadı! {e}")
            self.model = None

        self.hareketler = np.array([
            'merhaba', 'gunaydin', 'nasilsin', 'iyiyim', 'tesekkurler',
            'gorusuruz', 'ben', 'sen', 'o', 'sevmek',
            'istemek', 'almak', 'vermek', 'gitmek', 'gelmek',
            'beklemek', 'anlamak', 'bilmek', 'calismak', 'okul',
            'ev', 'kahve', 'su', 'para', 'araba',
            'bugun', 'yarin', 'evet', 'hayir', 'simdi'
        ])
        
        #MANTIK DEĞİŞKENLERİ
        self.dizi = [] 
        self.cumle_listesi = [] 
        self.dil_motoru = DilMotoru() 
        self.esik_degeri = 0.80 
        
        self.mevcut_tahmin = ""
        self.tahmin_sayaci = 0
        self.onay_kare_sayisi = 15 
        self.en_iyi_3_tahmin = ["", "", ""] 

        #ARAYÜZ TASARIMI
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)


        # SOL: KAMERA ALANI
        self.sol_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="black") 
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        self.sol_panel.grid_rowconfigure(0, weight=1)
        self.sol_panel.grid_columnconfigure(0, weight=1)

        self.lbl_kamera = ctk.CTkLabel(self.sol_panel, text="")
        self.lbl_kamera.grid(row=0, column=0, sticky="nsew") 


        # SAĞ: KONTROL PANELİ

        self.sag_panel = ctk.CTkFrame(self, width=340, corner_radius=0) 
        self.sag_panel.grid(row=0, column=1, sticky="nsew")
        self.sag_panel.grid_propagate(False)

        # Başlık
        self.lbl_baslik = ctk.CTkLabel(self.sag_panel, text="TİD ÇEVİRİSİ", font=("Roboto", 22, "bold"), text_color="#3B8ED0")
        self.lbl_baslik.pack(pady=(25, 10))

        # ANLIK TAHMİN
        self.lbl_tahmin_baslik = ctk.CTkLabel(self.sag_panel, text="ALGILANAN:", font=("Arial", 12))
        self.lbl_tahmin_baslik.pack(pady=(5, 0))
        
        self.giris_tahmin = ctk.CTkEntry(self.sag_panel, width=300, height=45, font=("Arial", 24, "bold"), justify="center")
        self.giris_tahmin.pack(pady=5)
        self.giris_tahmin.insert(0, "...")
        self.giris_tahmin.configure(state="disabled")

        # Güven Barı
        self.cubuk_guven = ctk.CTkProgressBar(self.sag_panel, width=300, height=8)
        self.cubuk_guven.set(0)
        self.cubuk_guven.pack(pady=10)

        self.ayirici1 = ctk.CTkFrame(self.sag_panel, height=2, fg_color="#444")
        self.ayirici1.pack(fill="x", padx=20, pady=10)

        # ALTERNATİFLER
        self.lbl_oneriler = ctk.CTkLabel(self.sag_panel, text="ALTERNATİFLER", font=("Arial", 11), text_color="gray")
        self.lbl_oneriler.pack(pady=(0, 2))

        self.panel_oneriler = ctk.CTkFrame(self.sag_panel, fg_color="transparent")
        self.panel_oneriler.pack()

        self.btn_oneri1 = ctk.CTkButton(self.panel_oneriler, text="-", width=140, height=30, fg_color="#333", command=lambda: self.alternatif_sec(1))
        self.btn_oneri1.grid(row=0, column=0, padx=5)
        self.btn_oneri2 = ctk.CTkButton(self.panel_oneriler, text="-", width=140, height=30, fg_color="#333", command=lambda: self.alternatif_sec(2))
        self.btn_oneri2.grid(row=0, column=1, padx=5)

        self.ayirici2 = ctk.CTkFrame(self.sag_panel, height=2, fg_color="#444")
        self.ayirici2.pack(fill="x", padx=20, pady=15)

        # CÜMLE KUTUSU
        self.lbl_cumle_baslik = ctk.CTkLabel(self.sag_panel, text="OLUŞTURULAN CÜMLE:", font=("Roboto", 14, "bold"))
        self.lbl_cumle_baslik.pack(pady=(0, 5))

        self.txt_cumle = ctk.CTkTextbox(self.sag_panel, width=300, height=100, font=("Arial", 16), border_width=2, border_color="#333")
        self.txt_cumle.pack(pady=5)
        self.txt_cumle.insert("0.0", "Hazır...")
        self.txt_cumle.configure(state="disabled")

        # BUTONLAR
        self.panel_butonlar = ctk.CTkFrame(self.sag_panel, fg_color="transparent")
        self.panel_butonlar.pack(pady=15, fill="x", padx=10)

        # Geri Al Butonu
        self.btn_geri_al = ctk.CTkButton(self.panel_butonlar, text="GERİ AL", width=145, height=35, fg_color="#E67E22", hover_color="#D35400", font=("Arial", 12, "bold"), command=self.son_kelimeyi_sil)
        self.btn_geri_al.grid(row=0, column=0, padx=5, pady=5)

        # Temizle Butonu
        self.btn_temizle = ctk.CTkButton(self.panel_butonlar, text="TEMİZLE", width=145, height=35, fg_color="#C0392B", hover_color="#922B21", font=("Arial", 12, "bold"), command=self.hepsini_temizle)
        self.btn_temizle.grid(row=0, column=1, padx=5, pady=5)

        # KAPAT  Butonu
        self.btn_cikis = ctk.CTkButton(self.panel_butonlar, text="PROGRAMI KAPAT", width=300, height=45, fg_color="black", hover_color="black", font=("Arial", 12, "bold"), command=self.uygulamayi_kapat
        )
        self.btn_cikis.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Kamera Başlatma
        self.kamera = cv2.VideoCapture(0)
        
        # Mediapipe
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.kamera_dongusu()

    # ANA MANTIK
    def kamera_dongusu(self):
        ret, cerceve = self.kamera.read()
        if ret:
            goruntu, sonuclar = self.mediapipe_algilama(cerceve, self.holistic)

            if self.model:
                anahtar_noktalar = self.anahtar_noktalari_cikar(sonuclar)
                self.dizi.append(anahtar_noktalar)
                self.dizi = self.dizi[-45:] 

                if len(self.dizi) == 45:
                    res = self.model.predict(np.expand_dims(self.dizi, axis=0), verbose=0)[0]
                    en_iyi_3_index = res.argsort()[-3:][::-1]
                    self.en_iyi_3_tahmin = [self.hareketler[i] for i in en_iyi_3_index]
                    guven_orani = res[en_iyi_3_index[0]]
                    en_iyi_kelime = self.en_iyi_3_tahmin[0]

                    self.cubuk_guven.set(guven_orani)
                    
                    if guven_orani > self.esik_degeri:
                        if en_iyi_kelime == self.mevcut_tahmin:
                            self.tahmin_sayaci += 1
                        else:
                            self.mevcut_tahmin = en_iyi_kelime
                            self.tahmin_sayaci = 0

                        if self.tahmin_sayaci > self.onay_kare_sayisi:
                            if en_iyi_kelime != "beklemek":
                                self.cumleye_ekle(en_iyi_kelime)
                                self.dizi = [] 
                                self.tahmin_sayaci = 0
                                self.tahmin_guncelle(f"{en_iyi_kelime.upper()}", guven_orani)
                                self.btn_oneri1.configure(text=f"{self.en_iyi_3_tahmin[1]}")
                                self.btn_oneri2.configure(text=f"{self.en_iyi_3_tahmin[2]}")
                    else:
                        self.tahmin_guncelle("...", 0)

            # Görüntü Boyutlandırma 
            goruntu = cv2.resize(goruntu, (960, 720)) 
            goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(goruntu)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_kamera.imgtk = imgtk
            self.lbl_kamera.configure(image=imgtk)

        self.after(10, self.kamera_dongusu)

    def mediapipe_algilama(self, goruntu, model):
        goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
        goruntu.flags.writeable = False
        sonuclar = model.process(goruntu)
        goruntu.flags.writeable = True
        goruntu = cv2.cvtColor(goruntu, cv2.COLOR_RGB2BGR)
        return goruntu, sonuclar

    def anahtar_noktalari_cikar(self, sonuclar):
        if sonuclar.pose_landmarks:
            pose = np.array([[res.x, res.y, res.z, res.visibility] for res in sonuclar.pose_landmarks.landmark]).flatten()
        else: pose = np.zeros(33*4)
        
        if sonuclar.left_hand_landmarks:
            lh = np.array([[res.x, res.y, res.z] for res in sonuclar.left_hand_landmarks.landmark]).flatten()
        else: lh = np.zeros(21*3)
        if sonuclar.right_hand_landmarks:
            rh = np.array([[res.x, res.y, res.z] for res in sonuclar.right_hand_landmarks.landmark]).flatten()
        else: rh = np.zeros(21*3)
        return np.concatenate([pose, lh, rh])

    def tahmin_guncelle(self, metin, guven):
        self.giris_tahmin.configure(state="normal")
        self.giris_tahmin.delete(0, 'end')
        self.giris_tahmin.insert(0, metin)
        self.giris_tahmin.configure(state="disabled")

    def cumleye_ekle(self, kelime):
        if len(self.cumle_listesi) > 0:
            if self.cumle_listesi[-1] == kelime:
                return 

        self.cumle_listesi.append(kelime)
        self.cumle_kutusunu_guncelle()

    def alternatif_sec(self, secenek_index):
        if self.en_iyi_3_tahmin[secenek_index] != "":
            yeni_kelime = self.en_iyi_3_tahmin[secenek_index]
            if len(self.cumle_listesi) > 0:
                self.cumle_listesi.pop()
            self.cumle_listesi.append(yeni_kelime)
            self.cumle_kutusunu_guncelle()

    def son_kelimeyi_sil(self):
        if len(self.cumle_listesi) > 0:
            self.cumle_listesi.pop()
            self.cumle_kutusunu_guncelle()

    def hepsini_temizle(self):
        self.cumle_listesi = []
        self.cumle_kutusunu_guncelle()

    def cumle_kutusunu_guncelle(self):
        if self.dil_motoru:
            tam_metin = self.dil_motoru.cumle_kur(self.cumle_listesi)
        else:
            tam_metin = " ".join(self.cumle_listesi)
        
        self.txt_cumle.configure(state="normal")
        self.txt_cumle.delete("0.0", "end")
        self.txt_cumle.insert("0.0", tam_metin)
        self.txt_cumle.configure(state="disabled")

    def uygulamayi_kapat(self):
        if self.kamera.isOpened():
            self.kamera.release()
        self.destroy()

if __name__ == "__main__":
    app = IsaretDiliUygulamasi()
    app.mainloop()