from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from csv_test import team_fixer
from webdriver_manager.chrome import ChromeDriverManager


#converts decimal odd to american
def convert(odd):
    odds = float(odd)
    if odds >= 2:
        return f'+{round((odds - 1) * 100)}'
    else:
        return str(round(-100 / (odds - 1)))
    
#this will get you the info you need for pointsbet, pass to it the url of the sport of concern
def betmgm(sport_site, sport, chrome_options):
    #start = time.time()
    print(f'mgm {sport}')
    website = sport_site
    #path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'
    xpath = "//ms-six-pack-event[@class='grid-event grid-six-pack-event ms-active-highlight two-lined-name ng-star-inserted']"
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'


    # Create a ChromeOptions object
    # chrome_options = Options()

    # # Set any options you need, for example, headless mode
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-gpu')

    # chrome_options.add_experimental_option(
    #     "prefs", {
    #         # block image loading
    #         "profile.managed_default_content_settings.images": 2,
    #     }
    # )


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    #opens the window
    #opens the window
    driver.get(website)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
    # screenshot_path = './screenshotMGM2.png'

    # # Capture the screenshot
    # driver.save_screenshot(screenshot_path)

    while True:
        try:
            # Check for the presence of the element
            element = driver.find_element(By.XPATH, "//div[@class = 'grid-footer show-more ng-star-inserted']")
            driver.execute_script("arguments[0].scrollIntoView();",element)
            time.sleep(2)
            # If the element is found, click it
            element.click()
        except:
            break

    time.sleep(2)
    lines = driver.find_elements(By.XPATH, xpath)

    lines_list=[]
    status=0

    team1 = 4
    team2 = 5
    

    for entry in lines:
        list_elem = entry.text.strip().split('\n')
        #print('lets go list elem for mgm', len(list_elem))
        print(list_elem, len(list_elem))
        

        if len(list_elem) == 19 and (list_elem[0] == "LIVE" or list_elem[0] == 'Intermission'): #need to double check to make sure this works, pretyy sure pregame is good
            #print('live')
            team_Name1 = list_elem[team1].strip()
            team_Name2 = list_elem[team2].strip()
            teamName1 = team_fixer(team_Name1, sport)
            teamName2 = team_fixer(team_Name2, sport)

            spread_count1, total_count1 = 8,12
            spread_count2, total_count2= 10,14


            spread_odds1 = convert(list_elem[9])
            total_odds1 = convert(list_elem[13])
            moneyline1 = convert(list_elem[16])

            spread_odds2 = convert(list_elem[11])
            total_odds2 = convert(list_elem[15])
            moneyline2 = convert(list_elem[17])

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book':'betmgm',
                               'when':'Today', 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                               'link':sport_site}) 
        
        elif len(list_elem)==17 or len(list_elem)==18 or len(list_elem)==16: #pre game, today or tomorrow, 17 and 18 need to be included here
            #['Today • 7:00 PM', 'Spread', 'Total', 'Money', 'Delaware', 'Robert Morris', '-4.5', '1.91', '+4.5', '1.91', 'O 143.5', '1.95', 'U 143.5', '1.87', '1.50', '2.65', 'Build Parlay', 'All Wagers'] 18
            #['Today • 7:00 PM', 'Spread', 'Total', 'Money', 'Jacksonville', 'South Carolina State', '-5.5', '1.91', '+5.5', '1.91', 'O 145.5', '1.91', 'U 145.5', '1.91', '1.40', '3.00', 'All Wagers'] 17
            #print('before pregame try')
            try:
                #print('after pregame try')
                team_Name1 = list_elem[team1].strip()
                team_Name2 = list_elem[team2].strip()
                teamName1 = team_fixer(team_Name1, sport)
                teamName2 = team_fixer(team_Name2, sport)

                spread_count1, total_count1 = 6,10
                spread_count2, total_count2 = 8,12

                spread_odds1 = convert(list_elem[7])
                total_odds1 = convert(list_elem[11])
                moneyline1 = convert(list_elem[14])

                spread_odds2 = convert(list_elem[9])
                total_odds2 = convert(list_elem[13])
                moneyline2 = convert(list_elem[15])
        
                day = list_elem[status].split('•')[0].strip()
                #print(day)
                if day == 'Tomorrow':
                    pass
                elif day == 'Today':
                    day = 'Today'
                
               
             
                lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'betmgm',
                                'when':day, 
                                'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                                'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                                'link':sport_site}) 
            except Exception as e:
                print(e)
                pass
        time.sleep(0.08)
    driver.quit()
    #print('printing lines_list')
    #print(lines_list)
    return lines_list



