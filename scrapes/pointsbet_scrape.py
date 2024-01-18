from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from csv_test import team_fixer
from fastapi import FastAPI
import threading
from threading import Thread
import logging

#logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

def pb_pp(url, sport):
    ...

#this will get you the info you need for pointsbet, pass to it the url of the sport of concern
def pointsbet(sport_site, sport, chrome_options):

    start = time.time()
    print(f'pointsbet {sport}')
    website = sport_site
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'
    # path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

    # # Create a ChromeOptions object
    # chrome_options = Options()

    # # Set any options you need, for example, headless mode
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument('--window-size=1920,1080')  
    # chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')


    service = ChromeService(path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    #opens the window
    driver.get(website)

    
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//div[@class='fohvkg f4ru8xs']")))
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//div[@class='fohvkg f4ru8xs']")))


    while True:
        time.sleep(2)
        position = driver.execute_script("return window.scrollY") #position on page
        height = driver.execute_script("return document.body.scrollHeight") #how much we can scroll
    
        if position >= height-1500:
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    lines1 = driver.find_elements(By.XPATH, "//div[@class='fohvkg f4ru8xs']")
    
    lines_list=[]
    team1 = 3 #the first team listed is always at the 3rd index
  
    for entry in lines1: 
        list_elem = entry.text.strip().split('\n')
        #print(list_elem, len(list_elem))
        team1, team2 = list_elem[0].split('@')
        #team1 = team1.strip()
        #team2 = team2.strip()
        teamName1 = team_fixer(team1.strip(), sport)
        teamName2 = team_fixer(team2.strip(), sport)
        status = 1
        if len(list_elem) == 21 and list_elem[2] == 'LIVE': #live game, have each teams score included in list_elem therefore length is 21
            spread_count1, spread_odds1, total_count1, total_odds1, moneyline1 = 9,10,11,12,13
            spread_count2, spread_odds2, total_count2, total_odds2, moneyline2 = 16,17,18,19,20

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book':'pointsbet',
                               'when':'Today', 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],list_elem[spread_odds1]], 'total':[f'O {list_elem[total_count1].split(" ")[1]}', list_elem[total_odds1]], 'moneyline':list_elem[moneyline1]}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],list_elem[spread_odds2]], 'total':[f'U {list_elem[total_count2].split(" ")[1]}', list_elem[total_odds2]], 'moneyline':list_elem[moneyline2]}],
                               'link':sport_site}) 
            
        elif len(list_elem) == 19: #pregame
            spread_count1, spread_odds1, total_count1, total_odds1, moneyline1 = 8,9,10,11,12
            spread_count2, spread_odds2, total_count2, total_odds2, moneyline2 = 14,15,16,17,18
            status = 1

            day = list_elem[status].split(',')[0].strip().find('Today')
            if day == -1:
                day = 'Tomorrow'
            else:
                day = 'Today'

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book':'pointsbet',
                               'when':day, 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],list_elem[spread_odds1]], 'total':[f'O {list_elem[total_count1].split(" ")[1]}', list_elem[total_odds1]], 'moneyline':list_elem[moneyline1]}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],list_elem[spread_odds2]], 'total':[f'U {list_elem[total_count2].split(" ")[1]}', list_elem[total_odds2]], 'moneyline':list_elem[moneyline2]}],
                               'link':sport_site}) 
        time.sleep(0.05)
    end = time.time()
    #print(end-start)
    driver.quit()
    return lines_list


   

# print('NHL')
#print(pointsbet('https://on.pointsbet.ca/sports/ice-hockey/NHL/', 'NHL')) #nhl odds
# print('')
# print('NBA')
# print(pointsbet('https://on.pointsbet.ca/sports/basketball/NBA', 'NBA')) #nba odds
# print('')
# print('NFL')
# print(pointsbet('https://on.pointsbet.ca/sports/american-football/NFL', 'NFL')) #nfl odds
# print('')
# print('NCAA')
#print(pointsbet('https://on.pointsbet.ca/sports/basketball/NCAA', 'NCAA')) #NCAA basketball odds

# x = pointsbet('https://on.pointsbet.ca/sports/basketball/NBA', 'NBA')
# for entry in x:
#     print(entry)

# x = pointsbet('https://on.pointsbet.ca/sports/american-football/NFL', 'NFL')
# for entry in x:
#     print(entry)


# iteration=0
# bigx=[]


# @app.get("/")
# def test():
#     global bigx
#     return(bigx)

# def update_x():
#     global bigx
#     global iteration

#     # Create a ChromeOptions object
#     chrome_options = Options()


#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument('--disable-notifications')
#     chrome_options.add_argument('--disable-infobars')
#     chrome_options.add_argument('--disable-extensions')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

#     chrome_options.add_experimental_option(
#         "prefs", {
#             # block image loading
#             "profile.managed_default_content_settings.images": 2,
#         }
#     )
    
#     while True:
#         print(f'Iteration {iteration}')
#         site = pointsbet('https://on.pointsbet.ca/sports/ice-hockey/NHL/', 'NHL', chrome_options) #nhl odds
#         #if oldx!=site:
#         bigx = site
#         #oldx = site
#         iteration+=1
#         time.sleep(10) #longer delay cuz 1) dont needa be checking every so often as odds dont change that much 2) checking very often will get us banned likely

# thread = threading.Thread(target=update_x)
# thread.start()


# path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'


# chrome_options = Options()


# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument('--window-size=1920,1080')  
# chrome_options.add_argument('--disable-notifications')
# chrome_options.add_argument('--disable-infobars')
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# chrome_options.add_experimental_option(
#     "prefs", {
#         # block image loading
#         "profile.managed_default_content_settings.images": 2,
#     }
# )




# x = pointsbet('https://on.pointsbet.ca/sports/ice-hockey/NHL/', 'NHL', chrome_options)
# for entry in x:
#     print(entry)

# x = pointsbet('https://on.pointsbet.ca/sports/basketball/NBA', 'NBA')
# for entry in x:
#     print(entry)

# x = pointsbet('https://on.pointsbet.ca/sports/american-football/NFL', 'NFL')
# for entry in x:
#     print(entry)

#nba nhl nfl ncaa done (double check ncaa)


#right now were working on these names, making sure the csv is as we want it and its working correctly, then need to do it for all the other sports.


