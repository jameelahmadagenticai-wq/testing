# 🧠 Autonomous News Fact-Checker & Summarizer

An intelligent FastAPI-based system that automatically searches, extracts, summarizes, and critiques information from the web — with an iterative self-improving loop.

---

## 🚀 Features

* 🔍 **Automated Web Search** using DuckDuckGo
* 🌐 **Web Scraping** for real-time content extraction
* ✂️ **Extractive Summarization** using keyword + scoring logic
* 🧠 **Critique System** to evaluate summary quality
* 🔁 **Self-Improving Loop** (refines query automatically)
* ⚡ **Streaming API** (real-time logs + results)
* 📊 Optional **Streamlit UI**

---

## 🧱 Project Structure

```
project/
│
├── main.py           # FastAPI entry point (API + streaming)
├── agent.py          # LangGraph-based autonomous agent logic
├── search.py         # Fetches search results (links)
├── scraper.py        # Extracts text from webpages
├── summarizer.py     # Extractive summarization logic
├── critique.py       # Evaluates summary quality
├── app.py            # (Optional) Streamlit UI
├── requirements.txt  # Dependencies
└── README.md
```

---

## 🔄 How It Works

```
User Query
   ↓
Search (DuckDuckGo)
   ↓
Scrape Web Pages
   ↓
Combine Text
   ↓
Summarize Content
   ↓
Critique Summary
   ↓
Improve Query (if needed)
   ↓
Repeat Loop
   ↓
Final Summary (Streamed)
```

---

## 🧠 Core Logic

* **Search:** Retrieves top links based on query
* **Scraper:** Extracts raw text from webpages
* **Summarizer:** Scores sentences using:

  * keyword frequency
  * sentence length
* **Critique:** Evaluates:

  * missing details
  * technical depth
  * completeness
* **Agent:** Decides whether to:

  * stop (good summary)
  * or refine query and repeat

---

## 📦 Dependencies

Create a `requirements.txt` file:

```
fastapi
uvicorn
requests
beautifulsoup4
ddgs
langgraph
langchain-core
python-dotenv
httpx
streamlit
```

---

## ⚙️ Installation


pip install -r requirements.txt
```

---

## ▶️ Run FastAPI Server

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example API Usage

```
GET /analyze?topic=latest AI research 2025
```

---

## 💻 Run Streamlit UI (Optional)

```bash
streamlit run app.py
```

---


---

## 🧠 Type of System

* Autonomous Agent (loop-based)
* Extractive Summarization
* Rule-based Critique System
* Real-time Data Processing

---

## ⚠️ Limitations

* No deep semantic understanding (rule-based)
* Scraping may fail on some websites
* Keyword-based summarization bias

---

## 🚀 Future Improvements

* Add LLM-based summarization
* Improve scraping (newspaper3k / trafilatura)
* Add source credibility scoring
* Multi-agent architecture
* UI improvements

---

## 👨‍💻 Author

Jameel Ahmad

---

