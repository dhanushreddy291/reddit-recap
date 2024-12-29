import os

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.remote.remote_connection import ClientConfig

BRIGHTDATA_USERNAME = os.getenv("BRIGHTDATA_USERNAME")
BRIGHTDATA_PASSWORD = os.getenv("BRIGHTDATA_PASSWORD")
BRIGHTDATA_REMOTE_SERVER_ADDR = os.getenv("BRIGHTDATA_REMOTE_SERVER_ADDR")

config = ClientConfig(
    username=BRIGHTDATA_USERNAME,
    password=BRIGHTDATA_PASSWORD,
    remote_server_addr=BRIGHTDATA_REMOTE_SERVER_ADDR,
)


def scrape_url(url):
    print("Connecting to Scraping Browser...")

    options = ChromeOptions()
    options.page_load_strategy = "normal"
    options.set_capability("timeouts", {"pageLoad": 60000, "script": 60000})

    sbr_connection = ChromiumRemoteConnection(
        None, "goog", "chrome", client_config=config
    )
    with Remote(sbr_connection, options=options) as driver:
        try:
            print("Connected! Navigating...")
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(60)

            driver.get(url)

            print("Navigated! Scraping page content...")
            html = driver.page_source

            soup = BeautifulSoup(html, "html.parser")

            # Extract Main Content
            main_content = soup.find("main")  # Look for <main> tag
            if not main_content:  # Fallback to <article> tag
                main_content = soup.find("article")
            if not main_content:  # Last fallback - generic container with class
                main_content = soup.find("div", {"class": "content"})

            if main_content:
                for img in main_content.find_all("img"):
                    img.decompose()

            if main_content:
                content_markdown = md(str(main_content))
            else:
                return None

            return content_markdown

        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    url = "https://www.bbc.com/news/articles/ckgzprprlyeo"
    content = scrape_url(url)
    print(content)
