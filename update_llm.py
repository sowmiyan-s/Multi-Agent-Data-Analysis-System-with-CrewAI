import re
path = 'config/llm_config.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add custom to configs
inject = '''
        "custom": {
            "model":   os.getenv("LLM_MODEL", "custom/model"),
            "api_key": current_llm_api_key.get() or os.getenv("CUSTOM_API_KEY", ""),
            "base_url": os.getenv("CUSTOM_BASE_URL"),
        },
'''
if '"custom": {' not in c:
    c = c.replace('"openai": {', inject.lstrip() + '        "openai": {')

# Add custom to requires_key
c = c.replace('"openrouter", "deepseek", "perplexity"', '"openrouter", "deepseek", "perplexity", "custom"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
