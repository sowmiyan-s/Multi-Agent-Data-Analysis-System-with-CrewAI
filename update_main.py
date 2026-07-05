import re
import os

path = 'main.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace endpoint parameters to add custom_base_url
c = c.replace('api_key: Optional[str] = Form(""),', 'api_key: Optional[str] = Form(""),\n    custom_base_url: Optional[str] = Form(""),')

# Before _load_crew() in these endpoints, set the env var
inject = """
    if custom_base_url:
        import os
        os.environ["CUSTOM_BASE_URL"] = custom_base_url
"""
c = c.replace('    _load_crew()', inject + '    _load_crew()')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
