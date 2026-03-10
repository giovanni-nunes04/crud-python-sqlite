from database import connect


def create_user(nome, email):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
            (nome, email)
        )
        conn.commit()


def get_users():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios")
        return cursor.fetchall()


def update_user(user_id, nome, email):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
            (nome, email, user_id)
        )
        conn.commit()
        return cursor.rowcount


def delete_user(user_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount