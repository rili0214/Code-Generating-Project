class FeedbackLoop:
    def __init__(self, llm_manager, chosen_mode, max_loops=3):
        self.llm_manager = llm_manager
        self.mode = chosen_mode
        self.max_loops = max_loops

    def run_feedback(self, initial_results, analysis_results):
        results = initial_results
        for loop in range(self.max_loops):
            feedback_needed = any(
                result["errors"] for result in analysis_results.values()
            )
            if not feedback_needed:
                break
            # Pass feedback results back to the LLMs for refinement
            for llm_name, analysis in analysis_results.items():
                results[llm_name]["code"] = self.llm_manager.llms[llm_name](
                    results[llm_name]["code"]
                )
            # Re-evaluate after each loop
            analysis_results = self.evaluate(results)
        return results
