import json

class FeedbackLoop:
    def __init__(self, llm_manager, threshold = 5, max_loops = 1):
        self.llm_manager = llm_manager
        self.max_loops = max_loops
        self.threshold = threshold

    def save_combined_json(self, file1_path, file2_path, output_path):
        """
        Combines two JSON files into one and saves the result to a specified output path.

        Parameters:
            file1_path (str): Path to the first JSON file.
            file2_path (str): Path to the second JSON file.
            output_path (str): Path to save the combined JSON file.

        Returns:
            dict: The combined JSON object.
        """
        # Load the first JSON file
        with open(file1_path, 'r') as f1:
            result1 = json.load(f1)
        
        # Load the second JSON file
        with open(file2_path, 'r') as f2:
            result2 = json.load(f2)
        
        # Combine the two JSON objects
        combined_json = {**result1, **result2}
        
        # Save the combined JSON to the output path
        with open(output_path, 'w') as f:
            json.dump(combined_json, f, indent=4)  # Pretty-print with an indent

        return combined_json

    def get_models_score(data):
        return data["model"], data["evaluation_score"]["final_score"]

    def run_feedback(self, result_1, result_2):
        # Check if any model passed the theshord
        model_1, score_1 = self.get_models_score(result_1)
        model_2, score_2 = self.get_models_score(result_2)

        if score_1 >= self.threshold:
            return result_1
        elif score_2 >= self.threshold:
            return result_2

        higher_score_model = model_1 if score_1 > score_2 else model_2

        # Generate combined JSON for next feedback cycle
        self.save_combined_json(result_1, result_2)

        # Run feedback loop to the both LLMs and using the new combined JSON and prompts


