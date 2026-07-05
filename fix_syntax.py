import sys

with open('web/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Revert my previous FormData modification
c = c.replace("\n    fd.append('custom_base_url', localStorage.getItem('api_url_custom') || '');", "")

# In saveSettings:
c = c.replace('els.apiKey.value = apiKey;', """
  if (provider === 'custom') {
    const customUrl = els.urlCustom.value.trim() || 'https://api.openai.com/v1';
    apiKey = customUrl + '|' + apiKey;
  }
  els.apiKey.value = apiKey;
""")

# In testIndividualConnection
c = c.replace('const apiKey = targetInput.value.trim();', """
  let apiKey = targetInput.value.trim();
  if (provider === 'custom') {
    const customUrl = els.urlCustom.value.trim() || 'https://api.openai.com/v1';
    apiKey = customUrl + '|' + apiKey;
  }
""")

with open('web/app.js', 'w', encoding='utf-8') as f:
    f.write(c)

# Now update config/llm_config.py to parse this combo key
with open('config/llm_config.py', 'r', encoding='utf-8') as f:
    c_llm = f.read()

# I need to add a parser right inside get_llm_config or get_llm_params
inject = """
    if provider == "custom" and api_key and "|" in api_key:
        parts = api_key.split("|", 1)
        os.environ["CUSTOM_BASE_URL"] = parts[0]
        api_key = parts[1]
"""
# We'll inject this at the beginning of validate_llm_connection and apply_runtime_llm_settings
if 'parts = api_key.split("|", 1)' not in c_llm:
    c_llm = c_llm.replace(
        'def apply_runtime_llm_settings(\n    provider: str,\n    model: str,\n    api_key: str = "",\n    env_key_name: str = "",\n) -> None:\n    """Inject provider/model/key into context variables before agent execution."""',
        'def apply_runtime_llm_settings(\n    provider: str,\n    model: str,\n    api_key: str = "",\n    env_key_name: str = "",\n) -> None:\n    """Inject provider/model/key into context variables before agent execution."""\n' + inject
    )
    
    c_llm = c_llm.replace(
        'def validate_llm_connection(provider: str, model: str, api_key: str = "") -> dict:\n    """\n    Ping the configured LLM with a minimal prompt.\n    Returns {"valid": bool, "message": str}.\n    """',
        'def validate_llm_connection(provider: str, model: str, api_key: str = "") -> dict:\n    """\n    Ping the configured LLM with a minimal prompt.\n    Returns {"valid": bool, "message": str}.\n    """\n' + inject
    )

with open('config/llm_config.py', 'w', encoding='utf-8') as f:
    f.write(c_llm)
