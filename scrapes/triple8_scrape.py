from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
def triple8(sport_site, sport, chrome_options):
    print(f'888 {sport}')
    #start = time.time()
    website = sport_site
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'
    xpath = "//div[@class='bet-card']"
    xpath1 = "//span[@class='bb-sport-event__selection']"
    xpath3 = '//header[@class="bb-content-section__header"]'
    xpath4 = '//section[@class="bb-content-section eventList__content-section"]'

    game_lines_path = "//div[@class='bet-card__bet-buttons']"

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



    driver = webdriver.Chrome(options=chrome_options)    #opens the window

    #opens the window
    driver.get(website)
    # time.sleep(12)
    # screenshot_path = './screenshot.png'
    # driver.save_screenshot(screenshot_path)

    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
    


    lines1 = driver.find_elements(By.XPATH, xpath)
    title = driver.find_elements(By.XPATH, xpath3)
    test = driver.find_elements(By.XPATH, xpath4)
    vals = driver.find_elements(By.XPATH, xpath1)
    main = driver.find_elements(By.XPATH, game_lines_path)
    

    #to get dates
    dates=[]
    for entry in test:
        list_elem = entry.text.strip().split('\n')
        #print(list_elem, len(list_elem))
        dates.append(list_elem)

    '''
    dates looks like this:
    ['Today', 'Puck Line', 'Total', 'Money Line', 'CLB Blue Jackets @', '2', 'TOR Maple Leafs', '0', "Period 2 14'", '1.667', '2.00', '1.80', '1.85', '2.875', '1.364', 'WSH Capitals @', '1', 'PHI Flyers', '1', "Period 2 12'", '1.75', '1.90', '2.00', '1.70', '1.727', '1.95', 'CAR Hurricanes @', '1', 'DET Red Wings', '0', "Period 1 1'", '1.80', '1.833', '2.00', '1.70', '3.25', '1.286', 'CGY Flames @', '0', 'MIN Wild', '0', "Period 1 18'", '1.571', '2.15', '1.70', '2.00', '1.615', '2.15', 'OTT Senators @', '0', 'STL Blues', '0', "Period 1 19'", '1.90', '1.75', '1.80', '1.85', '1.85', '1.80', 'TB Lightning @', 'EDM Oilers', '21:00', '2.35', '1.60', '1.75', '2.05', '1.533', '2.45', 'FLA Panthers @', 'VAN Canucks', '22:00', '1.40', '2.95', '2.00', '1.80', '2.00', '1.80', 'CHI Blackhawks @', 'Seattle Kraken', '22:00', '2.00', '1.80', '1.80', '2.00', '1.40', '2.95'] 86
    ['Tomorrow', 'Puck Line', 'Total', 'Money Line', 'ANA Ducks @', 'NY Rangers', '19:00', '1.85', '1.95', '2.05', '1.75', '1.333', '3.20', 'BOS Bruins @', 'NY Islanders', '19:30', '1.45', '2.75', '1.80', '2.00', '2.05', '1.75', 'NSH Predators @', 'CAR Hurricanes', '19:30', '2.35', '1.60', '2.00', '1.80', '1.533', '2.45', 'OTT Senators @', 'DAL Stars', '20:00', '2.25', '1.65', '2.00', '1.80', '1.50', '2.55', 'SJ Sharks @', 'ARI Coyotes', '21:00', '2.15', '1.70', '2.05', '1.75', '1.45', '2.75', 'BUF Sabres @', 'VEG Golden Knights', '22:00', '2.05', '1.75', '2.00', '1.80', '1.45', '2.75'] 58
    ['Sat 16 Dec', 'Puck Line', 'Total', 'Money Line', 'VAN Canucks @', 'MIN Wild', '14:00', '1.85', '1.95', 'PIT Penguins @', 'TOR Maple Leafs', '19:00', '1.533', '2.45', 'NJ Devils @', 'CLB Blue Jackets', '19:00', '2.55', '1.50', 'COL Avalanche @', 'WPG Jets', '19:00', '1.90', '1.90', 'NY Rangers @', 'BOS Bruins', '19:00', '1.70', '2.15', 'NY Islanders @', 'MTL Canadiens', '19:00', '2.55', '1.50', 'DET Red Wings @', 'PHI Flyers', '19:00', '1.90', '1.90', 'DAL Stars @', 'STL Blues', '20:00', '2.35', '1.60', 'WSH Capitals @', 'NSH Predators', '20:00', '1.75', '2.05', 'BUF Sabres @', 'ARI Coyotes', '21:00', '1.90', '1.90', 'FLA Panthers @', 'EDM Oilers', '22:00', '1.75', '2.05', 'TB Lightning @', 'CGY Flames', '22:00', '1.90', '1.90', 'LA Kings @', 'Seattle Kraken', '22:00', '2.00', '1.80'] 69


    '''

    lines_list=[]
    i=0
    for entry in lines1: 
        list_elem = entry.text.strip().split('\n')
        inner = main[i].find_elements(By.XPATH, ".//span[@class='bb-sport-event__selection']")
        for bet in inner:
            list_elem.append(bet.get_attribute("data-label"))
        #print(list_elem, len(list_elem))

        

        #may need to double check indexes here, couldnt do so at the time i wrote them
        if len(list_elem) == 17: #live
            team1=list_elem[0] #CLB Blue Jackets @
            team2=list_elem[2] #TOR Maple Leafs, we want to keep it as this form cus the dates list has it like this too

            #['WSH Capitals @', '2', 'PHI Flyers', '1', 'PAUSE', '2.60', '1.40', '2.05', '1.667', '2.70', '1.40','-1.5', '+1.5', 'O 6.5', 'U 6.5', None, None] 17
            #[team1 @, team1 score, team2, team2 score, game status, team2 spread odds, team1 spread odds, team1 total odds, team2 total odds, team2 moneyline, team1 moneyline, team2 spread count, team1 spread count, team 1 total count, team2 total count, none, none] 17
            when = 'Today'
            
            teamName1= name_fixer(team1.strip('@').strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
            # print(f'Before: {team1} vs {team2}')
            # print(f'After: {teamName1} vs {teamName2}')

            spread_count1=12
            spread_odds1= convert(list_elem[6])
            total_count1 = 13
            total_odds1 = convert(list_elem[7])
            moneyline1 = convert(list_elem[10])
            

            spread_count2=11
            spread_odds2=convert(list_elem[5])
            total_count2 = 14
            total_odds2 = convert(list_elem[8])
            moneyline2 = convert(list_elem[9])

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'888',
                                'when':when, 
                                'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                                'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                                'link':sport_site}) 

            
        #sometimes, a live game can be of legnth 15, need to check this
        elif len(list_elem) == 15: #pregame
            try:
                #['ANA Ducks @', 'NY Rangers', '19:00', '1.75', '2.05', '2.05', '1.75', '1.30', '3.50', '-1.5', '+1.5', 'O 6.5', 'U 6.5', None, None] 15, the nones at the end r the two moneylines we dont care about
                team1 = list_elem[0]
                team2 = list_elem[1]
                
                for game in dates:
                    #print(f'is {team1} in {game}')
                    if team1 in game and game[game.index(team1) + 2] == team2: #today
                        when = game[0]
                        break
                    elif team1 in game and game[game.index(team1) + 1] == team2: #tomorrow
                        when=game[0]
                        break
                    else: #doesnt matter
                        when = 'TBD'

                teamName1= name_fixer(team1.strip('@').strip(), sport)
                teamName2 = name_fixer(team2.strip(), sport)
                # print(f'Before: {team1} vs {team2}')
                # print(f'After: {teamName1} vs {teamName2}')

                spread_count1=10
                spread_odds1= convert(list_elem[4])
                total_count1 = 11
                total_odds1 = convert(list_elem[5])
                moneyline1 = convert(list_elem[8])
                

                spread_count2=9
                spread_odds2=convert(list_elem[3])
                total_count2 = 12
                total_odds2 = convert(list_elem[6])
                moneyline2 = convert(list_elem[7])

                lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                    'book':'888',
                                    'when':when, 
                                    'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                                    'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                                    'link':sport_site}) 
            except Exception as e:
                pass
        i+=1
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
            


# x = triple8('https://www.888sport.ca/ice-hockey/nhl/', 'NHL', driver)
# for entry in x:
#     print(entry)

# x = triple8('https://www.888sport.ca/basketball/nba/', 'NBA')
# for entry in x:
#     print(entry)

# x = triple8('https://www.888sport.ca/football/nfl/', 'NFL')
# for entry in x:
#     print(entry)

#print(triple8('https://www.888sport.ca/basketball/ncca-odds/', 'NCAA'))
# for entry in x:
#     print(entry)




#working on ncaa naming