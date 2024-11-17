import logging
import json

def format_output(mode, llm_name, text, language, dafny_text):
        return {
            "mode": mode,
            "model": llm_name,
            "text": text,
            "language": language,
            "dafny_text": dafny_text
        }