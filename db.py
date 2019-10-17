import sqlite3

def create_table():
    with sqlite3.connect("eSHOP.db") as conn:
        conn.execute("""CREATE TABLE users
        (
            user_login VARCHAR(40),
            user_password VARCHAR(50),
            name VARCHAR(255),
            shopping_cart integer 
        );""")


def select(table, *args):
    args = ", ".join(args)
    with sqlite3.connect("eSHOP.db") as conn:
        cur = conn.cursor()
        data = cur.execute(f"SELECT {args} FROM {table}")
        info = data.fetchall()
        return info
