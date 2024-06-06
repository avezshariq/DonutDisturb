import sqlite3
import os
import random


def create_db(db_name: str = "server") -> None:
    """
    Creates a Database

    Args:
        db_name (str): Name of the database. Defaults to 'server'

    Returns:
        None
    """
    conn = sqlite3.connect(f"{db_name}.db")
    conn.close()


def create_table(
    db_name: str = "server",
    table_name: str = "users",
    schema: list[tuple[str, str]] = [("name", "TEXT")],
) -> None:
    """
    Creates a table

    Args:
        db_name (str): Name of the database. Defaults to 'server'
        table_name (str): Name of the table. Defaults to 'users'
        schema (list[tuple]): List containing tuples. Tuple is a pair of column name and column data type

    Returns:
        None
    """
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()
    schema_str = f"CREATE TABLE IF NOT EXISTS {table_name} (\n\t {table_name}_id INTEGER PRIMARY KEY AUTOINCREMENT"
    for col_name, col_dtype in schema:
        schema_str += f"\n\t,{col_name} {col_dtype}"
    schema_str += "\n)"
    c.execute(schema_str)
    conn.commit()
    conn.close()


def insert_data(
    db_name: str = "server",
    table_name: str = "users",
    data: list[tuple[str, str]] = [(1, 2)],
) -> None:
    """
    Insert data into a table

    Args:
        db_name (str): Name of the database. Defaults to 'server'
        table_name (str): Name of the table. Defaults to 'users'
        data (list[tuple]): List containing tuples. Tuple contain all data of a row

    Returns:
        None
    """
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()
    for row in data:
        if isinstance(row, str):
            val = row
        else:
            val = '", "'.join(row)
        stringy = f'(NULL, "{val}")'
        insert_stringy = f"INSERT INTO {table_name} VALUES {stringy}"
        print(insert_stringy)
        c.execute(insert_stringy)
    conn.commit()
    conn.close()

def get_all_items(
    db_name: str = "server",
) -> list:
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()
    select_stringy = 'SELECT c.name, i.name, i.price from item i join category c on i.category_id=c.category_id'
    c.execute(select_stringy)
    data = c.fetchall()
    data_dict = {}
    for item in data:
        if item[0] in data_dict.keys():
            data_dict[item[0]].append((item[1], item[2]))
        else:
            data_dict[item[0]] = [(item[1], item[2])]

    conn.commit()
    conn.close()
    return data_dict


def get_all_prices(
    db_name: str = "server",
) -> list:
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()
    select_stringy = 'SELECT name, price from item'
    c.execute(select_stringy)
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def get_discount(
    db_name: str = "server",
    coupon_name: str = None,
) -> list:
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()
    if coupon_name:
        select_stringy = f"SELECT discount from coupon where name='{coupon_name}'"
        c.execute(select_stringy)
        data = c.fetchone()
    else:
        data = 0
    conn.commit()
    conn.close()
    return data[0] if data else 0


if __name__ == "__main__":
    db_name = "server"
    os.remove(f"{db_name}.db")
    create_db(db_name=db_name)

    # users
    users_schema = [("email", "TEXT"), ("password", "TEXT")]
    create_table(db_name=db_name, table_name="users", schema=users_schema)
    data = [("admin", "admin"), ("avez", "avez")]
    insert_data(db_name=db_name, table_name="users", data=data)

    # category
    category_schema = [("name", "TEXT")]
    create_table(db_name=db_name, table_name="category", schema=category_schema)
    data = [("Pizza"), ("Burger"), ("Cake"), ("Mojito")]
    insert_data(db_name=db_name, table_name="category", data=data)

    # items
    item_schema = [("name", "TEXT"), ("price", "FLOAT"), ("category_id", "INTEGER")]
    create_table(db_name=db_name, table_name="item", schema=item_schema)
    data = [
        ("Veg Pizza", "242", "1"),
        ("Non-Veg Pizza", "180", "1"),
        ("Non-Veg Burger", "120", "2"),
        ("Veg Burger", "80", "2"),
        ("Choco Cake", "160", "3"),
        ("Mango Cake", "160", "3"),
        ("Red Velvet Cake", "160", "3"),
        ("Mint Mojito", "60", "4"),
        ("Virgin Mojito", "60", "4"),
        ("Watermelon Mojito", "60", "4"),
    ]
    insert_data(db_name=db_name, table_name="item", data=data)

    # coupon
    coupon_schema = [("name", "TEXT"), ("discount", "INTEGER")]
    create_table(db_name=db_name, table_name="coupon", schema=coupon_schema)
    data = [("RANDOMDISC", str(random.randint(10, 30)))]
    insert_data(db_name=db_name, table_name="coupon", data=data)
