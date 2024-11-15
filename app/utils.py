import logging
import json

def format_output(llm_name, code, language, dafny_code):
    return {
        "model": llm_name,
        "code": code,
        "language": language,
        "dafny_code": dafny_code
    }

def calculate_mode1_score(scores):
    return scores["static_score"]

def calculate_mode2_score(scores):
    return (scores["static_score"] * 0.35 + scores["dynamic_score"] * 0.35 +
            scores["dafny_score"] * 0.2 + scores["rankme_score"] * 0.1)

def save_intermediate_results(model_name, analysis_result, phase):
    filename = f"results/intermediate/{model_name}_{phase}_analysis.json"
    with open(filename, 'w') as f:
        json.dump(analysis_result, f)

def save_combined_json(results):
    combined_result = {
        "llama_code": results["llama"]["code"],
        "llama_analysis": results["llama"]["analysis"],
        "qwen_code": results["qwen"]["code"],
        "qwen_analysis": results["qwen"]["analysis"]
    }
    filename = "results/combined_results.json"
    with open(filename, 'w') as f:
        json.dump(combined_result, f)
    return combined_result
