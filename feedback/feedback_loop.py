import json
from app.utils import calculate_mode1_score, calculate_mode2_score, save_combined_json

class FeedbackLoop:
    def __init__(self, llm_manager, max_loops=2):
        self.llm_manager = llm_manager
        self.max_loops = max_loops

    def run_feedback(self, initial_results):
        results = initial_results

        # Evaluate initial results and get top-scoring solution
        analysis_results = self.evaluate(results)
        highest_score_model = max(analysis_results, key=lambda x: analysis_results[x]['score'])
        top_model_code = results[highest_score_model]["code"]

        # Check if any model passed without errors
        if all(not analysis["errors"] for analysis in analysis_results.values()):
            return self.format_final_output(top_model_code, analysis_results)

        # Generate combined JSON for next feedback cycle if errors are present
        combined_json = save_combined_json(results)
        for loop in range(self.max_loops):
            for model_name in results.keys():
                # Re-generate solution based on combined JSON input
                refined_code = self.llm_manager.generate_solution(
                    model_name, combined_json, None  # Language is not necessary for combined feedback
                )
                # Re-run checks and update results
                analysis = self.llm_manager.run_checking_phase({
                    'model': model_name,
                    'code': refined_code
                })
                results[model_name]["code"] = refined_code
                results[model_name]["analysis"] = analysis

        # Final selection of top scoring solution
        final_analysis_results = self.evaluate(results)
        best_model = max(final_analysis_results, key=lambda x: final_analysis_results[x]["score"])
        return self.format_final_output(results[best_model]["code"], final_analysis_results)

    def evaluate(self, results):
        analysis_results = {}
        for model_name, model_result in results.items():
            scores = model_result["analysis"]
            total_score = calculate_mode2_score(scores) if self.mode == "mode2" else calculate_mode1_score(scores)
            analysis_results[model_name] = {
                "errors": total_score < 0.8,
                "score": total_score
            }
        return analysis_results

    def format_final_output(self, code, analysis_results):
        explanation = "Summarization of analysis results: " + str(analysis_results)
        return {"code": code, "explanation": explanation}

