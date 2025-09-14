
# MySQL Python Practices

This project is a hands-on collection of Python scripts for learning and practicing MySQL concepts, from beginner to expert level. It uses SQLAlchemy and pandas for modern, best-practice database interaction.

## Features

- **mysql_concepts_walkthrough.py**: Demonstrates MySQL basics (CREATE, ALTER, INSERT, UPDATE, DELETE, TRUNCATE, DROP).
- **mysql_advanced_practice.py**: Covers advanced MySQL (constraints, indexes, views, stored procedures, triggers, transactions, user management, import/export).
- **mysql_expert_practice.py**: Explores expert topics (window functions, partitioning, error handling, performance, JSON, event scheduler, temporary tables).
- **sql_practice_examples.py**: Real-world SQL examples using SQLAlchemy and pandas, with best practices and comments.

## Project Structure

- `src/` – All practice scripts and exercises
- `tests/` – (For future test scripts)
- `docs/` – (For documentation and notes)
- `requirements.txt` – Python dependencies

## Dependencies

Install all dependencies with `pip install -r requirements.txt`.

- `mysql-connector-python`
- `sqlalchemy`
- `pandas`

## Database Setup

- Requires a running MySQL server (local or remote).
- Update the connection string in each script for your MySQL credentials and host.
- Some scripts create and drop databases for a clean demo each run.
- Example schemas: `logistics_db`, `demo_db`, `adv_demo_db`, `expert_demo_db` (created automatically by scripts).

## Setup

1. **Clone the repository**
2. **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Script Usage

Run any script from the `src/` folder. For example:

```bash
python src/mysql_concepts_walkthrough.py
python src/mysql_advanced_practice.py
python src/mysql_expert_practice.py
python src/sql_practice_examples.py
```

> **Note:** Never hardcode credentials in production. Use environment variables or config files for sensitive data.

## Troubleshooting

- **MySQL connection errors:**
   - Ensure MySQL server is running and accessible.
   - Check your username, password, and host in the connection string.
   - Install the required MySQL driver (`mysql-connector-python`).
- **Permission errors:**
   - Make sure your MySQL user has privileges to create/drop databases.
- **Module not found:**
   - Double-check that all dependencies are installed in your virtual environment.

## Contributing

Feel free to add new scripts, tests, or documentation! Open issues or pull requests for improvements.
