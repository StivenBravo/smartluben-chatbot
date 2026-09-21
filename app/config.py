import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv(
    "DEEPSEEK_BASE_URL",
    "https://api.deepseek.com"
)
DEEPSEEK_MODEL = os.getenv(
    "DEEPSEEK_MODEL",
    "deepseek-chat"
)
print(
    "API Key cargada:",
    DEEPSEEK_API_KEY[:6] + "..." if DEEPSEEK_API_KEY else "NO CARGADA"
)
CORE_API_URL = os.getenv(
    "CORE_API_URL",
    "http://127.0.0.1:8000/api"
)