from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def fetch_laptops_selenium(pages=2):
    laptops = []
    driver = get_driver()

    for page in range(1, pages + 1):
        url = f"https://www.newegg.com/p/pl?d=laptop&page={page}"
        print(f"Scraping: {url}")
        driver.get(url)
        time.sleep(3)  # Let JS load

        items = driver.find_elements(By.CLASS_NAME, "item-cell")
        for item in items:
            try:
                name = item.find_element(By.CLASS_NAME, "item-title").text
                price = item.find_element(By.CLASS_NAME, "price-current").text.split()[0].replace('$', '').replace(',', '')
                specs = item.find_elements(By.CLASS_NAME, "item-features")

                # Basic defaults
                cpu, ram, storage, gpu = '', '', '', ''

                for spec_group in specs:
                    for li in spec_group.find_elements(By.TAG_NAME, "li"):
                        text = li.text.lower()
                        if 'intel' in text or 'amd' in text:
                            cpu = li.text
                        elif 'ram' in text:
                            ram = li.text
                        elif 'ssd' in text or 'hdd' in text:
                            storage = li.text
                        elif 'graphics' in text or 'gpu' in text:
                            gpu = li.text

                laptops.append({
                    "name": name,
                    "price_usd": price,
                    "CPU": cpu,
                    "RAM": ram,
                    "Storage": storage,
                    "GPU": gpu
                })
            except Exception:
                continue

    driver.quit()
    return laptops

def collect_and_save():
    laptops = fetch_laptops_selenium(pages=2)
    df = pd.DataFrame(laptops)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/laptops.csv", index=False)
    print(f"Saved {len(df)} laptops to data/laptops.csv")

if __name__ == "__main__":
    collect_and_save()
