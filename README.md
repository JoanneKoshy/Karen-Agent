## 💼 KAREN — The HR You’ll *Actually* judge

> *"Okay Karen, screen me the best resumes!"*  

Meet **KAREN**, your smart, slightly-sassy HR agent who doesn’t just “speak to the manager” — she **is** the manager.  
KAREN screens heaps of resumes, understands the job description, and picks out the **top 3 candidates** using AI magic 🪄.

---

# 🧠 What KAREN Does  

KAREN automates resume screening using **embeddings**, **vector search**, and **LLMs** — so you can focus on hiring, not sorting.  

### Workflow  
1. 🗂️ Upload multiple **resumes (PDFs)**.  
2. 💬 Add the **Job Description (JD)** for the desired role.  
3. 🧩 **Resume text** is extracted via `pdfplumber` and converted into embeddings using `sentence-transformers`.  
4. 🧠 Embeddings are stored in **ChromaDB** (vector database).  
5. 📄 The **JD** is also converted into embeddings.  
6. 🤝 Both embeddings are sent to **Groq’s LLM** through **LangChain**.  
7. 🏆 KAREN ranks all candidates and outputs the **Top 3 resumes** with similarity scores.  

Built with **Streamlit** for a clean and interactive interface.

---

## 🧰 Tech Stack  

| Purpose | Tool |
|----------|------|
| 💻 Frontend | Streamlit |
| 🧠 LLM Integration | LangChain + Groq |
| 🗃️ Vector Database | ChromaDB |
| 🧩 Embeddings | Sentence Transformers |
| 📄 PDF Parsing | pdfplumber |
| 🔐 Environment Management | python-dotenv |
| 🐍 Language | Python |

---

# ⚙️ Installation & Setup  
git clone https://github.com/yourusername/karen.git
cd karen

---

# Install dependencies:
pip install -r requirements.txt

---

# Create a .env file and add your Groq API key:
GROQ_API_KEY=your_key_here

---

# Run the Streamlit app:
streamlit run app.py

---

# Why Karen 🤓?

Because every HR team needs a Karen —
but this one doesn’t judge your outfit or ask to “speak to the manager.”

KAREN flips the popular Gen Z stereotype:
“Karen” — once a symbol of entitlement — is now Kind, Analytical, Reliable, Efficient, and Non-biased. 💅

KAREN doesn’t complain. She computes.

---

# Example Output:
Top 3 candidates for “AI Engineer”:
1. Alex Johnson – Score: 0.94
2. Priya Menon – Score: 0.89
3. Daniel Kim – Score: 0.87





