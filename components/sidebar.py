import streamlit as st
import os
from config.app_config import settings

def render_sidebar():
    with st.sidebar:
        st.markdown(f"<h2 style='color: var(--secondary);'>💎 Settings</h2>", unsafe_allow_html=True)
        
        provider = st.selectbox(
            "Intelligence Provider", 
            ["openai", "groq", "anthropic", "nvidia", "gemini"], 
            index=0,
            help="Choose the LLM backend for the agents."
        )
        
        model_map = {
            "openai": ["gpt-4o", "gpt-4o-mini"],
            "groq": ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant"],
            "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"],
            "nvidia": ["nvidia_nim/mistralai/mistral-medium-3.5-128b"],
            "gemini": ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"]
        }
        
        selected_model = st.selectbox("Model Tier", model_map[provider])
        
        # API Key management
        env_key_name = f"{provider.upper()}_API_KEY"
        existing_key = os.getenv(env_key_name, "")
        
        api_key = st.text_input(f"{provider.upper()} API Key", value=existing_key, type="password")
        
        if api_key:
            os.environ[env_key_name] = api_key.strip()
            os.environ["LLM_PROVIDER"] = provider
            os.environ["LLM_MODEL"] = selected_model

        st.markdown("---")
        st.markdown(f"""
            <div style='font-size: 0.85rem; color: var(--text-dim);'>
                <b>{settings.APP_NAME}</b><br>
                Version {settings.VERSION}<br>
                <span style='color: var(--primary);'>●</span> Production Grade
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
