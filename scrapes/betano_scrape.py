from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from csv_test import team_fixer
from betrivers_scrape import name_fixer


#this will get you the info you need for pointsbet, pass to it the url of the sport of concern
def betano(sport_site, sport, chrome_options):
    print(f'betano {sport}')
    # Get current date
    current_date = datetime.now()
    tomorrows_date = current_date + timedelta(days=1)

    day = current_date.strftime("%b %d").upper()
    day_month = current_date.strftime("%b").upper()
    tomorrow = tomorrows_date.strftime("%b %d").upper()
    tomorrow_month = tomorrows_date.strftime("%b").upper()
    #print(day)
    #print(tomorrow)
    

    #start = time.time()
    website = sport_site
    xpath = "//div[contains(@class,'tw-flex tw-flex-col tw-items-start tw-justify-center tw-w-full dark:tw-bg-n-22-licorice tw-bg-white-snow tw-mb-n dark:hover:tw-bg-n-28-cloud-burst hover:tw-bg-n-97-porcelain')]" 
    xpath2 = '//div[contains(@class, "tw-w-full tw-bg-n-94-dirty-snow tw-bg-white-snow")]'
    xpath_button = "//button[contains(@class,'sb-modal__close__btn')]" #note in case of future need: i got this by running this file without headless mode, for some reason just going to the site it wasnt popping up for me


    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    #opens the window
    driver.get(website)

    #in case the pop up comes:
    try:
        WebDriverWait(driver,50).until(EC.presence_of_element_located((By.XPATH, xpath_button)))
        button = driver.find_element(By.XPATH, xpath_button)        
        button.click()
    except:
        pass
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
    time.sleep(2)
    
    
    lines1 = driver.find_elements(By.XPATH, xpath)
    test = driver.find_elements(By.XPATH, xpath2)

    dates=[] #will be a list of lists
    start=0
    for game in test:
        list_elem = game.text.strip().split('\n')
        for i, entry in enumerate(list_elem):
            if day_month in entry or tomorrow_month in entry:
                if i != start:
                    dates.append(list_elem[start:i])
                start = i

    # Append the last sublist
    dates.append(list_elem[start:])
    
    # for entry in dates:
    #     print(entry)
    '''
    What dates looks like, a list of lists
    ['DEC 17', 'Moneyline', 'Spread', 'Total', 'LIVE', 'Houston Rockets', 'Milwaukee Bucks', '159', '+530', '-909', '+6.5', '-114', '-6.5', '-114', 'LIVE', 'Washington Wizards', 'Phoenix Suns', '255', '-102', '-125', '+1.5', '-122', '-1.5', '-102', 'O 229.5', '-120', 'U 229.5', '-105', 'LIVE', 'Golden State Warriors', 'Portland Trail Blazers', '326', '-323', '+240', '-8.5', '-114', '+8.5', '-111', 'O 232.5', '-114', 'U 232.5', '-111']
    ['DEC 18', 'Moneyline', 'Spread', 'Total', '07:10 PM', 'Houston Rockets', 'Cleveland Cavaliers', '188', '+167', '-200', '+4.5', '-102', '-4.5', '-118', 'O 214.5', '-111', 'U 214.5', '-110', '07:10 PM', 'Los Angeles Clippers', 'Indiana Pacers', '26', '-133', '+115', '-2.5', '-111', '+2.5', '-111', 'O 243.5', '-114', 'U 243.5', '-108', '07:10 PM', 'Chicago Bulls', 'Philadelphia 76ers', '434', '+420', '-556', '+10.5', '-110', '-10.5', '-111', 'O 228.5', '-111', 'U 228.5', '-111', '07:40 PM', 'Detroit Pistons', 'Atlanta Hawks', '205', '+385', '-500', '+9.5', '-110', '-9.5', '-111', 'O 240.5', '-114', 'U 240.5', '-108', '07:40 PM', 'Minnesota Timberwolves', 'Miami Heat', '188', '-133', '+112', '-2.5', '-108', '+2.5', '-114', 'O 219.5', '-111', 'U 219.5', '-111', '07:40 PM', 'Charlotte Hornets', 'Toronto Raptors', '26', '+365', '-476', '+9.5', '-105', '-9.5', '-118', 'O 225.5', '-111', 'U 225.5', '-111', '08:10 PM', 'Memphis Grizzlies', 'Oklahoma City Thunder', '409', '+345', '-435', '+9.5', '-108', '-9.5', '-114', 'O 228.5', '-111', 'U 228.5', '-111', '09:10 PM', 'Dallas Mavericks', 'Denver Nuggets', '411', '+235', '-286', '+7.5', '-115', '-7.5', '-105', 'O 238.5', '-111', 'U 238.5', '-111', '09:10 PM', 'Brooklyn Nets', 'Utah Jazz', '311', '-167', '+140', '-3.5', '-111', '+3.5', '-111', 'O 231.5', '-111', 'U 231.5', '-111', '10:10 PM', 'Washington Wizards', 'Sacramento Kings', '3', '+420', '-556', '+10.5', '-110', '-10.5', '-111', 'O 244.5', '-111', 'U 244.5', '-111', '10:40 PM', 'New York Knicks', 'Los Angeles Lakers', '151', '+150', '-175', '+4.5', '-118', '-4.5', '-102', 'O 228.5', '-111', 'U 228.5', '-111']

    '''
    lines_list=[]
    
    for entry in lines1:
        list_elem = entry.text.strip().split('\n')
        #print(list_elem, len(list_elem))

        #both regame and live are length 14
        if len(list_elem) == 14: #['LIVE', 'Houston Rockets', 'Milwaukee Bucks', '245', '+385', '-588', '+9.5', '-105', '-9.5', '-120', 'O 245.5', '-111', 'U 245.5', '-114'] 14
            team1=list_elem[1] 
            team2=list_elem[2] 

            #print(f'checking {team1} vs {team2}')
            for game in dates:
                #print(dates)
                if team1 in game and game[game.index(team1) + 1] == team2:
                    date = game[0]
                    #print(f'date is {day}, game is on {date}')
                    if date == day:
                        #print(day, date)
                        when = 'Today'
                    elif date == tomorrow:
                        #print(tomorrow, date)
                        when = 'Tomorrow'
                    else:
                        when = 'TBD'
            
            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
            # print(f'Before: {team1} vs {team2}')
            # print(f'After: {teamName1} vs {teamName2}')

            spread_count1=6
            spread_odds1= list_elem[7]
            total_count1 = 10
            total_odds1 = list_elem[11]
            moneyline1 = list_elem[4]
            

            spread_count2=8
            spread_odds2=list_elem[9]
            total_count2 = 12
            total_odds2 = list_elem[13]
            moneyline2 = list_elem[5]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'betano',
                                'when':when, 
                                'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                                'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                                'link':sport_site}) 
    
        elif len(list_elem) == 15 and list_elem[1] == 'SO': #['07:37 PM', 'SO', 'Edmonton Oilers', 'New York Islanders', '189', '-133', '+122', '-1.5', '+162', '+1.5', '-200', 'O 6.5', '-125', 'U 6.5', '+102'] 15
            team1=list_elem[2] 
            team2=list_elem[3] 

            #print(f'checking {team1} vs {team2}')
            for game in dates:
                #print(dates)
                if team1 in game and game[game.index(team1) + 1] == team2:
                    date = game[0]
                    #print(f'date is {day}, game is on {date}')
                    if date == day:
                        #print(day, date)
                        when = 'Today'
                    elif date == tomorrow:
                        #print(tomorrow, date)
                        when = 'Tomorrow'
                    else:
                        when = 'TBD'
                    break
            #print(f'therefore, game is {when}')
            teamName1= name_fixer(team1.strip(), sport)
            teamName2 = name_fixer(team2.strip(), sport)
            # print(f'Before: {team1} vs {team2}')
            # print(f'After: {teamName1} vs {teamName2}')

            spread_count1=7
            spread_odds1= list_elem[8]
            total_count1 = 11
            total_odds1 = list_elem[12]
            moneyline1 = list_elem[5]
            

            spread_count2=9
            spread_odds2=list_elem[10]
            total_count2 = 13
            total_odds2 = list_elem[14]
            moneyline2 = list_elem[6]

            lines_list.append({'game':f'{teamName1} vs {teamName2}',
                                'book':'betano',
                                'when':when, 
                                'team1':[{'name':teamName1, 'spread': [list_elem[spread_count1],spread_odds1], 'total':[list_elem[total_count1], total_odds1], 'moneyline':moneyline1}], 
                                'team2':[{'name':teamName2, 'spread': [list_elem[spread_count2],spread_odds2], 'total':[list_elem[total_count2], total_odds2], 'moneyline':moneyline2}],
                                'link':sport_site}) 

    driver.quit()
    return lines_list



