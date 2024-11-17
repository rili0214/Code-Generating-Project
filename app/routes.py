from flask import Flask, request, jsonify
from app.llm_manager import LLMManager
from feedback.feedback_loop import FeedbackLoop

app = Flask(__name__)
llm_manager = LLMManager()
feedback_loop = FeedbackLoop(llm_manager)

@app.route('/generate_output', methods=['POST'])
def generate_output():
    data = request.json
    mode = data.get("mode")
    code = data.get("buggy_code")
    language = data.get("language")
    dafny_code = llm_manager.generate_dafny_code(language, code)

    # Generate initial output with the selected LLMs
    llm_manager.generate_initial_output(mode, code, language)

    # Run the feedback loop
    feedback_loop.run_feedback(initial_results)

    # Return the final output with explanations
    return jsonify({"final_output": final_results})