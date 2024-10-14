import random
import string
from app.database import get_db_connection


def generate_unique_id(object_name, object_table):
    while True:
        new_id = f"{object_name}_" + "".join(
            random.choices(string.ascii_lowercase + string.digits, k=18)
        )
        conn = get_db_connection()
        c = conn.cursor()

        # Check if the generated ID already exists.
        c.execute(
            f"""
            SELECT id
            FROM {object_table}
            WHERE id = %s
            """,
            (new_id,),
        )

        if not c.fetchone():
            conn.close()
            return new_id
        conn.close()
