import pandas as pd
import os

def load_words_from_csv(filepath):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, filepath)
    try:
        df = pd.read_csv(full_path)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"File not found: {full_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []