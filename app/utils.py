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

def save_intermediate_results(model_name, analysis_result, phase):
    filename = f"results/intermediate/{model_name}_{phase}_analysis.json"
    with open(filename, 'w') as f:
        json.dump(analysis_result, f)



