from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import datetime

app = Flask(__name__)

# Load model ML
model = pickle.load(open('model.pkl', 'rb'))

# Home page: form input nama sapi
@app.route('/')
def index():
    return render_template('index.html')

# Saat tombol "Mulai Proses" diklik
@app.route('/start', methods=['POST'])
def start():
    nama_sapi = request.form.get('nama_sapi')
    with open('current_cow.txt', 'w') as f:
        f.write(nama_sapi)
    return f"<h3>Data '{nama_sapi}' diterima. Silakan nyalakan alat.</h3>"

# Endpoint untuk ESP32 kirim data sensor
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = data['sensor']  # Dict misal: {'pH': 6.5, 'absorbance': 0.87, 'berat': 820}
        
        # Ubah ke DataFrame (pastikan urutan kolom sesuai saat training)
        df = pd.DataFrame([input_data])

        # Prediksi pakai model
        prediction = model.predict(df)[0]  # hasil: 1 (mastitis) atau 0 (normal)
        hasil = '+' if prediction == 1 else '-'

        # Ambil nama sapi
        try:
            with open('current_cow.txt', 'r') as f:
                nama_sapi = f.read().strip()
        except:
            nama_sapi = 'Unknown'

        # Simpan log ke CSV
        log = input_data.copy()
        log['hasil'] = hasil
        log['nama_sapi'] = nama_sapi
        log['timestamp'] = datetime.datetime.now().isoformat()
        df_log = pd.DataFrame([log])
        df_log.to_csv('data_log.csv', mode='a', header=not pd.io.common.file_exists('data_log.csv'), index=False)

        return jsonify({'hasil': hasil})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
