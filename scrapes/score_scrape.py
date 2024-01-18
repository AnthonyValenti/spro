#//div[contains(@class, 'bg-card-primary rounded p-4')]

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
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager


app = FastAPI()

def pb_pp(url, sport):
    ...

#this will get you the info you need for pointsbet, pass to it the url of the sport of concern
def score(sport_site, sport, chrome_options):

    start = time.time()
    print(f'score {sport}')

    current_date = datetime.now()
    tomorrows_date = current_date + timedelta(days=1)

    day = current_date.strftime("%b %d").title()
    tomorrow = tomorrows_date.strftime("%b%e").title()
    # print(day)
    # print(day_month)
    #print(tomorrow)
    # print(tomorrow_month)


    website = sport_site
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

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


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    #opens the window

    #opens the window
    driver.get(website)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'bg-card-primary rounded p-4')]")))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'bg-card-primary rounded p-4')]")))


    lines1 = driver.find_elements(By.XPATH, "//div[contains(@class, 'bg-card-primary rounded p-4')]")
    
    lines_list=[]

    for entry in lines1: 
        list_elem = entry.text.strip().split('\n')
        #print(list_elem, len(list_elem))


        #need to double check live

        #['LIVE', '6:49 1st', '1st & 10', 'Pinstripe Bowl', 'Spread', 'Total', 'Money', 'Rutgers', '7', '-7.5', '-110', 'O 43.5', '-120', '-330', 'Miami (FL)', '0', '+7.5', '-120', 'U 43.5', '-110', '+240', 'MIA 15'] 22
        if len(list_elem) == 19 and list_elem[0] == 'LIVE':
            team1 = 5
            team2 = 12
            team_Name1 = list_elem[team1].strip()
            team_Name2 = list_elem[team2].strip()
            teamName1 = team_fixer(team_Name1, sport)
            teamName2 = team_fixer(team_Name2, sport)

            spread_count1, total_count1 = 7,9
            spread_count2, total_count2= 14,16


            spread_odds1 = list_elem[8]
            total_odds1 = list_elem[10]
            moneyline1 = list_elem[11]

            spread_odds2 = list_elem[15]
            total_odds2 = list_elem[17]
            moneyline2 = list_elem[18]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book':'score',
                               'when':'Today', 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                               'link':sport_site})

        
        #['Today · 9:15 PM', 'Alamo Bowl', 'Spread', 'Total', 'Money', 'Arizona', '-2.5', '-110', 'O 59.5', '-110', '-130', 'Oklahoma', '+2.5', '-110', 'U 59.5', '-110', '+110'] 17
        elif len(list_elem) == 17: #pregame type 2
            team1 = 5
            team2 = 11
            team_Name1 = list_elem[team1].strip()
            team_Name2 = list_elem[team2].strip()
            teamName1 = team_fixer(team_Name1, sport)
            teamName2 = team_fixer(team_Name2, sport)

            spread_count1, total_count1 = 6,8
            spread_count2, total_count2= 12,14

            day = list_elem[0].split('·')[0].strip()
            if 'Today' in day:
                when = 'Today'
            elif tomorrow in day:
                when = 'Tomorrow'
            else:
                when = 'TBD'

            spread_odds1 = list_elem[7]
            total_odds1 = list_elem[9]
            moneyline1 = list_elem[10]

            spread_odds2 = list_elem[13]
            total_odds2 = list_elem[15]
            moneyline2 = list_elem[16]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book':'score',
                               'when':when, 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                               'link':sport_site}) 


        #['Today · 7:30 PM', 'Spread', 'Total', 'Money', 'DET Pistons', '2-28, 15th Eastern', '+16.5', '-105', 'O 232.5', '-110', '+1000', 'BOS Celtics', '23-6, 1st Eastern', '-16.5', '-115', 'U 232.5', '-110', '-1800'] 18

        elif len(list_elem) == 18: #pregame type 3
            team1 = 4
            team2 = 11
            team_Name1 = list_elem[team1].strip()
            team_Name2 = list_elem[team2].strip()
            teamName1 = team_fixer(team_Name1, sport)
            teamName2 = team_fixer(team_Name2, sport)

            spread_count1, total_count1 = 6,8
            spread_count2, total_count2= 13,15

            day = list_elem[0].split('·')[0].strip()

           
            if 'Today' in day:
                when = 'Today'
            elif tomorrow in day:
                when = 'Tomorrow'
            else:
                when = 'TBD'

            spread_odds1 = list_elem[7]
            total_odds1 = list_elem[9]
            moneyline1 = list_elem[10]

            spread_odds2 = list_elem[14]
            total_odds2 = list_elem[16]
            moneyline2 = list_elem[17]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book':'score',
                               'when':when, 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                               'link':sport_site}) 
    driver.quit()
    return lines_list

# path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

# # Create a ChromeOptions object
# chrome_options = Options()


# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
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

# x = score('https://thescore.bet/sport/hockey/organization/united-states/competition/nhl/featured-page', 'NHL', chrome_options)
# for entry in x:
#     print(entry)




# x = score('https://thescore.bet/sport/basketball/organization/united-states/competition/nba', 'NBA', driver)
# for entry in x:
#     print(entry)

# x = score('https://thescore.bet/sport/hockey/organization/united-states/competition/nhl/featured-page', 'NHL', chrome_options)
# for entry in x:
#     print(entry)

# x = score('https://thescore.bet/sport/football/organization/united-states/competition/nfl/featured-page', 'NFL')
# for entry in x:
#     print(entry)


#pretty sure the score is good, just double check, especially live, before adding 
