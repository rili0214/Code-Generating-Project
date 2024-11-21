#############################################################################################################################
# Program: LLMs.dafny_generator.dafny_generate.py                                                                           #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program use Azure OpenAI API(GPT-4-Turbo) to generate Dafny code.                                       #                                                                                                 
#############################################################################################################################

import openai
from pathlib import Path
from LLMs.base_llm import (
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_DEPLOYMENT, 
    AZURE_API_VERSION, 
    dafny_system_prompt, 
    dafny_user_prompt, 
    save_response_to_txt)
from logs import setup_logger

# Setup logging
logger = setup_logger()

openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_type = "azure"
openai.api_version = AZURE_API_VERSION

# Set the path to save the generated Dafny code
dafny_path = str(Path(__file__).parent.parent / 'results' / 'openai_results' / 'dafny_output.txt')

def generate_dafny_code(code_input):
    """
    Generate Dafny code for formal verification using Azure OpenAI API.

    params:
        code_input (str): Source code for which Dafny code is generated.
        system_prompt (str, optional): System-level instructions for the model.
        user_prompt (str, optional): User-level instructions for the model.

    returns:
        str: Generated Dafny code.

    raises:
        Exception: If an error occurs during Dafny code generation.
    """
    system_prompt = dafny_system_prompt
    user_prompt = dafny_user_prompt
    
    try:
        prompt_parts = []
        if system_prompt:
            prompt_parts.append(f"System: {system_prompt}")
        if user_prompt:
            prompt_parts.append(f"User: {user_prompt}")
        prompt_parts.append(f"Code Input:\n{code_input}")
        full_prompt = "\n\n".join(prompt_parts)

        logger.info("Sending request to Azure OpenAI API.")
        response = openai.Completion.create(
            engine = AZURE_OPENAI_DEPLOYMENT,
            prompt = full_prompt,
            max_tokens = 300,  
            temperature = 0.5 
        )
        generated_text = response.choices[0].text.strip()

        if response:
            save_response_to_txt(response, dafny_path)
            return response
        logger.info("Successfully generated Dafny code from OpenAI.")

        return generated_text
    
    except Exception as e:
        logger.error(f"Error during Dafny code generation: {e}")
        raise