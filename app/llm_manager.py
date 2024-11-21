#############################################################################################################################
# Program: llm_manager.py                                                                                                   #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program manages the LLM interactions and code generation.                                               #                                                                                                 
#############################################################################################################################

from pathlib import Path
from LLMs.qwen.qwen_generate import (
    initial_call as qwen_initial_call, 
    feedback_call as qwen_feedback_call, 
    qwen_initial_path, 
    generate_final_report)
from LLMs.llama.llama_generate import initial_call as llama_initial_call, llama_initial_path
from LLMs.phi.phi_generate import initial_call as phi_initial_call, phi_initial_path
from LLMs.dafny_generator.dafny_generate import generate_dafny_code
from logs import setup_global_logger

# The final analysis file which is used for final output
final_analysis_path = Path(__file__).parent.parent / 'results' / 'final_analysis.json'

# Setup global logger
logger = setup_global_logger()

# Define modes with model sequences
# mode_1: Primarily qwen2.5-coder-32b-inst, supplementally llama-3.2-3b-inst
# mode_2: Primarily qwen2.5-coder-32b-inst, supplementally phi-3-mini-128k-inst
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

# Function that calls the feedback generator
llm_feedback_generators = qwen_feedback_call

# List of Dafny supported languages
dafny_lang = ["C#", "Go", "Python", "Java", "JavaScript"]

"""
LLMManager class:
This class manages the LLM interactions and code generation.
"""
class LLMManager:
    def __init__(self):
        """
        Initializes the LLMManager class.
        
        paras:
            modes (dict): A dictionary mapping modes to model sequences.
            llm_initial_generators (dict): A dictionary mapping model names to function calls.
            llm_feedback_generators (function): A function that calls the feedback generator.
            dafny_lang (list): A list of Dafny supported languages.
            generate_final_report (function): A function that generates the final report.
        """
        self.modes = modes
        self.llm_initial_generators = llm_initial_generators
        self.llm_feedback_generators = llm_feedback_generators
        self.dafny_lang = dafny_lang
        self.generate_final_report = generate_final_report

    def generate_initial_code(self, code_input, mode="mode_1", language="Python"):
        """
        Generates initial code using the specified mode and language.
        
        paras:
            code_input (str): The input code to generate initial code for.
            mode (str, optional): The mode to use for code generation. Default is "mode_1".
            language (str, optional): The programming language for code generation. Default is "Python".
            
        returns:
            str: The generated initial code.
            
        raises:
            ValueError: If an invalid mode is selected.
            Exception: If an error occurs during code generation.
        """
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
        """
        Generates feedback code using the specified mode and language.
        
        paras:
            chosen_mode (str, optional): The mode to use for feedback code generation. Default is "mode_1".
            language (str, optional): The programming language for feedback code generation. Default is "Python".
            
        returns:
            str: The generated feedback code.
            
        raises:
            Exception: If an error occurs during feedback code generation.
        """
        model_name = "qwen2.5-coder-32b-inst"
        try:
            feedback_generated_code = self.llm_feedback_generators(mode = chosen_mode, language = language)
            if feedback_generated_code:
                logger.info(f"Global: Feedback generated with {model_name} in {chosen_mode}")
        except Exception as e:
            logger.error(f"Global: Error in feedback generation with {model_name} in {chosen_mode}: {e}")

    def generate_gpt_dafny_code(self, language, code_input, mode="mode_1"):
        """
        Generates Dafny code using the OpenAI API.
        
        paras:
            language (str): The programming language for Dafny code generation.
            code_input (str): The input code to generate Dafny code for.
            mode (str, optional): The mode to use for Dafny code generation. Default is "mode_1".
            
        returns:
            str: The generated Dafny code.
            
        raises:
            Exception: If an error occurs during Dafny code generation.
        """
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
        
    def finalize_output(self):
        """
        Finalizes the output by generating the final report.
        
        raises:
            Exception: If an error occurs during final report generation.
        """
        try:
            self.generate_final_report()
            logger.info("Global: Final report generated successfully.")
        except Exception as e:
            logger.error(f"Global: Error generating final report: {e}")

if __name__ == "__main__":
    llm_manager = LLMManager()
    code = "def fibonacci(n):\n    if n <= 0:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)"
    llm_manager.generate_initial_code(code, mode = "mode_1", language = "Python")
    llm_manager.generate_feedback_code(chosen_mode = "mode_1", language = "Python")