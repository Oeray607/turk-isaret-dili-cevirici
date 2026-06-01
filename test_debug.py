import cv2
import numpy as np
import os
import mediapipe as mp
from tensorflow.keras.models import load_model


# eğittiğimiz model action.h5
model = load_model('action.h5')
# modelin çıktı olarak vereceği kelimeler
actions = np.array([
    'merhaba', 'gunaydin', 'nasilsin', 'iyiyim', 'tesekkurler',
    'gorusuruz', 'ben', 'sen', 'o', 'sevmek',
    'istemek', 'almak', 'vermek', 'gitmek', 'gelmek',
    'beklemek', 'anlamak', 'bilmek', 'calismak', 'okul',
    'ev', 'kahve', 'su', 'para', 'araba',
    'bugun', 'yarin', 'evet', 'hayir', 'simdi'
])


mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


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
    else:
        pose = np.zeros(33*4)
    

    if results.left_hand_landmarks:
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()
    else:
        lh = np.zeros(21*3)
        

    if results.right_hand_landmarks:
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()
    else:
        rh = np.zeros(21*3)
        
    # YÜZ YOK! Sadece Pose + Sol El + Sağ El = 258
    return np.concatenate([pose, lh, rh])

# ANA DÖNGÜ
sequence = [] # son 45 kareyi tutacak liste
sentence = []
threshold = 0.8 # ******************************************************güven eşiği**********************

cap = cv2.VideoCapture(0) # kamera açılısı

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        # algılama yapar
        image, results = mediapipe_detection(frame, holistic)
        # sadece elleri çiziyoruz karısmaması için
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Tahmin Mantığı
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-45:] # eski veriyi at

        if len(sequence) == 45:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            
            # EN YÜKSEK 3 TAHMİNİ BUL
            # argsort küçükten büyüğe sıralar
            top_3_indices = res.argsort()[-3:][::-1] 
            # tahminleri yazdırma
            y_pos = 50
            for index in top_3_indices:
                name = actions[index]
                score = res[index]
                
                # Ekrana yazdır
                text = f"{name}: %{int(score*100)}"
                color = (0, 255, 0) if score > 0.5 else (0, 0, 255) # %50 üstü yeşil
                
                cv2.putText(image, text, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y_pos += 30

        cv2.imshow('DEBUG/TEST EKRANI', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()