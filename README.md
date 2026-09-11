# ⚖️ Bharatiya Nyaya Sanhita Legal Assistant

An AI-powered legal question-answering system built using **Agentic RAG (Retrieval-Augmented Generation)** to answer questions based on the **Bharatiya Nyaya Sanhita (BNS), 2023**.

The system retrieves relevant BNS provisions from the source document and uses an LLM to generate concise, context-grounded responses.

## 🚀 Project Overview

The **Bharatiya Nyaya Sanhita Legal Assistant** allows users to ask questions related to offences, punishments, and provisions under the BNS, 2023.

Unlike a simple question-answering system, this project uses an **agentic architecture** where the LLM can call a dedicated retrieval tool to search the BNS knowledge base before generating the final response.

### Key Technologies

- Python
- LangChain
- Agentic RAG
- Large Language Models (LLMs)
- NVIDIA AI Endpoints
- NVIDIA Embeddings
- ChromaDB
- Streamlit
- PyPDFLoader
- RecursiveCharacterTextSplitter

## 🏗️ System Architecture

```text
                         User Query
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Conversation Layer  │
                  │  History Management │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Query Rewriting    │
                  │        LLM          │
                  └──────────┬──────────┘
                             │
                       Standalone Query
                             │
                             ▼
                  ┌─────────────────────┐
                  │     BNS Agent       │
                  │    LLM + Tool       │
                  │      Calling        │
                  └──────────┬──────────┘
                             │
                         Tool Call
                             │
                             ▼
                  ┌─────────────────────┐
                  │      bns_rag        │
                  │   Retrieval Tool    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      ChromaDB       │
                  │  Vector Similarity  │
                  │       Search        │
                  └──────────┬──────────┘
                             │
                      Relevant BNS
                        Sections
                             │
                             ▼
                  ┌─────────────────────┐
                  │      Final LLM      │
                  │   Answer Generation │
                  └──────────┬──────────┘
                             │
                             ▼
                        Final Answer
```

## 🔑 Key Features

### 🤖 Agentic RAG

The project uses an **agentic RAG architecture** instead of a fixed retrieval chain.

The LLM is connected to a custom `bns_rag` retrieval tool that retrieves relevant BNS provisions before generating the final answer.

```text
User Question
      ↓
BNS Agent
      ↓
Tool Call
      ↓
bns_rag
      ↓
ChromaDB Retrieval
      ↓
Relevant BNS Sections
      ↓
Final LLM
      ↓
Final Answer
```

### 🔎 Semantic Search with ChromaDB

The BNS document is divided into section-level documents and converted into vector embeddings using **NVIDIA Embeddings**.

These embeddings are stored in **ChromaDB**.

When a user asks a question, semantic similarity search retrieves the most relevant BNS sections.

### 🛠️ Tool Calling

The retrieval functionality is exposed to the LLM as a LangChain tool:

```python
@tool
def bns_rag(query: str) -> str:
    """
    Retrieve relevant sections and text
    from the Bharatiya Nyaya Sanhita, 2023.
    """

    results = retriever.invoke(query)

    return format_docs(results)
```

The LLM generates a structured tool call containing the retrieval query.

The application executes the tool and passes the retrieved BNS context to the final answer-generation step.

### 💬 Conversational Query Rewriting

The system supports multi-turn conversations by converting follow-up questions into standalone retrieval queries.

For example:

```text
User:
What is the punishment for murder?

Assistant:
Under Section 103...

User:
What if it is done by a minor?
```

The second question depends on the previous conversation, so the system rewrites it into a standalone retrieval query:

```text
"What if it is done by a minor?"
              ↓
"How does the BNS deal with a minor who commits murder?"
```

This improves retrieval for context-dependent follow-up questions.

## 📚 BNS Document Processing

The BNS PDF is processed through the following pipeline:

```text
BNS PDF
   ↓
PyPDFLoader
   ↓
Extract Full Text
   ↓
Detect BNS Section Numbers
   ↓
Create Section-Level Documents
   ↓
Split Large Sections
   ↓
Generate Embeddings
   ↓
Store in ChromaDB
```

