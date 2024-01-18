from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import csv
import os
    

#names is the team name, for ncaa we split this by space and check each word
def name_fixer(names, sport):

    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_directory, f'{sport}_names.csv')

    with open(csv_file_path, 'r') as file:
        csv_content = file.read()

        reader = csv.DictReader(csv_content.splitlines())

        if sport == 'NCAA':
            i=0
            #print(names)
            names = names.split(' ')
            #print(f'checking {names}')
            #loop through each row (each row is a dict where \ufeffSchool is the key to our possible names, 'nickname' is the key to our nickname which well set everything to)
            for row in reader:
                #print(row)
                name = row['Full Name'].strip()
                possibly = row['\ufeffSchool'].split('/')
                possible = [entry.strip() for entry in possibly]
               
                for entry in names:
                    #print(f'comparing {entry} to {name} or {possible}')
                    if entry in name or entry in possible or any(entry == possibility for possibility in possible):
                        #print('match')
                        i+=1
                        if i == len(names):
                            return row['Full Name']
                    #no match, reset i and go to the next team in csv
                    else:
                        i=0
                        break
        elif sport == 'NHL' or sport == 'NBA' or sport == 'NFL':
            team = ''.join(names).strip()
            for row in reader:

                #team is what the book has posted, entry is a possible name from our csv
                if team in row['\ufeffFull Name'] or team in row['AbbName'] or team in row['AbbName2'] or team in row['AbbName3']:
                    return row['\ufeffFull Name']


#moneyline, total, spread
def betrivers(sport_site, sport, chrome_options):
    print(f'betrivers {sport}')
    website = sport_site
    #path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'
    xpath = "//article[contains(@data-testid, 'listview-group')]"
    more = "//button[contains(@data-testid, 'show-more-events-button')]"
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

    # # Create a ChromeOptions object
    # chrome_options = Options()

    # # Set any options you need, for example, headless mode
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--window-size=1920,1080')
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-infobars')
    # chrome_options.add_argument('--disable-crash-reporter')
    # chrome_options.add_argument('--disable-component-extensions-with-background-pages')
  
    # chrome_options.add_argument('--disable-in-process-stack-traces')
    # chrome_options.add_argument('--disable-default-apps')
    # chrome_options.add_argument('--disable-software-rasterizer')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--proxy-server="direct://"')
    # chrome_options.add_argument('--proxy-bypass-list=*')
    # chrome_options.add_argument('--disable-impl-side-painting')

    # chrome_options.add_experimental_option(
    #     "prefs", {
    #         # block image loading
    #         "profile.managed_default_content_settings.images": 2,
    #     }
    # )

    # # Create a ChromeService object with the executable path
    service = ChromeService(path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
 
    #opens the window
    driver.get(website)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
    combined_list=[]
    while True:
        try:
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
            lines = driver.find_elements(By.XPATH, xpath) #all current open betting lines on nba homepage
            for line in lines:
                word = line.text.strip()
                combined_list.append(word)
            # for entry in combined_list:
            #     print(entry.text)

            # Check for the presence of the element
            element = driver.find_element(By.XPATH, more)
            #driver.execute_script("arguments[0].scrollIntoView();",element)
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)

            #wait till buttons on screen
            WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, more)))

            # If the element is found, click it
            element.click()
        except:
            break
    time.sleep(2)

    big_list=[]
    for entry in combined_list:
        test = entry.split('\n')
        if test not in big_list and test != ['']:
            big_list.append(test)

 

    status = 0

    lines_list=[]
    for entry in big_list: 

        list_elem = entry
        #print(list_elem, len(list_elem))
        
        #live game: ['LIVE', 'Liberty Flames', 'Florida Atlantic Owls', 'SPREAD', 'WIN', 'TOTAL POINTS', '+8.5', '-117', '-8.5', '-120', '+300', '-480', 'O 138.5', '-114', 'U 138.5', '-122', '11 Bets', 'SGP'] len = 18
        #pre game: ['TODAY 11:00 PM', 'UC Riverside Highlanders', 'UCLA Bruins', 'SPREAD', 'WIN', 'TOTAL POINTS', '+19', '-114', '-19', '-106', '+1600', '-10000', 'O 128', '-109', 'U 128', '-110', '108 Bets', 'SGP', 'Stats', 'Tips'] len = 20
        if len(list_elem) == 18 and list_elem[0] == 'LIVE': #live game with all 3 lines open i.e moneyline spread total
            
            team1=list_elem[1] #no score shown for this run, why? is this how it ususally is? may need to adjust if its different later
            team2=list_elem[2]

            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
         
            spread_count1=6
            spread_odds1=7
            total_count1 = 12
            total_odds1 = 13
            moneyline_count1 = 10
            

            spread_count2=8
            spread_odds2=9
            total_count2 = 14
            total_odds2 = 15
            moneyline_count2 = 11

            # print(f'Before conversion: {team1} vs {team2}')
            # print(f'After conversion: {teamName1} vs {teamName2}')
            # print('')

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                               'book': 'betrivers',
                               'when': 'Today', 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],list_elem[spread_odds1]], 'total':[list_elem[total_count1], list_elem[total_odds1]], 'moneyline':list_elem[moneyline_count1]}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],list_elem[spread_odds2]], 'total':[list_elem[total_count2], list_elem[total_odds2]], 'moneyline':list_elem[moneyline_count2]}],
                               'link':sport_site}) 
        
        elif len(list_elem) == 20 or len(list_elem) == 18 or len(list_elem) == 19: #length 20 is pregame for  agame today, length 18 or 19 is pregame for a game tomorrow
            team1=list_elem[1] 
            team2=list_elem[2]

            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)

            spread_count1=6
            spread_odds1=7
            total_count1 = 12
            total_odds1 = 13
            moneyline_count1 = 10
            

            spread_count2=8
            spread_odds2=9
            total_count2 = 14
            total_odds2 = 15
            moneyline_count2 = 11

            day = list_elem[status].split(' ')[0].strip().title()
            # print(f'Before conversion: {team1} vs {team2}')
            # print(f'After conversion: {teamName1} vs {teamName2}')
            # print('')
            
            lines_list.append({'game':f'{teamName1} vs {teamName2}', 
                               'book': 'betrivers',
                               'when':day, 
                               'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],list_elem[spread_odds1]], 'total':[list_elem[total_count1], list_elem[total_odds1]], 'moneyline':list_elem[moneyline_count1]}], 
                               'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],list_elem[spread_odds2]], 'total':[list_elem[total_count2], list_elem[total_odds2]], 'moneyline':list_elem[moneyline_count2]}],
                               'link':sport_site}) 
        time.sleep(0.05)
    driver.quit()
    return lines_list


