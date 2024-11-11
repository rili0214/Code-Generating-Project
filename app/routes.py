from flask import request, jsonify
from .llm_manager import LLMManager
from .feedback_manager import FeedbackManager

llm_manager = LLMManager()
feedback_manager = FeedbackManager()

def initialize_routes(app):
    @app.route("/generate", methods=["POST"])
    def generate_code():
        data = request.json
        initial_results = llm_manager.generate_initial(data["code"], data["language"])
        return jsonify(initial_results)
    
    @app.route("/feedback", methods=["POST"])
    def feedback_loop():
        data = request.json
        feedback_results = feedback_manager.run_feedback(data["initial_results"], data["analysis_results"])
        return jsonify(feedback_results)