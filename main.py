import mysql.connector
import time
from rich.console import Console
from rich.table import Table
from contextlib import contextmanager

console = Console()


@contextmanager
def mysql_cursor():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="test_performance"
    )
    cursor = conn.cursor(dictionary=True)
    yield cursor
    conn.commit()
    cursor.close()
    conn.close()


def execute_and_time(cursor, sql):
    start = time.time()
    cursor.execute(sql)
    cursor.fetchall()
    end = time.time()
    return round((end - start) * 1000, 2)


def run_benchmarks():
    queries = [
        {
            "label": "Complex Query 1",
            "sql": """
                SELECT product_name, city, state, platform, device_type, AVG(price) AS avg_price
                FROM test_data
                WHERE price > 500 AND rating > 3 AND is_new_customer = TRUE AND status = 'delivered'
                GROUP BY product_name, city, state, platform, device_type
                ORDER BY avg_price DESC
                LIMIT 20;
            """,
        },
        {
            "label": "Complex Query 2",
            "sql": """
                SELECT td1.product_name, td1.city, td1.price
                FROM test_data td1
                WHERE td1.price = (
                    SELECT MAX(td2.price) FROM test_data td2 WHERE td2.city = td1.city
                ) AND td1.rating >= 4
                LIMIT 20;
            """,
        },
    ]

    table = Table(title="Benchmark Results")
    table.add_column("Query")
    table.add_column("Execution Time (ms)")

    with mysql_cursor() as cursor:
        for q in queries:
            duration = execute_and_time(cursor, q["sql"])
            table.add_row(q["label"], str(duration))

    console.print(table)


def setup_indexes():
    with mysql_cursor() as cursor:
        console.print("[bold]Creating indexes...[/bold]")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_q1_composite ON test_data
            (price, rating, is_new_customer, status, product_name, city, state, platform, device_type);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_q2_city_price ON test_data (city, price);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rating ON test_data (rating);
        """)
        console.print("[green]Indexes created.[/green]")


def drop_indexes():
    with mysql_cursor() as cursor:
        console.print("[bold yellow]Dropping existing indexes...[/bold yellow]")
        for idx in ["idx_q1_composite", "idx_q2_city_price", "idx_rating"]:
            try:
                cursor.execute(f"DROP INDEX {idx} ON test_data")
            except mysql.connector.Error as e:
                console.print(
                    f"[red]Warning:[/red] Couldn't drop index {idx} — {e.errno}\n{e.msg}"
                )


def optimize_schema():
    with mysql_cursor() as cursor:
        console.print("[bold]Altering table for InnoDB and cache columns...[/bold]")
        cursor.execute("""
            ALTER TABLE test_data ENGINE=InnoDB;
        """)
        try:
            cursor.execute("""
                ALTER TABLE test_data ADD COLUMN price_rating_cache FLOAT
                GENERATED ALWAYS AS (price * rating) STORED;
            """)
        except mysql.connector.Error as e:
            if e.errno == 1060:  # Duplicate column
                pass
        console.print("[green]Schema optimization done.[/green]")


def main():
    console.rule("[bold blue]Benchmarking Before Optimization")
    drop_indexes()
    run_benchmarks()

    console.rule("[bold blue]Optimizing Schema & Indexes")
    optimize_schema()
    setup_indexes()

    console.rule("[bold blue]Benchmarking After Optimization")
    run_benchmarks()


if __name__ == "__main__":
    main()
