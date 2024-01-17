#//div[@class="events-table-module_rowWrapper__brOLD"] #to get bet entries

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

#converts decimal odd to american
def convert(odd):
    odds = float(odd)
    if odds >= 2:
        return f'+{round((odds - 1) * 100)}'
    else:
        return str(round(-100 / (odds - 1)))

#this will get you the info you need for pointsbet, pass to it the url of the sport of concern
def tonybet(sport_site, sport, chrome_options):
    print(f'tonybet {sport}')
    # Get current date
    current_date = datetime.now()
    tomorrows_date = current_date + timedelta(days=1)

    # Format the date as dd.mm.yyyy
    formatted_date = current_date.strftime("%d.%m.%Y")
    formatted_tomorrows_date = tomorrows_date.strftime("%d.%m.%Y")

    #start = time.time()
    website = sport_site
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'
    xpath = "//div[contains(@class, 'events-table-module_rowWrapper')]" 
    

    # Create a ChromeOptions object
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


    service = ChromeService(path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    #opens the window
    driver.get(website)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))

    lines1 = driver.find_elements(By.XPATH, xpath)
    lines_list=[]
   
    #No live game for tonybet, only pregame
    for entry in lines1:
        list_elem = entry.text.strip().split('\n')
        #print(list_elem, len(list_elem))
        
        if len(list_elem) == 14: 
            team1=list_elem[1] 
            team2=list_elem[2] 


            #['22.12.2023, 07:00 PM', 'Detroit Red Wings', 'Philadelphia Flyers', '+120', '+340', '+179', '-239', '-455', '-162', '+116', '- 0.5 +', '-141', '-114', '6', '-108', '338'] 16
            #['16.12.2023, 09:00 PM', 'Arizona Coyotes', 'Buffalo Sabres', '1.89', '1.92', '-1.5', '3.05', '+1.5', '1.38', '0 6.5', '1.9', 'U 6.5', '1.91', '334'] 14
            
            
            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
            # print(f'Before: {team1} vs {team2}')
            # print(f'After: {teamName1} vs {teamName2}')

            spread_count1=5
            spread_odds1= list_elem[6]
            #total_count1 = 9

            total_count1x = list_elem[9] #will always be over i.e 0, convert to O
            splitit = total_count1x.split(' ')
            total_count1 = splitit[0].replace('0', 'O') + ' ' + splitit[1]

            total_odds1 = list_elem[10]
            moneyline1 = list_elem[3]
            date= list_elem[0].split(',')[0]
            if date == formatted_date:
                when='Today'
            elif date == formatted_tomorrows_date:
                when= 'Tomorrow'
            else:
                when = date
            

            spread_count2=7
            spread_odds2=list_elem[8]
            #total_count2 = 11
            total_count2 = list_elem[11]
            total_odds2 = list_elem[12]
            moneyline2 = list_elem[4]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'tonybet',
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


# # Create a ChromeService object with the executable path
# service = ChromeService(path)

# # Pass the ChromeService object and ChromeOptions object to the webdriver.Chrome constructor
# driver = webdriver.Chrome(service=service, options=chrome_options)

# x = tonybet('https://tonybet.ca/prematch/leagues/1013499-nhl', 'NHL', driver)
# for entry in x:
#     print(entry)

# x = tonybet('https://tonybet.ca/prematch/leagues/1008918-nba', 'NBA')
# for entry in x:
#     print(entry)

# x = tonybet('https://tonybet.ca/prematch/leagues/1014465-nfl', 'NFL')
# for entry in x:
#     print(entry)

# x = tonybet('https://tonybet.ca/prematch/leagues/1008955-ncaa-regular-season', 'NCAA')
# for entry in x:
#     print(entry)
#nhl done, nba done, nfl done