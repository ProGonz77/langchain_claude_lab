from dotenv import load_dotenv
import os

load_dotenv()
print("Claude API key begins with:", os.getenv("ANTHROPIC_API_KEY", "")[:5], " ... ")
