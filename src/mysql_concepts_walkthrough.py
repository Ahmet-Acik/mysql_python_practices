"""
mysql_concepts_walkthrough.py
A script to demonstrate MySQL concepts: CREATE, ALTER, INSERT, UPDATE, DELETE, TRUNCATE, and DROP.
Each run starts from scratch for a clean demo.
"""

import sqlalchemy
from sqlalchemy import create_engine, text

# Connect to MySQL server (not a specific DB yet)
engine = create_engine('mysql+mysqlconnector://root:root7623@localhost')

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

    print("\n--- INSERT DEMONSTRATIONS ---")
    # 1. Basic single-row insert
    conn.execute(text("INSERT INTO customers (name) VALUES ('Alice')"))
    print("Inserted single row into customers.")

    # 2. Multi-row insert
    conn.execute(text("INSERT INTO customers (name) VALUES ('Bob'), ('Charlie')"))
    print("Inserted multiple rows into customers.")

    # 3. INSERT ... SET syntax (MySQL only)
    conn.execute(text("INSERT INTO customers SET name = 'Diana'"))
    print("Inserted using SET syntax.")

    # 4. INSERT IGNORE (will not error on duplicate, but will skip)
    conn.execute(text("INSERT IGNORE INTO customers (customer_id, name) VALUES (1, 'Duplicate Alice')"))
    print("Inserted with IGNORE (should skip duplicate PK).")

    # 5. INSERT ... ON DUPLICATE KEY UPDATE
    conn.execute(text("INSERT INTO customers (customer_id, name) VALUES (1, 'Alice Updated') ON DUPLICATE KEY UPDATE name = 'Alice Updated'"))
    print("Inserted with ON DUPLICATE KEY UPDATE (should update Alice).")

    # 6. INSERT with SELECT (copy data)
    conn.execute(text("INSERT INTO customers (name) SELECT name FROM customers WHERE name = 'Bob'"))
    print("Inserted with SELECT (copied Bob).")

    # 7. REPLACE INTO (insert or replace by PK)
    conn.execute(text("REPLACE INTO customers (customer_id, name) VALUES (2, 'Bob Replaced')"))
    print("REPLACE INTO (should replace Bob).")

    # 8. INSERT DEFAULT VALUES (if table allows, not used here since name is NOT NULL)
    # conn.execute(text("INSERT INTO customers () VALUES ()"))
    # print("Inserted default values (if allowed).")

    # Show all customers after inserts
    result = conn.execute(text("SELECT * FROM customers"))
    print("Customers after all INSERTs:")
    for row in result:
        print(row)

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

    print("\n--- ALTER TABLE DEMONSTRATIONS ---")
    # 1. ADD COLUMN
    conn.execute(text("ALTER TABLE customers ADD COLUMN email VARCHAR(100) DEFAULT 'unknown@example.com'"))
    print("Added email column to customers.")

    # 2. DROP COLUMN
    conn.execute(text("ALTER TABLE customers DROP COLUMN email"))
    print("Dropped email column from customers.")

    # 3. MODIFY COLUMN (change type)
    conn.execute(text("ALTER TABLE customers MODIFY COLUMN name VARCHAR(200) NOT NULL"))
    print("Modified 'name' column type to VARCHAR(200).")

    # 4. CHANGE COLUMN (rename and change type)
    conn.execute(text("ALTER TABLE customers CHANGE COLUMN name full_name VARCHAR(150) NOT NULL"))
    print("Renamed 'name' to 'full_name' and changed type to VARCHAR(150).")

    # 5. ADD INDEX
    conn.execute(text("ALTER TABLE customers ADD INDEX idx_full_name (full_name)"))
    print("Added index on full_name.")

    # 6. DROP INDEX
    conn.execute(text("ALTER TABLE customers DROP INDEX idx_full_name"))
    print("Dropped index on full_name.")

    # 7. ADD UNIQUE
    conn.execute(text("ALTER TABLE customers ADD UNIQUE uq_full_name (full_name)"))
    print("Added UNIQUE constraint on full_name.")

    # 8. DROP UNIQUE (by dropping the index)
    conn.execute(text("ALTER TABLE customers DROP INDEX uq_full_name"))
    print("Dropped UNIQUE constraint on full_name.")

    # 9. RENAME TABLE
    conn.execute(text("RENAME TABLE customers TO customers_renamed"))
    print("Renamed table 'customers' to 'customers_renamed'.")

    # 10. ADD COLUMN for FK demo
    conn.execute(text("ALTER TABLE customers_renamed ADD COLUMN ref_order_id INT NULL"))
    print("Added ref_order_id column for FK demo.")

    # 11. ADD FOREIGN KEY
    conn.execute(text("ALTER TABLE customers_renamed ADD CONSTRAINT fk_ref_order FOREIGN KEY (ref_order_id) REFERENCES orders(order_id)"))
    print("Added FOREIGN KEY constraint.")

    # 12. DROP FOREIGN KEY
    # Need to get the constraint name (MySQL auto-generates it if not named)
    fk_name = None
    result = conn.execute(text("SHOW CREATE TABLE customers_renamed"))
    for row in result:
        create_stmt = row[1]
        import re
        m = re.search(r'CONSTRAINT `([^`]*)` FOREIGN KEY', create_stmt)
        if m:
            fk_name = m.group(1)
    if fk_name:
        conn.execute(text(f"ALTER TABLE customers_renamed DROP FOREIGN KEY {fk_name}"))
        print(f"Dropped FOREIGN KEY constraint: {fk_name}")
    else:
        print("Could not find FK constraint name to drop.")

    # SHOW COLUMNS
    result = conn.execute(text("SHOW COLUMNS FROM customers_renamed"))
    print("Columns in customers_renamed:")
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
