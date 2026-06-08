import json
import os


class Translator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.translations = {}
        self._load_all()

    def _load_all(self):
        base = os.path.join(os.path.dirname(__file__))
        for lang in ["fa", "en"]:
            path = os.path.join(base, f"{lang}.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
            else:
                self.translations[lang] = {}

    def t(self, key: str, default: str = None) -> str:
        import streamlit as st
        lang = st.session_state.get("language", "fa")
        return self.translations.get(lang, {}).get(key, default or key)

    def get_available_languages(self):
        return [
            {"code": "fa", "label": "فارسی", "icon": "🇮🇷"},
            {"code": "en", "label": "English", "icon": "🇬🇧"},
        ]
