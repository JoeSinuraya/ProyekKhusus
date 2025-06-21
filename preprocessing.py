import pandas as pd
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from tqdm import tqdm
import random
import os

tqdm.pandas()

factory = StemmerFactory()
stemmer = factory.create_stemmer()

try:
    stop_words = set(stopwords.words('indonesian'))
except LookupError:
    import nltk
    nltk.download("stopwords")
    stop_words = set(stopwords.words('indonesian'))

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    text = re.sub(r'\d+', '', text)      
    return text.strip()

def tokenize(text):
    if not isinstance(text, str):
        return []
    
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [word for word in tokens if word not in stop_words]

def stem_text(text):
    if not isinstance(text, str):
        return ""
    return stemmer.stem(text)

def random_insertion(words, n=2):
    if not words:
        return []
    new_words = words[:]
    for _ in range(n):
        word = random.choice(words)
        idx = random.randint(0, len(new_words))
        new_words.insert(idx, word)
    return new_words

df = pd.read_csv("data/hasil_scraping.csv")

columns_to_process = ["Judul"]

for col in columns_to_process:
    tqdm.pandas(desc=f"🔄 Preprocessing kolom {col}")
    df[f"CLEAN_{col}"] = df[col].progress_apply(clean_text)
    df[f"STEM_{col}"] = df[f"CLEAN_{col}"].progress_apply(stem_text)
    df[f"TOKEN_{col}"] = df[f"CLEAN_{col}"].progress_apply(tokenize)
    df[f"RANDOM_INSERTION_{col}"] = df[f"TOKEN_{col}"].progress_apply(random_insertion)
    df[f"STEM_RANDOM_INSERTION_{col}"] = df[f"RANDOM_INSERTION_{col}"].progress_apply(
        lambda tokens: stem_text(" ".join(tokens))
    )

output_path = "data/hasil_preprocessing.csv"
os.makedirs("data", exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✅ Preprocessing selesai! File disimpan di {output_path}")
