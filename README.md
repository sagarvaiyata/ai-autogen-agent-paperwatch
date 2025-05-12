# PaperWatchAgent

A console-based pipeline for on-demand literature reviews, built with Microsoft Autogen’s AgentChat framework.

## 🚀 Features

- **Interactive REPL** — type any research prompt at `Task> ` and get a streamed, collaborative review.  
- **“Latest” filtering** — agents automatically use a `time_tool` to restrict searches to today’s date (web) or the last 12 months (arXiv).  
- **Structured Markdown output** —  
  - Web results in a Markdown table (title, URL, date, snippet, relevance)  
  - arXiv papers in a Markdown list (title, authors, URL, date, abstract excerpt)  
  - A 5-section literature review with references  

## 📦 Prerequisites

- Python **3.9+**  
- An [OpenAI API key](https://platform.openai.com/account/api-keys) (set in a `.env` file)  
- Git (to clone the repo)

## 🛠️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/sagarvaiyata/PaperWatchAgent.git
   cd PaperWatchAgent
````

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   # macOS / Linux
   source venv/bin/activate
   # Windows (Powershell)
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install autogen-agentchat autogen-ext aioconsole python-dotenv
   ```

4. **Configure environment variables**
   Copy the example and fill in your API key:

   ```bash
   cp .env.example .env
   # then edit .env and set:
   # OPENAI_API_KEY=sk-...
   ```

## 🎮 Usage

Simply run:

```bash
python main.py
```

You’ll see:

```
🖥️  LLM Agent Console
 • Type your task and press Enter.
 • Type 'TERMINATE', 'exit' or 'quit' to stop.

Task>
```

1. **Type your research task**, e.g.

   ```
   Task> Survey the latest research on multimodal LLMs in education
   ```
2. **Press Enter** and watch the agents collaborate:

   * **Google\_Search\_Agent** fetches web hits
   * **Arxiv\_Search\_Agent** retrieves academic papers
   * **Report\_Agent** synthesizes a formatted review
3. **End** your session with `TERMINATE`, `exit`, or `quit`.

## 📂 Project Structure

```
PaperWatchAgent/
├── agents.py         # Agent definitions & system prompts
├── tools.py          # google_search, arxiv_search, time_tool implementations
├── main.py           # REPL entry point (just `python main.py`)
├── .env.example      # Example environment variables
├── README.md         # This file
└── requirements.txt 
```

* **Non-interactive mode**
  If you need scriptable output, replace the REPL loop in `main.py` with a one-off:

  ```python
  await Console(team.run_stream(task="Your task here"))
  ```


