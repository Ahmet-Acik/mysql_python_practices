"""
mysql_advanced_practice.py
A script to practice advanced MySQL concepts: constraints, indexes, views, stored procedures, functions, triggers, transactions, user management, advanced SELECT, and import/export.
Each run starts from scratch for a clean demo.
"""
import sqlalchemy
from sqlalchemy import create_engine, text

# Update with your actual connection string
engine = create_engine('mysql+mysqldb://root:root7623@localhost')

with engine.connect() as conn:
    # Drop and create database
    conn.execute(text("DROP DATABASE IF EXISTS adv_demo_db"))
    print("Dropped database if existed.")
    conn.execute(text("CREATE DATABASE adv_demo_db"))
    print("Created adv_demo_db.")
    conn.execute(text("USE adv_demo_db"))
    print("Using adv_demo_db.")

    # 1. Constraints & Indexes
    conn.execute(text('''
        CREATE TABLE customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            age INT DEFAULT 18 CHECK (age >= 18)
        )
    '''))
    print("Created customers table with constraints.")

    conn.execute(text('''
        CREATE TABLE orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            order_date DATE DEFAULT (CURRENT_DATE),
            status VARCHAR(20) DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    '''))
    print("Created orders table with constraints.")

    # Indexes
    conn.execute(text("CREATE INDEX idx_customer_name ON customers(name)"))
    print("Created index on customers(name).")
    conn.execute(text("CREATE INDEX idx_order_customer_status ON orders(customer_id, status)"))
    print("Created multi-column index on orders(customer_id, status).")
    conn.execute(text("DROP INDEX idx_customer_name ON customers"))
    print("Dropped index idx_customer_name from customers.")

    # 2. Views
    conn.execute(text('''
        CREATE VIEW customer_order_summary AS
        SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
    '''))
    print("Created view customer_order_summary.")
    result = conn.execute(text("SELECT * FROM customer_order_summary"))
    print("View: customer_order_summary")
    for row in result:
        print(row)
    conn.execute(text("DROP VIEW customer_order_summary"))
    print("Dropped view customer_order_summary.")

    # 3. Stored Procedures & Functions
    # Stored Procedure (no DELIMITER)
    try:
        conn.execute(text('''
            CREATE PROCEDURE insert_customer(IN cname VARCHAR(100), IN cemail VARCHAR(100), IN cage INT)
            BEGIN
                INSERT INTO customers (name, email, age) VALUES (cname, cemail, cage);
            END
        '''))
        print("Created stored procedure insert_customer.")
    except Exception as e:
        print("Stored procedure insert_customer may already exist or error:", e)
    conn.execute(text("CALL insert_customer('Eve', 'eve@example.com', 25)"))
    print("Called stored procedure insert_customer.")

    # Function (no DELIMITER)
    try:
        conn.execute(text('''
            CREATE FUNCTION order_count(cid INT) RETURNS INT
            DETERMINISTIC
            BEGIN
                DECLARE cnt INT;
                SELECT COUNT(*) INTO cnt FROM orders WHERE customer_id = cid;
                RETURN cnt;
            END
        '''))
        print("Created function order_count.")
    except Exception as e:
        print("Function order_count may already exist or error:", e)
    result = conn.execute(text("SELECT order_count(1) AS orders_for_1"))
    print("Function order_count(1):", [row for row in result])

    # 4. Triggers
    conn.execute(text('''
        CREATE TABLE order_log (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            action VARCHAR(20),
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''))
    print("Created order_log table.")
    try:
        conn.execute(text('''
            CREATE TRIGGER after_order_insert
            AFTER INSERT ON orders
            FOR EACH ROW
            BEGIN
                INSERT INTO order_log (order_id, action) VALUES (NEW.order_id, 'INSERT');
            END
        '''))
        print("Created trigger after_order_insert.")
    except Exception as e:
        print("Trigger after_order_insert may already exist or error:", e)
    conn.execute(text("INSERT INTO orders (customer_id) VALUES (1)"))
    print("Inserted order to trigger after_order_insert.")
    result = conn.execute(text("SELECT * FROM order_log"))
    print("Order log:")
    for row in result:
        print(row)

    # 5. Transactions
    try:
        with conn.begin():
            conn.execute(text("INSERT INTO customers (name, email, age) VALUES ('FailTest', 'fail@example.com', 17)"))
    except Exception as e:
        print("Transaction failed (age < 18, check constraint):", e)

    # 6. User Management & Permissions (requires admin)
    # Uncomment if you have privileges
    # conn.execute(text("CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpass'"))
    # conn.execute(text("GRANT SELECT ON adv_demo_db.* TO 'testuser'@'localhost'"))
    # print("Created user and granted SELECT.")
    # conn.execute(text("REVOKE SELECT ON adv_demo_db.* FROM 'testuser'@'localhost'"))
    # print("Revoked SELECT from testuser.")
    # conn.execute(text("DROP USER 'testuser'@'localhost'"))
    # print("Dropped testuser.")

    # 7. Advanced SELECT
    result = conn.execute(text('''
        SELECT customer_id, COUNT(*) AS num_orders
        FROM orders
        GROUP BY customer_id
        HAVING num_orders > 0
    '''))
    print("Advanced SELECT (GROUP BY, HAVING):")
    for row in result:
        print(row)

    # 8. Clean up
    conn.execute(text("DROP DATABASE adv_demo_db"))
    print("Dropped adv_demo_db.")
