import logging
from pathlib import Path

def setup_logger():
    log_file_path = Path(__file__).parent.parent / 'logs' / 'app.log'
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def setup_global_logger():
    log_file_path = Path(__file__).parent.parent / 'logs' / 'logs.txt'
    logging.basicConfig(
        filename=log_file_path, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)