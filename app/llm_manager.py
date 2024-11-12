# llm_manager.py
import logging
from pathlib import Path
from generator import azure_openai_generate_code
from LLMs.llama_31_nemotron_70b.generate import generate_code as llama_generate_code
from LLMs.deepseek_coder_v2.generate import generate_code as deepseek_generate_code
from LLMs.qwen2_5_72b_instruct.generate import generate_code as qwen_generate_code

# Set up logging
log_file_path = Path(__file__).parent.parent / 'logs' / 'logs.txt'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define a dictionary to map model names to their generate functions
llm_generators = {
    'llama_31_nemotron_70b': llama_generate_code,
    'deepseek_coder_v2': deepseek_generate_code,
    'qwen2_5_72b_instruct': qwen_generate_code,
    'azure_openai_gpt4': azure_openai_generate_code  # New option for Azure's GPT-4 model
}

def generate_code_with_llms(code_input, model_name):
    try:
        if model_name == 'azure_openai_gpt4':
            generated_code = azure_openai_generate_code(code_input)
        else:
            generate_function = llm_generators[model_name]
            generated_code = generate_function(code_input)
        logger.info(f"Successfully generated code with {model_name}")
        return generated_code
    except KeyError:
        logger.error(f"Unsupported LLM model: {model_name}")
        raise
    except Exception as e:
        logger.error(f"Error generating code with {model_name}: {e}")
        raise
