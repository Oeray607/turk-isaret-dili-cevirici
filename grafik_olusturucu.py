import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import classification_report
import pandas as pd


DATA_PATH = r'C:\Users\eray_\OneDrive\Masaüstü\AUTSL-KARISIK\Tez_IsaretDili\MP_Data'   #  DATA YOLU DEGISTIRILEBILIR
model = load_model('action.h5')


actions = np.array([
    'merhaba', 'gunaydin', 'nasilsin', 'iyiyim', 'tesekkurler',
    'gorusuruz', 'ben', 'sen', 'o', 'sevmek',
    'istemek', 'almak', 'vermek', 'gitmek', 'gelmek',
    'beklemek', 'anlamak', 'bilmek', 'calismak', 'okul',
    'ev', 'kahve', 'su', 'para', 'araba',
    'bugun', 'yarin', 'evet', 'hayir', 'simdi'
])


y_true = []
y_pred = []

print(" BASLIYOR")

for action_name in actions:
    action_path = os.path.join(DATA_PATH, action_name)
    if not os.path.exists(action_path):
        continue

    video_folders = [d for d in os.listdir(action_path)
                     if os.path.isdir(os.path.join(action_path, d))]

    for video_folder in video_folders:
        video_path = os.path.join(action_path, video_folder)

        try:
            frames = sorted(os.listdir(video_path), key=lambda x: int(x.split('.')[0]))
            sequence = []

            for frame in frames:
                frame_path = os.path.join(video_path, frame)
                sequence.append(np.load(frame_path))

            # 45 frame sabitleme
            if len(sequence) >= 45:
                sequence = sequence[-45:]
            else:
                while len(sequence) < 45:
                    sequence.append(sequence[-1])

            sequence = np.array(sequence)

            # Tahmin
            res = model.predict(np.expand_dims(sequence, axis=0), verbose=0)
            pred_index = np.argmax(res)
            pred_action = actions[pred_index]

            y_true.append(action_name)
            y_pred.append(pred_action)

        except:
            pass


if len(y_true) == 0:
    print("Hiç test verisi bulunamadi")
    exit()

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: %{accuracy*100:.2f}")


labels = sorted(list(set(y_true)))
cm = confusion_matrix(y_true, y_pred, labels=labels)

plt.figure(figsize=(12, 10))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    xticklabels=labels,
    yticklabels=labels,
    cmap='Blues'
)

plt.title(f'Dataset Confusion Matrix\nAccuracy: %{accuracy*100:.2f}')
plt.ylabel('Gerçek Etiket')
plt.xlabel('Tahmin')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

plt.savefig('confusion_matrix_kendi_dataset_v2.png', dpi=300)





report = classification_report(
    y_true,
    y_pred,
    labels=labels,
    output_dict=True
)

df = pd.DataFrame(report).transpose()

# PRECISION - RECALL - F1
df_classes = df.iloc[:-3][['precision', 'recall', 'f1-score']]

plt.figure(figsize=(14, 6))
df_classes.plot(kind='bar')

plt.title('Sınıf Bazlı Precision - Recall - F1 Skoru')
plt.xlabel('Kelimeler')
plt.ylabel('Skor')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 1)
plt.legend(['Kesinlik (Precision)', 'Duyarlılık (Recall)', 'F1 Skoru'])

plt.tight_layout()
plt.savefig('precision_recall_f1.png', dpi=300)



# TRAIN vs VALIDATION
plt.figure(figsize=(12, 5))

plt.plot(history.history['categorical_accuracy'], label='Eğitim Doğruluğu')
plt.plot(history.history['val_categorical_accuracy'], label='Doğrulama Doğruluğu')

plt.title('Eğitim ve Doğrulama Doğruluğu Karşılaştırması')
plt.xlabel('Epoch')
plt.ylabel('Doğruluk')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('train_validation_accuracy.png', dpi=300)

print (" BITTI")