# print('NHL')
# print(betmgm('https://sports.on.betmgm.ca/en/sports/hockey-12/betting/usa-9/nhl-34')) #nhl odds
# print('')
# print('NBA')
# print(betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/nba-6004')) #nba odds
# print('')
# print('NFL')
# print(betmgm('https://sports.on.betmgm.ca/en/sports/football-11/betting/usa-9/nfl-35')) #nfl odds
# print('')
# print('NCAA')
# print(betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/ncaa-264')) #NCAA basketball odds
#print(betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/ncaa-264','NCAA'))
'''
print('NHL')
print(betmgm('https://sports.on.betmgm.ca/en/sports/hockey-12/betting/usa-9/nhl-34')) #nhl odds
print('')
'''
#betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/ncaa-264')

#print(betmgm('https://sports.on.betmgm.ca/en/sports/hockey-12/betting/usa-9/nhl-34', 'NHL'))
# for entry in x:
#     print(entry)

#print(betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/nba-6004', 'NBA'))
# for entry in x:
#     print(entry)

# path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'


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




# x = betmgm('https://sports.on.betmgm.ca/en/sports/hockey-12/betting/usa-9/nhl-34', 'NHL', chrome_options)
# for entry in x:
#     print(entry)

# x = betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/nba-6004', 'NBA')
# for entry in x:
#     print(entry)

# x = betmgm('https://sports.on.betmgm.ca/en/sports/football-11/betting/usa-9/nfl-35', 'NFL')
# for entry in x:
#     print(entry)

# x = betmgm('https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/ncaa-264', 'NCAA')
# for entry in x:
#     print(entry)

'''
['Penguins', 'Sabres', '2', '3', 'Bet now', 'LIVE', 'P3 < 02:30', 'All Wagers']
['Islanders', 'Senators', '1', '1', '+1.5', '1.34', '-1.5', '3.10', 'O 6.5', '1.72', 'U 6.5', '2.05', '2.05', '1.75', 'LIVE', '1st Intermission', 'All Wagers']
['Lightning', 'Hurricanes', '0', '0', '+1.5', '1.42', '-1.5', '2.75', 'O 4.5', '1.55', 'U 4.5', '2.35', '2.20', '1.67', 'LIVE', 'P1 < 05:45', 'All Wagers']
['Jets', 'Panthers', '0', '0', '+1.5', '1.40', '-1.5', '2.80', 'O 5.5', '2.05', 'U 5.5', '1.72', '2.05', '1.75', 'LIVE', 'P1 < 08:45', 'All Wagers']
['Flames', 'Stars', '+1.5', '1.60', '-1.5', '2.40', 'O 6', '1.91', 'U 6', '1.91', '2.45', '1.57', 'Starting in 8 min', 'Build Parlay', 'All Wagers']
['Avalanche', 'Wild', '-1.5', '2.80', '+1.5', '1.45', 'O 6.5', '1.83', 'U 6.5', '2.00', '1.75', '2.10', 'Starting in 8 min', 'Build Parlay', 'All Wagers']
['Canucks', 'Kraken', '-1.5', '3.00', '+1.5', '1.40', 'O 6.5', '1.80', 'U 6.5', '2.05', '1.87', '1.95', 'Today • 10:08 PM', 'Build Parlay', 'All Wagers']

live with no moneyline
['Sabres', 'Devils', '1', '5', '+4.5', '1.67', '-4.5', '2.10', 'O 9.5', '2.25', 'U 9.5', '1.60', 'LIVE', 'P2 < 11:00', 'All Wagers']
'''

#nhl nba ncaa done (double check ncaa)