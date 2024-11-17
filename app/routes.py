from flask import Flask, request, jsonify
from app.llm_manager import LLMManager
from feedback.feedback_loop import FeedbackLoop

app = Flask(__name__)
llm_manager = LLMManager()
feedback_loop = FeedbackLoop(llm_manager)

# Generate Dafny code
language = "C#"
code = "..."
dafny_code = llm_manager.generate_dafny_code(language, code)

@app.route('/generate_initial_output', methods=['POST'])
def generate_initial_output():
    data = request.json
    mode = data.get("mode")
    code = data.get("buggy_code")
    language = data.get("language")

    # Generate initial output with the selected LLMs
    initial_output = llm_manager.generate_initial_output(mode, code, language)

    # Format response for the frontend
    response = {"initial_output": initial_output}
    return jsonify(response)

@app.route('/run_feedback_loop', methods=['POST'])
def run_feedback_loop():
    data = request.json
    mode = data.get("mode")
    initial_results = data.get("initial_results")

    # Run the feedback loop
    final_results = feedback_loop.run_feedback(initial_results)

    # Return the final output with explanations
    return jsonify({"final_output": final_results})