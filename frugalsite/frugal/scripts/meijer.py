from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)
options.add_argument("--window-size=1920,1080")

def search_on_meijer(product: str) -> list:
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get(f"https://www.meijer.com/shopping/search.html?text={product}")
    time.sleep(3)

    results = list()

    while True:
        try:
            time.sleep(4)
            products = driver.find_elements(
                By.XPATH,
                value='//div[@class="product-tile"]/a/div/div/div[@class="product-tile__title"]',
            )
            image_urls = driver.find_elements(
                By.XPATH, value='//div[@class="product-tile"]/a/div/div/div/img'
            )
            prices = driver.find_elements(
                By.XPATH,
                value='//div[@class="product-tile"]/a/div/div[@class="product-tile__price"]',
            )
            ids = driver.find_elements(By.CLASS_NAME, "product-tile")

            for i in range(len(products)):
                if "Sponsored" in ids[i].text:
                    continue

                product = dict()
                product["store"] = "meijer"
                product["name"] = products[i].text
                id = ids[i].get_attribute("data-cnstrc-item-id")
                product["store_id"] = int(id)
                product["image_url"] = image_urls[i].get_attribute("src")

                p = prices[i].text.split("\n")

                for j in range(len(p)):
                    if len(p) == 2:
                        price = re.search("\$\d+\.\d+", p[1]).group()
                        product["price"] = format(
                            float(price.replace("$", "").strip()), ".2f"
                        )
                    elif len(p) == 4:
                        price = re.search("\$\d+\.\d+", p[2]).group()
                        product["price"] = format(
                            float(price.replace("$", "").strip()), ".2f"
                        )

                        sale_price = re.search("\$\d+\.\d+", p[0]).group()
                        product["sale_price"] = format(
                            float(sale_price.replace("$", "").strip()), ".2f"
                        )

                results.append(product)
            break

        except StaleElementReferenceException:
            continue

        except NoSuchElementException:
            continue

    driver.quit()

    return results

