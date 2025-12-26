import json
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE_URL = "https://wise.com"
INDEX_URL = "https://wise.com/help/topics/5bVKT0uQdBrDp6T62keyfz/sending-money"

def extract_links():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(INDEX_URL, timeout=60000)

        # Wait for accordion header to appear
        page.wait_for_selector("h2", timeout=60000)

        # Find the "Where is my money?" section
        headers = page.query_selector_all("h2")

        target_header = None
        for h in headers:
            text = h.inner_text().lower()
            if "where is my money" in text:
                target_header = h
                break

        if not target_header:
            raise RuntimeError("Where is my money section not found")

        # Navigate DOM: h2 → button → next ul
        button = target_header.evaluate_handle(
            "el => el.closest('button')"
        )
        ul = button.evaluate_handle(
            "el => el.nextElementSibling"
        )

        links = ul.query_selector_all("a")

        results = []
        for a in links:
            results.append({
                "title": a.inner_text().strip(),
                "url": urljoin(BASE_URL, a.get_attribute("href"))
            })

        browser.close()

    with open("data/raw/where_is_my_money_links.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Extracted {len(results)} links")

if __name__ == "__main__":
    extract_links()
