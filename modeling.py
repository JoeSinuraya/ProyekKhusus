import pandas as pd
import numpy as np
import ast
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, accuracy_score

print("📥 Membaca data...")
df = pd.read_csv("data/hasil_preprocessing_dan_labelling.csv")
print("✅ Data berhasil dimuat.")

print("🔄 Mengonversi kolom SDGs_Class ke format list...")
def parse_labels(x):
    if isinstance(x, str):
        return [label.strip() for label in x.split(",")]
    return x

df["SDGs_Class"] = df["SDGs_Class"].apply(parse_labels)

label_mapping = {
    "SDG 10 - Reduced Inequality": "SDG 10 - Reduced Inequalities",
    "SDG 9 - Industry": "SDG 9 - Industry, Innovation and Infrastructure",
    "Innovation and Infrastructure": "SDG 9 - Industry, Innovation and Infrastructure",
    "SDG 16 - Peace": "SDG 16 - Peace, Justice and Strong Institutions",
    "Justice and Strong Institutions": "SDG 16 - Peace, Justice and Strong Institutions"
}

def normalize_labels(label_list):
    return [label_mapping.get(label, label) for label in label_list]

df["SDGs_Class"] = df["SDGs_Class"].apply(normalize_labels)
print("✅ Label SDGs berhasil dikonversi ke format list.")

print("\n📊 Distribusi label:")
all_labels = df.explode("SDGs_Class")["SDGs_Class"]
print(all_labels.value_counts())

df = df.dropna(subset=["CLEAN_Judul"])

print("\n✍️ Melakukan TF-IDF vektorisasi pada teks...")
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["CLEAN_Judul"])

print("🔢 Melakukan binarisasi label...")
mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(df["SDGs_Class"])

print("🔀 Membagi data menjadi train dan test...")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("🤖 Melatih model Logistic Regression multi-label...")
model = OneVsRestClassifier(LogisticRegression(max_iter=1000, class_weight='balanced'))
model.fit(X_train, Y_train)

y_pred = model.predict(X_test)

print("\n📈 Evaluasi model:")
print(classification_report(Y_test, y_pred, target_names=mlb.classes_))

sample_accuracy = accuracy_score(Y_test, y_pred)
print(f"\n🎯 Accuracy (per sample): {sample_accuracy:.4f}")

print("\n💾 Menyimpan model dan vectorizer...")
joblib.dump(model, "logreg_multilabel_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
joblib.dump(mlb, "label_binarizer.pkl")
print("✅ Selesai.")
