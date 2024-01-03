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
options.add_argument("--window-size=1920,2100")


def search_on_walmart(product: str) -> list:
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get(f"https://www.walmart.com/search?q={product}")
    time.sleep(4)

    results = list()

    while True:
        try:
            products = driver.find_elements(
                By.XPATH,
                '//section/div/div/div/div/div[@data-testid="list-view"]/div/span/span[@data-automation-id="product-title"]',
            )
            prices = driver.find_elements(
                By.XPATH,
                '//section/div/div/div/div/div[@data-testid="list-view"]/div/div[@data-automation-id="product-price"]',
            )
            image_urls = driver.find_elements(
                By.XPATH,
                '//section/div/div/div/div/div[@data-testid="list-view"]/div/div/div/img[@data-testid="productTileImage"]',
            )
            links = driver.find_elements(By.XPATH, "//section/div/div/div/div/a")
            data = driver.find_elements(
                By.XPATH, '//section/div/div/div/div/div[@data-testid="list-view"]'
            )

            priced_products = list()
            priced_image_urls = list()
            priced_data = list()
            priced_links = list()

            # remove any indexes where no price is listed
            for i in range(len(data)):
                if not "$" in data[i].text:
                    continue
                else:
                    priced_products.append(products[i])
                    priced_image_urls.append(image_urls[i])
                    priced_links.append(links[i].get_attribute("href"))
                    priced_data.append(data[i])

            for i in range(len(priced_data)):
                if "Sponsored" in priced_data[i].text:
                    continue

                product = dict()

                product["store"] = "walmart"
                product["name"] = priced_products[i].text
                product["image_url"] = priced_image_urls[i].get_attribute("src")
                id = re.findall(r"/(?=(\d+))\d+\?", priced_links[i])
                product["store_id"] = id[0]

                temp_price_list = prices[i].text.split("\n")

                for price in temp_price_list:
                    if "current price" in price:
                        current_price = re.search("\$\d+\.\d+", price).group()
                        current_price = float(current_price.replace("$", "").strip())
                        product["price"] = format(current_price, ".2f")

                    elif "Was" in price:
                        product["sale_price"] = product["price"]
                        previous_price = re.search("\$\d+\.\d+", price).group()
                        previous_price = float(previous_price.replace("$", "").strip())
                        product["price"] = format(previous_price, ".2f")

                results.append(product)
            break

        except StaleElementReferenceException:
            continue

        except NoSuchElementException:
            continue

    driver.quit()

    return results


def walmart_product_id_lookup(product_id: str):
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get(f"https://www.walmart.com/search?q={product_id}")
    time.sleep(3)

    prices_div = driver.find_element(
        By.XPATH, '//div[@data-automation-id="product-price"]'
    )

    product_prices = dict()

    while True:
        try:
            prices = prices_div.text.split("\n")

            for price in prices:
                if "current price" in price:
                    current_price = re.search("\$\d+\.\d+", price).group()
                    current_price = float(current_price.replace("$", "").strip())
                    product_prices["price"] = format(current_price, ".2f")

                elif "Was" in price:
                    product_prices["sale_price"] = product_prices["price"]
                    previous_price = re.search("\$\d+\.\d+", price).group()
                    previous_price = float(previous_price.replace("$", "").strip())
                    product_prices["price"] = format(previous_price, ".2f")

            break

        except StaleElementReferenceException:
            continue

        except NoSuchElementException:
            continue

    driver.quit()

    return product_prices
