
from playwright.sync_api import sync_playwright
import csv
import time
import re

BASE_URL = "https://www.g2.com/categories/marketing-automation?order=g2_score&page={}&page_size=15#product-list"


def extract_products(page):
    product_cards = page.locator("div.product-card__title.mb-1")
    count = product_cards.count()

    print("Total product cards found:", count)

    products = []

    for i in range(count):
        card = product_cards.nth(i)

        # Check if name exists first
        name_locator = card.locator("div[itemprop='name']")
        if name_locator.count() == 0:
            print(f"Skipping card {i} (no product name found)")
            continue

        try:
            name = name_locator.first.inner_text(timeout=3000).strip()

            # Review Count
            review_locator = card.locator("a.link span.pl-4th")
            review_count = ""
            if review_locator.count() > 0:
                review_text = review_locator.first.inner_text(timeout=3000).strip()
                review_count = re.sub(r"[(),]", "", review_text)

            # Rating
            rating_locator = card.locator("span.c-midnight-90 span.fw-semibold")
            rating = ""
            if rating_locator.count() > 0:
                rating = rating_locator.first.inner_text(timeout=3000).strip()

            products.append({
                "name": name,
                "review_count": review_count,
                "rating": rating
            })

        except Exception as e:
            print(f"Skipping problematic card {i}: {e}")
            continue

    return products

def save_to_csv(products):
    # Remove duplicates based on name
    unique_products = {p["name"]: p for p in products}.values()

    with open("g2_products_full_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Review Count", "Rating"])

        for p in unique_products:
            writer.writerow([p["name"], p["review_count"], p["rating"]])

    print("Saved", len(unique_products), "unique products to g2_products_full_data.csv")


def main():
    with sync_playwright() as p:
        print("Connecting to existing Chrome...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        if not browser.contexts:
            print("No browser context found.")
            return

        context = browser.contexts[0]

        if context.pages:
            page = context.pages[0]
        else:
            page = context.new_page()

        all_products = []
        page_number = 1

        while True:
            url = BASE_URL.format(page_number)
            print(f"\nOpening Page {page_number}: {url}")

            page.goto(url, timeout=300000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(3)

            print("Page title:", page.title())

            products = extract_products(page)

            if not products:
                print("No products found. Stopping pagination.")
                break

            print(f"Page {page_number} -> {len(products)} products found")

            all_products.extend(products)

            page_number += 1

            if page_number > 30:  # Safety stop
                print("Safety break triggered.")
                break

        save_to_csv(all_products)


if __name__ == "__main__":
    main()