
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from api.scrape.extract import extract_content


# Set up Selenium with Chrome in headless mode
options = Options()
options.add_argument('--headless=new')
options.add_argument("--window-size=1920,1080")  # Set window size for full-page screenshot


def get_website_content_and_screenshot(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Load the webpage
        driver.get(url)
        # Save a screenshot
        screenshot = driver.get_screenshot_as_png()

        html_content = driver.page_source

        # Extract and structure the main content
        main_content = extract_content(html_content)

    finally:
        driver.quit()

    return main_content, screenshot
