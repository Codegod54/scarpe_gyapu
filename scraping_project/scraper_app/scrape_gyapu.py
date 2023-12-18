from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .models import Product
import time
import re

def scrape_gyapu():
    base_url = 'https://www.gyapu.com/category/laptops1'
    total_pages = 5  # Set the total number of pages to scrape (adjust as needed)

    # Set the path to your Edge WebDriver executable
    edge_driver_path = 'D:/gyapu/edgedriver_win32/msedgedriver.exe'  # Replace with your actual path

    for page_number in range(1, total_pages + 1):
        url = f'{base_url}?page={page_number}'

        # Set Edge options for headless mode
        edge_options = Options()
        edge_options.add_argument("--headless")  # Enable headless mode
        edge_options.add_experimental_option("detach", True)

        # Initialize Edge WebDriver with options and service
        service = Service(edge_driver_path)
        driver = Edge(service=service, options=edge_options)
        driver.get(url)
        driver.implicitly_wait(35)  # Implicit wait for elements to load
        time.sleep(40)
        while True:
            # Get the page source after the JavaScript is rendered
            page_source = driver.page_source

            # Use BeautifulSoup to parse the page content
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find the product containers based on the specific HTML structure
            products = soup.find_all('div', class_='fscont')

            for product in products:
                name = product.find('div', class_='fsdet_title').text.strip()
                price_with_rs = product.find('div', class_='price').text.strip()

                # Remove 'Rs' and any non-numeric characters from the price string using regex
                price_numeric = re.sub(r'\D', '', price_with_rs)

                price = price_numeric
                image = product.find('div', class_='fslink').find('img')['src']

                # Check if the product already exists in the database
                existing_product = Product.objects.filter(name=name, price=price, image=image).exists()

                if not existing_product:
                    # Create a new Product object and save it to the database
                    new_product = Product(name=name, price=price, image=image)
                    new_product.save()

            # Find and click the "Next" button
            next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next')]")
            if next_button.is_enabled():
                next_button.click()
                time.sleep(5)  # Adjust this wait time if needed
            else:
                break  # Break out of the loop if the "Next" button is not found or
    driver.quit()

# Call the function to execute the scraping process
scrape_gyapu()