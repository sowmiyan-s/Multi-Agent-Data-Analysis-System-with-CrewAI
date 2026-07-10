<div align="center">
  <img src="assets/branding_image.png" alt="Crewlyze - Transform Raw Datasets Into Insights With Agentic AI Analysts" width="100%" />
</div>

<h1 align="center">Crewlyze</h1>
<p align="center">
  <strong>An autonomous multi-agent data analysis platform built with FastAPI, CrewAI, and a Vanilla JS web interface.</strong>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/sponsors/SowmiyanS"><img src="https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink" alt="Sponsor"></a>
</p>

## 🚀 About the Project
Crewlyze is an advanced, multi-agent AI data analysis platform that transforms raw datasets into actionable business insights. Using autonomous AI analysts, Crewlyze handles everything from data cleaning and profiling to complex strategic recommendations and interactive visualizations. It offers both a powerful Data Analyst Crew pipeline and an interactive Chat AI interface, providing a comprehensive toolkit for modern data science.

### 🌟 Key Advantages
* **Autonomous Data Pipeline:** Automatically cleans, profiles, and explores your data without writing code.
* **Dual Interface:** Choose between a full pipeline analysis or an interactive AI chat to query your data.
* **Premium Executive Reports:** Generates world-class PDF reports with cinematic covers, embedded charts, and actionable strategies.
* **Interactive Visualizations:** Natively generates interactive Plotly charts directly from your data.
* **Local & Privacy First:** Can be run locally using local LLMs (via Ollama) or connected to cloud providers (OpenAI, Gemini, Anthropic).
* **Multi-Provider Support:** Leverage any model supported by LiteLLM.

---

## 💻 Installation & Usage

### Running via NPM (Recommended)
You can easily install and run Crewlyze globally on your local system using NPM:

1. **Install Globally:**
   ```bash
   npm install -g .
   ```
2. **Start the Application:**
   ```bash
   crewlyze
   ```
   Navigate to [http://localhost:8000](http://localhost:8000) in your browser.

### Alternative Options
<details>
<summary><strong>Option 2: Run via Docker</strong></summary>

```bash
docker-compose up --build 
```
Navigate to [http://localhost:8000](http://localhost:8000).
</details>

<details>
<summary><strong>Option 3: Manual Startup</strong></summary>

1. **Prepare Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Start FastAPI Backend:**
   ```bash
   python main.py
   ```
3. **Open SPA UI:**
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).
</details>

---

## 🔑 API Guidelines & Configuration

Crewlyze leverages **LiteLLM** to support a vast array of Large Language Models.

* **Adding API Keys:** Navigate to the **Settings** page in the app. You can securely input your API keys for major providers (OpenAI, Gemini, Anthropic, Groq).
* **Configuring Models:** You can select your preferred model from the dropdown menu on the Home Page or within the Settings.
* **Types of Models:** 
  * **Cloud Models:** GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, etc.
  * **Local Models:** You can connect your local **Ollama** instance to run completely offline (e.g., Llama 3, Mistral).
  * **Custom Providers:** If your provider isn't listed by default, you can add it via the search/custom provider option in the settings.

---

## 📸 App Preview & Walkthrough

Here is a step-by-step preview of the Crewlyze experience:

### 1. Home Page
**Home Page Look:** We can see the currently active model, all past projects, and options to create or import a project.
![Home Page](assets/Screenshots/1.HOME%20PAGE.png)

### 2. Settings & Configuration
**Settings:** Helps configure API keys. We can add any API key provided by LiteLLM. If a specific provider is not found, we can add it from the search menu.
![Settings](assets/Screenshots/2.SETTINGS.png)

### 3. Project Inside Page
**Inside the Project:** Shows two main options: **Chat AI** and **Data Analyst Crew**. We can select whichever tool fits our current needs.
![Inside Project](assets/Screenshots/3.INSIDE%20PROJECT.png)

### 4. Interactive Chat AI
**Chat AI:** An example of interacting directly with the dataset using the conversational Crew Chat interface.
![Chat AI](assets/Screenshots/4.CHAT%20AI.png)

### 5. Data Analyst Crew
**Data Analysis Configuration:** Inside the Data Analyst Crew page, where we can configure and launch the autonomous multi-agent pipeline.
![Data Analysis](assets/Screenshots/5.DATA%20ANALYSIS.png)

### 6. Autonomous Processing
**Analysing:** The processing page showing the agents actively working on data profiling, cleaning, relations, and insights generation.
![Analysing](assets/Screenshots/6.ANALYSING.png)

### 7. Executive Business Insights
**Business Insights:** An example of the generated report detailing observation, business implication, and actionable strategies.
![Business Insights](assets/Screenshots/7.BUSINESS%20INSIGHTS.png)

### 8. Interactive Visualizations
**Visualization:** An example of the rich, interactive data visualizations generated automatically by the pipeline.
![Visualization](assets/Screenshots/8.VISUALIZATION.png)

---

## 📄 Example PDF Report Output

Crewlyze generates world-class, premium PDF reports that can be directly presented to executives and stakeholders. 

📥 **[View the Example Executive Report PDF](assets/Screenshots/EXAMPLE%20REPORT.pdf)**

---

## 🤝 Contributors

Contributions make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

* **Sowmiyan S** - Lead Developer & Architect
* *Prithiv A.K* 
* *Sebin S*

---

## 💖 Sponsor this Project

If you find this project useful and would like to support its continued development, please consider sponsoring:

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/SowmiyanS)

---

## 👨‍💻 Owner Details

**Sowmiyan S**
- 🌐 GitHub: [@SowmiyanS](https://github.com/SowmiyanS)
- 💼 LinkedIn: [Sowmiyan S](https://linkedin.com/in/sowmiyan-s/) 

---

*Crewlyze*  
*Copyright (c) 2025 Sowmiyan S*  
*Licensed under the MIT License*
