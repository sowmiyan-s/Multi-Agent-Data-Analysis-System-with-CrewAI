import re

path = 'web/app.js'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add to MODEL_OPTIONS
if 'custom: [' not in c:
    c = c.replace(
        "ollama:      ['ollama/llama3','ollama/mistral','ollama/gemma2'],",
        "ollama:      ['ollama/llama3','ollama/mistral','ollama/gemma2'],\n  custom:      ['custom/model'],"
    )

# Add to DOM elements
if 'urlCustom:' not in c:
    c = c.replace(
        "urlOllama:                $('urlOllama'),",
        "urlOllama:                $('urlOllama'),\n  urlCustom:                $('urlCustom'),\n  keyCustom:                $('keyCustom'),\n  showCustom:               $('showCustom'),"
    )

# Add to PROVIDERS array if exists
if "{ id: 'custom'" not in c:
    c = c.replace(
        "{ id: 'ollama', name: 'Ollama (local)' }",
        "{ id: 'ollama', name: 'Ollama (local)' },\n  { id: 'custom', name: 'Custom API' }"
    )

# Add to default keys
if 'custom:' not in c and "ollama: 'ollama/llama3'" in c:
    c = c.replace(
        "ollama: 'ollama/llama3',",
        "ollama: 'ollama/llama3',\n  custom: 'custom/model',"
    )

# Update api_url loading
if 'api_url_custom' not in c:
    c = c.replace(
        "els.urlOllama.value = localStorage.getItem('api_url_ollama') || 'http://localhost:11434';",
        "els.urlOllama.value = localStorage.getItem('api_url_ollama') || 'http://localhost:11434';\n  els.urlCustom.value = localStorage.getItem('api_url_custom') || 'https://api.openai.com/v1';\n  els.keyCustom.value = localStorage.getItem('api_key_custom') || '';"
    )
    c = c.replace(
        "localStorage.setItem('api_url_ollama', els.urlOllama.value.trim());",
        "localStorage.setItem('api_url_ollama', els.urlOllama.value.trim());\n  localStorage.setItem('api_url_custom', els.urlCustom.value.trim());\n  localStorage.setItem('api_key_custom', els.keyCustom.value.trim());"
    )

# Target input for Custom
if 'els.keyCustom' not in c and 'els.urlOllama' in c:
    c = c.replace(
        "else if (provider === 'ollama') targetInput = els.urlOllama;",
        "else if (provider === 'ollama') targetInput = els.urlOllama;\n    else if (provider === 'custom') targetInput = els.keyCustom;"
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
