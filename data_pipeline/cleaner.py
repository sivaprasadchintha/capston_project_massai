import pandas as pd

GBP_TO_INR = 105.50

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def clean_books(df):
    """
    Cleans the scraped book data according to the project requirements.
    """

    cleaned_df = df.copy()

    # -----------------------------
    # Clean Price (GBP)
    # -----------------------------
    cleaned_df["price_gbp"] = pd.to_numeric(
        cleaned_df["price"].str.replace("£", "", regex=False),
        errors="coerce"
    )

    # -----------------------------
    # Convert Star Rating
    # -----------------------------
    cleaned_df["rating"] = cleaned_df["star_rating"].map(RATING_MAP)

    # -----------------------------
    # Convert Availability
    # -----------------------------
    cleaned_df["in_stock"] = cleaned_df["availability"].str.contains(
        "In stock",
        case=False,
        na=False
    )

    # -----------------------------
    # Handle Parsing Errors
    # -----------------------------
    cleaned_df["price_gbp"] = cleaned_df["price_gbp"].fillna(
        cleaned_df["price_gbp"].median()
    )

    cleaned_df["rating"] = cleaned_df["rating"].fillna(
        cleaned_df["rating"].median()
    ).astype(int)

    # -----------------------------
    # Convert GBP to INR
    # -----------------------------
    cleaned_df["price_inr"] = (
        cleaned_df["price_gbp"] * GBP_TO_INR
    ).round(2)

    # -----------------------------
    # Keep Required Columns
    # -----------------------------
    cleaned_df = cleaned_df[
        [
            "title",
            "category",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock"
        ]
    ]

    return cleaned_df


if __name__ == "__main__":

    from scraper import scrape_books

    raw_df = scrape_books()

    clean_df = clean_books(raw_df)

    # -----------------------------
    # Display Settings
    # -----------------------------
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 60)

    print("\nCleaned Data\n")

    print(clean_df.head().to_string(index=False))

    print("\n---------------------------")

    print("Data Types:\n")

    print(clean_df.dtypes)

    print("\n---------------------------")

    print(f"Total Cleaned Books : {len(clean_df)}")