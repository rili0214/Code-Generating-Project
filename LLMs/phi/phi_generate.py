from huggingface_hub import InferenceClient
from pathlib import Path
from LLMs.base_llm import API_TOKEN_phi, system_prompt, user_prompt, prepare_messages, call_huggingface_chat, save_response_to_json
from logs import setup_logger

phi_initial_path = str(Path(__file__).parent.parent / 'results' / 'phi_results' / 'phi_initial_results.json')

# Logging Configuration
logger = setup_logger()

# Configuration Constants
client = InferenceClient(api_key = API_TOKEN_phi)

model = "microsoft/Phi-3-mini-128k-instruct"

def initial_call(mode, code_, language):
    system_prompt_ = system_prompt
    user_prompt_ = user_prompt
    code_input_ = code_

    messages = prepare_messages(system_prompt_, user_prompt_, code_snippet = code_input_)
    logger.info("Phi execution started.")

    response = call_huggingface_chat(model, messages)
    logger.info("Phi execution completed.")

    if response:
        save_response_to_json(mode=mode, model="phi", generated_code=response, call_type="phi_initial", language=language)
        logger.info("Generated Phi output saved to " + phi_initial_path)
    else:
        logger.error("Failed to generate Phi output.")
    

if __name__ == "__main__":
    code = "def twosum(nums, target):\n    nums.sort()\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\nif nums[i] + nums[j] == target:\n                return [j, i]\n    return []"
    initial_call(mode="mode_1", code_=code, language="Python")