#//li[contains(@class, '-sandwich-filter__event-list-item')] #bet entry xpath 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from csv_test import team_fixer
from betrivers_scrape import name_fixer
from webdriver_manager.chrome import ChromeDriverManager


#converts decimal odd to american
def convert(odd):
    odds = float(odd)
    if odds >= 2:
        return f'+{round((odds - 1) * 100)}'
    else:
        return str(round(-100 / (odds - 1)))

#this will get you the info you need for pointsbet, pass to it the url of the sport of concern
def northstar(sport_site, sport, chrome_options):
    print(f'northstar {sport}')
    # Get current date
    current_date = datetime.now()
    tomorrows_date = current_date + timedelta(days=1)

    day = current_date.strftime("%a")
    tomorrow = tomorrows_date.strftime("%a")
    

    #start = time.time()
    website = sport_site
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'
    xpath = "//li[contains(@class, '-sandwich-filter__event-list-item')]" 

    chrome_options.add_argument('--window-size=1920,1080')  
    

    # # Create a ChromeOptions object
    # chrome_options = Options()

    # # Set any options you need, for example, headless mode
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # chrome_options.add_argument('--window-size=1920,1080')  
    # chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")



    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    #opens the window

    #opens the window
    driver.get(website)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))

    lines1 = driver.find_elements(By.XPATH, xpath)
    lines_list=[]

    
    for entry in lines1:
        list_elem = entry.text.strip().split('\n')
        #print(list_elem, len(list_elem))

        #['48:28', '0', '1', 'Detroit Red Wings', '@ Philadelphia Flyers', '+1.5', '-177', '-1.5', '+130', '+340', '-480', 'Over', '2.5', '-225', 'Under', '2.5', '+160', '46 MORE BETS'] 18 Live
        #['Sat', '10:00 p.m.', 'Florida Panthers', '@ Edmonton Oilers', '+1.5', '-215', '-1.5', '+175', '+116', '-141', 'Over', '7', '+110', 'Under', '7', '-134', '342 MORE BETS'] 17 pregame

        if len(list_elem) == 18:
            team1=list_elem[3] 
            team2=list_elem[4].strip('@') 

            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
            # print(f'Before: {team1} vs {team2}')
            # print(f'After: {teamName1} vs {teamName2}')
            if list_elem[11] == 'Over':
                total_count1 = f'O {list_elem[12]}'
                total_count2 = f'U {list_elem[15]}'
            elif list_elem[11] == 'Under':
                total_count1 = f'U {list_elem[12]}'
                total_count2 = f'O {list_elem[15]}'

            spread_count1=5
            spread_odds1= list_elem[6]
            total_odds1 = list_elem[13]
            moneyline1 = list_elem[9]
            
            when = 'Today'
            
            spread_count2=7
            spread_odds2=list_elem[8]
            total_odds2 = list_elem[16]
            moneyline2 = list_elem[10]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'northstar',
                                'when':when, 
                                'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[total_count1, total_odds1], 'moneyline':moneyline1}], 
                                'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[total_count2, total_odds2], 'moneyline':moneyline2}],
                                'link':sport_site}) 
        elif len(list_elem) == 17:
            team1=list_elem[2] 
            team2=list_elem[3].strip('@') 

            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
            # print(f'Before: {team1} vs {team2}')
            # print(f'After: {teamName1} vs {teamName2}')
            if list_elem[10] == 'Over':
                total_count1 = f'O {list_elem[11]}'
                total_count2 = f'U {list_elem[14]}'
            elif list_elem[10] == 'Under':
                total_count1 = f'U {list_elem[11]}'
                total_count2 = f'O {list_elem[14]}'

            spread_count1=4
            spread_odds1= list_elem[5]
            total_odds1 = list_elem[12]
            moneyline1 = list_elem[8]
            
            if list_elem[0] == day:
                when = 'Today'
            elif list_elem[0] == tomorrow:
                when = 'Tomorrow'
            else:
                when = 'TBD'
            
            spread_count2=6
            spread_odds2=list_elem[7]
            total_odds2 = list_elem[15]
            moneyline2 = list_elem[9]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'northstar',
                                'when':when, 
                                'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[total_count1, total_odds1], 'moneyline':moneyline1}], 
                                'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[total_count2, total_odds2], 'moneyline':moneyline2}],
                                'link':sport_site}) 
    
    driver.quit()
    return lines_list


# path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

# # Create a ChromeOptions object
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


# x = northstar('https://www.northstarbets.ca/sportsbook#sports-hub/ice_hockey/nhl', 'NHL', chrome_options)
# for entry in x:
#     print(entry)

# x = northstar('https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba', 'NBA')
# for entry in x:
#     print(entry)

# x = northstar('https://www.northstarbets.ca/sportsbook#sports-hub/american_football/nfl', 'NFL')
# for entry in x:
#     print(entry)

#nhl, nba, nfl done
