🚀 G2 Marketing Automation Scraper

Playwright-Based JavaScript-Aware Web Scraper (Python)

📌 Overview

This project is a JavaScript-rendered web scraper built using Playwright (Python) to extract product data from the G2 Marketing Automation category.

Since G2 loads content dynamically, traditional scraping tools like requests + BeautifulSoup fail.
This scraper connects to a real Chrome browser session using CDP (Chrome DevTools Protocol) to extract structured product data reliably. It helps us to protect from captcha also. 

if CAPTCHA appears:

The browser will show the CAPTCHA page.

The script will pause while waiting.

You manually solve the CAPTCHA in the browser window.

After solving it, the page loads normally.

The script continues extracting data.

🧠 Why This Works

Since you're connected to an already running Chrome session:

You can interact with it manually.

You can solve CAPTCHA like a human. And then press enter in terminal.

Once solved, the DOM updates.

Your locators start working again.

That’s actually one advantage of using CDP connection instead of headless automation.

🎯 What This Scraper Extracts

For each product:

✅ Product Name

✅ Review Count

✅ Rating

The data is saved into:

g2_products_full_data.csv

🧠 Why Playwright?

G2 is a JavaScript-heavy platform:

Products are dynamically rendered

Content loads after page initialization

DOM updates asynchronously

👉 Playwright controls a real Chromium browser, ensuring:

Full JS rendering

Accurate element selection

Better reliability

⚙️ Installation

1️⃣ Clone the Repository

git clone https://github.com/Parv-manglani/G2-Products-Scraping-Project.git

cd g2-marketing-automation-scraper

2️⃣ Create Virtual Environment

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies

pip install playwright

playwright install

🚀 Running the Scraper

Step 1: Start Chrome in Debug Mode

🪟 Windows

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug"

If Chrome is in PATH:

chrome --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug"
🍎 Mac

open -a "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"

Step 2: Run the Script

python main.py

python whole_data.py

🔍 How It Works

1️⃣ Connects to Existing Chrome Session

browser = p.chromium.connect_over_cdp("http://localhost:9222")

2️⃣ Pagination System

Automatically loops through pages:

while True:
    url = BASE_URL.format(page_number)

Stops when:

No products found

Page number exceeds 30 (safety break)

3️⃣ Smart Element Handling

Before extracting data:

if name_locator.count() == 0:
    continue

Prevents crashes due to missing elements.

4️⃣ Data Cleaning (Regex)

Removes commas and parentheses from review count:

re.sub(r"[(),]", "", review_text)

5️⃣ Deduplication

unique_products = {p["name"]: p for p in products}.values()

Ensures unique product entries.

Then run python whole_data.py

Then see the g2_products_complete_data.csv


📊 Output Format

Name	Review Count	Rating     Product Description       Review Summary

Example:

HubSpot Marketing Hub, 10543, 4.4

Marketo Engage, 2321, 4.2

🔥 Key Features

✔️ JavaScript-aware scraping

✔️ Chrome DevTools Protocol connection

✔️ Automatic pagination

✔️ Timeout handling

✔️ Duplicate removal

✔️ Clean CSV export

✔️ Safety stop to prevent infinite loops
