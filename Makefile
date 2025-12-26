build_and_run:
	python ingestion/scrape_index.py
	python ingestion/scrape_articles.py
	python vectorstore/build_store.py
	ollama serve &
	python server.py

build_and_run_fastapi:
	python ingestion/scrape_index.py
	python ingestion/scrape_articles.py
	python vectorstore/build_store.py
	ollama serve &
	uvicorn app:app --reload
	ngrok http 8000

run:
	ollama serve &
	python server.py

run_fastapi:
	ollama serve &
	uvicorn app:app --reload
	ngrok http 8000



