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
* The system ensures grounded responses by restricting the LLM to retrieved context only.

Result:

* Accurate
* Context-aware
* No hallucination
* Enterprise-ready

---

# 3. System Workflow

```text
Employee Query
   ↓
Streamlit UI
   ↓
Session Memory Check
   ↓
Knowledge Source Selection
   ├── Chat History
   ├── Uploaded Documents
   └── Base ChromaDB
   ↓
Embedding + Similarity Search
   ↓
Relevant Context Retrieved
   ↓
Prompt + Safety Control Layer
   (strict rules: no hallucination)
   ↓
Groq LLaMA 3
   ↓
Grounded Answer / "I don't know"
   ↓
Streamlit Chat Response

```

---

# 4. Architecture

                ┌───────────────────────┐
                │       User            │
                │    (Employee)         │
                └─────────┬─────────────┘
                          │
                          ▼
                ┌───────────────────────┐
                │   Streamlit UI        │
                │ (Frontend Interface)  │
                └─────────┬─────────────┘
                          │
                          ▼
                ┌───────────────────────┐
                │     FastAPI           │
                │   (Backend API)       │
                └─────────┬─────────────┘
                          │
                          ▼
                ┌───────────────────────┐
                │     LangGraph         │
                │ (Workflow Control)    │
                └─────────┬─────────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Chat History   │ │ Uploaded Files │ │   ChromaDB     │
│   (Memory)     │ │  (User Docs)   │ │ (Knowledge DB) │
└──────┬─────────┘ └──────┬─────────┘ └──────┬─────────┘
       │                  │                  │
       └──────────────┬───┴───────────────┬──┘
                      ▼                   ▼
             ┌───────────────────────────────┐
             │   Embedding Model             │
             │ Sentence-Transformers         │
             │ (all-MiniLM-L6-v2)            │
             └──────────────┬────────────────┘
                            │
                            ▼
             ┌───────────────────────────────┐
             │     Groq LLaMA 3 (LLM)        │
             │   (Answer Generation)         │
             └──────────────┬────────────────┘
                            │
                            ▼
             ┌───────────────────────────────┐
             │   LangSmith (Observability)   │
             └──────────────┬────────────────┘
                            │
                            ▼
             ┌───────────────────────────────┐
             │   Final Response to User      │
             └───────────────────────────────┘

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
│ 
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
├── chroma_db
├── create_db.py         # Build ChromaDB
├── requirements.txt
└── .env
```

---

# 6. Key Features

## Knowledge-Based AI

* Answers only from internal documents

## Hallucination Control
* Strict prompt engineering ensures no answer is generated outside the knowledge base
  
## Chat Memory
* Remembers user inputs
* Handles follow-up questions

## Observability
* Uses LangSmith for end-to-end observability  
* Helps in debugging, performance monitoring, and improving system accuracy  

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

| Layer              | Technology                                  |
|-------------------|----------------------------------------------|
| UI (Frontend)     | Streamlit                                    |
| Backend API       | FastAPI                                      |
| Programming       | Python                                       |
| LLM               | Groq (LLaMA 3)                               |
| Embedding Model   | Sentence-Transformers (all-MiniLM-L6-v2)     |
| Vector Database   | ChromaDB                                     |
| File Processing   | PyPDF, python-docx                           |
| Observability     | LangSmith                                    |

---

# 9. How to Run

```bash
pip install -r requirements.txt
python create_db.py
uvicorn backend.main:app --reload
streamlit run app.py
```

---

# 10. Deployment

* Platform: Hugging Face Spaces
* SDK: Streamlit
* Add secrets:

  * GROQ_API_KEY
  * LANG_CHAIN_API_KEY

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

# Conclusion

BizSense AI is a secure and intelligent enterprise assistant that:

* Eliminates hallucination using strict RAG architecture
* Provides accurate, context-driven answers
* Reduces time spent searching internal data
* Enhances organizational productivity

It demonstrates how AI can be safely deployed in enterprise environments with controlled knowledge access.
---

“From scattered data to smart answers.”

---

# 🔗 Live Demo

You can access the deployed application here:

👉 https://huggingface.co/spaces/leelakrishna1133/BizSenseAI_RAG)

---