Large sections are divided using `RecursiveCharacterTextSplitter` while preserving the original section metadata.

Each section contains metadata such as:

```python
{
    "source": "BNS_2023.pdf",
    "section": 103
}
```

This allows retrieved content to be associated with its corresponding BNS section.

## 🧠 Query Processing Flow

```text
User Question
      ↓
Conversation History
      ↓
Query Rewriting
      ↓
Standalone Query
      ↓
BNS Agent
      ↓
Generate Tool Call
      ↓
bns_rag Retrieval Tool
      ↓
ChromaDB Similarity Search
      ↓
Relevant BNS Sections
      ↓
Final LLM
      ↓
Context-Grounded Answer
```

For the first question, query rewriting is skipped because there is no previous conversation context.

For follow-up questions, conversation history is used to resolve contextual references before retrieval.

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core development |
| LangChain | Agent and RAG architecture |
| NVIDIA AI Endpoints | LLM and embedding models |
| ChromaDB | Vector database |
| PyPDFLoader | PDF document loading |
| RecursiveCharacterTextSplitter | Document chunking |
| Streamlit | Web interface |

## 📁 Project Structure

```text
BNS-Legal-Assistant/
│
├── app.py
├── test.py
├── config.py
├── bns_loader.py
├── vector_store.py
├── agent.py
├── conversation.py
│
├── BNS.pdf
│
├── chroma_db/
│
└── README.md
```

## 📄 File Description

### `app.py`

Provides the Streamlit-based user interface and manages the chat session.

### `bns_loader.py`

Handles:

- Loading the BNS PDF
- Extracting text
- Detecting BNS section numbers
- Creating section-level documents
- Splitting large sections

### `vector_store.py`

Handles:

- NVIDIA embeddings
- ChromaDB
- Vector store creation
- Retriever configuration
- Formatting retrieved documents

### `agent.py`

Contains:

- NVIDIA LLM
- BNS retrieval tool
- Tool calling
- Agent logic
- Final answer generation
- Query rewriting chain

### `conversation.py`

Handles:

- Conversation history
- Follow-up questions
- Query rewriting
- Session-based conversations

### `test.py`

Provides a terminal-based interface for testing the assistant without using Streamlit.

## 💡 Example Queries

The system can answer questions such as:

```text
What is the punishment for murder under BNS?

What is the punishment for theft?

Which section deals with criminal intimidation?

What if the offence is committed by a minor?

What is the punishment for an attempt to commit murder?
```

It also supports contextual follow-up questions:

```text
User:
What is the punishment for murder?

Assistant:
[Answer based on relevant BNS section]

User:
What if it is done by a minor?

Assistant:
[Answer based on the contextualized query]
```

## 🎯 Design Principles

The system follows these principles:

- Answers should be grounded in retrieved BNS content.
- Relevant BNS sections should be mentioned whenever available.
- The system should not rely on IPC provisions.
- The model should not invent sections, offences, punishments, or legal provisions.
- If the retrieved context is insufficient, the assistant should clearly state that.
- Conversation history should be used to resolve references in follow-up questions.

## ⚙️ Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd BNS-Legal-Assistant
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Set your NVIDIA API key.

### Windows PowerShell

```powershell
$env:NVIDIA_API_KEY="YOUR_API_KEY"
```

> **Important:** Never hard-code your API key or commit it to GitHub.

## ▶️ Running the Application

### Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser.

### Terminal Testing

```bash
python test.py
```

## 🔮 Future Improvements

- Hybrid keyword + vector retrieval
- Section-aware reranking
- Metadata-based filtering
- Source citations in the user interface
- Streaming responses
- Persistent conversation memory
- Dedicated legal QA evaluation dataset
- Improved retrieval for closely related BNS provisions
- Docker-based deployment
- Cloud deployment

## ⚠️ Disclaimer

This project is developed for **educational and research purposes**.

It is not a substitute for professional legal advice. Users should consult a qualified legal professional for advice regarding actual legal matters.

## 👨‍💻 Author

**Abhishek Jindal**

B.Tech – Computer Science and Engineering  
Dr. B. R. Ambedkar National Institute of Technology Jalandhar
