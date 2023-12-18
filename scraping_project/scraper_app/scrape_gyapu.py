from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from .models import Product
import time
import re

def scrape_gyapu():
    base_url = 'https://www.gyapu.com/category/laptops1'
    page_number = 1  # Start from the first page
    total_pages = 2  # Set the total number of pages to scrape (adjust as needed)

    while page_number <= total_pages:
        url = f'{base_url}?page={page_number}'

        # Set Edge options for headless mode
        edge_options = Options('--headless')
        edge_options.add_experimental_option("detach", True)

        # Set the path to your Edge WebDriver executable
        edge_driver_path = 'D:\gyapu\edgedriver_win32\msedgedriver.exe'  # Replace with your actual path
        service = Service(edge_driver_path)

        # Initialize Edge WebDriver with options and service
        driver = Edge(service=service, options=edge_options)
        driver.get(url)
        driver.implicitly_wait(40)  # Implicit wait for elements to load

        # Wait for the products to load using a more dynamic approach
        time.sleep(50)  # Adjust this wait time if needed

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

        driver.quit()
        page_number += 1  # Move to the next page

# Call the function to execute the scraping process
scrape_gyapu()
