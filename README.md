
## 🧠📄Study Assistant Agent: A Tool-Augmented AI Agent for Smarter Learning✨🔍

A smart, interactive study assistant that allows users to upload academic PDFs, get clean summaries, ask custom questions, and receive answers enriched with relevant web and YouTube resources. Powered by **FastAPI**, **Phidata Agents**, and **LLMs from Groq (DeepSeek)** with personalized user memory and multi-user support.

---

##  Features

*  **PDF Summarization**: Upload a PDF and get key points in 5–8 bullet points
*  **Interactive Q\&A**: Ask questions based on the uploaded PDF
*  **Web & Video Enrichment**: Pulls relevant web articles and YouTube videos
*  **Multi-user Memory**: Tracks each user’s questions and activity
*  **Follow-up Support**: Ask more questions using the same context
*  **Context-aware Responses**: Agent uses previous interactions for suggestions

---

##  Demo


<img width="1275" height="580" alt="Screenshot 2025-07-29 095009" src="https://github.com/user-attachments/assets/17dba76a-91cd-4a45-9ad4-0aba73e001dd" />
<img width="1278" height="587" alt="Screenshot 2025-07-29 095108" src="https://github.com/user-attachments/assets/f4b178a2-392a-4647-b3a4-77de95df33dd" />
<img width="1268" height="622" alt="Screenshot 2025-07-29 102835" src="https://github.com/user-attachments/assets/01dfe3e4-f7f7-4d2a-bc01-70ae74fa1212" />
<img width="1274" height="635" alt="Screenshot 2025-07-29 102930" src="https://github.com/user-attachments/assets/69c3bcda-abd0-4bb8-8ed4-792cbca5f422" />


---

##  Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-learning-assistant.git
cd ai-learning-assistant
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate      # For Linux/Mac
venv\Scripts\activate         # For Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the root directory

```
GROQ_API_KEY="your_groq_key_here"
TOGETHER_API_KEY="your_together_key_here"
```

> Replace `your_groq_key_here` with your actual your_groq_key_here API key.

---

##  Project Structure

```
.
├── main.py                   # FastAPI app entry point
├── templates/               # Jinja2 HTML templates
│   ├── new.html             # Upload and question form
│   └── result.html          # Output display
├── static/                  # CSS and assets
├── tools/                   # Custom tools (PDFReader, Summarizer, etc.)
├── Agent.py                  # Multiagent logic using phi + groq
├── uploads/                 # Uploaded PDFs
├── user_activity.json       # Persistent user memory
└── README.md
```

---

##  How to Use

1. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

2. Open in browser:

```
http://localhost:8000
```

3. Upload a PDF → enter your name and a question → get a summary + answer
4. Ask follow-up questions — the assistant remembers you

---

##  Future Enhancements

* Chat-style threaded interface with memory bubble UI
*  Export notes and answers as PDF
*  Multiple file support per user session
*  Integration with YouTube transcript search
*  Real-time document highlighting from agent responses

---

##  Technologies Used

* [FastAPI](https://fastapi.tiangolo.com/)
* [Phidata Agent Framework](https://docs.phidata.com/)
* [Groq DeepSeek LLM](https://groq.com/)
* [DuckDuckGo Tool](https://github.com/phidata-tools)
* [YouTube Search Tool](https://developers.google.com/youtube)
* Jinja2, HTML, CSS

---

##  Author
**Deepali Umesh**

---

Rather than a multi-agent system, this project uses one central agent that orchestrates multiple capabilities through tool-based interactions — a lightweight and modular design inspired by modern AI agent frameworks.
This approach makes it ideal for extending, debugging, and personalizing the assistant — all while keeping the system simple, efficient, and user-friendly.
