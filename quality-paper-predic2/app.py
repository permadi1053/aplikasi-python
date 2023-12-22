from flask import Flask, render_template, request, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import joblib
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load model
try:
    model = joblib.load('KNeighborsClassifier1.pkl')
except FileNotFoundError:
    # train_and_save_model()  # Uncomment this line if you have a function for training and saving the model
    model = joblib.load('KNeighborsClassifier1.pkl')

class User(UserMixin):
    def __init__(self, username, institution):
        self.id = username
        self.username = username
        self.institution = institution

# Function to add user to the database file
def add_user_to_database(username, institution):
    with open('user_database.txt', 'a') as file:
        file.write(f'{username},{institution}\n')

@login_manager.user_loader
def load_user(user_id):
    # For simplicity, use the username as the user_id
    return User(user_id, None)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', username=current_user.username)
    else:
        return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    institution = request.form['institution']
    
    # For simplicity, we don't perform any user validation
    user = User(username, institution)
    login_user(user)
    
    # Add the user to the database
    add_user_to_database(username, institution)
    
    #flash('Login berhasil!', 'success')
    return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect('/suggestion')

# Function to add suggestion to the database file
def add_suggestion_to_database(name, institution, message):
    with open('suggestion_database.txt', 'a') as file:
        #file.write(f'{name},{institution},{message}\n')
        file.write(f'[{name}],[{institution}],[{message}]\n')

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if request.method == 'POST':
        name = request.form['name']
        institution = request.form['institution']
        message = request.form['message']

        # Add the suggestion to the database
        add_suggestion_to_database(name, institution, message)

        flash('Suggestion submitted successfully!', 'success')
        return redirect('/')
    
    return render_template('suggestion.html')


@app.route('/predict', methods=['POST'])
@login_required
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
        return render_template('result.html', predicted_quality=predicted_quality[0])

if __name__ == '__main__':
    app.run(debug=True)
