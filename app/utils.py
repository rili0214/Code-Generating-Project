import logging

def setup_logger():
    logging.basicConfig(filename='logs/logs.txt', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def format_output(llm_name, code, language, dafny_code):
    return {
        "model": llm_name,
        "code": code,
        "language": language,
        "dafny_code": dafny_code
    }
