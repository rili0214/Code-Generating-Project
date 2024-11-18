import json
import logging
from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import API_TOKEN_qwen, qwen_system_prompt_initial, qwen_system_prompt_feedback, qwen_user_prompt_initial, qwen_user_prompt_feedback, load_json_data, prepare_messages, call_huggingface_chat, save_response_to_json
from logs import setup_logger

json_file_path = Path(__file__).parent.parent.parent / 'results' / 'intermediate' / 'qwen_analysis.json'

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_qwen)

model = "Qwen/Qwen2.5-Coder-32B-Instruct"

def initial_call(code_):
    """Initial call without JSON data."""
    system_prompt_ = qwen_system_prompt_initial
    user_prompt_ = qwen_user_prompt_initial
    
    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet=code_)
    logger.info("Qwen execution started.")

    response = call_huggingface_chat(model, messages)
    logger.info("Qwen execution completed.")

    if response:
        save_response_to_json(response, "qwen", "initial")
        return response
    return None

# Feedback Generation
def feedback_call():
    """Feedback call with additional JSON data."""
    system_prompt_ = qwen_system_prompt_feedback
    user_prompt_ = qwen_user_prompt_feedback

    additional_data_ = load_json_data(json_file_path)
    if not additional_data_:
        logger.error("No additional data loaded. Aborting feedback call.")
        return None

    messages = prepare_messages(system_prompt_, user_prompt_, additional_data=additional_data_)
    logger.info("Qwen execution started.")

    response = call_huggingface_chat(model, messages)
    logger.info("Qwen execution completed.")

    if response:
        save_response_to_json(response, "qwen", "feedback")
        return response
    return None

if __name__ == "__main__":
    initial_call("def twosum(nums, target):\n    nums.sort()\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\nif nums[i] + nums[j] == target:\n                return [j, i]\n    return []")
    
    feedback_call()
