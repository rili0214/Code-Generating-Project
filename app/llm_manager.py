# llm_manager.py
import logging
from pathlib import Path
from LLMs.azure_openai.openai_generate import azure_openai_generate_code
from LLMs.llama.generate import generate_code as llama_generate_code
from LLMs.qwen.generate import generate_code as qwen_generate_code
from LLMs.dafny_generator.dafny_generate import generate_code as dafny_generate_code

# Set up logging
log_file_path = Path(__file__).parent.parent / 'logs' / 'logs.txt'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dictionary to map model names to their generate functions
llm_generators = {
    'llama_3_1_70B_Inst': llama_generate_code,
    'qwen2_5_72B_instruct': qwen_generate_code,
    'openai_gpt4o_mini': azure_openai_generate_code
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