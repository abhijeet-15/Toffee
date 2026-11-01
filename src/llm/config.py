from .models import Provider

PROVIDERS = [
    Provider("OpenAI", "OPENAI_API_KEY", False, "OPENAI_LLM_MODEL", "OPENAI_BASE_URL"),
    Provider("GroqAI", "GROQ_API_KEY", False, "GROQ_LLM_MODEL", "GROQ_BASE_URL"),
]