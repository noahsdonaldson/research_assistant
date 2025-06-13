# AI Research Assistant

## Overview

**AI Research Assistant** is a Streamlit web application that generates comprehensive research reports on companies, with a focus on their AI and LLM (Large Language Model) projects and initiatives. The app leverages OpenAI's GPT models and Tavily web search to gather, analyze, and summarize information into a structured markdown report.

---

## Features

- **Automated Web Research:** Uses AI to generate relevant search queries and collect up-to-date information from the web.
- **Comprehensive Reports:** Produces detailed markdown reports with sections such as Executive Summary, AI/LLM Projects, Use Cases, Partners, ROI, Risks, Technical Architecture, and more.
- **Step-by-Step Progress:** Provides real-time status and progress updates during the research process.
- **Downloadable Results:** Allows users to download the full report in Markdown or plain text format.
- **Separation of Concerns:** Backend logic (data gathering, analysis) is separated from the frontend (Streamlit UI) for easier maintenance and iteration.

---

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Tavily Python SDK](https://github.com/tavily/tavily-python)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- Your own API keys for OpenAI and Tavily

Install dependencies with:

```
pip install -r requirements.txt
```

---

## Setup

1. **Clone the Repository**

   ```sh
   git clone <your-repo-url>
   cd research_assistant
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the project root with your API keys:

   ```
   APP_KEY=your_app_key
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   TAVILY_API_KEY=your_tavily_api_key
   ```

   (You may also need to configure Azure OpenAI endpoint and authentication if using Azure.)

3. **(Optional) Set Up a Virtual Environment**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

---

## Running the App

### **Locally (without Docker)**

Start the Streamlit app from the project root with:

```sh
streamlit run app/research_app.py
```

If you encounter import errors, try:

```sh
PYTHONPATH=. streamlit run app/research_app.py
```

The app will open in your browser. Enter a company name and click "Start Research" to generate a report.

---

### **With Docker**

1. **Build the Docker image:**

   ```sh
   docker build -t ai-research-assistant .
   ```

2. **Run the Docker container (using your local `.env` file for secrets):**

   ```sh
   docker run --env-file .env -p 8501:8501 ai-research-assistant
   ```

3. **Open your browser and go to:**

   [http://localhost:8501](http://localhost:8501)

---

**Note:**  
- The Dockerfile is set up so that your import paths work out-of-the-box.
- Your `.env` file is not copied into the image; it is provided at runtime with `--env-file .env`.

---

## Project Structure

```
research_assistant/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── research_app.py         # Streamlit frontend (UI)
│   └── research_backend.py     # Backend logic (data gathering, analysis)
├── .env                        # Your API keys (not committed)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Customization

- **Backend Logic:** Modify `app/research_backend.py` to change how data is gathered or analyzed.
- **UI/UX:** Edit `app/research_app.py` to adjust the user interface or add new features.

---

## Troubleshooting

- Make sure your API keys are valid and have sufficient quota.
- If you encounter errors, check the terminal output for details.
- For large reports, use the plain text area or download the file for full content.
- If you have issues with Python imports, run:
  ```
  PYTHONPATH=. streamlit run app/research_app.py
  ```

---

## License

This project is for educational and research purposes. Please review the licenses of OpenAI and Tavily for commercial use.

---

## Acknowledgments

- [OpenAI](https://openai.com/)
- [Tavily](https://www.tavily.com/)
- [Streamlit](https://streamlit.io/)

---