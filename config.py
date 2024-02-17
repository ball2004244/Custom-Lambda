from dotenv import load_dotenv
import os

load_dotenv()
FUNC_DELIMITER = os.getenv('FUNC_DELIMITER')

# Length limits for function store files
LINE_LIMIT = 10000 # Max line per store

# Resource limits for 1 function invocation
MAX_STDOUT = 100 # Limit for terminal output
TIME_LIMIT = 300 # Seconds ~ 5 minutes
MEMORY_LIMIT = 1000000000 #Bytes ~ 1GB