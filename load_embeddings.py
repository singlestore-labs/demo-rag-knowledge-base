import glob
import os

import ijson

from lib.db import db

EMBEDDINGS_DIRECTORY = './embeddings'


def insert_batch(batch):
    with db.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO knowledge_base (source, content, embedding)
            VALUES (%s, %s, %s)
            """,
            batch
        )


def main():
    file_pattern = os.path.join(EMBEDDINGS_DIRECTORY, '*.json')
    batch = []
    batch_size = 100

    for file_path in glob.glob(file_pattern):
        source = os.path.splitext(os.path.basename(file_path))[0]

        with open(file_path, 'r', encoding='utf-8') as file:
            for item in ijson.items(file, 'item'):
                batch.append((
                    item.get('source', source),
                    item['content'],
                    item['embedding']
                ))

                if len(batch) >= batch_size:
                    insert_batch(batch)
                    batch.clear()

    if batch:
        insert_batch(batch)
        batch.clear()


if __name__ == '__main__':
    main()
