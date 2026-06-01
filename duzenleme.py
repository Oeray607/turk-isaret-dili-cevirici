import numpy as np
import os
# BU KOD ILE YUZDEKI VERILERI KALDIRARAK MODELIMIZIN EZBERLEME YAPMASINA
# ENGEL OLMAYA CALISACAĞIZ VE TUM AGIRLIGI HAREKETLERE VERECEĞIZ
# Veri yolu: Projenle aynı klasörde MP_Data olduğunu varsayıyoruz
DATA_PATH = os.path.join('MP_Data')

# KLASÖR KONTROLÜ
if not os.path.exists(DATA_PATH):
    print(f"HATA: '{DATA_PATH}' klasörü bulunamadı! Lütfen kodun doğru yerde olduğundan emin ol.")
    exit()

# Klasör listesini al
try:
    actions = os.listdir(DATA_PATH)
except Exception as e:
    print(f"Hata oluştu: {e}")
    actions = []

print("Veri temizliği başlıyor... Yüz verileri (Face Mesh) siliniyor...")
print("-" * 50)

count = 0
hata_sayisi = 0

for action in actions:
    action_path = os.path.join(DATA_PATH, action)
    
    # Sadece klasörleri işleme al
    if not os.path.isdir(action_path): 
        continue
    
    # Videoları (sequence) gez
    sequences = os.listdir(action_path)
    for sequence in sequences:
        sequence_path = os.path.join(action_path, sequence)
        
        # Kareleri (frame) gez
        frames = os.listdir(sequence_path)
        for frame in frames:
            if not frame.endswith('.npy'): 
                continue
            
            file_path = os.path.join(sequence_path, frame)
            
            try:
                # 1. Veriyi yükle
                data = np.load(file_path)
                
                
                if data.shape[0] == 258:
                    continue
                
                # 2. PARÇALA VE BİRLEŞTİR
                # Pose: İlk 132 değer
                pose = data[:132]
                
                # Hands
                hands = data[1536:] 
                
                # 3. Yeni veriyi birleştir (33*4 + 21*3 + 21*3 = 258)
                new_data = np.concatenate([pose, hands])
                
                # 4. Aynı dosyanın üzerine kaydet
                np.save(file_path, new_data)
                count += 1
                
            except Exception as e:
                print(f"Hata: {file_path} - {e}")
                hata_sayisi += 1

print("-" * 50)
print(f" İŞLEM TAMAMLANDI!")
print(f"  Toplam {count} dosya ")
if hata_sayisi > 0:
    print(f" {hata_sayisi} dosyada hata oluştu.")