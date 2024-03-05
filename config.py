from dotenv import load_dotenv
import os

load_dotenv()
FUNC_DELIMITER = os.getenv('FUNC_DELIMITER')

# Length limits for function store files
LINE_LIMIT = 10000  # Max line per store
MAX_UPLOAD_SIZE = 5 * (2**20)  # Bytes ~ 5MiB

# Resource limits for 1 function invocation
MAX_STDOUT = 100  # Limit for terminal output
TIME_LIMIT = 300  # Seconds ~ 5 minutes
MEMORY_LIMIT = 2**30  # Bytes ~ 1GiB

FUNC_STORE = 'functions_store'
CONF_STORE = 'config_store'
