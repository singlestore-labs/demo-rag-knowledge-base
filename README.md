# RAG Knowledge Base

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

## Create Tabels

Execute the following command in your terminal to create tables:

```sh
python ./create_tables.py
```

## Create Embeddings

Execute the following command in your terminal to create embeddings:

```sh
python ./create_embeddings.py
```

## Load Embeddings

Execute the following command in your terminal to load embeddings:

```sh
python ./load_embeddings.py
```
