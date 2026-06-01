import cv2
import numpy as np
import os

# MP_Data klasöründeki sayısal (.npy) iskelet verilerini okur ve bunları
# görselleştirerek tekrar video (.mp4) formatına dönüştürür.
# Amaç: Hatalı veya bozuk verileri gözle kontrol etmek ve düzenlemek
# gözle kontrol edip temizlemek için analiz.

actions = [
    'merhaba', 'gunaydin', 'nasilsin', 'iyiyim', 'tesekkurler',
    'gorusuruz', 'ben', 'sen', 'o', 'sevmek',
    'istemek', 'almak', 'vermek', 'gitmek', 'gelmek',
    'beklemek', 'anlamak', 'bilmek', 'calismak', 'okul',
    'ev', 'kahve', 'su', 'para', 'araba',
    'bugun', 'yarin', 'evet', 'hayir', 'simdi'

]

BASLANGIC = 60
BITIS = 160
DATA_PATH_ROOT = os.path.join('MP_Data')
BASE_OUTPUT_FOLDER = 'Data_Inceleme'

print(f"{len(actions)} Kelime")

for action in actions:
    print(f"\n İşleniyor: {action.upper()}...")
    
    
    action_output_folder = os.path.join(BASE_OUTPUT_FOLDER, action)
    if not os.path.exists(action_output_folder):
        os.makedirs(action_output_folder)
    
    
    for sequence_num in range(BASLANGIC, BITIS):
        video_path = os.path.join(DATA_PATH_ROOT, action, str(sequence_num))
        
        # Klasör yoksa atla
        if not os.path.exists(video_path):
            continue

        # Verileri Yükle
        frames = []
        for frame_num in range(45):
            npy_path = os.path.join(video_path, f"{frame_num}.npy")
            if os.path.exists(npy_path):
                try: frames.append(np.load(npy_path))
                except: pass
        
        if not frames: continue

        # Video Kaydet
        save_path = os.path.join(action_output_folder, f"{sequence_num}.mp4")
        
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        out = cv2.VideoWriter(save_path, fourcc, 10.0, (500, 500))

        for i, data in enumerate(frames):
            image = np.zeros((500, 500, 3), dtype=np.uint8)
            try:
                # Veri Ayrıştırma
                pose = data[:132].reshape(33, 4)
                lh = data[132:195].reshape(21, 3)
                rh = data[195:].reshape(21, 3)

                # Çizim
                for lm in pose:
                    cv2.circle(image, (int(lm[0]*500), int(lm[1]*500)), 3, (0,0,255), -1)
                if np.sum(lh) != 0:
                    for lm in lh:
                        cv2.circle(image, (int(lm[0]*500), int(lm[1]*500)), 2, (255,0,0), -1)
                if np.sum(rh) != 0:
                    for lm in rh:
                        cv2.circle(image, (int(lm[0]*500), int(lm[1]*500)), 2, (0,255,0), -1)
            except: pass
            
            cv2.putText(image, f"{action} - {sequence_num}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(image)

        out.release()
        

print("\n TÜM VİDEOLAR HAZIR!")