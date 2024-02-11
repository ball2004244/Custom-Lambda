from dotenv import load_dotenv
import os

load_dotenv()
FUNC_DELIMITER = os.getenv('FUNC_DELIMITER')

LINE_LIMIT = 10000