# ingestion/scrape_articles.py

import json
from playwright.sync_api import sync_playwright

def scrape_articles():
    with open("data/raw/where_is_my_money_links.json") as f:
        links = json.load(f)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for item in links:
            print(f"Scraping: {item['title']}")
            page.goto(item["url"], timeout=60000)

            # Wait for main content to render
            page.wait_for_selector("main", timeout=60000)

            # Try multiple safe containers
            content = None
            for selector in ["article", "main", '[role="main"]']:
                el = page.query_selector(selector)
                if el:
                    content = el.inner_text()
                    break

            if not content or len(content.strip()) < 100:
                print(f"⚠️ Empty content for {item['title']}")
                continue

            results.append({
                "question": item["title"],
                "answer": content.replace(f"Help home\nSending money\n{item['title']}",''),
                "source": item["url"]
            })

        browser.close()

    with open("data/processed/wise_articles.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Scraped {len(results)} articles")

if __name__ == "__main__":
    scrape_articles()
