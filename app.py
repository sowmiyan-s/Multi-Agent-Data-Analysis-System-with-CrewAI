import streamlit as st
import pandas as pd
import os
from pathlib import Path
import sys
import contextlib
import html
import json
import re
import glob
from PIL import Image
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from crew import run_crew

# Disable CrewAI Telemetry
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Set page config
st.set_page_config(
    page_title="Agentic Data Analyst | Premium BI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #8b5cf6;
        --secondary: #06b6d4;
        --bg-dark: #0f172a;
        --card-bg: #1e293b;
        --text-main: #f8fafc;
        --text-dim: #94a3b8;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.025em;
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #a78bfa, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: none;
        letter-spacing: 0.025em;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.3);
        background: linear-gradient(135deg, #a78bfa 0%, #818cf8 100%);
    }

    /* Status Indicator */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .status-active { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }

    /* Insight Cards */
    .insight-card {
        border-left: 4px solid #8b5cf6;
        background: rgba(139, 92, 246, 0.05);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def parse_relations(text):
    """Parses relations from the agent's output."""
    relations = []
    lines = text.split('\n')
    for line in lines:
        # Match pattern: X: [col] | Y: [col] | Type: [plot]
        match = re.search(r"X:\s*(.*?)\s*\|\s*Y:\s*(.*?)\s*\|\s*Type:\s*(.*)", line)
        if match:
            relations.append({
                'x': match.group(1).strip(),
                'y': match.group(2).strip(),
                'type': match.group(3).strip()
            })
    return relations

def render_dynamic_visualizations(df, relations):
    """Renders visualizations based on agent suggestions."""
    if not relations:
        st.info("The Relationship Mapper didn't suggest specific plots, using default analysis.")
        return False

    cols = st.columns(2)
    for i, rel in enumerate(relations):
        with cols[i % 2]:
            st.markdown(f"#### Sugggestion {i+1}: {rel['x']} vs {rel['y']}")
            try:
                plot_type = rel['type'].lower()
                fig = None
                
                if 'scatter' in plot_type:
                    fig = px.scatter(df, x=rel['x'], y=rel['y'], color_discrete_sequence=['#8b5cf6'], template="plotly_dark")
                elif 'bar' in plot_type:
                    fig = px.bar(df, x=rel['x'], y=rel['y'], color_discrete_sequence=['#06b6d4'], template="plotly_dark")
                elif 'line' in plot_type:
                    fig = px.line(df, x=rel['x'], y=rel['y'], color_discrete_sequence=['#f59e0b'], template="plotly_dark")
                elif 'box' in plot_type:
                    fig = px.box(df, x=rel['x'], y=rel['y'], color_discrete_sequence=['#ec4899'], template="plotly_dark")
                
                if fig:
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning(f"Unsupported plot type: {rel['type']}")
            except Exception as e:
                st.error(f"Error plotting {rel['x']} vs {rel['y']}: {e}")
    return True

import io

# Ensure UTF-8 encoding for terminal output to prevent UnicodeEncodeErrors
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        # Fallback if Streamlit's wrapped stdout doesn't support reconfigure
        pass

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='color: #a78bfa;'>💎 Configuration</h2>", unsafe_allow_html=True)
        
        provider = st.selectbox("LLM Provider", ["nvidia", "groq", "openai", "gemini", "anthropic"], index=0)
        
        model_map = {
            "nvidia": ["nvidia_nim/mistralai/mistral-medium-3.5-128b", "nvidia_nim/mistralai/mistral-large-2407"],
            "groq": ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant"],
            "openai": ["gpt-4o", "gpt-4o-mini"],
            "gemini": ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"],
            "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"]
        }
        
        selected_model = st.selectbox("Model Selection", model_map[provider])
        
        # Respect existing environment variables
        env_key_name = f"{provider.upper()}_API_KEY"
        existing_key = os.getenv(env_key_name, "")
        
        api_key = st.text_input(f"{provider.upper()} API Key", value=existing_key, type="password")
        
        if api_key:
            os.environ[env_key_name] = api_key.strip()
        
        os.environ["LLM_PROVIDER"] = provider
        os.environ["LLM_MODEL"] = selected_model

        st.markdown("---")
        st.markdown("""
            <div style='font-size: 0.8rem; color: #94a3b8;'>
                <b>Agentic Data Analyst v2.0</b><br>
                Powered by CrewAI & Plotly
            </div>
        """, unsafe_allow_html=True)

    # Main Header
    st.markdown("<h1 class='main-title'>Agentic Data Analyst</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>The next generation of autonomous business intelligence.</p>", unsafe_allow_html=True)

    # File Upload
    uploaded_file = st.file_uploader("Drop your CSV here", type=['csv'])

    if uploaded_file:
        file_path = Path("data") / uploaded_file.name
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        session_key = f"analysis_{uploaded_file.name}"
        
        # Ensure session state has all required keys (handles stale state)
        if session_key not in st.session_state or not isinstance(st.session_state[session_key], dict) or 'relation' not in st.session_state[session_key]:
            st.session_state[session_key] = {
                'clean': None,
                'validate': None,
                'relation': None,
                'insights': None,
                'dataframe': pd.read_csv(file_path),
                'status': 'idle'
            }

        # Tabs for real-time results
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Data Explorer", "🧹 Cleaning Report", "💡 Strategic Insights"])

        with tab2:
            st.markdown("### 🔍 Dataset Explorer")
            st.dataframe(st.session_state[session_key]['dataframe'].head(100), use_container_width=True)
            st.markdown("#### Statistical Overview")
            st.write(st.session_state[session_key]['dataframe'].describe())

        # Placeholder containers
        dash_container = tab1.empty()
        clean_container = tab3.empty()
        insight_container = tab4.empty()

        # Update displays from session state
        def update_displays():
            data = st.session_state[session_key]
            df = data.get('dataframe')

            # Error Display
            if data.get('status') == 'error':
                st.error(f"⚠️ Analysis Error: {data.get('error')}")
                if st.button("🔄 Reset & Retry"):
                    st.session_state[session_key]['status'] = 'idle'
                    st.session_state[session_key]['error'] = None
                    st.rerun()

            # Pipeline Status (Dynamic Placeholders)
            st.markdown("### 🛠 Pipeline Status")
            status_cols = st.columns(4)
            status_placeholders = [col.empty() for col in status_cols]
            
            steps = [
                ('clean', '🧹 Cleaning'),
                ('validate', '✅ Validation'),
                ('relation', '📊 Relations'),
                ('insights', '💡 Insights')
            ]

            def draw_pipeline():
                for i, (key, label) in enumerate(steps):
                    has_data = st.session_state[session_key].get(key)
                    status_color = "#4ade80" if has_data else "#94a3b8"
                    status_placeholders[i].markdown(f"""
                        <div style='text-align: center; padding: 10px; border-radius: 10px; border: 1px solid {status_color}; color: {status_color}; background: rgba(255,255,255,0.02);'>
                            {label}<br>{'✅' if has_data else '⏳'}
                        </div>
                    """, unsafe_allow_html=True)

            draw_pipeline()

            # Dashboard
            with dash_container.container():
                if data.get('relation'):
                    st.markdown("### 📈 Visual Intelligence")
                    rel_data = data.get('relation')
                    relations = parse_relations(rel_data.raw if hasattr(rel_data, 'raw') else str(rel_data))
                    render_dynamic_visualizations(df, relations)
                    
                    st.markdown("---")
                    c1, c2 = st.columns(2)
                    with c1:
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Cleaned Dataset", data=csv, file_name="cleaned_data.csv", mime="text/csv")
                    with c2:
                        report_text = f"ANALYSIS REPORT\n\nCleaning:\n{data.get('clean')}\n\nValidation:\n{data.get('validate')}\n\nInsights:\n{data.get('insights')}"
                        st.download_button("📄 Download Analysis Report", data=report_text, file_name="analysis_report.txt", mime="text/plain")
                elif data.get('status') == 'running':
                    st.info("⌛ Waiting for Relationship Mapper agent...")

            # Cleaning
            with clean_container.container():
                if data.get('clean'):
                    st.markdown("### 🧹 Data Cleaning Report")
                    clean_data = data.get('clean')
                    st.markdown(f"<div class='glass-card'>{clean_data.raw if hasattr(clean_data, 'raw') else str(clean_data)}</div>", unsafe_allow_html=True)
                
                if data.get('validate'):
                    st.markdown("#### ✅ Validation Decision")
                    val_data = data.get('validate')
                    val = val_data.raw if hasattr(val_data, 'raw') else str(val_data)
                    color = "#4ade80" if "YES" in val.upper() else "#f87171"
                    st.markdown(f"<div style='border-left: 4px solid {color}; padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 8px;'>{val}</div>", unsafe_allow_html=True)

            # Insights
            with insight_container.container():
                if data.get('insights'):
                    st.markdown("### 💡 Strategic Business Insights")
                    insights_data = data.get('insights')
                    insights_text = insights_data.raw if hasattr(insights_data, 'raw') else str(insights_data)
                    for insight in insights_text.split('\n'):
                        if insight.strip():
                            st.markdown(f"<div class='insight-card'>{insight}</div>", unsafe_allow_html=True)
                elif data.get('status') == 'running':
                    st.info("⌛ Business Strategist is synthesizing insights...")

            return draw_pipeline # Return the function to use in callbacks

        draw_pipeline_fn = update_displays()

        if st.session_state[session_key]['status'] == 'idle':
            if st.button("🚀 Start Autonomous Analysis", use_container_width=True):
                st.session_state[session_key]['status'] = 'running'
                st.rerun()
        
        elif st.session_state[session_key]['status'] == 'running':
            # Background execution
            def task_callback(task_name, output):
                st.session_state[session_key][task_name] = output
                # Live update the pipeline status during the callback
                draw_pipeline_fn()

            with st.status("🤖 AI Agents at work...", expanded=True) as status:
                log_container = st.empty()
                logs = []
                class Logger:
                    def write(self, m):
                        if m.strip():
                            logs.append(html.escape(m))
                            log_container.markdown(f"<div style='height: 150px; overflow-y: auto; background: #000; color: #0f0; padding: 10px; font-family: monospace; font-size: 0.7rem;'>{'$ ' + '<br>$ '.join(logs[-5:])}</div>", unsafe_allow_html=True)
                    def flush(self): pass

                with contextlib.redirect_stdout(Logger()):
                    try:
                        result = run_crew(str(file_path), task_callback=task_callback)
                        if result and result.get('status') == 'complete':
                            st.session_state[session_key]['status'] = 'complete'
                            status.update(label="✅ All Agents Finished!", state="complete", expanded=False)
                        else:
                            st.session_state[session_key]['status'] = 'error'
                            st.session_state[session_key]['error'] = result.get('error', 'Unknown error')
                            status.update(label="❌ Analysis Failed", state="error")
                        st.rerun()
                    except Exception as e:
                        st.session_state[session_key]['status'] = 'error'
                        st.session_state[session_key]['error'] = str(e)
                        st.error(f"Analysis failed: {e}")
                        status.update(label="❌ Analysis Failed", state="error")
                        st.rerun()

    if st.sidebar.button("🗑 Clear All Session History"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
