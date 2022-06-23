from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from os import path

class TranscriptScraper:
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # pass in a dictionary of name to url
    # returns all the file paths generated
    def scrape_films(self, outputFolder, films):
        paths = []
        for (name, url) in films:
            paths.append(self.scrape(outputFolder, name, url))
        return paths
    
    # scrapes a url and saves it as a txt file
    # if scrapeExisting is false, it won't scrape any existing, matching names in the folder
    # to reduce the number of requests
    def scrape(self, outputFolder, name, url, scrapeExisting=False):
        filePath = f"{outputFolder}/{name}.txt"
        if not scrapeExisting and path.exists(filePath):
            return filePath

        try:
            # Get the website
            self.driver.get(url)
            # drills and waits for script, written in innerHTML and <b> tags
            script_html = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'pre')))
        finally:
            # save script to txt file for future parsing
            with open(filePath, "w", encoding="utf-8") as f:
                f.write(script_html.get_attribute('innerHTML'))
                return filePath
    
    def finish(self):
        self.driver.close()