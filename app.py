import streamlit as st
import pandas as pd
import os
import json
import re
from pathlib import Path
from utils.logger import app_logger
from config.app_config import settings
from crew import run_analysis_pipeline
from components.sidebar import render_sidebar
import plotly.express as px

def render_visualizations(df, viz_specs_raw):
    """Parses JSON viz specs and renders them using Plotly."""
    try:
        # Clean the raw string (sometimes agents wrap JSON in markdown blocks)
        clean_json = re.sub(r"```json\n?|\n?```", "", str(viz_specs_raw)).strip()
        specs = json.loads(clean_json)
        
        cols = st.columns(2)
        for i, spec in enumerate(specs):
            with cols[i % 2]:
                st.markdown(f"#### {spec.get('title', 'Untitled Visualization')}")
                try:
                    v_type = spec.get('type', 'bar').lower()
                    x, y = spec.get('x'), spec.get('y')
                    
                    if v_type == 'scatter':
                        fig = px.scatter(df, x=x, y=y, template="plotly_dark", color_discrete_sequence=['#6366f1'])
                    elif v_type == 'line':
                        fig = px.line(df, x=x, y=y, template="plotly_dark", color_discrete_sequence=['#22d3ee'])
                    elif v_type == 'bar':
                        fig = px.bar(df, x=x, y=y, template="plotly_dark", color_discrete_sequence=['#8b5cf6'])
                    elif v_type == 'box':
                        fig = px.box(df, x=x, y=y, template="plotly_dark", color_discrete_sequence=['#f43f5e'])
                    elif v_type == 'histogram':
                        fig = px.histogram(df, x=x, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
                    elif v_type == 'pie':
                        fig = px.pie(df, names=x, values=y, template="plotly_dark")
                    else:
                        st.warning(f"Unsupported chart type: {v_type}")
                        continue
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=0, t=30, b=0),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption(spec.get('reason', ''))
                except Exception as ve:
                    st.error(f"Failed to render chart: {ve}")
    except Exception as e:
        st.error(f"Could not parse visualization specs: {e}")
        st.code(viz_specs_raw)

# Set page config
st.set_page_config(
    page_title=f"{settings.APP_NAME} | Enterprise BI",
    page_icon="💎",
    layout="wide"
)

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("assets/style.css")
except Exception as e:
    st.error(f"Error loading CSS: {e}")

def main():
    # Render Sidebar
    render_sidebar()

    # Hero Section
    st.markdown("<h1 class='main-title'>Agentic Data Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-dim); font-size: 1.2rem; margin-bottom: 2rem;'>Autonomous data analysis powered by multi-agent reasoning.</p>", unsafe_allow_html=True)

    # File Upload
    with st.container():
        uploaded_file = st.file_uploader("Upload your enterprise dataset (CSV/XLSX)", type=['csv', 'xlsx'])

    if uploaded_file:
        file_path = Path(settings.DATA_DIR) / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        session_id = f"session_{uploaded_file.name}"
        
        if session_id not in st.session_state:
            st.session_state[session_id] = {
                'status': 'idle',
                'results': None,
                'logs': [],
                'agent_updates': {}
            }

        state = st.session_state[session_id]

        # Workspace Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Executive Dashboard", 
            "🔍 Data Explorer", 
            "🛡️ Quality & Validation", 
            "🧠 Agent Intelligence"
        ])

        with tab2:
            df = pd.read_csv(file_path) if file_path.suffix == '.csv' else pd.read_excel(file_path)
            st.markdown("### 🔍 Dataset Preview")
            st.dataframe(df.head(100), use_container_width=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Rows", len(df))
            c2.metric("Columns", len(df.columns))
            c3.metric("Missing Values", df.isnull().sum().sum())

        with tab1:
            if state['status'] == 'idle':
                if st.button("🚀 Execute Autonomous Analysis", use_container_width=True):
                    state['status'] = 'running'
                    st.rerun()
            
            elif state['status'] == 'running':
                with st.status("🤖 Orchestrating AI Agents...", expanded=True) as status_box:
                    def on_task_complete(task_name, output):
                        state['agent_updates'][task_name] = output
                        st.toast(f"✅ {task_name.capitalize()} Agent Finished!", icon="🤖")
                    
                    try:
                        result = run_analysis_pipeline(str(file_path), task_callback=on_task_complete)
                        if result.status == 'complete':
                            state['status'] = 'complete'
                            state['results'] = result
                            status_box.update(label="✅ Analysis Complete", state="complete")
                        else:
                            state['status'] = 'error'
                            state['error'] = result.error
                            status_box.update(label="❌ Analysis Failed", state="error")
                        st.rerun()
                    except Exception as e:
                        app_logger.exception("App-level crash during analysis")
                        state['status'] = 'error'
                        state['error'] = str(e)
                        st.rerun()

            elif state['status'] == 'error':
                st.error(f"⚠️ Analysis Failed: {state.get('error', 'Unknown Error')}")
                if st.button("🔄 Reset & Retry", use_container_width=True):
                    state['status'] = 'idle'
                    state['error'] = None
                    st.rerun()

            elif state['status'] == 'complete':
                res = state['results']
                st.success("Analysis Complete!")
                
                # Render Insights
                st.markdown("### 💡 Strategic Insights")
                insights_text = res.reports['tasks'].get('insights', "No insights generated.")
                st.markdown(f"""
                    <div class='glass-card' style='border-left: 4px solid var(--accent);'>
                    
                    {insights_text}
                    
                    </div>
                """, unsafe_allow_html=True)

                # Visualizations
                st.markdown("### 📈 Visual intelligence")
                viz_specs = res.reports['tasks'].get('viz', "[]")
                render_visualizations(res.data, viz_specs)

        with tab3:
            if state['status'] == 'complete':
                res = state['results']
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### 🧹 Quality Audit")
                    clean_res = res.reports['tasks'].get('clean', "N/A")
                    st.markdown(f"<div class='glass-card'>\n\n{clean_res}\n\n</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("#### ✅ Statistical Validation")
                    val_res = res.reports['tasks'].get('validate', "N/A")
                    st.markdown(f"<div class='glass-card'>\n\n{val_res}\n\n</div>", unsafe_allow_html=True)

        with tab4:
            st.markdown("### 🧠 Agent Reasoning Logs")
            if state['agent_updates']:
                for task, output in state['agent_updates'].items():
                    with st.expander(f"Agent: {task.capitalize()}"):
                        st.markdown(output.raw if hasattr(output, 'raw') else str(output))
            else:
                st.info("Agent logs will appear here during execution.")

    else:
        # Empty state
        st.markdown("""
            <div style='text-align: center; padding: 5rem; color: var(--text-dim);'>
                <h3>Ready for your data...</h3>
                <p>Upload a file to begin the agentic intelligence journey.</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
