"""
mysql_concepts_walkthrough.py
A script to demonstrate MySQL concepts: CREATE, ALTER, INSERT, UPDATE, DELETE, TRUNCATE, and DROP.
Each run starts from scratch for a clean demo.
"""

import sqlalchemy
from sqlalchemy import create_engine, text

# Connect to MySQL server (not a specific DB yet)
engine = create_engine('mysql+mysqldb://root:root7623@localhost')

with engine.connect() as conn:
    # Drop and create database
    conn.execute(text("DROP DATABASE IF EXISTS demo_db"))
    print("Dropped database if existed.")
    conn.execute(text("CREATE DATABASE demo_db"))
    print("Created demo_db.")
    conn.execute(text("USE demo_db"))
    print("Using demo_db.")

    # SHOW DATABASES
    result = conn.execute(text("SHOW DATABASES"))
    print("Databases:")
    for row in result:
        print(row[0])

    # Create tables: customers, orders, order_items
    conn.execute(text("""
        CREATE TABLE customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """))
    print("Created customers table.")

    conn.execute(text("""
        CREATE TABLE orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """))
    print("Created orders table.")

    conn.execute(text("""
        CREATE TABLE order_items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            product VARCHAR(100),
            quantity INT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """))
    print("Created order_items table.")

    # SHOW TABLES
    result = conn.execute(text("SHOW TABLES"))
    print("Tables in demo_db:")
    for row in result:
        print(row[0])

    # INSERT sample data
    conn.execute(text("INSERT INTO customers (name) VALUES ('Alice'), ('Bob')"))
    conn.execute(text("INSERT INTO orders (customer_id, order_date) VALUES (1, '2025-09-14'), (2, '2025-09-14')"))
    conn.execute(text("INSERT INTO order_items (order_id, product, quantity) VALUES (1, 'Widget', 3), (1, 'Gadget', 2), (2, 'Widget', 1)"))
    print("Inserted sample data.")

    # SELECT with JOIN
    result = conn.execute(text('''
        SELECT c.name, o.order_id, oi.product, oi.quantity
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
    '''))
    print("Joined data:")
    for row in result:
        print(row)

    # Demonstrate UPDATE
    conn.execute(text("UPDATE customers SET name = 'Alice Smith' WHERE customer_id = 1"))
    print("Updated customer name.")

    # Demonstrate DELETE
    conn.execute(text("DELETE FROM order_items WHERE item_id = 3"))
    print("Deleted one order item.")

    # Demonstrate ALTER TABLE
    conn.execute(text("ALTER TABLE customers ADD COLUMN email VARCHAR(100) DEFAULT 'unknown@example.com'"))
    print("Added email column to customers.")

    # SHOW COLUMNS
    result = conn.execute(text("SHOW COLUMNS FROM customers"))
    print("Columns in customers:")
    for row in result:
        print(row)

    # Demonstrate TRUNCATE
    conn.execute(text("TRUNCATE TABLE order_items"))
    print("Truncated order_items table.")

    # Demonstrate DROP TABLE
    conn.execute(text("DROP TABLE order_items"))
    print("Dropped order_items table.")

    # Clean up: drop database
    conn.execute(text("DROP DATABASE demo_db"))
    print("Dropped demo_db.")
