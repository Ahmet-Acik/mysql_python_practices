"""
sql_practice_examples.py

A collection of real-world SQL practice examples using SQLAlchemy and pandas.
Each example demonstrates a best practice for SQL in Python, with comments explaining the rationale.

Assumes a MySQL database with a logistics schema (customers, products, orders, order_items).
Update the connection string as needed for your environment.
"""

import pandas as pd
from sqlalchemy import create_engine, text

# Best Practice: Never hardcode credentials in production; use environment variables or config files
engine = create_engine('mysql+mysqldb://root:root7623@localhost:3306/logistics_db')

# Utility function for displaying results
def show_df(df, title=None):
    if title:
        print(f"\n=== {title} ===")
    print(df.head())

# 1. Total sales by product
# Best Practice: Use explicit JOINs, GROUP BY, and ORDER BY for clarity
# Best Practice: Avoid SELECT *; specify columns needed
def total_sales_by_product():
    query = '''
    SELECT p.name AS product, SUM(oi.quantity * p.price) AS total_sales
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY p.id, p.name
    ORDER BY total_sales DESC;
    '''
    df = pd.read_sql(query, engine)
    show_df(df, "Total Sales by Product")

# 2. Top 5 customers by revenue
# Best Practice: Use LIMIT for pagination/top-N queries
# Best Practice: Use aggregation and GROUP BY for business metrics
def top_customers_by_revenue():
    query = '''
    SELECT c.name AS customer, SUM(oi.quantity * p.price) AS revenue
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY c.id, c.name
    ORDER BY revenue DESC
    LIMIT 5;
    '''
    df = pd.read_sql(query, engine)
    show_df(df, "Top 5 Customers by Revenue")

# 3. Parameterized query to prevent SQL injection
# Best Practice: Use parameterized queries for user input
def orders_for_customer(customer_name):
    query = '''
    SELECT o.id, o.order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE c.name = %s
    '''
    df = pd.read_sql(query, engine, params=(customer_name,))
    show_df(df, f"Orders for Customer: {customer_name}")

# 4. CTE for complex queries
# Best Practice: Use CTEs (WITH) for readability
def high_value_customers(threshold=10000):
    query = f'''
    WITH customer_revenue AS (
        SELECT c.id, c.name, SUM(oi.quantity * p.price) AS revenue
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        GROUP BY c.id, c.name
    )
    SELECT name, revenue
    FROM customer_revenue
    WHERE revenue > {threshold}
    ORDER BY revenue DESC;
    '''
    df = pd.read_sql(query, engine)
    show_df(df, f"Customers with Revenue > {threshold}")

# 5. Avoid SELECT *; specify columns
# Best Practice: Only select needed columns
def customer_columns():
    query = 'SELECT id, name, email FROM customers;'
    df = pd.read_sql(query, engine)
    show_df(df, "Customer Columns")

# 6. Transactions for multi-step changes
# Best Practice: Use transactions for atomicity
def insert_order_with_items(customer_id, items):
    """
    Insert a new order and associated order_items atomically.
    items: list of (product_id, quantity)
    """
    with engine.begin() as conn:
        conn.execute(text('''
            INSERT INTO orders (customer_id, order_date)
            VALUES (:customer_id, NOW())
        '''), {"customer_id": customer_id})
        order_id = conn.execute(text('SELECT LAST_INSERT_ID()')).scalar()
        for product_id, quantity in items:
            conn.execute(text('''
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (:order_id, :product_id, :quantity)
            '''), {"order_id": order_id, "product_id": product_id, "quantity": quantity})
    print(f"Inserted order {order_id} for customer {customer_id}")

# 7. Analyze and optimize queries
# Best Practice: Use EXPLAIN and indexes
def explain_orders_query():
    query = 'EXPLAIN SELECT * FROM orders WHERE customer_id = 1;'
    df = pd.read_sql(query, engine)
    show_df(df, "EXPLAIN Orders Query")
    # To create an index (uncomment if needed):
    # with engine.connect() as conn:
    #     conn.execute(text('CREATE INDEX idx_orders_customer_id ON orders(customer_id);'))

