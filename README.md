# BizSense AI – Enterprise Knowledge Assistant

**Powered by Nexora Technologies**

---

# 1. Problem Statement

Organizations struggle with:

* Scattered internal knowledge across documents
* Employees wasting time searching information
* AI models giving hallucinated answers
* No centralized intelligent assistant for company data

There is a need for a system that:

* Understands internal documents
* Answers accurately
* Avoids external or hallucinated responses

---

# 2. Solution

BizSense AI solves this by building a Retrieval-Augmented Generation (RAG) system that:

* Uses internal company documents (knowledge base)
* Retrieves relevant data using embeddings (ChromaDB)
* Generates accurate answers using LLM (Groq LLaMA 3)
* Maintains conversation memory
* Supports user file uploads

Result:

* Accurate
* Context-aware
* No hallucination
* Enterprise-ready

---

# 3. System Workflow

```text
User Query
   ↓
Streamlit UI (app.py)
   ↓
Backend Logic (backend_logic.py)
   ↓
Retrieve Data From:
   • ChromaDB (company knowledge)
   • Uploaded documents
   • Chat history (memory)
   ↓
LLM (Groq - LLaMA 3)
   ↓
Final Answer
```

---

# 4. Architecture

## Components

* Frontend: Streamlit UI
* Backend: Python logic
* Vector DB: ChromaDB
* Embeddings: HuggingFace MiniLM
* LLM: Groq (LLaMA 3)

---

# 5. Project Structure

```text
BIZSENSEAI/
│
├── backend/
│   ├── auth.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── chroma_db/
│
├── components/
│   ├── loader.py        # Load documents
│   ├── parser.py        # Parse PDF/DOCX/TXT
│   ├── splitter.py      # Chunking logic
│   ├── vectorstore.py   # ChromaDB creation
│   ├── retriever.py     # Retrieval logic
│   ├── model.py         # LLM setup (Groq)
│   └── prompt.py        # Prompt engineering
│
├── data/
│   ├── 01_nexora_company_profile.txt
│   ├── 02_nexora_leave_policy.txt
│   ├── 03_nexora_wfh_policy.txt
│   ├── 04_nexora_code_of_conduct.txt
│   ├── 05_nexora_escalation_process.txt
│   └── 06_nexora_system_overview.txt
│
├── app.py               # Streamlit UI
├── backend_logic.py     # Core RAG logic
├── create_db.py         # Build ChromaDB
├── requirements.txt
└── .env
```

---

# 6. Key Features

## Knowledge-Based AI

* Answers only from internal documents

## File Upload Support

* TXT, PDF, DOCX supported
* Creates temporary vector database

## Chat Memory

* Remembers user inputs
* Handles follow-up questions

## Multi-Source Retrieval

* Chat History
* Uploaded Files
* Base Knowledge DB

## Download Chat

* Export conversation as `.txt`

---

# 7. Example Use Cases

* “How many employees are in Nexora?”
* “Who is the HR manager?”
* “What is work-from-home policy?”
* “Summarize uploaded document”
* “What is my name?” (chat memory)

---

# 8. Technologies Used

| Layer      | Technology         |
| ---------- | ------------------ |
| UI         | Streamlit          |
| Backend    | Python             |
| LLM        | Groq (LLaMA 3)     |
| Embeddings | HuggingFace        |
| Vector DB  | ChromaDB           |
| Parsing    | PyPDF, python-docx |

---

# 9. How to Run

```bash
pip install -r requirements.txt
python create_db.py
streamlit run app.py
```

---

# 10. Deployment

* Platform: Hugging Face Spaces
* SDK: Streamlit
* Add secrets:

  * GROQ_API_KEY

---

# 11. System Constraints

* No external knowledge usage
* Strict RAG-based answers
* If not found, the system responds with: "I don't know"

---

# 12. Future Improvements

* Persistent user memory
* Database integration
* Multi-user support
* PDF export
* Advanced ranking (reranker)

---

# 13. Author

Leela Krishna
AI Engineer – Nexora Technologies

---

# Conclusion

BizSense AI is a secure enterprise assistant that:

* Eliminates hallucination
* Improves knowledge access
* Enhances productivity
* Provides intelligent document understanding

---

“From scattered data to smart answers.”
