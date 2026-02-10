import os

import input_content
from dotenv import load_dotenv
load_dotenv()

print(os.environ.get("GEMINI_API_KEY"))