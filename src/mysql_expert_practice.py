"""
mysql_expert_practice.py
A script to practice expert-level MySQL concepts: advanced SELECTs, transactions, partitioning, foreign key actions, error handling in procedures, performance, temporary tables, JSON data, event scheduler, and import/export.
Each run starts from scratch for a clean demo.
"""
import sqlalchemy
from sqlalchemy import create_engine, text

engine = create_engine('mysql+mysqldb://root:root7623@localhost')

with engine.connect() as conn:
    # Create and use database if not exists
    conn.execute(text("CREATE DATABASE IF NOT EXISTS expert_demo_db"))
    print("Created expert_demo_db if not exists.")
    conn.execute(text("USE expert_demo_db"))
    print("Using expert_demo_db.")

    # 1. Advanced SELECTs: window functions, subqueries
    try:
        conn.execute(text('''
            CREATE TABLE sales (
                sale_id INT AUTO_INCREMENT PRIMARY KEY,
                salesperson VARCHAR(100),
                amount DECIMAL(10,2),
                sale_date DATE
            )
        '''))
        conn.execute(text("""
            INSERT INTO sales (salesperson, amount, sale_date) VALUES
            ('Alice', 100, '2025-09-01'),
            ('Bob', 200, '2025-09-01'),
            ('Alice', 150, '2025-09-02'),
            ('Bob', 300, '2025-09-02'),
            ('Alice', 250, '2025-09-03')
        """))
        print("Inserted sales data.")
        result = conn.execute(text('''
            SELECT salesperson, amount, sale_date,
                   SUM(amount) OVER (PARTITION BY salesperson ORDER BY sale_date) AS running_total
            FROM sales
        '''))
        print("Window function (running total):")
        for row in result:
            print(row)
        result = conn.execute(text('''
            SELECT s1.* FROM sales s1
            WHERE amount > (SELECT AVG(amount) FROM sales)
        '''))
        print("Subquery (sales above average):")
        for row in result:
            print(row)
    except Exception as e:
        print("Advanced SELECTs or window functions may not be supported:", e)

    # 2. Transactions: isolation levels
    try:
        conn.execute(text("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED"))
        # End any implicit transaction before starting a new one
        conn.commit()
        with conn.begin():
            conn.execute(text("INSERT INTO sales (salesperson, amount, sale_date) VALUES ('Carol', 500, '2025-09-04')"))
            raise Exception("Simulated error")
    except Exception as e:
        print("Transaction rolled back or isolation level not supported:", e)

    # 3. Partitioning (requires MySQL 5.7+ and proper settings)
    try:
        # Partition key must be part of every unique key (including PK)
        conn.execute(text('''
            CREATE TABLE part_sales (
                sale_id INT,
                sale_year INT,
                amount DECIMAL(10,2),
                sale_date DATE,
                PRIMARY KEY (sale_id, sale_year)
            ) PARTITION BY RANGE (sale_year) (
                PARTITION p2025 VALUES LESS THAN (2026),
                PARTITION pmax VALUES LESS THAN MAXVALUE
            )
        '''))
        print("Created partitioned table part_sales.")
    except Exception as e:
        print("Partitioning may not be supported:", e)

    # 4. Foreign Key Actions
    try:
        conn.execute(text('''
            CREATE TABLE parent (
                id INT PRIMARY KEY
            )
        '''))
        conn.execute(text('''
            CREATE TABLE child (
                id INT PRIMARY KEY,
                parent_id INT,
                FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE CASCADE
            )
        '''))
        print("Created parent/child tables with ON DELETE CASCADE.")
    except Exception as e:
        print("Foreign key actions may not be supported:", e)

    # 5. Error Handling in Procedures (may not work via SQLAlchemy)
    try:
        conn.execute(text('''
            CREATE PROCEDURE safe_insert(IN val INT)
            BEGIN
                DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
                BEGIN
                    SELECT 'Error occurred';
                END;
                INSERT INTO parent (id) VALUES (val);
            END
        '''))
        print("Created procedure with error handler.")
    except Exception as e:
        print("Procedure with error handler may already exist or error (often not supported via SQLAlchemy):", e)

    # 6. Performance: EXPLAIN
    try:
        result = conn.execute(text("EXPLAIN SELECT * FROM sales WHERE amount > 100"))
        print("EXPLAIN plan:")
        for row in result:
            print(row)
    except Exception as e:
        print("EXPLAIN may not be supported:", e)

    # 7. Temporary Tables
    try:
        conn.execute(text("CREATE TEMPORARY TABLE temp_sales AS SELECT * FROM sales WHERE amount > 100"))
        result = conn.execute(text("SELECT * FROM temp_sales"))
        print("Temporary table temp_sales:")
        for row in result:
            print(row)
    except Exception as e:
        print("Temporary tables may not be supported:", e)

    # 8. JSON Data (requires MySQL 5.7+)
    try:
        conn.execute(text('''
            CREATE TABLE json_test (
                id INT PRIMARY KEY,
                data JSON
            )
        '''))
        conn.execute(text('''
            INSERT INTO json_test VALUES (1, '{"a": 1, "b": 2}')
        '''))
        result = conn.execute(text("SELECT data->'$.a' AS a_value FROM json_test"))
        print("JSON column query:")
        for row in result:
            print(row)
    except Exception as e:
        print("JSON columns may not be supported:", e)

    # 9. Event Scheduler (if enabled)
    try:
        conn.execute(text('''
            CREATE EVENT my_event
            ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 1 MINUTE
            DO
                INSERT INTO sales (salesperson, amount, sale_date) VALUES ('Event', 999, CURRENT_DATE)
        '''))
        print("Created event my_event.")
    except Exception as e:
        print("Event may not be enabled or error:", e)

    # 11. Spatial Data (requires MySQL with spatial support)
    try:
        conn.execute(text('''
            CREATE TABLE locations (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                position POINT
            )
        '''))
        conn.execute(text("""
            INSERT INTO locations VALUES (1, 'A', ST_GeomFromText('POINT(10 20)')),
                                         (2, 'B', ST_GeomFromText('POINT(15 25)'))
        """))
        result = conn.execute(text("SELECT id, name, ST_AsText(position) FROM locations"))
        print("Spatial data (locations):")
        for row in result:
            print(row)
    except Exception as e:
        print("Spatial data may not be supported:", e)

    # 12. Full-Text Search (requires MySQL with full-text support)
    try:
        conn.execute(text('''
            CREATE TABLE articles (
                id INT PRIMARY KEY,
                title VARCHAR(200),
                body TEXT,
                FULLTEXT(title, body)
            )
        '''))
        conn.execute(text("""
            INSERT INTO articles VALUES
                (1, 'MySQL Full-Text', 'This article is about MySQL full-text search.'),
                (2, 'Python and MySQL', 'Using Python to access MySQL databases.'),
                (3, 'Advanced SQL', 'Window functions, CTEs, and more.')
        """))
        result = conn.execute(text("SELECT id, title FROM articles WHERE MATCH(title, body) AGAINST('MySQL')"))
        print("Full-text search results for 'MySQL':")
        for row in result:
            print(row)
    except Exception as e:
        print("Full-text search may not be supported:", e)

    # 13. Performance Tuning: Index hints and ANALYZE
    try:
        result = conn.execute(text("SELECT * FROM sales USE INDEX () WHERE amount > 100"))
        print("Query with index hint (USE INDEX()):")
        for row in result:
            print(row)
        conn.execute(text("ANALYZE TABLE sales"))
        print("Analyzed sales table for performance stats.")
    except Exception as e:
        print("Performance tuning features may not be supported:", e)

    # 14. Replication and Advanced Security
    # NOTE: These require server configuration and admin rights, so only commented as guidance.
    # -- Replication: SETUP MASTER/SLAVE, CHANGE MASTER TO, START SLAVE, SHOW SLAVE STATUS
    # -- Security: CREATE USER, GRANT/REVOKE, SSL, PASSWORD POLICIES, AUDIT PLUGINS
    print("Replication and advanced security require server configuration and are not demoed in this script.")

    # 10. Import/Export (skipped: requires file access)
    # Clean up
    conn.execute(text("DROP DATABASE expert_demo_db"))
    print("Dropped expert_demo_db.")
