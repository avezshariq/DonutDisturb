import sqlite3
import os
import random
import uuid
import datetime


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

def get_user(
    db_name: str = "server",
    table_name: str = "users",
    email:str = ''
) -> list:
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()
    select_stringy = f"SELECT email, password from users where email='{email}'"
    c.execute(select_stringy)
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data

def create_bar_chart (labels, data, x_name, y_name):
    chart = {
        'type': 'bar',
        'data':{
            'labels': labels, 'datasets': [{
                'label': 'Total Sales',
                'backgroundColor': '#af7e5d',
                'data': data
                }]
            },
        'options': {
                'scales': {
                    'x': {
                    'title': {
                        'display': 'true',
                        'text': x_name
                    }
                    },
                    'y': {
                    'title': {
                        'display': 'true',
                        'text': y_name
                    }
                    }
                }
                }
        }
    return chart

def create_scatter_chart (labels, data, x_name, y_name):
    chart = {
        'type': 'scatter',
        'data':{
            'datasets': [{
                'label': 'Total Sales',
                'backgroundColor': '#af7e5d',
                'data': data
                }]
            },
        'options': {
                'scales': {
                    'x': {
                    'title': {
                        'display': 'true',
                        'text': x_name
                    }
                    },
                    'y': {
                    'title': {
                        'display': 'true',
                        'text': y_name
                    }
                    }
                }
                }
        }
    return chart

def analytics(db_name: str = "server") -> list[list]:
    conn = sqlite3.connect(f"{db_name}.db")
    c = conn.cursor()

    # Number of Users
    select_stringy = f"SELECT count(*) from users"
    c.execute(select_stringy)
    no_of_users = c.fetchone()[0]

    # Payment Methods
    select_stringy = f"SELECT payment_method, count(*) from sale group by payment_method"
    c.execute(select_stringy)
    temp = c.fetchall()
    labels = [x[0] for x in temp]
    data = [x[1] for x in temp]
    payment_methods_chart = create_bar_chart( labels, data, 'Payment Method', 'Number of Sales')

    # Sold Items
    select_stringy = f"SELECT name, sold_items from item"
    c.execute(select_stringy)
    temp = c.fetchall()
    labels = [x[0] for x in temp]
    data = [x[1] for x in temp]
    sold_items_chart = create_bar_chart( labels, data, 'Item', 'Number of units')

    # Payment Methods vs discount
    select_stringy = f"SELECT discount, grand_total from sale"
    c.execute(select_stringy)
    temp = c.fetchall()
    labels = ['debit_card', 'credit_card', 'net_banking', 'upi']
    data = [{"x":x[0], "y":x[1]} for x in temp]
    payment_methods_scatter_chart = create_scatter_chart(labels, data, 'Discount', 'Grand Total')

    # Total Business
    total_business_list = [x[1] for x in temp]
    total_business = sum(total_business_list)
    print(total_business)

    # Total Orders
    total_orders = len(total_business_list)

    conn.commit()
    conn.close()
    return no_of_users, payment_methods_chart, sold_items_chart, payment_methods_scatter_chart, total_business, total_orders


if __name__ == "__main__":
    db_name = "server"
    os.remove(f"{db_name}.db")
    create_db(db_name=db_name)

    # users
    users_schema = [("email", "TEXT"), ("password", "TEXT")]
    create_table(db_name=db_name, table_name="users", schema=users_schema)
    data = [("admin@admin.com", "admin"), ("avez@avez.com", "avez")]
    insert_data(db_name=db_name, table_name="users", data=data)

    # category
    category_schema = [("name", "TEXT")]
    create_table(db_name=db_name, table_name="category", schema=category_schema)
    data = [("Pizza"), ("Burger"), ("Cake"), ("Mojito")]
    insert_data(db_name=db_name, table_name="category", data=data)

    # items
    item_schema = [("name", "TEXT"), ("price", "FLOAT"), ("category_id", "INTEGER"), ("sold_items", "INTEGER")]
    create_table(db_name=db_name, table_name="item", schema=item_schema)
    data = [
        ("Veg Pizza", "242", "1", "10"),
        ("Non-Veg Pizza", "180", "1", "20"),
        ("Non-Veg Burger", "120", "2", "8"),
        ("Veg Burger", "80", "2", "12"),
        ("Choco Cake", "160", "3", "15"),
        ("Mango Cake", "160", "3", "4"),
        ("Red Velvet Cake", "160", "3", "9"),
        ("Mint Mojito", "60", "4", "7"),
        ("Virgin Mojito", "60", "4", "0"),
        ("Watermelon Mojito", "60", "4", "0"),
    ]
    insert_data(db_name=db_name, table_name="item", data=data)

    # coupon
    coupon_schema = [("name", "TEXT"), ("discount", "INTEGER")]
    create_table(db_name=db_name, table_name="coupon", schema=coupon_schema)
    data = [("RANDOMDISC", str(random.randint(10, 30)))]
    insert_data(db_name=db_name, table_name="coupon", data=data)

    # sale
    sale_schema = [("invoice_id", "TEXT"), ("discount", "INTEGER"), ("grand_total", "FLOAT"), ("payment_method", "TEXT")]
    create_table(db_name=db_name, table_name="sale", schema=sale_schema)
    payment_methods = ['credit_card', 'net_banking', 'upi', 'debit_card']
    for i in range(20):
        data = [(str(uuid.uuid4()), str(random.randint(0, 30)), str(random.randint(100, 1000)), random.choice(payment_methods))]
        insert_data(db_name=db_name, table_name="sale", data=data)
