from lib.db import db


def main():
    with db.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                source VARCHAR(255),
                content TEXT,
                embedding VECTOR(1536)
            )
            """
        )


if __name__ == "__main__":
    main()