# print('NHL')
# print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093657&type=matches')) #nhl odds
# print('')


# print('NBA')
# print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches')) #nba odds
# print('')

# print('NFL')
# print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093656&type=matches')) #nfl odds
# print('')

# print('NCAA')
#print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093654&type=matches', 'NCAA')) #NCAA basketball odds
#print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093654&type=matches','NCAA'))
'''
print('NHL')
print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093657&type=matches')) #nhl odds
print('')
'''
#print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093657&type=matches','NHL')) #nhl odds

#print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093654&type=matches', 'NCAA'))
# for entry in x:
#     print(entry)

#print(betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches', 'NBA'))
# for entry in x:
#     print(entry)

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

# x = betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093657&type=matches','NHL', driver)
# for entry in x:
#     print(entry)

# x = betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches', 'NBA')
# for entry in x:
#     print(entry)

# x = betrivers('https://on.betrivers.ca/?page=sportsbook&group=1000093656&type=matches', 'NFL')
# for entry in x:
#     print(entry)

#ncaa names need to be monitored

#br_pp('https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=playerprops', 'NBA')

# def main():
#     start = time.time()
#     with concurrent.futures.ProcessPoolExecutor() as executor:

       
#         br_nba = executor.submit(betrivers, 'https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches','NBA')
#         br_nba_pp = executor.submit(br_pp, 'https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=playerprops', 'NBA')
#         print(br_nba.result())
#         print(br_nba_pp.result())     

#     end = time.time()
#     print(end-start)

# if __name__ == '__main__':
#     main()