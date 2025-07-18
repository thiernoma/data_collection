import re
import pandas as pd

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).replace("F CFA", "")  # Supprime "F CFA"
    text = str(text).replace("km", "")  # Supprime "km"
    text = re.sub(r'\s+', ' ', text)       # Remplace les espaces multiples par un seul
    text = text.strip()                    # Supprime les espaces en début/fin
    text = re.sub(r'[^\w\s$€£-]', '', text)  # Supprime caractères spéciaux
    return text
