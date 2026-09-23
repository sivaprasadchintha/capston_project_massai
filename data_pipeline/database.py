import sqlite3
from scraper import scrape_books
from cleaner import clean_books

DATABASE_NAME = "books_data.db"


def create_database():
    """
    Creates the SQLite database and required tables.
    """

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # -----------------------------
    # Categories Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    )
    """)

    # -----------------------------
    # Books Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price_gbp REAL NOT NULL,
        price_inr REAL NOT NULL,
        rating INTEGER NOT NULL,
        in_stock INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY(category_id)
            REFERENCES categories(category_id)
    )
    """)

    conn.commit()

    return conn, cursor


def insert_data(clean_df, conn, cursor):
    """
    Insert cleaned data into SQLite database.
    """

    # Remove old data if script is rerun
    cursor.execute("DELETE FROM books")
    cursor.execute("DELETE FROM categories")

    conn.commit()

    category_map = {}

    # -----------------------------
    # Insert Categories
    # -----------------------------
    categories = sorted(clean_df["category"].unique())

    for category in categories:

        cursor.execute("""
        INSERT INTO categories(category_name)
        VALUES(?)
        """, (category,))

        category_id = cursor.lastrowid

        category_map[category] = category_id

    # -----------------------------
    # Insert Books
    # -----------------------------
    for _, row in clean_df.iterrows():

        cursor.execute("""
        INSERT INTO books(
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            int(row["in_stock"]),
            category_map[row["category"]]
        ))

    conn.commit()


def show_database_summary(cursor):
    """
    Display database statistics.
    """

    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]

    print("\nDatabase Created Successfully")
    print("-" * 35)

    print(f"Categories Inserted : {category_count}")
    print(f"Books Inserted      : {book_count}")


if __name__ == "__main__":

    print("\nScraping Books...")

    raw_df = scrape_books()

    print("\nCleaning Data...")

    clean_df = clean_books(raw_df)

    print("\nCreating Database...")

    conn, cursor = create_database()

    print("Inserting Records...")

    insert_data(clean_df, conn, cursor)

    show_database_summary(cursor)

    conn.close()

    print("\nDatabase saved as books_data.db")