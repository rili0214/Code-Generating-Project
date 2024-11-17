import json
import logging
from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import API_TOKEN_qwen, load_json_data, prepare_messages, call_huggingface_chat, save_response_to_json
from logs import setup_logger

json_file_path = Path(__file__).parent.parent.parent / 'results' / 'intermediate' / 'qwen_analysis.json'

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_qwen)

model = "Qwen/Qwen2.5-Coder-32B-Instruct"

def initial_call(code_):
    """Initial call without JSON data."""
    system_prompt = "You are a code debugging assistant. Just give the debugged code. No need to explain your code!"
    user_prompt = "Please fix the issues in the following code:"
    code_input = code_

    messages = prepare_messages(system_prompt, user_prompt, code_snippet = code_input)
    response = call_huggingface_chat(model, messages)

    save_response_to_json(response, "qwen", "qwen_initial")

def feedback_call(code_, better_model_):
    """Feedback call that includes additional JSON data."""
    system_prompt = "You are a code debugging assistant with additional analysis results. Just give the debugged code. No need to explain your code!"
    user_prompt = "Please enhance and debug the code with the given static, dynamic, and formal analysis results."
    code_input = code_

    additional_data = load_json_data(json_file_path)
    if not additional_data:
        logger.error("No additional data loaded. Aborting feedback call.")
        return None

    messages = prepare_messages(system_prompt, user_prompt, code_snippet = code_input, additional_data = additional_data)
    response = call_huggingface_chat(model, messages)

    save_response_to_json(response, "qwen", "qwen_feedback")

if __name__ == "__main__":
    logger.info("Qwen execution started.")

    initial_call("def add(a, b): return a + b")
    
    feedback_call("def add(a, b): return a + b")

    logger.info("Qwen execution completed.")