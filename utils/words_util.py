import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_words_from_csv(filepath='data/words.csv'):
    full_path = os.path.join(BASE_DIR, filepath)
    print(f"Loading words from: {full_path}")
    try:
        df = pd.read_csv(full_path)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"File not found: {full_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []