# RAG + Twilio Voice Agent

This repository demonstrates a **simple voice agent** built using **LangChain + FAISS + ElevenLabs** , with a **proof-of-concept Twilio Voice integration**.


## 🧱 Project Structure

| Path | Description |
|-----|------------|
| `agent/` | Core agent logic |
| `agent/rag_agent.py` | LangChain-based RAG voice agent |
| `agent/intent_gate.py` | Guardrails to restrict queries within project scope |
| `vectorstore/` | Vector database utilities |
| `vectorstore/build_store.py` | Builds and persists FAISS index |
| `data/` | Dataset storage |
| `data/processed/` | Cleaned and structured data |
| `data/processed/wise_articles.json` | Preprocessed FAQ-style data |
| `data/raw/` | Raw input datasets |
| `data/raw/where_is_my_money.json` | Raw questions data |
| `app.py` | FastAPI app + Twilio webhook (can be exposed using ngrok) |
| `run.py` | Local RAG agent runner (main execution logic) |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |


---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```


## Testing In Console 

For Build the pipline and running the server and ollama
```bash
make build_and_run 
```

For running the server and ollama
```bash
make run 
```


For running the server and ollama with twailo and ngork sample webhook with pipline
```bash
make build_and_run_fastapi 
```


For running the server and ollama with twailo and ngork sample webhook without pipline
```bash
make  run_fastapi
```


## ✅ Summary (Execution Order)

```text
1. Prepare processed data (JSON)
2. Build vector store
3. Run Local Ollama
4. Run local RAG agent
5. (Optional Not Tested ) 4. Start FastAPI server and Connect Twilio
```
****
