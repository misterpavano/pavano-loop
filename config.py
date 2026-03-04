import json, os

# Kimi
KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "sk-hzhlGmz9zPArzEw9N8tqhc6PlpKIAJcIElB4pag8O59lFrZN")
KIMI_MODEL = "moonshot-v1-128k"
KIMI_BASE_URL = "https://api.moonshot.ai/v1/chat/completions"

# Anthropic
def get_anthropic_key():
    # Try env first, fall back to openclaw auth store
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    path = os.path.expanduser("~/.openclaw/agents/main/agent/auth-profiles.json")
    with open(path) as f:
        return json.load(f)["profiles"]["anthropic:pavano"]["token"]

ANTHROPIC_KEY = get_anthropic_key()
OPUS_MODEL = "claude-opus-4-5"
HAIKU_MODEL = "claude-haiku-4-5"
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/messages"

# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
CODEX_MODEL = "gpt-5.3-codex"
GPT5_MODEL = "gpt-5.2"
O3_MODEL = "o3"
OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"

MAX_ITERATIONS = 3
