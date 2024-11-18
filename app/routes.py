"""
1. frontend API will give the buggy code, the mode, and the language

2. This project(backend 1) will generate the initial outputs based on the buggy code, the mode, 
and the language and then using APi to pass the outputs(a combined .json file, each 
model's output inlucdes {mode, model, generated_text, language, dafny_text}) to another 
backend (backend 2) for analysis, checking and evaluation and the other backend will send back the
analysis and evaluation results to this backend (backend 1), then backend 1 will run the 
generate_feedback_code function to generate the enhanced output based on the analysis and 
evaluation results (same format as the initial outputs but only one model's output is includedin 
the .json file) and then send back the backend 2 for analysis, checking and evaluation. The checking
results will be sent back to this backend (backend 1) for further wrap up like summrization and 
validation.

3. The final output will be returned to the frontend API.
"""

from flask import Flask, request, jsonify
import json
from pathlib import Path
import requests
from app.llm_manager import LLMManager
from logs import setup_global_logger
from app.parse_json import save_combined_json

app = Flask(__name__)
llm_manager = LLMManager()

# URL of Backend 2's API
BACKEND_2_API_URL = "http://backend2.example.com/analyze" 

combined_file_path = Path(__file__).parent.parent / 'results' / 'intermediate' / 'combined_analysis.json'

inital_paths = {
    "mode_1": ["phi", "qwen"],
    "mode_2": ["llama", "qwen"]
}

logger = setup_global_logger()

@app.route('/generate_output', methods=['POST'])
def generate_output():
    try:
        # Parse the input data
        data = request.json
        mode_ = data.get("mode")
        code_ = data.get("code")
        language_ = data.get("language")
        models_analysis_path = []

        if not mode_ or not code_ or not language_:
            return jsonify({"error": "Missing required fields: mode, code, or language"}), 400

        # Step 1: Generate initial output with the selected LLMs
        llm_manager.generate_initial_code(code_input=code_, mode=mode_, language=language_)
        llm_manager.generate_gpt_dafny_code(language=language_, code_input=code_)

        # Step 2: Call Backend 2's API for initial analysis
        for model_name in inital_paths[mode_]:
            path = Path(__file__).parent.parent / 'results' / f"{model_name}_results" / f"{model_name}_initial_results.json"
            analysis_response = requests.post(BACKEND_2_API_URL, json = path)
            if analysis_response.status_code != 200:
                return jsonify({"error": "Error communicating with Backend 2","details": analysis_response.text}), 500
            
            storage = Path(__file__).parent.parent / 'results' / "intermediate" / f"{model_name}_analysis.json"
            models_analysis_path.append(storage)
            
            with open(storage, 'w') as file:
                json.dump(analysis_response, file, indent=4)
            logger.info(f"Analysis response from eva_backend saved to {storage}")
        
        save_combined_json(models_analysis_path[0], models_analysis_path[1], combined_file_path)
        
        # Step 3: Run the feedback loop to enhance the output
        llm_manager.generate_feedback_code(mode=mode_, language=language_)

        # Step 4: Send feedback output back to Backend 2 for further analysis
        feedback_path = Path(__file__).parent.parent / 'results' / "qwen_results" / "qwen_feedback_results.json"
        feedback_analysis_response = requests.post(BACKEND_2_API_URL, json=feedback_path)
        if feedback_analysis_response.status_code != 200:
            return jsonify({"error": "Error communicating with Backend 2 for feedback analysis", "details": feedback_analysis_response.text}), 500
        
        final_path = Path(__file__).parent.parent / 'results' / "final_analysis.json"
        
        with open(final_path, 'w') as file:
            json.dump(feedback_analysis_response, file, indent=4)
        logger.info(f"Final analysis response from eva_backend saved to {final_path}")
        
        # Step 5: Wrap up the final output with summaries and validations
        final_output = llm_manager.finalize_output(final_path)

        # Return the final output to the frontend API
        return jsonify({"final_output": final_output}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    