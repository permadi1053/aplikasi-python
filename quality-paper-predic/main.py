from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Memastikan model sudah dilatih dan disimpan
#try:
# Mencoba memuat model dari file
model = joblib.load('KNeighborsClassifier3.pkl')
#except FileNotFoundError:
# Jika file tidak ditemukan, latih dan simpan model
#train_and_save_model()
#model = joblib.load('KNeighborsClassifier1.pkl')


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
  if request.method == 'POST':
    # Mengambil nilai dari formulir HTML
    roughness = float(request.form['roughness'])
    brightness = float(request.form['brightness'])
    thickness = float(request.form['thickness'])
    curling = float(request.form['curling'])
    dirt = float(request.form['dirt'])
    clip = float(request.form['clip'])
    wave = float(request.form['wave'])

    # Membuat DataFrame dengan input pengguna
    user_input = pd.DataFrame({
        'roughness': [roughness],
        'brightness': [brightness],
        'thickness': [thickness],
        'curling': [curling],
        'dirt': [dirt],
        'clip': [clip],
        'wave': [wave]
    })

    # Melakukan prediksi dengan model
    predicted_quality = model.predict(user_input)

    # Menampilkan hasil prediksi
    return render_template('result.html',
                           predicted_quality=predicted_quality[0])


#if __name__ == "__main__":
#app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
