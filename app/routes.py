#############################################################################################################################
# Program: routes.py                                                                                                        #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines the routes for the Flask app.                                                           #                                                                                                 
#############################################################################################################################

"""
The pipeline of the 2 backends is as follows:

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

from flask import Blueprint, request, jsonify
import json
from pathlib import Path
import requests
from app.llm_manager import LLMManager
from LLMs.base_llm import save_response_to_txt
from logs import setup_global_logger
from app.parse_json import save_combined_json

app_routes = Blueprint("app_routes", __name__) 
llm_manager = LLMManager()                          # Initialize LLMManager

# Backend 2(Evaluation and Checking backend) API URL
BACKEND_2_API_URL = ""     

# Path to the combined analysis file which used for feedback generation
combined_file_path = Path(__file__).parent.parent / 'results' / 'intermediate' / 'combined_analysis.json'

# Define modes with model sequences
initial_paths = {
    "mode_1": ["qwen", "llama"],
    #"mode_2": ["phi", "qwen"],
    "mode_2": ["qwen", "llama"],
}

# Setup global logger
logger = setup_global_logger()

"""
This route is used to generate the output for the frontend API.
"""
@app_routes.route('/generate_output', methods=['POST'])
def generate_output():
    try:
        # Parse the input data
        data = request.json
        mode_ = data.get("mode")
        code_ = data.get("code")
        language_ = data.get("language")
        models_analysis_path = []

        # Check if required fields are present
        if not mode_ or not code_ or not language_:
            return jsonify({"error": "Missing required fields: mode, code, or language"}), 400

        # Step 1: Generate initial output with the selected LLMs
        llm_manager.generate_initial_code(code_input = code_, mode = mode_, language = language_)
        llm_manager.generate_gpt_dafny_code(language = language_, code_input = code_)

        # Step 2: Call Backend 2's API for initial analysis
        for model_name in initial_paths[mode_]:
            path = Path(__file__).parent.parent / 'results' / f"{model_name}_results" / f"{model_name}_initial_results.json"
            
            with open(path, 'r') as file:
                model_data = json.load(file)
            
            analysis_response = requests.post(BACKEND_2_API_URL, json = model_data)
            
            # Check if the analysis was successful
            if analysis_response.status_code != 200:
                return jsonify({"error": "Error communicating with Backend 2", "details": analysis_response.text}), 500
            
            # Save the analysis response
            storage = Path(__file__).parent.parent / 'results' / "intermediate" / f"{model_name}_analysis.json"
            models_analysis_path.append(storage)
            
            with open(storage, 'w') as file:
                json.dump(analysis_response.json(), file, indent = 4)
            
            logger.info(f"Analysis response from Backend 2 saved to {storage}")
        
        # Combine analysis results
        save_combined_json(file1_path = models_analysis_path[0], file2_path = models_analysis_path[1], output_path = combined_file_path)
        
        # Step 3: Run the feedback loop to enhance the output
        llm_manager.generate_feedback_code(chosen_mode = mode_, language = language_)

        # Step 4: Send feedback output back to Backend 2 for further analysis
        feedback_path = Path(__file__).parent.parent / 'results' / "qwen_results" / "qwen_feedback_results.json"
        with open(feedback_path, 'r') as file:
            feedback_data = json.load(file)

        feedback_analysis_response = requests.post(BACKEND_2_API_URL, json = feedback_data)
        if feedback_analysis_response.status_code != 200:
            return jsonify({"error": "Error communicating with Backend 2 for feedback analysis", "details": feedback_analysis_response.text}), 500
        
        # Save final analysis results
        final_path = Path(__file__).parent.parent / 'results' / "final_analysis.json"
        with open(final_path, 'w') as file:
            json.dump(feedback_analysis_response.json(), file, indent = 4)
        logger.info(f"Final analysis response from Backend 2 saved to {final_path}")
        
        # Step 5: Wrap up the final output with summaries and validations
        final_output = llm_manager.finalize_output()

        final_output_path = Path(__file__).parent.parent / 'results' / "final_output.txt"
        save_response_to_txt(final_output, final_output_path)

        # Return the final output to the frontend API
        final_opt = {}
        final_opt["final_output"] = final_output

        return jsonify(final_opt), 200

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500