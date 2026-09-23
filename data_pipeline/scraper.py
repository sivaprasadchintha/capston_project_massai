import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

# Create a reusable session
session = requests.Session()
session.headers.update(HEADERS)


def get_category_links():
    """
    Fetch all category names and their URLs.
    """

    response = session.get(BASE_URL, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    category_links = {}

    categories = soup.select(".side_categories ul li ul li a")

    for category in categories:
        name = category.get_text(strip=True)
        url = urljoin(BASE_URL, category["href"])
        category_links[name] = url

    return category_links


def get_book_links(category_url):
    """
    Fetch all book URLs from a category.
    Handles pagination automatically.
    """

    book_links = []

    while True:

        response = session.get(category_url, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.select("article.product_pod h3 a")

        for book in books:

            href = book["href"].replace("../../../", "")

            book_url = urljoin(BASE_URL + "catalogue/", href)

            book_links.append(book_url)

        next_page = soup.select_one("li.next a")

        if next_page:
            category_url = urljoin(category_url, next_page["href"])
        else:
            break

    return book_links


def scrape_book(book_url, category):
    """
    Scrape details from a single book page.
    """

    response = session.get(book_url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text(strip=True)

    price = soup.select_one(".price_color").get_text(strip=True)

    rating = soup.select_one("p.star-rating")["class"][1]

    availability = soup.select_one(".availability").get_text(strip=True)

    return {
        "title": title,
        "price": price,
        "star_rating": rating,
        "availability": availability,
        "category": category
    }


def scrape_books():
    """
    Scrape books from multiple categories.
    """

    categories = get_category_links()

    selected_categories = [
        "Religion",
        "Music",
        "Sports and Games",
        "Art",
        "History",
        "Thriller",
        "Business"
    ]

    all_books = []

    for category in selected_categories:

        print(f"\nScraping {category}...")

        category_url = categories[category]

        book_links = get_book_links(category_url)

        print(f"Found {len(book_links)} books.")
        print("-" * 40)

        for book_url in book_links:

            try:

                book = scrape_book(book_url, category)

                all_books.append(book)

            except requests.exceptions.RequestException as e:

                print(f"Request Failed: {book_url}")
                print(e)
                continue

            except Exception as e:

                print(f"Unexpected Error: {book_url}")
                print(e)
                continue

    df = pd.DataFrame(all_books)

    return df


if __name__ == "__main__":

    books_df = scrape_books()

    print("\nFirst 5 Books:\n")

    print(books_df.head())

    print("\n----------------------------")

    print(f"Total Books Scraped : {len(books_df)}")