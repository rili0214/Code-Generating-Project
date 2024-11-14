from flask import request, jsonify
from .llm_manager import LLMManager
from .feedback_manager import FeedbackLoop

llm_manager = LLMManager()
feedback_manager = FeedbackManager()

def initialize_routes(app):
    @app.route("/generate", methods=["POST"])
    def generate_ini_code():
        data = request.json
        language = data["language"]
        chosen_mode, initial_results = llm_manager.generate_initial_code(data["code"], data["mode"])
        return chosen_mode, jsonify(initial_results)
    
    @app.route("/feedback", methods=["POST"])
    def feedback_loop(chosen_mode):
        data = request.json
        fdbk = FeedbackLoop(llm_manager, chosen_mode)
        feedback_results = fdbk.run_feedback(data["initial_results"], data["analysis_results"])
        return jsonify(feedback_results)