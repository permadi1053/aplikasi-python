import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

def train_and_save_model():
    # Membaca data dari CSV
    df = pd.read_csv("data.csv")

    # Memisahkan fitur (X) dan label (y)
    X = df.drop('quality', axis=1)
    y = df['quality']

    # Membagi data menjadi set pelatihan dan set pengujian
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    

    # Inisialisasi model KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=3)

    # Melatih model
    model.fit(X_train, y_train)

    # Menyimpan model ke file
    joblib.dump(model, 'KNeighborsClassifier3.pkl')

if __name__ == "__main__":
    train_and_save_model()
