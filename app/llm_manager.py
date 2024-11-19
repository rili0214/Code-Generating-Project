from pathlib import Path
import json
from LLMs.qwen.qwen_generate import initial_call as qwen_initial_call, feedback_call as qwen_feedback_call, qwen_initial_path, qwen_feedback_path
from LLMs.llama.llama_generate import initial_call as llama_initial_call, llama_initial_path
from LLMs.phi.phi_generate import initial_call as phi_initial_call, phi_initial_path
from LLMs.dafny_generator.dafny_generate import generate_dafny_code, dafny_path
from logs import setup_global_logger

# Setup global logger
logger = setup_global_logger()

# Define modes with model sequences
modes = {
    "mode_1": ["qwen2.5-coder-32b-inst", "llama-3.2-3b-inst"],
    #"mode_2": ["phi-3-mini-128k-inst", "qwen2.5-coder-32b-inst"]
    "mode_2": ["qwen2.5-coder-32b-inst", "llama-3.2-3b-inst"]
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

    def generate_initial_code(self, code_input, mode="mode_1", language="Python"):
        if mode not in modes:
            logger.error(f"Invalid mode selected: {mode}. Choose either 'mode_1' or 'mode_2'.")
            raise ValueError("Invalid mode selected.")

        for model_name in modes[mode]:
            try:
                initial_generate_function = self.llm_initial_generators[model_name]
                initial_generated_code = initial_generate_function(mode = mode, code_ = code_input, language = language)
                if initial_generated_code:
                    logger.info(f"Global: Code generated with {model_name} in {mode}")
            except Exception as e:
                logger.error(f"Global: Error generating code with {model_name} in {mode}: {e}")

    def generate_feedback_code(self, chosen_mode="mode_1", language="Python"):
        model_name = "qwen2.5-coder-32b-inst"
        try:
            feedback_generated_code = self.llm_feedback_generators(mode=chosen_mode, language=language)
            if feedback_generated_code:
                logger.info(f"Global: Feedback generated with {model_name} in {chosen_mode}")
        except Exception as e:
            logger.error(f"Global: Error in feedback generation with {model_name} in {chosen_mode}: {e}")

    def generate_gpt_dafny_code(self, language, code_input, mode="mode_1"):
        if language in self.dafny_lang:
            try:
                generated_dafny_code = generate_dafny_code(code_input)
                logger.info("Successfully generated Dafny code using OpenAI.")
                if mode == "mode_1":
                    llama_initial_path["dafny_text"] = generated_dafny_code
                elif mode == "mode_2":
                    phi_initial_path["dafny_text"] = generated_dafny_code
                qwen_initial_path["dafny_text"] = generated_dafny_code

            except Exception as e:
                logger.error(f"Error generating Dafny code: {e}")
        
    def finalize_output(self, path_):
        with open(path_, 'r') as file:
            feedback_data = json.load(file)
        return feedback_data
        


if __name__ == "__main__":
    llm_manager = LLMManager()
    code = "def fibonacci(n):\n    if n <= 0:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)"
    llm_manager.generate_initial_code(code, mode="mode_1", language="Python")
    #llm_manager.generate_feedback_code(chosen_mode="mode_1", language="Python")