# MySQL & SQLAlchemy Best Practices

This file summarizes best practices for using MySQL with Python and SQLAlchemy, including security, performance, and maintainability tips.

## 1. Connection Management
- Use SQLAlchemy's `create_engine` for connection pooling.
- Never hardcode credentials in code. Use environment variables or config files.
- Always close connections (use context managers: `with engine.connect() as conn:`).

## 2. Security
- Use parameterized queries to prevent SQL injection: `text("SELECT * FROM users WHERE id = :id")`
- Restrict database user privileges to the minimum required.
- Never expose database credentials in public repos.

## 3. Schema Design
- Use `INT AUTO_INCREMENT PRIMARY KEY` for surrogate keys.
- Always define explicit foreign keys and indexes for joins.
- Use `NOT NULL` and appropriate defaults for all columns.
- Normalize data, but denormalize for performance if needed.

## 4. Data Manipulation
- Use bulk inserts for large data loads: `executemany` or pandas `.to_sql()`
- Prefer `ON DUPLICATE KEY UPDATE` for upserts.
- Use `TRUNCATE` for fast table clearing (but beware of FK constraints).

## 5. Querying
- Use explicit column lists, not `SELECT *`.
- Use JOINs instead of subqueries for better performance.
- Use indexes on columns used in WHERE, JOIN, and ORDER BY.
- Use LIMIT for pagination.

## 6. Error Handling
- Catch and log exceptions; never expose raw DB errors to users.
- Use transactions (`with conn.begin(): ...`) for multi-step operations.
- Roll back on error to avoid partial updates.

## 7. Performance
- Profile queries with `EXPLAIN`.
- Avoid N+1 query problems (fetch related data in one query).
- Use connection pooling for high-concurrency apps.

## 8. Maintainability
- Use Alembic or similar for schema migrations.
- Document schema and business logic in code and README.
- Write unit tests for all DB logic.

---

Feel free to expand this file with more best practices as your project grows!
