conda create -n langmultiagent python=3.11 -y

conda activate langmultiagent

pip install -r requirements.txt

=========================================================
# 🔎 LangChain Multi-Agent Research System

An AI-powered research assistant built with **LangChain**, **Google Gemini**, and **Streamlit**.

The system uses multiple AI agents to search for relevant information, scrape reliable sources, generate a research report, and critically evaluate the result before accepting it.

## 🚀 Features

- 🔍 **Search Agent** — Finds recent and relevant sources.
- 📖 **Reader Agent** — Selects useful URLs and extracts detailed content.
- ✍️ **Writer** — Generates a structured research report.
- 🧐 **Critic** — Reviews the report and provides feedback.
- 🔄 **Iterative Research** — Rewrites the report when improvements are required.
- 🌐 **Source Replacement** — Searches for another source when the current source has credibility or relevance problems.
- 🖥️ **Streamlit UI** — Simple web interface for entering research topics.
- 📥 **Markdown Export** — Download the final report as a `.md` file.

## 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │   User Topic    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Search Agent   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Reader Agent   │
                 │ Search + Scrape │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     Writer      │
                 │ Generate Report │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     Critic      │
                 │  Score + Review │
                 └────────┬────────┘
                          │
                    ┌─────┴─────┐
                    │           │
                  Accept      Reject
                    │           │
                    ▼           ▼
                 Final      Improve /
                 Report     New Source
```

## 🔄 Research Workflow

The system works in two levels of iteration.

### Inner Loop

The Writer and Critic work together on the same source.

```text
Writer → Critic
          │
          ├── Score ≥ 7 → Accept
          │
          └── Score < 7 → Rewrite
```

The system allows a maximum of **3 writer/critic attempts** for the same source.

### Outer Loop

If the source itself is considered problematic, the system rejects it and searches for another source.

```text
Search → Reader → Writer → Critic
                         │
                    Source Problem
                         │
                         ▼
                  Reject Source
                         │
                         ▼
                    New Source
```

The system allows a maximum of **3 different source attempts**.

## 🛠️ Technologies Used

- **Python**
- **LangChain**
- **Google Gemini**
- **Pydantic**
- **Streamlit**
- **Web Search**
- **Web Scraping**

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
```

If you use another LLM provider, add its API key accordingly.

> Do not commit your `.env` file to GitHub.

Add this to `.gitignore`:

```gitignore
.env
__pycache__/
.venv/
```

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Enter a research topic such as:

```text
AI Guardrails
```

The system will search for sources, read the selected source, generate a report, critique it, and display the final result.

## 📄 Example Output

The application produces a research report containing information gathered from the selected sources.

The final report can be downloaded using:

```text
⬇️ Download Report (.md)
```

The downloaded file can then be opened in any Markdown editor or uploaded to GitHub.

## 🧠 Critic System

The Critic evaluates the generated report using structured output.

Example:

```text
Score: 8/10

Strengths:
- Clear explanation
- Relevant information
- Good organization

Areas to Improve:
- Add more examples

Verdict:
Good report with minor improvements needed.
```

The Critic also determines whether the **source itself** should be replaced.

A source is considered problematic only when there is a clear issue such as:

- Irrelevant content
- Unreliable source
- Unverifiable information
- Fundamental lack of information required for the topic

## 🎯 Future Improvements

Possible future improvements include:

- 📊 Research progress visualization
- 📚 Multiple-source research
- 🔗 Display source URLs in the final report
- 💾 Save previous research sessions
- 📄 PDF export
- 🧠 Better source ranking
- ⚡ Parallel source processing
- 🔐 Authentication
- ☁️ Cloud deployment
- 📈 Research history and analytics

## 👨‍💻 Author

**Sundara Ragavan**

Built as a hands-on project for learning and experimenting with **LangChain, AI agents, LLM workflows, structured outputs, and Streamlit**.