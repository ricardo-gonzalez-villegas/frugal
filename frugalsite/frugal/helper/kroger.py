from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import threading
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


def search_on_kroger(product: str) -> list:
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get(
        f"https://www.kroger.com/search?query={product}&searchType=default_search"
    )
    time.sleep(3)

    results = list()

    while True:
        try:
            products = driver.find_elements(
                By.XPATH, value='//span[@data-qa="cart-page-item-description"]'
            )
            product_sizes = driver.find_elements(
                By.XPATH, value='//span[@data-qa="cart-page-item-sizing"]'
            )
            prices = driver.find_elements(By.CLASS_NAME, value="mb-8")
            image_urls = driver.find_elements(
                By.XPATH, '//img[@data-qa="cart-page-item-image-loaded"]'
            )
            for i in range(len(products)):
                product = dict()
                id = (
                    image_urls[i]
                    .get_attribute("src")
                    .replace("https://www.kroger.com/product/images/medium/front/", "")
                    .strip()
                )

                product["store"] = "kroger"
                product["store_id"] = id
                product["image_url"] = image_urls[i].get_attribute("src")
                product["name"] = f"{products[i].text} {product_sizes[i].text}"

                results.append(product)

            price_list = list()

            for price in prices:
                if len(price.text) == 0:
                    continue
                if price.text == "Sign In to Add":
                    continue
                if price.text == "Low Stock":
                    continue
                else:
                    price = price.text.replace("\n", "")
                    if "discounted from" in price:
                        temp_price_list = price.split("discounted from")

                        sale_price = re.search("\$\d+\.\d+", temp_price_list[0]).group()
                        sale_price = format(float(sale_price.replace("$", "")), ".2f")
                        regular_price = re.search(
                            "\$\d+\.\d+", temp_price_list[1]
                        ).group()
                        regular_price = format(
                            float(regular_price.replace("$", "")), ".2f"
                        )

                        price_list.append(
                            {"price": regular_price, "sale_price": sale_price}
                        )
                    elif "about" in price:
                        regular_price = re.search("\$\d+\.\d+", price).group()
                        regular_price = format(
                            float(regular_price.replace("$", "")), ".2f"
                        )

                        price_list.append({"price": regular_price})
                    elif "Prices May Vary" in price:
                        regular_price = "Prices May Very"
                        price_list.append({"price": regular_price})
                    else:
                        regular_price = format(float(price.replace("$", "")), ".2f")
                        price_list.append({"price": regular_price})

            for j in range(len(results)):
                results[j].update(price_list[j])
            break

        except StaleElementReferenceException:
            continue

        except NoSuchElementException:
            continue

    driver.quit()

    return results


def kroger_product_id_lookup(product_id: str):
    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.get(
        f"https://www.kroger.com/search?query={product_id}&searchType=default_search"
    )
    time.sleep(3)

    prices = driver.find_elements(By.CLASS_NAME, "kds-Price")

    product_prices = dict()

    while True:
        try:
            for price in prices:
                if len(price.text) == 0:
                    continue
                if price.text == "Sign In to Add":
                    continue
                if price.text == "Low Stock":
                    continue
                else:
                    price = price.text.replace("\n", "")
                    if "discounted from" in price:
                        temp_price_list = price.split("discounted from")

                        sale_price = re.search("\$\d+\.\d+", temp_price_list[0]).group()
                        sale_price = format(float(sale_price.replace("$", "")), ".2f")
                        regular_price = re.search(
                            "\$\d+\.\d+", temp_price_list[1]
                        ).group()
                        regular_price = format(
                            float(regular_price.replace("$", "")), ".2f"
                        )

                        product_prices["price"] = regular_price
                        product_prices["sale_price"] = sale_price

                    elif "about" in price:
                        regular_price = re.search("\$\d+\.\d+", price).group()
                        regular_price = format(
                            float(regular_price.replace("$", "")), ".2f"
                        )

                        product_prices["price"] = regular_price
                    elif "Prices May Vary" in price:
                        regular_price = "Prices May Very"
                        product_prices["price"] = regular_price
                    else:
                        regular_price = format(float(price.replace("$", "")), ".2f")
                        product_prices["price"] = regular_price

            break

        except StaleElementReferenceException:
            continue

        except NoSuchElementException:
            continue

    driver.quit()

    return product_prices
