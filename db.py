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


def select(table,*args, **where):
    args = ", ".join(args)
    where = where.get('where', False)
    if where:
        sql_req = f"SELECT {args} FROM {table} WHERE {where}"
    else:
        sql_req = f'SELECT {args} FROM {table}'
    with sqlite3.connect("eSHOP.db") as conn:
        cur = conn.cursor()
        data = cur.execute(sql_req)
        info = data.fetchall()
        return info


def select_product(product):
    with sqlite3.connect("eSHOP.db") as conn:
        cur = conn.cursor()
        data = cur.execute(f"SELECT * FROM products where name='{product}'")
        info = data.fetchone()
        return info


def insert_to_shopping_cart(login, product, count, price, cost):
    with sqlite3.connect("eSHOP.db") as conn:
        conn.execute("INSERT INTO shopping_cart (user_login, product, count, cost, price)"
                     " VALUES (?, ?, ?, ?, ?)", (login, product, count, cost, price))


def insert_to_users(**kwargs):
    with sqlite3.connect("eSHOP.db") as conn:
        conn.execute("INSERT INTO users (user_login, user_password, name, address, email)"
                     " VALUES (?, ?, ?, ?, ?)", (kwargs['user_login'], kwargs['password'], kwargs['name'], kwargs['address'],
                                                 kwargs['email']))


def change_status(name):
    with sqlite3.connect("eSHOP.db") as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE shopping_cart SET status='Заказано' WHERE user_login='{name}' ")


def add_to_products(**kwargs):
    print(kwargs)
    with sqlite3.connect("eSHOP.db") as conn:
        conn.execute("INSERT INTO products (name, price, image, category, description)"
                     " VALUES (?, ?, ?, ?, ?)", (kwargs['name'], kwargs['price'], kwargs['image'],
                                                 kwargs['category'], kwargs['description']))