from scraper import scrape_books
from cleaner import clean_books
from database import create_database, insert_data, show_database_summary
from queries import execute_queries


def main():

    print("=" * 60)
    print("ZEPTO DATA PIPELINE")
    print("=" * 60)

    # ---------------------------------
    # Step 1 : Scrape Books
    # ---------------------------------
    print("\nStep 1 : Scraping Books...")

    raw_df = scrape_books()

    print(f"\nTotal Books Scraped : {len(raw_df)}")

    # ---------------------------------
    # Step 2 : Clean Data
    # ---------------------------------
    print("\nStep 2 : Cleaning Data...")

    clean_df = clean_books(raw_df)

    print(f"Total Clean Books : {len(clean_df)}")

    # ---------------------------------
    # Step 3 : Create Database
    # ---------------------------------
    print("\nStep 3 : Creating SQLite Database...")

    conn, cursor = create_database()

    # ---------------------------------
    # Step 4 : Insert Data
    # ---------------------------------
    print("\nStep 4 : Inserting Records...")

    insert_data(clean_df, conn, cursor)

    show_database_summary(cursor)

    conn.close()

    # ---------------------------------
    # Step 5 : Execute SQL Queries
    # ---------------------------------
    print("\nStep 5 : Running SQL Queries...")

    execute_queries()

   


if __name__ == "__main__":
    main()