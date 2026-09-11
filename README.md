# ⚖️ Bharatiya Nyaya Sanhita Legal Assistant

An AI-powered legal question-answering system built using **Agentic RAG (Retrieval-Augmented Generation)** to answer questions from the **Bharatiya Nyaya Sanhita (BNS), 2023**.

The system retrieves relevant BNS provisions from the official BNS document and uses an LLM to generate concise, context-grounded answers.

---

## 🚀 Project Overview

The Bharatiya Nyaya Sanhita Legal Assistant allows users to ask questions related to offences, punishments, and provisions under the BNS, 2023.

The system combines:

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Vector similarity search
- Tool calling
- Conversational query rewriting
- ChromaDB
- LangChain
- NVIDIA AI endpoints
- Streamlit

The goal is to provide answers based specifically on the retrieved BNS content rather than relying on general model knowledge.

---

## 🏗️ Architecture

                         User Query
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Conversation Layer  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Query Rewriting     │
                  │   LLM               │
                  └──────────┬──────────┘
                             │
                    Standalone Query
                             │
                             ▼
                  ┌─────────────────────┐
                  │   BNS Agent         │
                  │   LLM + Tool Call  │
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
                  │ Vector Similarity   │
                  │      Search         │
                  └──────────┬──────────┘
                             │
                       Relevant BNS
                        Sections
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Final LLM       │
                  │  Answer Generation  │
                  └──────────┬──────────┘
                             │
                             ▼
                         Final Answer





🔑 Key Features
1. Agentic RAG
Instead of directly passing every query to a fixed retrieval chain, the system uses an LLM-based agent that can decide to call the bns_rag retrieval tool.
''' text
                           User Question
                                ↓
                              Agent
                                ↓
                            Tool Call
                                ↓
                            BNS Retrieval
                                 ↓
                           Relevant Sections
                                  ↓
                            Final Answer
 


Base
The BNS PDF is processed into individual sections.
Each section is stored as a document with metadata such as:
{
    "source": "BNS_2023.pdf",
    "section": 103
}
This allows the system to associate retrieved text with its corresponding BNS section.



3. Semantic Search with ChromaDB
BNS sections are converted into vector embeddings using NVIDIA embeddings.
These embeddings are stored in ChromaDB.
When a user asks a question, semantic similarity search retrieves the most relevant BNS sections.



4. Tool Calling
The agent exposes a retrieval tool:
@tool
def bns_rag(query: str) -> str:
    ...
The LLM generates a structured tool call containing the retrieval query.
The application then executes the tool and passes the retrieved BNS context to the final answer-generation step.



5. Conversational Query Rewriting
The system supports follow-up questions.
For example:
User:
What is the punishment for murder?

Assistant:
Under Section 103...

User:
What if it is done by a minor?

The second question depends on the previous conversation.
The system rewrites it into a standalone retrieval query before performing retrieval.

"What if it is done by a minor?"

              ↓

"How does the BNS deal with a minor
who commits murder?"
This improves retrieval for multi-turn conversations.



📚 BNS Document Processing

The PDF processing pipeline is:


BNS PDF
   ↓
PyPDFLoader
   ↓
Extract Full Text
   ↓
Detect Section Numbers
   ↓
Create Section Documents
   ↓
Split Large Sections
   ↓
Generate Embeddings
   ↓
Store in ChromaDB

Large sections are divided using:
RecursiveCharacterTextSplitter
while preserving the original section metadata.

🛠️ Technologies Used

Python
LangChain
RAG and agent architecture
NVIDIA AI Endpoints
Embeddings and LLM
ChromaDB
Vector database
PyPDFLoader
PDF processing
Supporting utilities
Streamlit
User interface
RecursiveCharacterTextSplitter



📁 Project Structure
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


📄 File Description
app.py
Provides the Streamlit user interface and manages the chat session.

bns_loader.py
Handles:
PDF loading
Section detection
Section-level document creation
Chunking of large sections

vector_store.py
Handles:
NVIDIA embeddings
ChromaDB
Vector store creation
Retriever configuration
Formatting retrieved documents

agent.py
Contains:
NVIDIA LLM
BNS retrieval tool
Tool calling
Agent logic
Final answer generation
Query rewriting chain

conversation.py
Handles:
Conversation history
Follow-up questions
Query rewriting
Session-based chat history

test.py
Provides a terminal-based interface for testing the assistant without Streamlit.




🎯 Design Principles
The system follows these principles:
Answers should be grounded in retrieved BNS content.
Relevant BNS sections should be mentioned whenever available.
The system should not rely on IPC provisions.
The model should not invent sections or punishments.
If retrieved information is insufficient, the assistant should clearly state that.




🔮 Future Improvements
Possible improvements include:
Hybrid keyword + vector retrieval
Section-aware reranking
Metadata filtering
Source citations in the UI
Streaming responses
Persistent conversation memory
Evaluation using a dedicated legal QA dataset
Improved retrieval for closely related BNS provisions
Deployment using Docker and cloud infrastructure






Disclaimer
This project is intended for educational and research purposes.
It is not a substitute for professional legal advice. Users should consult a qualified legal professional for advice regarding actual legal matters.





👨‍💻 Author
Abhishek Jindal
B.Tech – Computer Science and Engineering
Dr. B. R. Ambedkar National Institute of Technology Jalandhar