# 8. Test queries with edge cases and large datasets
# Best Practice: Always test with empty, NULL, and large data sets
def test_edge_cases():
    # Example: Query with no results
    query = 'SELECT * FROM customers WHERE name = "Nonexistent";'
    df = pd.read_sql(query, engine)
    show_df(df, "Edge Case: No Results")
    # Example: Paginate large results
    query = 'SELECT * FROM orders LIMIT 5 OFFSET 0;'
    df = pd.read_sql(query, engine)
    show_df(df, "Paginated Orders (First 5)")

# 9. Readable SQL with indentation, aliases, and comments
def readable_sql_example():
    query = '''
    SELECT
        c.name AS customer, -- Customer name
        COUNT(o.id) AS total_orders, -- Number of orders
        SUM(oi.quantity * p.price) AS total_spent -- Total spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY c.id, c.name
    ORDER BY total_spent DESC
    LIMIT 10
    '''
    df = pd.read_sql(query, engine)
    show_df(df, "Readable SQL Example")

# 10. Explicit vs. implicit JOINs
def explicit_vs_implicit_joins():
    # Explicit JOIN (recommended)
    query_explicit = '''
    SELECT c.name, o.id
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    '''
    df_explicit = pd.read_sql(query_explicit, engine)
    show_df(df_explicit, "Explicit JOIN")
    # Implicit join (not recommended)
    query_implicit = '''
    SELECT c.name, o.id
    FROM customers c, orders o
    WHERE c.id = o.customer_id
    '''
    df_implicit = pd.read_sql(query_implicit, engine)
    show_df(df_implicit, "Implicit JOIN")

# Example: Batch insert with error handling
def batch_insert_products(products):
    """
    Insert multiple products in a single transaction.
    products: list of dicts with keys 'name', 'price'
    """
    from sqlalchemy.exc import SQLAlchemyError
    try:
        with engine.begin() as conn:
            for prod in products:
                conn.execute(text('''
                    INSERT INTO products (name, price)
                    VALUES (:name, :price)
                '''), prod)
        print(f"Inserted {len(products)} products.")
    except SQLAlchemyError as e:
        print("Batch insert failed:", e)

# Example: Run a SQL file
def run_sql_file(filepath):
    """
    Execute all SQL statements in a .sql file.
    """
    with open(filepath, 'r') as file:
        sql_script = file.read()
    with engine.begin() as conn:
        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
    print(f"Executed SQL file: {filepath}")

# Example: Window function (running total)
def running_total_orders():
    query = '''
SELECT t1.id, t1.customer_id, t1.created_at,
       (SELECT SUM(t2.total_amount)
        FROM shipments t2
        WHERE t2.created_at <= t1.created_at) AS running_total
FROM shipments t1
ORDER BY t1.created_at
'''
    df = pd.read_sql(query, engine)
    show_df(df, "Running Total of Orders")

# Example: CTE for recursive queries (if supported)
def cte_example_recursive():
    # Example assumes a table 'categories' with id, name, parent_id
    query = '''
    WITH RECURSIVE category_tree AS (
        SELECT category_id, name, parent_id, 0 AS level
        FROM categories
        WHERE parent_id IS NULL
        UNION ALL
        SELECT c.category_id, c.name, c.parent_id, ct.level + 1
        FROM categories c
        JOIN category_tree ct ON c.parent_id = ct.category_id
    )
    SELECT * FROM category_tree ORDER BY level, name;
    '''
    try:
        df = pd.read_sql(query, engine)
        show_df(df, "Category Tree (Recursive CTE)")
    except Exception as e:
        print("Recursive CTE not supported or error:", e)


if __name__ == "__main__":
    total_sales_by_product()
    top_customers_by_revenue()
    orders_for_customer('Alice')
    high_value_customers(10000)
    customer_columns()
    insert_order_with_items(1, [(2, 3), (3, 1)])
    explain_orders_query()
    test_edge_cases()
    readable_sql_example()
    explicit_vs_implicit_joins()
    batch_insert_products([
        {'name': 'New Product 1', 'price': 19.99},
        {'name': 'New Product 2', 'price': 29.99}
    ])
    # run_sql_file('path/to/your/script.sql')  # Uncomment and provide path
    running_total_orders()
    cte_example_recursive() # May not work if MySQL version < 8.0
