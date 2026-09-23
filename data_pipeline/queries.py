import sqlite3
import pandas as pd

DATABASE_NAME = "books_data.db"


def execute_queries():

    # -----------------------------
    # Display Settings
    # -----------------------------
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 60)

    conn = sqlite3.connect(DATABASE_NAME)

    output = []

    # =============================
    # QUERY 1
    # =============================
    query1 = """
    SELECT title, rating
    FROM books
    WHERE rating >= 3;
    """

    df1 = pd.read_sql(query1, conn)

    print("\n========== QUERY 1 ==========")
    print("Books with Rating >= 3\n")
    print(df1.head().to_string(index=False))

    output.append("\n========== QUERY 1 ==========\n")
    output.append(query1)
    output.append(df1.to_string(index=False))

    # =============================
    # QUERY 2
    # =============================
    query2 = """
    SELECT title, price_inr
    FROM books
    ORDER BY price_inr DESC
    LIMIT 8;
    """

    df2 = pd.read_sql(query2, conn)

    print("\n========== QUERY 2 ==========")
    print("Top 8 Most Expensive Books\n")
    print(df2.to_string(index=False))

    output.append("\n========== QUERY 2 ==========\n")
    output.append(query2)
    output.append(df2.to_string(index=False))

    # =============================
    # QUERY 3
    # =============================
    query3 = """
    SELECT DISTINCT category_name
    FROM categories;
    """

    df3 = pd.read_sql(query3, conn)

    print("\n========== QUERY 3 ==========")
    print("Distinct Categories\n")
    print(df3.to_string(index=False))

    output.append("\n========== QUERY 3 ==========\n")
    output.append(query3)
    output.append(df3.to_string(index=False))

    # =============================
    # QUERY 4
    # =============================
    query4 = """
    SELECT title, price_inr
    FROM books
    WHERE price_inr BETWEEN 3500 AND 5600;
    """

    df4 = pd.read_sql(query4, conn)

    print("\n========== QUERY 4 ==========")
    print("Books Between ₹3500 and ₹5600\n")
    print(df4.head().to_string(index=False))

    output.append("\n========== QUERY 4 ==========\n")
    output.append(query4)
    output.append(df4.to_string(index=False))

    # =============================
    # QUERY 5 (JOIN)
    # =============================
    query5 = """
    SELECT
        b.title,
        c.category_name,
        b.rating,
        b.price_inr
    FROM books b
    LEFT JOIN categories c
    ON b.category_id = c.category_id;
    """

    sql_join = pd.read_sql(query5, conn)

    print("\n========== QUERY 5 ==========")
    print("LEFT JOIN : Books with Categories\n")
    print(sql_join.head().to_string(index=False))

    output.append("\n========== QUERY 5 ==========\n")
    output.append(query5)
    output.append(sql_join.to_string(index=False))

    # =============================
    # pd.merge()
    # =============================
    print("\n========== pd.merge() ==========\n")

    books = pd.read_sql("SELECT * FROM books", conn)

    categories = pd.read_sql("SELECT * FROM categories", conn)

    merge_df = pd.merge(
        books,
        categories,
        on="category_id"
    )

    merge_df = merge_df[
        [
            "title",
            "category_name",
            "rating",
            "price_inr"
        ]
    ]

    print(merge_df.head().to_string(index=False))

    output.append("\n========== pd.merge() ==========\n")
    output.append(merge_df.to_string(index=False))

    # =============================
    # Compare Results
    # =============================
    if sql_join.equals(merge_df):

        print("\nSUCCESS : SQL JOIN and pd.merge() outputs are Matching.")

        output.append(
            "\nSUCCESS : SQL JOIN and pd.merge() outputs are Matching."
        )

    else:

        print("\nERROR : Outputs are MissMatch.")

        output.append(
            "\nERROR : Outputs are MissMatch."
        )

    # =============================
    # Save Results
    # =============================
    with open("sql_query_results.txt", "w", encoding="utf-8") as file:

        for item in output:
            file.write(item)
            file.write("\n\n")

    conn.close()

    print("\nQuery results saved to sql_query_results.txt")


if __name__ == "__main__":

    execute_queries()