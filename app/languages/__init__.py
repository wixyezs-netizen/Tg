import json
import os

LANGUAGES_DIR = os.path.dirname(__file__)

def get_text(key: str, lang_code: str = "ru") -> str:
    """Получение текста для ключа и языка"""
    lang_file = os.path.join(LANGUAGES_DIR, f"{lang_code}.json")
    
    if not os.path.exists(lang_file):
        lang_file = os.path.join(LANGUAGES_DIR, "ru.json")
    
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(key, key)
    except Exception:
        return key