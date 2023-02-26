from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


def test_shopping(brows):
    product = "Samsung Galaxy S23"
    url_amazon = "https://www.amazon.co.uk/ref=nav_logo"
    url_bestbuy = "https://www.bestbuy.com/"
    brows.get(url_amazon)

    search_box = brows.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')
    search_box.send_keys(product)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    amazon_price = 100000000000000
    bestbuy_price = 10000000000000

    while True:
        time.sleep(2)
        item_card = brows.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for i in item_card:

            product_name = i.find_element(By.XPATH,
                                          '//span[@class="a-size-medium a-color-base a-text-normal"]').text.lower()
            correct = True
            for item in product.split():
                if item.lower() not in product_name:
                    correct = False
                    break

            if 'case' in product_name:
                correct = False

            if correct:
                review_amazon = i.find_element(By.XPATH, '//span[@class="a-size-base s-underline-text"]')
                review_cleared_amazon = int(''.join(filter(str.isdigit, review_amazon.text)))

                if review_cleared_amazon > 200:
                    price_amazon = i.find_element(By.XPATH, '//span[@class="a-price-whole"]')
                    price_cleared_amazon = float(''.join(filter(str.isdigit, price_amazon.text)))

                    if price_cleared_amazon < amazon_price:
                        amazon_price = price_cleared_amazon

        try:
            next_page_link = brows.find_element(By.CSS_SELECTOR, ".s-pagination-container .s-pagination-next")
            next_page_url = next_page_link.get_attribute("href")
            if next_page_url is None:
                break
            else:
                brows.get(next_page_url)
        except:
            break

    print(amazon_price)
    brows.get(url_bestbuy)
    time.sleep(2)
    choose_country_bott = brows.find_element(By.XPATH, '//div[@class="country-selection"]//*[@class="us-link"]')
    choose_country_bott.click()
    search_box = brows.find_element(By.XPATH, '//input[@class="search-input"]')
    search_box.send_keys(product)
    search_box.send_keys(Keys.RETURN)
    while True:
        time.sleep(2)
        item_card_bestbuy = brows.find_elements(By.XPATH, '//li[@class="sku-item"]')
        for z in item_card_bestbuy:
            product_name = z.find_element(By.XPATH, '//h4[@class="sku-title"]//a').text.lower()

            correct = True
            for item in product.split():
                if item.lower() not in product_name:
                    correct = False
                    break

            if 'case' in product_name:
                correct = False

            if correct:
                review_bestbuy = z.find_element(By.XPATH,
                                                '//li[@class="sku-item"]//*[contains(@class,"c-reviews ")]').text
                try:
                    review_cleared_bestbuy = int(''.join(filter(str.isdigit, review_bestbuy)))
                except ValueError:
                    continue

                if review_cleared_bestbuy > 10:
                    price_bestbuy = z.find_element(By.XPATH,'//li[@class="sku-item"]//*[contains(@class,"priceView-customer-price")]//span[@aria-hidden="true"]')
                    price_cleared_bestbuy = float(price_bestbuy.text.replace('$', '').replace(',', ''))
                    if price_cleared_bestbuy > 100:
                        if price_cleared_bestbuy < bestbuy_price:
                            bestbuy_price = price_cleared_bestbuy
        try:
            next_page_link = brows.find_element(By.XPATH, '//a[@class="sku-list-page-next"]')
            next_page_url = next_page_link.get_attribute("href")
            if next_page_url is None:
                break
            else:
                brows.get(next_page_url)
        except:
            break

    brows.close()
    print(bestbuy_price)
    pass
    assert amazon_price > bestbuy_price
