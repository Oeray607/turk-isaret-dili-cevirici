import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model


DATA_PATH = os.path.join('MP_Data') 


actions = np.array([
    'merhaba', 'gunaydin', 'nasilsin', 'iyiyim', 'tesekkurler',
    'gorusuruz', 'ben', 'sen', 'o', 'sevmek',
    'istemek', 'almak', 'vermek', 'gitmek', 'gelmek',
    'beklemek', 'anlamak', 'bilmek', 'calismak', 'okul',
    'ev', 'kahve', 'su', 'para', 'araba',
    'bugun', 'yarin', 'evet', 'hayir', 'simdi'
])

sequence_length = 45


label_map = {label:num for num, label in enumerate(actions)}
sequences, labels = [], []

print("Test verileri yükleniyor")

for action in actions:
    action_path = os.path.join(DATA_PATH, action)
    if not os.path.exists(action_path):
        continue
    
    video_list = [x for x in os.listdir(action_path) if os.path.isdir(os.path.join(action_path, x))]
    
    for sequence in video_list:
        window = []
        try:
            for frame_num in range(sequence_length):
                res = np.load(os.path.join(action_path, sequence, "{}.npy".format(frame_num)))
                window.append(res)
            
            if len(window) == sequence_length:
                sequences.append(window)
                labels.append(label_map[action])
        except:
            pass

print(f"{len(sequences)} video yüklendi.")

# Veri Hazırlığı
X = np.array(sequences)
y = to_categorical(labels).astype(int)

# Veriyi bölüyoruz (Eğitimdeki gibi rastgele bir test seti alıyoruz)
# Not: random_state=42 vererek her seferinde aynı test verisini almayı garantiliyoruz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# 3. KAYITLI MODELİ YÜKLE
print("Model yükleniyor")
model = load_model('action.h5')

# 4. TAHMİN VE MATRİS
print("Tahminler yapılıyor...")
y_pred = model.predict(X_test)

y_true_labels = np.argmax(y_test, axis=1)
y_pred_labels = np.argmax(y_pred, axis=1)

# Matrisi Hesapla
cm = confusion_matrix(y_true_labels, y_pred_labels)

# 5. GÖRSELLEŞTİRME VE KAYIT
plt.figure(figsize=(16, 12)) 
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=actions, 
            yticklabels=actions)

plt.title('Karışıklık Matrisi (Confusion Matrix)')
plt.xlabel('Tahmin Edilen (Predicted)')
plt.ylabel('Gerçek Olan (Actual)')


output_file = 'confusion_matrix_result.png'
plt.savefig(output_file)
print(f"Grafik '{output_file}' olarak kaydedildi.")

# Doğruluk Oranı
acc = accuracy_score(y_true_labels, y_pred_labels)
print(f"\nTEST DOĞRULUK ORANI: %{acc*100:.2f}")

plt.show()