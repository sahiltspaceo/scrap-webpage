from bs4 import BeautifulSoup
import requests

def check_scrape(url):
    source = requests.get(url).text
