import os
import csv
import asyncio
import random
import tempfile
from playwright.async_api import async_playwright
from web_scraping.config import (BASE_URL, OUTPUT_DIR, OUTPUT_FILE, MAX_RETRIES, RETRY_DELAY, START_PAGE, END_PAGE, BATCH_SIZE)

async def scrape_page_links(page, page_number):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await page.goto(
                f"{BASE_URL}/browse/new-apps/?p={page_number}",
                wait_until="domcontentloaded",
                timeout=30000)
            await page.wait_for_timeout(random.randint(4000, 6000))
            
            links = await page.locator("a.no-link-color").evaluate_all(
                "elements => elements.map(el => el.getAttribute('href'))")
            return list(dict.fromkeys([l for l in links if l and l.startswith("/software/")]))
        except Exception as e:
            print(f"Error getting links from page {page_number} (Attempt {attempt}): {e}")
            await asyncio.sleep(RETRY_DELAY)
    return []
#--------------------------------------------------------------------------------------------------------------------------------

async def scrape_app_details(page, url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await page.goto(f"{BASE_URL}{url}", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(random.randint(4000, 7000))
            
            overview = page.locator("header[data-testid='app-intro']")
            await overview.locator("h1").wait_for(state="visible", timeout=5000)
            
            title = (await overview.locator("h1").inner_text()).strip()
            description = (await overview.locator(".md").inner_text()).strip()
            
            specs_1 = await overview.locator(".grid-cols-2 span").all_inner_texts()
            cost = specs_1[0].strip() if len(specs_1) > 0 else "N/A"
            license = specs_1[1].strip().replace("\n", " ") if len(specs_1) > 1 else "N/A"
            
            app_type = ", ".join(await overview.locator("a[href*='?tag=']").all_inner_texts())
            origin = ", ".join(await overview.locator(".whitespace-nowrap span").all_inner_texts())
            platform = ", ".join(await overview.locator(".grow.col-span-2 span").all_inner_texts())
            supported_languages = ", ".join(await page.locator(".max-w-\\[400px\\] span").all_inner_texts())
            
            return {
                "title": title,
                "description": description,
                "cost": cost,
                "license": license,
                "app_type": app_type if app_type else "N/A",
                "origin": origin if origin else "N/A",
                "platform": platform if platform else "N/A",
                "supported_languages": supported_languages if supported_languages else "N/A"
            }
        except Exception as e:
            print(f"Error scraping app {url} (Attempt {attempt}): {e}")
            await asyncio.sleep(RETRY_DELAY)
    return None

#--------------------------------------------------------------------------------------------------------------------------------
def save_batch_to_csv(data, start, end):
    if not data:
        return
    batch_file = f"apps_batch_{start}-{end}.csv"
    final_path = os.path.join(OUTPUT_DIR, batch_file)
    headers_order = ["title", "description", "cost", "license", "app_type", "origin", "platform", "supported_languages"]
    keys = data[0].keys()
    with open(final_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers_order)
        writer.writeheader()
        writer.writerows(data)
    print(f"Batch {start}-{end} saved successfully to {final_path}")
#--------------------------------------------------------------------------------------------------------------------------------
async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Starting scraping from page {START_PAGE} to {END_PAGE} ")
    
    async with async_playwright() as p:
        tmp_dir = tempfile.mkdtemp()
        context = await p.chromium.launch_persistent_context(
            user_data_dir=tmp_dir,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        page = await context.new_page()
        for batch_start in range(START_PAGE, END_PAGE + 1, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE - 1, END_PAGE)
            print(f"starting batch ({batch_start} to {batch_end})")
            batch_data = []
            
            for page_num in range(batch_start, batch_end + 1):
                print(f"scraping Page {page_num}/{END_PAGE}")
                links = await scrape_page_links(page, page_num)
                print(f"Found {len(links)} apps on page {page_num}.")
                
                if not links:
                    print(f"Skipping page {page_num} due to no links found.")
                    continue
                for idx, link in enumerate(links, 1):
                    print(f"[Page {page_num}] App {idx}/{len(links)}: {link}")
                    app_info = await scrape_app_details(page, link)
                    
                    if app_info:
                        batch_data.append(app_info)
                
                if page_num < END_PAGE:
                    wait_time = random.randint(10, 20)
                    await asyncio.sleep(wait_time)
            
            if batch_data:
                save_batch_to_csv(batch_data, batch_start, batch_end)
            else:
                print(f"No data collected for batch {batch_start}-{batch_end}")

            if batch_end < END_PAGE:
                await asyncio.sleep(30)
                
        await context.close()
    print("\n All Batches scraping successfully!")

if __name__ == "__main__":
    asyncio.run(main())
