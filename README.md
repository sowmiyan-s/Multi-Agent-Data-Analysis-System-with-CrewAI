# 💎 Agentic Data Intelligence (ADI)

**Enterprise-Grade Multi-Agent Data Analysis System**

ADI is a production-ready autonomous business intelligence platform powered by **CrewAI**. It leverages a specialized team of AI agents to audit, validate, visualize, and strategize over your enterprise datasets.

## 🚀 Key Features

- **Multi-Agent Orchestration**: Sequential process flow between Data Engineers, Statisticians, and Business Strategists.
- **Enterprise Design System**: A premium, high-performance Streamlit UI with glassmorphism and modern typography.
- **Robust Tooling**: Custom-built `DatasetTools` for structural inspection, quality auditing, and statistical profiling.
- **Production Infrastructure**:
  - **Pydantic Configuration**: Type-safe settings management.
  - **Loguru Logging**: Comprehensive logging system with rotation and compression.
  - **Modular Architecture**: Decoupled UI components and business logic.
- **Multi-Model Support**: Seamless integration with OpenAI, Groq, Anthropic, Gemini, and NVIDIA NIM.

## 🛠 Project Structure

```text
├── agents/             # specialized AI agents
├── assets/             # CSS and design tokens
├── components/         # Modular Streamlit UI components
├── config/             # Pydantic settings and LLM configs
├── data/               # Local dataset storage
├── outputs/            # Generated reports and visualizations
├── tools/              # Custom agent tools
├── utils/              # Logging and utility functions
├── app.py              # Main application entry point
├── crew.py             # Agentic orchestration logic
└── requirements.txt    # Production dependencies
```

## 🏁 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_key
   GROQ_API_KEY=your_key
   # Add others as needed
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 🧠 The Agent Team

- **Data Integrity Specialist**: Audits datasets for structural and quality issues.
- **Statistical Auditor**: PhD-level validation of data distributions and significance.
- **Visualization Expert**: Designs high-impact interactive graphical representations.
- **Business Strategist**: Translates data patterns into revenue-driving insights.

---
*Optimized for Production by Antigravity*
