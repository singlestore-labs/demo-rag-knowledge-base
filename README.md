# Demo: RAG Knowledge Base

## Getting Started

1. Create and active a Python virtual environment by running the following commands:

```sh
python3 -m venv ./.venv
source ./.venv/bin/activate
```

2. Install required dependencies by runing the following command:

```sh
pip install singlestoredb langchain langchain-community langchain-openai openai pypdf ijson "fastapi[standard]" python-dotenv
```

3. Create a `.env` file in the root of the project based on the `.env.example` file.
4. Place a PDF, Markdown, or TXT file that you want to use as your knowledge base into the directory you just created.
5. Create tables by running the following command:

```sh
python ./create_tables.py
```

6. Create embeddings by running the following command:

```sh
python ./create_embeddings.py
```

7. Load embeddings by running the following command:

```sh
python ./load_embeddings.py
```

8. Run the app:

```sh
python ./app.py
```

9. Open http://localhost:8000/docs in your browser and test the `/ask` API endpoint.

---

[Start With SingleStore – $600 in Free Credits](https://portal.singlestore.com/intention/cloud?utm_source=yaroslav&utm_medium=github&utm_campaign=ai&utm_content=how-to-build-a-retrieval-augmented-knowledge-base-in-python-for-customer-support)
