
# MySQL Python Practices

This project is a hands-on collection of Python scripts for learning and practicing MySQL concepts, from beginner to expert level. It uses SQLAlchemy and pandas for modern, best-practice database interaction.

## Features

- **mysql_concepts_walkthrough.py**: Demonstrates MySQL basics (CREATE, ALTER, INSERT, UPDATE, DELETE, TRUNCATE, DROP).
- **mysql_advanced_practice.py**: Covers advanced MySQL (constraints, indexes, views, stored procedures, triggers, transactions, user management, import/export).
- **mysql_expert_practice.py**: Explores expert topics (window functions, partitioning, error handling, performance, JSON, event scheduler, temporary tables).
- **sql_practice_examples.py**: Real-world SQL examples using SQLAlchemy and pandas, with best practices and comments. Connects to an existing `logistics_db` (never drops/creates it).

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
- All credentials are managed securely via a `.env` file (never hardcoded). See `.env.example` for the required variables.
- Update your `.env` file with your MySQL credentials and host.
- **Database management:**
  - `sql_practice_examples.py` connects to an existing `logistics_db` (managed by another app; never dropped/created by this script).
  - `mysql_concepts_walkthrough.py`, `mysql_advanced_practice.py`, and `mysql_expert_practice.py` create/drop their own demo databases (`demo_db`, `adv_demo_db`, `expert_demo_db`) for a clean run each time.
- If you need the schema for `logistics_db`, see the `app/models.py` example in this repo or ask your app maintainer.

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


> **Note:** Never hardcode credentials in production. Use a `.env` file (gitignored) and `python-dotenv` for secure credential management. All scripts in this repo follow this best practice.

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
