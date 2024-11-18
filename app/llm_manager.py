import json
from LLMs.qwen.qwen_generate import initial_call as qwen_initial_call, feedback_call as qwen_feedback_call
from LLMs.llama.llama_generate import initial_call as llama_initial_call
from LLMs.phi.phi_generate import initial_call as phi_initial_call
#from LLMs.dafny_generator.dafny_generate import generate_code as dafny_generate_code
from app.parse_json import save_intermediate_results, save_combined_json
from logs import setup_global_logger

# Setup global logger
logger = setup_global_logger()

# Define modes with model sequences
modes = {
    "mode_1": ["qwen2.5-coder-32b-inst", "llama-3.2-3b-inst"],
    "mode_2": ["phi-3-mini-128k-inst", "qwen2.5-coder-32b-inst"]
}

# Model-to-function mappings
llm_initial_generators = {
    'llama-3.2-3b-inst': llama_initial_call,
    'qwen2.5-coder-32b-inst': qwen_initial_call,
    'phi-3-mini-128k-inst': phi_initial_call
}

llm_feedback_generators = qwen_feedback_call

dafny_lang = ["C#", "Go", "Python", "Java", "JavaScript"]

class LLMManager:
    def __init__(self):
        self.modes = modes
        self.llm_initial_generators = llm_initial_generators
        self.llm_feedback_generators = llm_feedback_generators
        self.dafny_lang = dafny_lang

    def generate_initial_code(self, code_input, mode="mode_1"):
        if mode not in modes:
            logger.error(f"Invalid mode selected: {mode}. Choose either 'mode_1' or 'mode_2'.")
            raise ValueError("Invalid mode selected.")

        for model_name in modes[mode]:
            try:
                initial_generate_function = self.llm_initial_generators[model_name]
                initial_generated_code = initial_generate_function(code_input)
                if initial_generated_code:
                    logger.info(f"Code generated with {model_name} in {mode}")
            except Exception as e:
                logger.error(f"Error generating code with {model_name} in {mode}: {e}")

    def generate_feedback_code(self, chosen_mode):
        model_name = "qwen2.5-coder-32b-inst"
        try:
            feedback_generated_code = self.llm_feedback_generators()
            if feedback_generated_code:
                logger.info(f"Feedback generated with {model_name} in {chosen_mode}")
        except Exception as e:
            logger.error(f"Error in feedback generation with {model_name} in {chosen_mode}: {e}")

"""
    def generate_dafny_code(self, language, code_input):
        if language in self.dafny_lang:
            try:
                generated_code = dafny_generate_code(code_input)
                logger.info("Successfully generated Dafny code using OpenAI.")
                return generated_code
            except Exception as e:
                logger.error(f"Error generating Dafny code: {e}")
                raise
        else:
            return ""
"""
        
if __name__ == "__main__":
    llm_manager = LLMManager()
    #llm_manager.generate_initial_code(code_input="def twosum(nums, target):\n    nums.sort()\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\nif nums[i] + nums[j] == target:\n                return [j, i]\n    return []", mode="mode_1")
    llm_manager.generate_feedback_code("mode_1")