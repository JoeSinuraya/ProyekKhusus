import joblib

model = joblib.load("model/sdgs_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
mlb = joblib.load("model/label_binarizer.pkl")

judul_baru = ["Pengembangan Teknologi Pengolahan Air Bersih di Daerah Terpencil"]

judul_vec = vectorizer.transform(judul_baru)

pred = model.predict(judul_vec)

hasil_prediksi = mlb.inverse_transform(pred)

print("✅ Prediksi SDGs:", hasil_prediksi)
