import glob
import itertools
import json
import os

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader

from lib.embed import embed_documents

SOURCE_DIRECTORY = './source'
OUTPUT_DIRECTORY = './embeddings'

EXTENSION_LOADER_MAP = {
    '.pdf': PyPDFLoader,
    '.md': UnstructuredMarkdownLoader,
    '.txt': TextLoader,
}

text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=64)


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def generate_chunks(file_path: str):
    extension = os.path.splitext(file_path)[1].lower()

    Loader = EXTENSION_LOADER_MAP.get(extension)
    if not Loader:
        return

    loader = Loader(file_path)
    docs = loader.load()

    for doc in docs:
        normalized_text = normalize_text(doc.page_content)
        split_texts = text_splitter.split_text(normalized_text)

        for text in split_texts:
            yield {
                'source': os.path.basename(file_path),
                'content': text
            }


def embed_file(file_path: str, batch_size: int = 100):
    base_name = os.path.basename(file_path)
    name = os.path.splitext(base_name)[0]

    output_path = os.path.join(OUTPUT_DIRECTORY, f"{name}.json")
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    generated_chunks = generate_chunks(file_path)
    is_first_chunk = True

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write('[')

        while True:
            batch = list(itertools.islice(generated_chunks, batch_size))
            if not batch:
                break

            content_to_embed = [chunk['content'] for chunk in batch]
            embeddings = embed_documents(content_to_embed)

            for chunk, embedding in zip(batch, embeddings):
                chunk['embedding'] = str(embedding)
                chunk_json = json.dumps(chunk, ensure_ascii=False)

                if not is_first_chunk:
                    output_file.write(',')

                output_file.write('\n' + chunk_json)
                is_first_chunk = False

        output_file.write('\n]')


def main():
    file_patterns = [os.path.join(SOURCE_DIRECTORY, f"**/*{ext}") for ext in EXTENSION_LOADER_MAP]

    for file_pattern in file_patterns:
        for file_path in glob.glob(file_pattern, recursive=True):
            embed_file(file_path, batch_size=100)


if __name__ == '__main__':
    main()
