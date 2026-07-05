import random
from web_scraping.config import BASE_URL
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    page = context.new_page()

    test_page_num = 5
    page.goto(f"{BASE_URL}/browse/new-apps/?p={test_page_num}")
    page.wait_for_timeout(5000)

    links = page.locator("a.no-link-color").evaluate_all(
        "elements => elements.map(el => el.getAttribute('href'))")
    valid_links = list(
        dict.fromkeys([link for link in links if link and link.startswith("/software/")]))

    page.wait_for_timeout(random.randint(2000, 4000))
    page.goto(f"{BASE_URL}{valid_links[4]}")
    page.wait_for_timeout(5000)

    overview = page.locator("header[data-testid='app-intro']")
    title = overview.locator("h1").inner_text().strip()

    description = overview.locator(".md").inner_text().strip()

    specs_1 = overview.locator(".grid-cols-2 span").all_inner_texts()
    cost = specs_1[0].strip() if len(specs_1) > 0 else "N/A"
    license = specs_1[1].strip().replace("\n", " ") if len(specs_1) > 1 else "N/A"

    app_type = ", ".join(overview.locator("a[href*='?tag=']").all_inner_texts())

    origin = ", ".join(overview.locator(".whitespace-nowrap span").all_inner_texts())
    platform = ", ".join(overview.locator(".grow.col-span-2 span").all_inner_texts())
    supported_languages = ", ".join(page.locator(".max-w-\\[400px\\] span").all_inner_texts())

    print({
        "title": title,
        "Description": description,
        "Cost": cost,
        "License": license,
        "App_Type": app_type,
        "Origin": origin,
        "Platform": platform,
        "Supported_Languages": supported_languages})

    context.close()
    browser.close()
