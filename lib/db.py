import os

import singlestoredb as s2
from dotenv import load_dotenv

load_dotenv()

db = s2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", 3306)),
    database=os.getenv("DB_NAME"),
    results_type="dicts",
)
