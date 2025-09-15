"""
mysql_concepts_walkthrough.py
A script to demonstrate MySQL concepts: CREATE, ALTER, INSERT, UPDATE, DELETE, TRUNCATE, and DROP.
Each run starts from scratch for a clean demo.
"""

import sqlalchemy
from sqlalchemy import create_engine, text
from db_utils import get_engine

# Connect to MySQL server (not a specific DB yet)
# Get the SQLAlchemy engine from utility function for better security and maintainability
engine = get_engine()

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

    print("\n--- UPDATE DEMONSTRATIONS ---")
    # All updates on 'customers' table before ALTER/RENAME
    # 1. Basic UPDATE (single row)
    conn.execute(text("UPDATE customers SET name = 'Alice Smith' WHERE customer_id = 1"))
    print("Updated name for customer_id=1 in customers.")

    # 2. UPDATE multiple rows
    conn.execute(text("UPDATE customers SET name = 'Updated Name' WHERE customer_id IN (2, 3)"))
    print("Updated name for customer_id=2 and 3 in customers.")

    # 3. UPDATE with WHERE and AND/OR
    conn.execute(text("UPDATE customers SET name = 'Special Name' WHERE customer_id = 4 OR name = 'Diana'"))
    print("Updated name for customer_id=4 or name='Diana' in customers.")

    # Show all customers after updates
    result = conn.execute(text("SELECT * FROM customers"))
    print("customers after all UPDATEs:")
    for row in result:
        print(row)

    # Demonstrate DELETE

    print("\n--- DELETE DEMONSTRATIONS ---")
    # 1. Basic DELETE (single row)
    conn.execute(text("DELETE FROM order_items WHERE item_id = 1"))
    print("Deleted order_item with item_id=1.")

    # 2. DELETE multiple rows with WHERE
    conn.execute(text("DELETE FROM order_items WHERE product = 'Widget'"))
    print("Deleted all order_items with product='Widget'.")

    # 3. DELETE all rows (DELETE vs TRUNCATE)
    # First, ensure a valid order_id exists
    order_id_result = conn.execute(text("SELECT order_id FROM orders LIMIT 1"))
    order_id_row = order_id_result.fetchone()
    if order_id_row:
        valid_order_id = order_id_row[0]
    else:
        # Insert a new order if none exist
        conn.execute(text("INSERT INTO orders (customer_id, order_date) VALUES (NULL, CURDATE())"))
        valid_order_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()
    # Insert a row to demonstrate
    conn.execute(text(f"INSERT INTO order_items (order_id, product, quantity) VALUES ({valid_order_id}, 'Temp', 1)"))
    conn.execute(text("DELETE FROM order_items"))
    print("Deleted all rows from order_items with DELETE.")

    # 4. DELETE with JOIN (delete customers_renamed with no orders)

    # 5. DELETE with ORDER BY and LIMIT (delete only one row)
    # First, insert two rows to demonstrate
    # Ensure a valid order_id exists
    order_id_result = conn.execute(text("SELECT order_id FROM orders LIMIT 1"))
    order_id_row = order_id_result.fetchone()
    if order_id_row:
        valid_order_id = order_id_row[0]
    else:
        conn.execute(text("INSERT INTO orders (customer_id, order_date) VALUES (NULL, CURDATE())"))
        valid_order_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()
    conn.execute(text(f"INSERT INTO order_items (order_id, product, quantity) VALUES ({valid_order_id}, 'Demo1', 1), ({valid_order_id}, 'Demo2', 2)"))
    conn.execute(text("DELETE FROM order_items ORDER BY item_id LIMIT 1"))
    print("Deleted one row from order_items using ORDER BY and LIMIT.")

    # 6. DELETE with subquery (delete order_items for orders placed today)
    today = conn.execute(text("SELECT CURDATE()")).scalar()
    conn.execute(text(f"DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE order_date = '{today}')"))
    print("Deleted order_items for orders placed today (using subquery).")

    # Show all order_items after deletes
    result = conn.execute(text("SELECT * FROM order_items"))
    print("order_items after all DELETEs:")
    for row in result:
        print(row)

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

    # Ensure all values in full_name are unique before adding UNIQUE constraint
    # Add a suffix to duplicates
    result = conn.execute(text("SELECT full_name, COUNT(*) FROM customers GROUP BY full_name HAVING COUNT(*) > 1"))
    duplicates = [row[0] for row in result]
    for dup in duplicates:
        # Get all customer_ids with this duplicate name, skip the first
        ids = [row[0] for row in conn.execute(text(f"SELECT customer_id FROM customers WHERE full_name = '{dup}' ORDER BY customer_id"))]
        for idx, cid in enumerate(ids[1:], start=2):
            conn.execute(text(f"UPDATE customers SET full_name = CONCAT(full_name, '_{idx}') WHERE customer_id = {cid}"))
    print("Ensured all full_name values are unique before adding UNIQUE constraint.")

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

    # 10. ADD COLUMN for FK demo (and for update demo)
    # Robust check: only add ref_order_id if it does not exist
    result = conn.execute(text("SHOW COLUMNS FROM customers_renamed LIKE 'ref_order_id'"))
    if result.fetchone() is None:
        conn.execute(text("ALTER TABLE customers_renamed ADD COLUMN ref_order_id INT NULL"))
        print("Added ref_order_id column for FK demo.")
    else:
        print("Column ref_order_id already exists in customers_renamed. Skipping add.")

    # --- UPDATE DEMONSTRATIONS ON customers_renamed ---
    print("\n--- UPDATE DEMONSTRATIONS ON customers_renamed ---")

    # 4. UPDATE with JOIN (set ref_order_id in customers_renamed based on orders)
    conn.execute(text("UPDATE customers_renamed c JOIN orders o ON c.customer_id = o.customer_id SET c.ref_order_id = o.order_id WHERE o.order_id = 1"))
    print("Updated ref_order_id in customers_renamed using JOIN.")

    # 5. UPDATE with ORDER BY and LIMIT (set only one row)
    conn.execute(text("UPDATE customers_renamed SET full_name = 'Limited Update' ORDER BY customer_id LIMIT 1"))
    print("Updated only one row in customers_renamed using ORDER BY and LIMIT.")

    # 6. UPDATE using expressions (increment customer_id for demo, not typical)
    # conn.execute(text("UPDATE customers_renamed SET customer_id = customer_id + 10 WHERE customer_id < 10"))
    # print("Incremented customer_id by 10 for those < 10 in customers_renamed.")

    # 7. UPDATE with subquery (set full_name to 'FromSubquery' for customers with min customer_id)

    # MySQL does not allow updating and selecting from the same table in a subquery. Workaround:
    min_id_result = conn.execute(text("SELECT MIN(customer_id) FROM customers_renamed"))
    min_id = min_id_result.scalar()
    if min_id is not None:
        conn.execute(text(f"UPDATE customers_renamed SET full_name = 'FromSubquery' WHERE customer_id = {min_id}"))
        print(f"Updated full_name for customer with min customer_id ({min_id}) in customers_renamed using subquery workaround.")
    else:
        print("No rows in customers_renamed to update with subquery.")

    # Show all customers_renamed after updates
    result = conn.execute(text("SELECT * FROM customers_renamed"))
    print("customers_renamed after all UPDATEs:")
    for row in result:
        print(row)

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
