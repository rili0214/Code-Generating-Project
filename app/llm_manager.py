# app/llm_manager.py
from llms.llama_31_nemotron_70b.generate import generate_code as llama_generate
from llms.deepseek_coder_v2.generate import generate_code as deepseek_generate
from llms.qwen2_5_72b_instruct.generate import generate_code as qwen_generate
from llms.dafny_generator.dafny_generate import generate_dafny_code

class LLMManager:
    def __init__(self):
        self.llms = {
            "Llama-3.1-Nemotron-70B": llama_generate,
            "DeepSeek-Coder-V2": deepseek_generate,
            "Qwen2.5-72B": qwen_generate
        }

    def generate_initial(self, code, language):
        results = {}
        for name, generate_fn in self.llms.items():
            debugged_code = generate_fn(code)
            dafny_code = generate_dafny_code(debugged_code)
            results[name] = {
                "code": debugged_code,
                "language": language,
                "dafny_code": dafny_code
            }
        return results