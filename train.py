import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import random

# Buat data palsu
data = []
for _ in range(100):
    pH = round(random.uniform(6.3, 6.9), 2)
    absorbance = round(random.uniform(0.3, 1.0), 2)
    berat = random.randint(500, 1100)

    # Logika sederhana buat label
    if pH < 6.5 and absorbance > 0.7 and berat < 750:
        hasil = 1  # mastitis
    else:
        hasil = 0  # normal

    data.append([pH, absorbance, berat, hasil])

# Simpan ke CSV (optional)
df = pd.DataFrame(data, columns=['pH', 'absorbance', 'berat_susu', 'hasil'])
df.to_csv('data_training_fake.csv', index=False)

# Training model
X = df[['pH', 'absorbance', 'berat_susu']]
y = df['hasil']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Simpan ke file model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model berhasil dibuat dan disimpan sebagai model.pkl")
