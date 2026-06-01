import cv2
import numpy as np
import os
import pandas as pd
import mediapipe as mp

# AUTSL veri setindeki ham videoları tarayıp, hedeflediğimiz kelimelere (ID) ait olanları bulur.
# Bu videoları MediaPipe ile işleyip sadece gerekli iskelet verilerini (Vücut+Eller) .npy formatında veri setime ekler.
# Yani bu kısım veri_aktarimi(autsl).py kısmının bir üst versiyonudur.

# Okul ve diğer gereksizler çıkarılmış temiz liste
MY_ACTIONS = [
    'ben', 'calismak', 'ev', 'evet', 'hayir', 
    'para', 'sen', 'sevmek', 'yarin'
]

OZEL_ESLESTIRME = {
    'gorusuruz': 'hoscakal',
    'iyiyim': 'iyi',
    'merhaba': 'selam',
    'su': 'icmek',         # Bizde 'su', onlarda 'icmek'
    'tesekkurler': 'tesekkur'
}

MAX_VIDEOS_PER_WORD = 100   
AUTSL_VIDEO_PATH = r'C:\AUTSL\train_set_vfbha39.zip\train'      
LABELS_CSV_PATH = r'C:\AUTSL\train_labels.csv' 
SIGN_LIST_PATH = r'C:\AUTSL\SignList_ClassId_TR_EN.csv'
OUTPUT_BASE_PATH = 'MP_Data' 


mp_holistic = mp.solutions.holistic

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def extract_keypoints(results):
    if results.pose_landmarks:
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()
    else: pose = np.zeros(33*4)
    
    if results.left_hand_landmarks:
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()
    else: lh = np.zeros(21*3)
        
    if results.right_hand_landmarks:
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()
    else: rh = np.zeros(21*3)
        
    return np.concatenate([pose, lh, rh])

print(" Sözlük ve Listeler Yükleniyor...")

try:
    sign_df = pd.read_csv(SIGN_LIST_PATH)
    word_to_id = dict(zip(sign_df['TR'].str.lower().str.strip(), sign_df['ClassId']))
    print(" SignList (Sözlük) yüklendi.")
except Exception as e:
    print(f" HATA: SignList dosyası okunamadı! Yol: {SIGN_LIST_PATH}")
    print(e)
    exit()

try:
    labels_df = pd.read_csv(LABELS_CSV_PATH, header=None, names=['sample', 'id'])
    print(" Video Listesi (Train Labels) yüklendi.")
except:
    print(" HATA: train_labels.csv okunamadı!")
    exit()


total_added = 0
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    for action in MY_ACTIONS:
        print(f"\n==========================================")
        print(f"Target: {action.upper()}")
        print(f"==========================================")
        
        autsl_name = OZEL_ESLESTIRME.get(action, action)
        target_id = word_to_id.get(autsl_name.lower())
        
        if target_id is None:
            print(f" '{autsl_name}' ({action}) AUTSL listesinde bulunamadı! (Atlanıyor)")
            continue
            
        print(f" Eşleşme: Senin '{action}' <-> AUTSL '{autsl_name}' (ID: {target_id})")
        
        # Videoları bul
        filtered_df = labels_df[labels_df['id'] == target_id]
        
        if filtered_df.empty:
            print(f" ID {target_id} için hiç video yok!")
            continue
            
        # Klasör hazırla
        action_path = os.path.join(OUTPUT_BASE_PATH, action)
        if not os.path.exists(action_path):
            os.makedirs(action_path)
            start_folder = 0
        else:
            try:
                dir_list = np.array([int(x) for x in os.listdir(action_path) if x.isdigit()])
                start_folder = np.max(dir_list) + 1 if len(dir_list) > 0 else 0
            except:
                start_folder = 0

        print(f" Kayıt {start_folder}. klasörden başlayacak. (Hedef: {MAX_VIDEOS_PER_WORD} Video)")

        # Videoları işle
        count = 0
        for index, row in filtered_df.iterrows():
            if count >= MAX_VIDEOS_PER_WORD: break
            
            video_filename = row['sample'] + "_color.mp4"
            video_path = os.path.join(AUTSL_VIDEO_PATH, video_filename)
            
            if not os.path.exists(video_path): continue

            cap = cv2.VideoCapture(video_path)
            
            save_path = os.path.join(action_path, str(start_folder + count))
            os.makedirs(save_path, exist_ok=True)
            
            frame_num = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                if frame_num >= 45: break
                
                image, results = mediapipe_detection(frame, holistic)
                keypoints = extract_keypoints(results)
                
                np.save(os.path.join(save_path, str(frame_num)), keypoints)
                frame_num += 1
                

            while frame_num < 45:
                np.save(os.path.join(save_path, str(frame_num)), keypoints)
                frame_num += 1
            
            cap.release()
            count += 1
            

            print(f" [{count}/{MAX_VIDEOS_PER_WORD}] Eklendi: {video_filename} -> Klasör: {start_folder + count - 1}")
            
        total_added += count
        print(f"\n '{action}' tamamlandı {count} video eklendi.")