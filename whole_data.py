from playwright.sync_api import sync_playwright
import csv
import time
import re

INPUT_CSV = "g2_products_full_data.csv"
OUTPUT_CSV = "g2_products_complete_data.csv"

BASE_URL = "https://www.g2.com/products/{}/reviews"


# Convert product name into G2 slug format
def create_slug(name):
    slug = name.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)  # remove special chars
    slug = re.sub(r"\s+", "-", slug)      # replace spaces with dash
    return slug


def scrape_product_details(page, slug):
    url = BASE_URL.format(slug)
    print(f"\nOpening: {url}")

    try:
        page.goto(url, timeout=500000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        # Product Description
        description = ""
        desc_locator = page.locator("p[itemprop='description']")
        if desc_locator.count() > 0:
            description = desc_locator.first.inner_text(timeout=5000).strip()

        # Review Summary
        review_summary = ""
        summary_locator = page.locator("div.elv-text-base.elv-leading-base.elv-mt-6")
        if summary_locator.count() > 0:
            review_summary = summary_locator.first.inner_text(timeout=5000).strip()

        return description, review_summary

    except Exception as e:
        print(f"Error scraping {slug}: {e}")
        return "", ""


def main():
    # Read existing CSV
    products = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)

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

        enriched_products = []

        for product in products:
            name = product["Name"]
            review_count = product["Review Count"]
            rating = product["Rating"]

            slug = create_slug(name)

            description, review_summary = scrape_product_details(page, slug)

            enriched_products.append({
                "name": name,
                "review_count": review_count,
                "rating": rating,
                "product_description": description,
                "review_summary": review_summary
            })

            time.sleep(1)  # small delay to avoid blocking

    # Save new CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name",
            "Review Count",
            "Rating",
            "Product Description",
            "Review Summary"
        ])

        for p in enriched_products:
            writer.writerow([
                p["name"],
                p["review_count"],
                p["rating"],
                p["product_description"],
                p["review_summary"]
            ])

    print("\nSaved enriched data to", OUTPUT_CSV)


if __name__ == "__main__":
    main()