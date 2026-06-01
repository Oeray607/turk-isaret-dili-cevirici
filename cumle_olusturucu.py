class DilMotoru:
    def __init__(self):
        # AKILLI CÜMLE ŞABLONLARI (ZAMAN DESTEKLİ)
        self.sablonlar = {}

# 1. SEVMEK (ek girişleri)
        self.ekle(['ben', 'o', 'sevmek'],   'Onu seviyorum.',     'Onu seveceğim.')
        self.ekle(['sen', 'o', 'sevmek'],   'Onu seviyorsun.',    'Onu seveceksin.')
        self.ekle(['o', 'sen', 'sevmek'],   'Seni seviyor.',      'Seni sevecek.')
        self.ekle(['ben', 'tesekkürler', 'sen'],   'Ben sana teşekkür ederim.',      'Ben sana teşekkür ederim.')

        # 2. İSTEMEK (ek girişleri)
        self.ekle(['ben', 'okul', 'istemek'], 'Ben okul istiyorum.',    'Ben okul isteyeceğim.')
        self.ekle(['sen', 'para', 'istemek'], 'Sen para istiyorsun.',   'Sen para isteyeceksin.')
        self.ekle(['sen', 'araba', 'istemek'],'Sen araba istiyorsun.',  'Sen araba isteyeceksin.')
        self.ekle(['sen', 'ev', 'istemek'],   'Sen ev istiyorsun.',     'Sen ev isteyeceksin.')
        self.ekle(['sen', 'okul', 'istemek'], 'Sen okul istiyorsun.',   'Sen okul isteyeceksin.')
        self.ekle(['o', 'para', 'istemek'],   'O para istiyor.',        'O para isteyecek.')
        self.ekle(['o', 'araba', 'istemek'],  'O araba istiyor.',       'O araba isteyecek.')
        self.ekle(['o', 'ev', 'istemek'],     'O ev istiyor.',          'O ev isteyecek.')
        self.ekle(['o', 'okul', 'istemek'],   'O okul istiyor.',        'O okul isteyecek.')

        # 3. ALMAK (ek girişleri)
        self.ekle(['sen', 'su', 'almak'],    'Sen su alıyorsun.',    'Sen su alacaksın.')
        self.ekle(['sen', 'para', 'almak'],  'Sen para alıyorsun.',  'Sen para alacaksın.')
        self.ekle(['sen', 'araba', 'almak'], 'Sen araba alıyorsun.', 'Sen araba alacaksın.')
        self.ekle(['sen', 'ev', 'almak'],    'Sen ev alıyorsun.',    'Sen ev alacaksın.')
        self.ekle(['sen', 'okul', 'almak'],  'Sen okul alıyorsun.',  'Sen okul alacaksın.')

        self.ekle(['o', 'su', 'almak'],      'O su alıyor.',         'O su alacak.')
        self.ekle(['o', 'para', 'almak'],    'O para alıyor.',       'O para alacak.')
        self.ekle(['o', 'araba', 'almak'],   'O araba alıyor.',      'O araba alacak.')
        self.ekle(['o', 'ev', 'almak'],      'O ev alıyor.',         'O ev alacak.')
        self.ekle(['o', 'okul', 'almak'],    'O okul alıyor.',       'O okul alacak.')

        # 4. VERMEK (ek girişleri)
        self.ekle(['sen', 'para', 'vermek'], 'Sen para veriyorsun.', 'Sen para vereceksin.')
        self.ekle(['sen', 'ben', 'vermek'],  'Sen bana veriyorsun.', 'Sen bana vereceksin.')
        self.ekle(['o', 'sen', 'vermek'],    'O sana veriyor.',      'O sana verecek.')
        self.ekle(['o', 'para', 'vermek'],   'O para veriyor.',      'O para verecek.')
        self.ekle(['o', 'ben', 'vermek'],    'O bana veriyor.',      'O bana verecek.')  # tamamlayıcı

        # 5. GİTMEK / GELMEK (ek girişleri)
        self.ekle(['sen', 'ev', 'gelmek'],   'Eve geliyorsun.',    'Eve geleceksin.')
        self.ekle(['sen', 'okul', 'gelmek'], 'Okula geliyorsun.',  'Okula geleceksin.')
        self.ekle(['o', 'ev', 'gelmek'],     'Eve geliyor.',       'Eve gelecek.')
        self.ekle(['o', 'okul', 'gelmek'],   'Okula geliyor.',     'Okula gelecek.')

        # 6. BEKLEMEK (ek girişleri)
        self.ekle(['sen', 'o', 'beklemek'],      'Onu bekliyorsun.',       'Onu bekleyeceksin.')
        self.ekle(['sen', 'para', 'beklemek'],   'Parayı bekliyorsun.',    'Parayı bekleyeceksin.')
        self.ekle(['o', 'ben', 'beklemek'],      'Beni bekliyor.',         'Beni bekleyecek.')
        self.ekle(['o', 'sen', 'beklemek'],      'Seni bekliyor.',         'Seni bekleyecek.')

        # 7. ANLAMAK / BİLMEK (ek girişleri)
        self.ekle(['sen', 'o', 'anlamak'],   'Onu anlıyorsun.',    'Onu anlayacaksın.')
        self.ekle(['o', 'ben', 'anlamak'],   'Beni anlıyor.',      'Beni anlayacak.')
        self.ekle(['sen', 'o', 'bilmek'],    'Onu biliyorsun.',    'Onu bileceksin.')
        self.ekle(['o', 'ben', 'bilmek'],    'Beni biliyor.',      'Beni bilecek.')
        self.ekle(['o', 'sen', 'bilmek'],    'Seni biliyor.',      'Seni bilecek.')

        # 8. ÇALIŞMAK (ek girişleri)
        self.ekle(['o', 'okul', 'calismak'], 'Okulda çalışıyor.', 'Okulda çalışacak.')

        # 9. KALIP İFADELER (ek girişleri)
        self.ekle(['bugun'],  'Bugün.', 'Bugün.')
        self.ekle(['simdi'],  'Şimdi.', 'Şimdi.')
        self.ekle(['yarin'],  'Yarın.', 'Yarın.')

        # 1. SEVMEK (Nesne + -i Hali)
        self.ekle(['ben', 'kahve', 'sevmek'],  'Ben kahveyi seviyorum.', 'Ben kahveyi seveceğim.')
        self.ekle(['ben', 'su', 'sevmek'],     'Ben suyu seviyorum.',    'Ben suyu seveceğim.')
        self.ekle(['ben', 'para', 'sevmek'],   'Ben parayı seviyorum.',  'Ben parayı seveceğim.')
        self.ekle(['ben', 'araba', 'sevmek'],  'Ben arabayı seviyorum.', 'Ben arabayı seveceğim.')
        self.ekle(['ben', 'ev', 'sevmek'],     'Ben evi seviyorum.',     'Ben evi seveceğim.')
        self.ekle(['ben', 'okul', 'sevmek'],   'Ben okulu seviyorum.',   'Ben okulu seveceğim.')
        self.ekle(['ben', 'sen', 'sevmek'],    'Ben Seni seviyorum.',        'Seni seveceğim.') # Bonus
        
        # Sen ... Seviyorsun / Seveceksin
        self.ekle(['sen', 'kahve', 'sevmek'],  'Sen kahveyi seviyorsun.', 'Sen kahveyi seveceksin.')
        self.ekle(['sen', 'su', 'sevmek'],     'Sen suyu seviyorsun.',    'Sen suyu seveceksin.')
        self.ekle(['sen', 'para', 'sevmek'],   'Sen parayı seviyorsun.',  'Sen parayı seveceksin.')
        self.ekle(['sen', 'araba', 'sevmek'],  'Sen arabayı seviyorsun.', 'Sen arabayı seveceksin.')
        self.ekle(['sen', 'ev', 'sevmek'],     'Sen evi seviyorsun.',     'Sen evi seveceksin.')
        self.ekle(['sen', 'okul', 'sevmek'],   'Sen okulu seviyorsun.',   'Sen okulu seveceksin.')

        # O ... Seviyor / Sevecek
        self.ekle(['o', 'kahve', 'sevmek'],    'O kahveyi seviyor.', 'O kahveyi sevecek.')
        self.ekle(['o', 'su', 'sevmek'],       'O suyu seviyor.',    'O suyu sevecek.')
        self.ekle(['o', 'para', 'sevmek'],     'O parayı seviyor.',  'O parayı sevecek.')
        self.ekle(['o', 'araba', 'sevmek'],    'O arabayı seviyor.', 'O arabayı sevecek.')
        self.ekle(['o', 'ev', 'sevmek'],       'O evi seviyor.',     'O evi sevecek.')
        self.ekle(['o', 'okul', 'sevmek'],     'O okulu seviyor.',   'O okulu sevecek.')


        # 2. İSTEMEK (Yalın Hal)
        # Ben ... İstiyorum / İsteyeceğim
        self.ekle(['ben', 'kahve', 'istemek'], 'Ben kahve istiyorum.', 'Ben kahve isteyeceğim.') 
        self.ekle(['ben', 'su', 'istemek'],    'Ben su istiyorum.',    'Ben su isteyeceğim.')
        self.ekle(['ben', 'para', 'istemek'],  'Ben para istiyorum.',  'Ben para isteyeceğim.')
        self.ekle(['ben', 'araba', 'istemek'], 'Ben araba istiyorum.', 'Ben araba isteyeceğim.')
        self.ekle(['ben', 'ev', 'istemek'],    'Ben ev istiyorum.',    'Ben ev isteyeceğim.')
        
        # Sen ... İstiyorsun / İsteyeceksin
        self.ekle(['sen', 'kahve', 'istemek'], 'Sen kahve istiyorsun.', 'Sen kahve isteyeceksin.')
        self.ekle(['sen', 'su', 'istemek'],    'Sen su istiyorsun.',    'Sen su isteyeceksin.')
        
        # O ... İstiyor / İsteyecek
        self.ekle(['o', 'kahve', 'istemek'],   'O kahve istiyor.', 'O kahve isteyecek.')
        self.ekle(['o', 'su', 'istemek'],      'O su istiyor.',    'O su isteyecek.')


        # 3. ALMAK (Nesne + -i Hali veya Yalın)
        # Ben ... Alıyorum / Alacağım
        self.ekle(['ben', 'kahve', 'almak'],   'Ben kahve alıyorum.',   'Ben kahve alacağım.')
        self.ekle(['ben', 'su', 'almak'],      'Ben su alıyorum.',      'Ben su alacağım.')
        self.ekle(['ben', 'araba', 'almak'],   'Ben araba alıyorum.',   'Ben araba alacağım.')
        self.ekle(['ben', 'ev', 'almak'],      'Ben ev alıyorum.',      'Ben ev alacağım.')
        
        # Sen ... Alıyorsun / Alacaksın
        self.ekle(['sen', 'kahve', 'almak'],   'Sen kahve alıyorsun.',   'Sen kahve alacaksın.')
        
        # O ... Alıyor / Alacak
        self.ekle(['o', 'kahve', 'almak'],     'O kahve alıyor.',   'O kahve alacak.')


        # 4. VERMEK (Yönelme -e/-a)

        self.ekle(['ben', 'para', 'vermek'],   'Ben para veriyorum.', 'Ben para vereceğim.')
        self.ekle(['ben', 'sen', 'vermek'],    'Ben sana veriyorum.', 'Ben sana vereceğim.')
        self.ekle(['o', 'ben', 'vermek'],      'O bana veriyor.',     'O bana verecek.')


        # 5. GİTMEK / GELMEK (Yönelme -e/-a)
        self.ekle(['ben', 'ev', 'gitmek'],    'Eve gidiyorum.',     'Eve gideceğim.')
        self.ekle(['ben', 'okul', 'gitmek'],  'Okula gidiyorum.',   'Okula gideceğim.')
        self.ekle(['sen', 'ev', 'gitmek'],    'Eve gidiyorsun.',    'Eve gideceksin.')
        self.ekle(['sen', 'okul', 'gitmek'],  'Okula gidiyorsun.',  'Okula gideceksin.')
        self.ekle(['o', 'ev', 'gitmek'],      'Eve gidiyor.',       'Eve gidecek.')
        self.ekle(['o', 'okul', 'gitmek'],    'Okula gidiyor.',     'Okula gidecek.')


        self.ekle(['ben', 'ev', 'gelmek'],    'Eve geliyorum.',     'Eve geleceğim.')
        self.ekle(['ben', 'okul', 'gelmek'],  'Okula geliyorum.',   'Okula geleceğim.')


        # 6. BEKLEMEK (Kimi? -i Hali)
        self.ekle(['ben', 'sen', 'beklemek'],  'Seni bekliyorum.',   'Seni bekleyeceğim.')
        self.ekle(['ben', 'o', 'beklemek'],    'Onu bekliyorum.',    'Onu bekleyeceğim.')
        self.ekle(['sen', 'ben', 'beklemek'],  'Beni bekliyorsun.',  'Beni bekleyeceksin.')
        self.ekle(['ben', 'araba', 'beklemek'],'Arabayı bekliyorum.','Arabayı bekleyeceğim.')


        # 7. ANLAMAK / BİLMEK (Neyi? -i Hali)
        self.ekle(['ben', 'o', 'anlamak'],     'Onu anlıyorum.',     'Onu anlayacağım.')
        self.ekle(['ben', 'sen', 'anlamak'],   'Seni anlıyorum.',    'Seni anlayacağım.')
        self.ekle(['sen', 'ben', 'anlamak'],   'Beni anlıyorsun.',   'Beni anlayacaksın.')
        
        self.ekle(['ben', 'o', 'bilmek'],      'Onu biliyorum.',     'Onu bileceğim.')
        self.ekle(['ben', 'bilmek'],           'Biliyorum.',         'Bileceğim.') 


        # 8. ÇALIŞMAK (Nerede? -de/-da Hali)
        self.ekle(['ben', 'okul', 'calismak'], 'Okulda çalışıyorum.', 'Okulda çalışacağım.')
        self.ekle(['ben', 'ev', 'calismak'],   'Evde çalışıyorum.',   'Evde çalışacağım.')
        self.ekle(['sen', 'okul', 'calismak'], 'Okulda çalışıyorsun.','Okulda çalışacaksın.')
        self.ekle(['o', 'ev', 'calismak'],     'Evde çalışıyor.',     'Evde çalışacak.')


        # 9. KALIP İFADELER

        self.ekle(['merhaba'],      'Merhaba.', 'Merhaba.')
        self.ekle(['gunaydin'],     'Günaydın.', 'Günaydın.')
        self.ekle(['nasilsin'],     'Nasılsın?', 'Nasılsın?')
        self.ekle(['iyiyim'],       'İyiyim.', 'İyiyim.')
        self.ekle(['tesekkurler'],  'Teşekkürler.', 'Teşekkürler.')
        self.ekle(['gorusuruz'],    'Görüşürüz.', 'Görüşürüz.')
        self.ekle(['merhaba', 'nasilsin'], 'Merhaba, nasılsın?', 'Merhaba, nasılsın?')

    def ekle(self, kelimeler, simdiki, gelecek):
        """Yardımcı fonksiyon: Listeye şablon ekler"""
        anahtar = frozenset(kelimeler)
        self.sablonlar[anahtar] = {'simdiki': simdiki, 'gelecek': gelecek}

    def cumle_kur(self, kelime_listesi):
        """Gelen kelimeleri analiz edip en uygun cümleyi döndürür."""
        if not kelime_listesi: return ""
        
        # 1. Temizlik
        temiz_kelimeler = [k.lower() for k in kelime_listesi]
        kelime_seti = frozenset(temiz_kelimeler)

        # 2. Zaman Tespiti 
        zaman = 'simdiki'
        arama_seti = set(temiz_kelimeler)
        
        if 'yarin' in arama_seti:
            zaman = 'gelecek'
            arama_seti.remove('yarin') 
        

        if 'bugun' in arama_seti: arama_seti.remove('bugun')
        if 'simdi' in arama_seti: arama_seti.remove('simdi')

        anahtar = frozenset(arama_seti)

        # 3. Şablon Ara
        if anahtar in self.sablonlar:
            cumle = self.sablonlar[anahtar][zaman]
            return cumle
        
        # 4. Kısmi Eşleşme (Fallback)
        return " ".join(temiz_kelimeler).capitalize() + "."

# Test Bloğu
if __name__ == "__main__":
    motor = DilMotoru()
    # Şimdiki Zaman Testleri
    print(motor.cumle_kur(['ben', 'kahve', 'sevmek']))    
    print(motor.cumle_kur(['sen', 'okul', 'gitmek']))        
    

    print(motor.cumle_kur(['yarin', 'ben', 'kahve', 'sevmek'])) 
    print(motor.cumle_kur(['yarin', 'ben', 'okul', 'gitmek']))  
    
    # Sıra Bağımsızlık Testi
    print(motor.cumle_kur(['sevmek', 'sen', 'ben']))       