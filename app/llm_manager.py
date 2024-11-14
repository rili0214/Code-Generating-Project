# llm_manager.py
import logging
import threading
from pathlib import Path
#from LLMs.azure_openai.openai_generate import azure_openai_generate_code as openai_generate_code
from LLMs.llama.llama_generate import initial_call as llama_initial_call
from LLMs.llama.llama_generate import feedback_call as llama_feedback_call
from LLMs.qwen.qwen_generate import initial_call as qwen_initial_call
from LLMs.qwen.qwen_generate import feedback_call as qwen_feedback_call
from LLMs.phi.phi_generate import initial_call as phi_initial_call
from LLMs.phi.phi_generate import feedback_call as phi_feedback_call
from LLMs.dafny_generator.dafny_generate import generate_code as dafny_generate_code
from logs import setup_global_logger

# Set up logging
logger = setup_global_logger()

# Mode-specific LLM sequences
modes = {
    "mode_1": ["qwen2.5-coder-32b-inst", "llama-3.2-3b-inst"],      # Fast, straightforward
    "mode_2": ["qwen2.5-coder-32b-inst", "phi-3-mini-128k-inst"],   # Slower, more functional
}

# Dictionary to map model names to their generate functions
llm_initial_generators = {
    'llama-3.2-3b-inst': llama_initial_call,
    'qwen2.5-coder-32b-inst': qwen_initial_call,
    'phi-3-mini-128k-inst': phi_initial_call
}

llm_feedback_generators = {
    'llama-3.2-3b-inst': llama_feedback_call,
    'qwen2.5-coder-32b-inst': qwen_feedback_call,
    'phi-3-mini-128k-inst': phi_feedback_call
}

def generate_initial_code(code_input, mode="mode_1"):
    """
    Generates initial code based on the selected mode.
    Mode 1: Fast and straightforward using Qwen and Llama.
    Mode 2: Slower but more functional using Phi and Qwen.
    """
    if mode not in modes:
        logger.error(f"Invalid mode selected: {mode}. Choose either 'mode_1' or 'mode_2'.")
        raise ValueError("Invalid mode. Choose either 'mode_1' or 'mode_2'.")

    for model_name in modes[mode]:
        try:
            initial_generate_function = llm_initial_generators[model_name]
            initial_generated_code = initial_generate_function(code_input)
            if initial_generated_code:
                logger.info(f"Successfully generated code with {model_name} in {mode}")
                return mode, initial_generated_code
            else:
                logger.warning(f"{model_name} in {mode} generated an empty or non-functional solution.")
        except Exception as e:
            logger.error(f"Error generating code with {model_name} in {mode}: {e}")

    logger.error("All models in the selected mode failed to generate code.")
    raise RuntimeError("Failed to generate code with the selected models in mode.")

def generate_feedback_code(code_input, chosen_mode):
    """
    Generates feedback code based on the selected mode and the results from checking phase.
    Mode 1: Fast and straightforward using Qwen and Llama.
    Mode 2: Slower but more functional using Phi and Qwen.
    """
    for model_name in modes[chosen_mode]:
        try:
            feedback_generate_function = llm_feedback_generators[model_name]
            feedback_generated_code = feedback_generate_function(code_input)
            if feedback_generated_code:
                logger.info(f"Successfully generated code with {model_name} in {chosen_mode}")
                return feedback_generated_code
            else:
                logger.warning(f"{model_name} in {chosen_mode} generated an empty or non-functional solution.")
        except Exception as e:
            logger.error(f"Error generating code with {model_name} in {chosen_mode}: {e}")

    logger.error("All models in the selected mode failed to generate code.")
    raise RuntimeError("Failed to generate code with the selected models in mode.")

def generate_dafny_with_LLM(code_input):
    """
    Specifically generates Dafny code using OpenAI, as per requirement.
    """
    try:
        generated_code = dafny_generate_code(code_input)
        logger.info("Successfully generated Dafny code using OpenAI.")
        return generated_code
    except Exception as e:
        logger.error(f"Error generating Dafny code: {e}")
        raise