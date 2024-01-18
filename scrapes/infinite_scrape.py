
#this file will be posting to an endpoint, endlessly running and updating that endpoint with our bets
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from fastapi import FastAPI
import threading
from threading import Thread
from sites_scrape import arbitrage
from sites_scrape import running_arbs
import time
import concurrent.futures
from pointsbet_scrape import pointsbet
from betmgm_scrape import betmgm
from betrivers_scrape import betrivers
#from bet99_scrape import bet99
from draftkings_endpoint import draftkings
from triple8_scrape import triple8
from tonybet_scrape import tonybet
from northstar_scrape import northstar
from betano_scrape import betano
import logging

#logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

iteration=0
bigx=[]


@app.get("/")
def test():
    global bigx
    return(bigx)

def update_x():
    global bigx
    global iteration


    #define driver, pass to running_arbs
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

    # Create a ChromeOptions object
    chrome_options = Options()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument('--window-size=1920,1080')  
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    chrome_options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )
    
    while True:
        print(f'Iteration {iteration}')
        
        bigx = running_arbs(chrome_options) #nhl odds
     
        iteration+=1
        time.sleep(10)

thread = threading.Thread(target=update_x)
thread.start()


#run uvicorn infinite_scrape:app --reload to get backend url

#asgi error -> cd into odds_scraping




