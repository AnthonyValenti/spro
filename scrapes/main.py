#from pointsbet_scrape import pointsbet
#from betmgm_scrape import betmgm
#from betrivers_scrape import betrivers
#from bet99_scrape import bet99
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pytz
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
from score_scrape import score
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import threading

#logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


origins = ["http://localhost", "http://localhost:5500", "http://127.0.0.1:5500/odds_scraping/frontend/index.html", "http://127.0.0.1:5500", '127.0.0.1:5500/odds_scraping/frontend/index.html']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

iteration=0
bigx=[]
arbs = {'NHL':[], 'NBA':[], 'NFL':[]}

def convert_utc_to_est():
    utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    est = pytz.timezone('US/Eastern')
    est_time = utc_time.astimezone(est)
    return est_time



def odds_arb(odds1, odds2):

    #its arbitrage if the absolute value of the pisitive off is bigger than the negative odd, or theyre both positive
    if odds1[0] == '+' and odds2[0] == '+' and (int(odds1)!=int(odds2)): #if both odds are positive and not equal to eachother
        return True
    elif odds1[0] == '+' and (abs(int(odds1))>abs(int(odds2))): #if one odd is positive check to see if its absolute value is greater than the negative odd
            return True
    elif odds2[0] == '+' and (abs(int(odds2))>abs(int(odds1))):
            return True
    else:
        return False

def spread_arb(spread_count1, spread_odds1, spread_count2, spread_odds2):
     #the way spread arb works is 1) you need to check the spread total, make sure the absolute valu is the spread. Then compare the odds, can use moneyline_arb function for this
    #print(f'checking {spread_count1} at {spread_odds1} vs {spread_count2} at {spread_odds2}')
    if abs(float(spread_count1))!=abs(float(spread_count2)) or str(spread_count1)[0] == str(spread_count2)[0]: #check that the spread odds are equal and that the first charcters are also not eqial i.e both arent - and - or + and +
         return False
    elif odds_arb(spread_odds1, spread_odds2):#the spread total are equal and  opposite, now check the odds for arb
         return True
    return False



def total_arb(total_count11, total_odds1, total_count22, total_odds2):
    
    #need to check if the numbers of the total are the same and opposite, then can pass their odds to odds arb
    total_count1 = total_count11.strip('O').strip('U').strip('0').strip()
    total_count2 = total_count22.strip('O').strip('U').strip('0').strip()

    #print(f'checking {total_count1} at {total_odds1} vs {total_count2} at {total_odds2}')

    if abs(float(total_count1))!=abs(float(total_count2)): #if the over/under number is not equal, false
         return False
    elif odds_arb(total_odds1, total_odds2):
        return True
    return False


#this function works like this: a list with all the bets a sportsbook has is passed to the function for each sportsbook. Then we find which has the most entries b/c we use that as our base
#and compare each game to the ones in the base list b/c the base list will cover everything in the other books.

#problem: this function only compsres the longest list to every other book, but what about comparing the other books to one another? that never happens, need to fix big time
#def arbitrage(pb, mgm, br, dk, trip8, tb, ns, bt, sc, sport):
def arbitrage(pb, mgm, br, dk, trip8, tb, ns, bt, sc, sport):

    global arbs

    print(f'Checking {sport}...')
    print(f'pointsbet {sport}:{pb}')
    print(f'mgm {sport}:{mgm}')
    print(f'betrivers {sport}:{br}')
    print(f'draftkings {sport} :{dk}')
    print(f'trip8 {sport}:{trip8}')
    print(f'tonybet {sport}:{tb}')
    print(f'northstar {sport}:{ns}')
    print(f'betano {sport}:{bt}')
    print(f'score:{sc}')
    master = []
    master.append(pb)
    master.append(mgm)
    master.append(br)
    master.append(dk)
    master.append(trip8)
    master.append(tb)
    master.append(ns)
    master.append(bt)
    master.append(sc)

    arbs_list=[]

    time_updated = convert_utc_to_est().strftime('%I:%M %p %Z').lstrip('0')

    for i in range(len(master)-1): #goes through each indivudal list
        k=0
        
        bet = master[i] 
        while k < len(bet):
            current_bet = bet[k] 
            #print(f'Checking {current_bet["game"]} on {current_bet["book"]}')
            for j in range (i+1, len(master)): #loop through each entry in master
                p=0
                
                comp = master[j]
                while p < len(comp): #loop through each indivudal entry in book comp within master
                    bets = comp[p]
                    #print(f'Comparing {bets["game"]} on {bets["book"]}')
                    #here we say is team1=team1 and team2 = team 2, or is team 1 = team 2 and team 2 = team 1 i.e same game, but position on different sportsbooks was flipped
                    if  (bets['game'] == current_bet['game'] or (bets['team1'][0]['name'] == current_bet['team2'][0]['name'] and bets['team2'][0]['name'] == current_bet['team1'][0]['name'])) and bets['when'] == current_bet['when']: #if its the same teams on the same day
                        #print(f'Teams Matched')

                        team1 = current_bet["team1"][0]["name"]
                        team2 = bets["team2"][0]["name"]
                        

                        team11 = current_bet["team1"][0]["name"]
                        spread_count11 = current_bet["team1"][0]['spread'][0] #ALERT: need to check here, should this be current_bet or bets, check below as well!!!!
                        spread_odds11 = current_bet["team1"][0]['spread'][1]
                        total_count11 = current_bet["team1"][0]['total'][0]
                        total_odds11 = current_bet["team1"][0]['total'][1]
                        moneyline11 = current_bet["team1"][0]["moneyline"]
                        
                        book1 = current_bet["book"]
                        book2 = bets["book"]
                        
                        link1 = current_bet["link"]
                        link2 = bets["link"]

                        if team1!=team2:
                            #check team 2 on book 2
                            team22 = bets["team2"][0]["name"]
                            spread_count22 = bets["team2"][0]['spread'][0] 
                            spread_odds22 = bets["team2"][0]['spread'][1]
                            total_count22 = bets["team2"][0]['total'][0]
                            total_odds22 = bets["team2"][0]['total'][1]
                            moneyline22 = bets["team2"][0]["moneyline"]
                            
                        
                        elif team1==team2: #this also means that team 1 total is an over AND team 2 total is an over, so we dont wanna compare totals, but spread and moneyline we can/want to compare. I hard oded the total such that itll never be a possible option. This doesnt work when tonybet is book1, b/c then we never make our comparisons to other books. need to fix
                            #check team 1 on book 2
                            team22 = bets["team1"][0]["name"]
                            spread_count22 = bets["team1"][0]['spread'][0] 
                            spread_odds22 = bets["team1"][0]['spread'][1]
                            total_count22 = bets["team1"][0]['total'][0]
                            total_odds22 = bets["team1"][0]['total'][1]
                            moneyline22 = bets["team1"][0]["moneyline"]


                        #print(f'checking moneyline team1 {moneyline11} vs team2 {moneyline22}')
                        if odds_arb(moneyline11, moneyline22): #function to check if theres a moneyline arbitrage oppurtunity
                            print(f'{team11} on {book1} moneyline is {moneyline11} vs {team22} on {book2} moneyline is {moneyline22}')
                            #arbs_list.append(f'{team11} on {book1} moneyline is {moneyline11} vs {team22} on {book2} moneyline is {moneyline22}')
                            arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Moneyline', 
                                              'team1':[{'name':team11, 'book':book1.title(), 'odds':moneyline11, 'link':link1}],
                                              'team2':[{'name':team22, 'book':book2.title(), 'odds':moneyline22, 'link':link2}]})

                        
                        #print(f'checking spread {team11} {spread_count11} {spread_odds11} on {book1} vs {team22} {spread_count22} {spread_odds22} on {book2}')
                        if spread_arb(spread_count11, spread_odds11, spread_count22, spread_odds22): 
                            print(f'{team11} on {book1} spread is {spread_count11} at {spread_odds11} vs {team22} on {book2} spread is {spread_count22} at {spread_odds22}')
                            #arbs_list.append(f'{team11} on {book1} spread is {spread_count11} at {spread_odds11} vs {team22} on {book2} spread is {spread_count22} at {spread_odds22}')
                            arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Spread', 
                                              'team1':[{'name':team11, 'book':book1.title(), 'count':spread_count11, 'odds':spread_odds11, 'link':link1}],
                                              'team2':[{'name':team22, 'book':book2.title(), 'count':spread_count22, 'odds':spread_odds22, 'link':link2}]})


                        if total_count11[0]!=total_count22[0]:
                            #print(f'checking total {team11} {total_count11} {total_odds11} on {book1} vs {team22} {total_count22} {total_odds22} on {book2}')
                            if total_arb(total_count11, total_odds11, total_count22, total_odds22): 
                                print(f'{team11} on {book1} total is {total_count11} at {total_odds11} vs {team22} on {book2} total is {total_count22} at {total_odds22}')
                                #arbs_list.append(f'{team11} on {book1} total is {total_count11} at {total_odds11} vs {team22} on {book2} total is {total_count22} at {total_odds22}')
                                arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Total', 
                                              'team1':[{'name':team11, 'book':book1.title(), 'count':total_count11, 'odds':total_odds11, 'link':link1}],
                                              'team2':[{'name':team22, 'book':book2.title(), 'count':total_count22, 'odds':total_odds22, 'link':link2}]})

                        #now lets flip, check the other game on book1 and compare it to the other game on book2
                        team1 = current_bet["team2"][0]["name"]
                        team2 = bets["team1"][0]["name"]

                        team12 = current_bet["team2"][0]["name"]
                        spread_count12 = current_bet["team2"][0]['spread'][0]
                        spread_odds12 = current_bet["team2"][0]['spread'][1]
                        total_count12 = current_bet["team2"][0]['total'][0]
                        total_odds12 = current_bet["team2"][0]['total'][1]
                        moneyline12 = current_bet["team2"][0]["moneyline"]

                        if team1!=team2:
                            #check team 2 on book 2
                            team21 = bets["team1"][0]["name"]
                            spread_count21 = bets["team1"][0]['spread'][0] 
                            spread_odds21 = bets["team1"][0]['spread'][1]
                            total_count21 = bets["team1"][0]['total'][0]
                            total_odds21 = bets["team1"][0]['total'][1]
                            moneyline21 = bets["team1"][0]["moneyline"]

                        elif team1==team2:
                            #check team 2 on book 2
                            team21 = bets["team2"][0]["name"]
                            spread_count21 = bets["team2"][0]['spread'][0] 
                            spread_odds21 = bets["team2"][0]['spread'][1]
                            total_count21 = bets["team2"][0]['total'][0]
                            total_odds21 = bets["team2"][0]['total'][1]
                            moneyline21 = bets["team2"][0]["moneyline"]

                        #print(f'checking moneyline {team11} on {book1} {moneyline12} vs {team21} on {book2} {moneyline21}')
                        if odds_arb(moneyline12, moneyline21): 
                            print(f'{team12} on {book1} moneyline is {moneyline12} vs {team21} on {book2} moneyline is {moneyline21}')
                            #arbs_list.append(f'{team12} on {book1} moneyline is {moneyline12} vs {team21} on {book2} moneyline is {moneyline21}')
                            arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Moneyline', 
                                              'team1':[{'name':team12, 'book':book1.title(), 'odds':moneyline12, 'link':link1}],
                                              'team2':[{'name':team21, 'book':book2.title(), 'odds':moneyline21, 'link':link2}]})
  
                        #print(f'checking spread {team12} {spread_count12} {spread_odds12} on {book1} vs {team21} {spread_count21} {spread_odds21} on {book2}')
                        if spread_arb(spread_count12, spread_odds12, spread_count21, spread_odds21): #need to check if this works as expected
                            print(f'{team12} on {book1} spread is {spread_count12} at {spread_odds12} vs {team21} on {book2} spread is {spread_count21} at {spread_odds21}')
                            #arbs_list.append(f'{team12} on {book1} spread is {spread_count12} at {spread_odds12} vs {team21} on {book2} spread is {spread_count21} at {spread_odds21}')
                            arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Spread', 
                                              'team1':[{'name':team12, 'book':book1.title(), 'count':spread_count12, 'odds':spread_odds12, 'link':link1}],
                                              'team2':[{'name':team21, 'book':book2.title(), 'count':spread_count21, 'odds':spread_odds21, 'link':link2}]})

                        if total_count12[0]!=total_count21[0]:
                            #print(f'checking total {team12} {total_count12} {total_odds12} on {book1 } vs {team21} {total_count21} {total_odds21} on {book2}')
                            if total_arb(total_count12, total_odds12, total_count21, total_odds21): #need to check if this works as expected
                                print(f'{team12} on {book1} total is {total_count12} at {total_odds12} vs {team21} on {book2} total is {total_count21} at {total_odds21}')
                                #arbs_list.append(f'{team12} on {book1} total is {total_count12} at {total_odds12} vs {team21} on {book2} total is {total_count21} at {total_odds21}')
                                arbs_list.append({'sport':sport, 'time':time_updated, 'game':current_bet['game'], 'when':current_bet['when'], 'market':'Total', 
                                              'team1':[{'name':team12, 'book':book1.title(), 'count':total_count12, 'odds':total_odds12, 'link':link1}],
                                              'team2':[{'name':team21, 'book':book2.title(), 'count':total_count21, 'odds':total_odds21, 'link':link2}]})

                        break
                    
                    p+=1
            k+=1  

    # print('')
    # print(f'All bets for {sport} Checked')
    # print('')
    arbs[sport] = arbs_list
    return arbs_list


def running_arbs(chrome_options):
    #start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:

        #figure out ncaa problem, then try getting the arbitrage function to run concurrently, rn we scrape for ncaa, then rub the arb functiuon, then scrape next sport, but i want to scrape the next sport as the arb for the previous sport is running 
        # try:
        #     pb_ncaa = executor.submit(pointsbet, 'https://on.pointsbet.ca/sports/basketball/NCAA','NCAA')
        #     mgm_ncaa = executor.submit(betmgm, 'https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/ncaa-264','NCAA') 
        #     br_ncaa = executor.submit(betrivers, 'https://on.betrivers.ca/?page=sportsbook&group=1000093654&type=matches','NCAA')
        #     dk_ncaa = executor.submit(draftkings, 92483,'NCAA')
        #     trip8_ncaa = executor.submit(triple8, 'https://www.888sport.ca/basketball/ncca-odds/', 'NCAA')
        #     #b99_ncaa = executor.submit(bet99, 'https://on.bet99.ca/en/sports/basketball/usa/ncaab/277695')
        #     arbitrage(pb_ncaa.result(), mgm_ncaa.result(), br_ncaa.result(), dk_ncaa.result(), trip8_ncaa.result(), 'NCAA')
        # except Exception as e:
        #     print(e)
        #     pass

        try:
            pb_nhl = executor.submit(pointsbet, 'https://on.pointsbet.ca/sports/ice-hockey/NHL/', 'NHL', chrome_options)
            mgm_nhl = executor.submit(betmgm, 'https://sports.on.betmgm.ca/en/sports/hockey-12/betting/usa-9/nhl-34', 'NHL', chrome_options)
            br_nhl = executor.submit(betrivers, 'https://on.betrivers.ca/?page=sportsbook&group=1000093657&type=matches', 'NHL', chrome_options)
            dk_nhl = executor.submit(draftkings, 42133, 'NHL')
            trip8_nhl = executor.submit(triple8, 'https://www.888sport.ca/ice-hockey/nhl/', 'NHL', chrome_options)
            tb_nhl = executor.submit(tonybet, 'https://tonybet.ca/prematch/leagues/1013499-nhl', 'NHL', chrome_options)
            ns_nhl = executor.submit(northstar, 'https://www.northstarbets.ca/sportsbook#sports-hub/ice_hockey/nhl', 'NHL', chrome_options)
            bt_nhl = executor.submit(betano, 'https://www.betano.ca/sport/hockey/north-america/nhl/10118/', 'NHL', chrome_options)
            sc_nhl = executor.submit(score, 'https://thescore.bet/sport/hockey/organization/united-states/competition/nhl/featured-page', 'NHL', chrome_options)
            #b99_nhl = executor.submit(bet99, 'https://on.bet99.ca/en/sports/ice_hockey/usa/nhl/3201')
            #arbitrage(pb_nhl.result(), mgm_nhl.result(), br_nhl.result(), dk_nhl.result(), trip8_nhl.result(), tb_nhl.result(), ns_nhl.result(), bt_nhl.result(), 'NHL')

            #nhl arbs is a list of our nhl arbs when arbitrage function returns an arbs_list
            arbitrage(pb_nhl.result(), mgm_nhl.result(), br_nhl.result(), dk_nhl.result(), trip8_nhl.result(), tb_nhl.result(), ns_nhl.result(), bt_nhl.result(), sc_nhl.result(), 'NHL')  
            #nhl_arbs = arbitrage(pb_nhl.result(), mgm_nhl.result(), br_nhl.result(), dk_nhl.result(), trip8_nhl.result(), tb_nhl.result(), ns_nhl.result(), bt_nhl.result(), 'NHL')
            #arbitrage(pb_nhl.result(), mgm_nhl.result(), 'NHL')
        except Exception as e:
            print('ERRRROOORRRRRR')
            print(e)
            import traceback
            traceback.print_exc()


        #time.sleep(3)
        try:
            pb_nba = executor.submit(pointsbet, 'https://on.pointsbet.ca/sports/basketball/NBA', 'NBA', chrome_options)
            mgm_nba = executor.submit(betmgm, 'https://sports.on.betmgm.ca/en/sports/basketball-7/betting/usa-9/nba-6004', 'NBA', chrome_options)
            br_nba = executor.submit(betrivers, 'https://on.betrivers.ca/?page=sportsbook&group=1000093652&type=matches', 'NBA', chrome_options)
            dk_nba = executor.submit(draftkings, 42648, 'NBA')
            trip8_nba = executor.submit(triple8, 'https://www.888sport.ca/basketball/nba/', 'NBA', chrome_options)
            tb_nba = executor.submit(tonybet, 'https://tonybet.ca/prematch/leagues/1008918-nba', 'NBA', chrome_options)
            ns_nba = executor.submit(northstar, 'https://www.northstarbets.ca/sportsbook#sports-hub/basketball/nba', 'NBA', chrome_options)
            bt_nba = executor.submit(betano, 'https://www.betano.ca/sport/basketball/north-america/nba/441g/', 'NBA', chrome_options)
            sc_nba = executor.submit(score, 'https://thescore.bet/sport/basketball/organization/united-states/competition/nba', 'NBA', chrome_options)
        #     #b99_nba = executor.submit(bet99, 'https://on.bet99.ca/en/sports/basketball/usa/nba/3139')
        #     #arbitrage(pb_nba.result(), mgm_nba.result(), br_nba.result(), dk_nba.result(), trip8_nba.result(), tb_nba.result(), ns_nba.result(), bt_nba.result(), 'NBA')
            arbitrage(pb_nba.result(), mgm_nba.result(), br_nba.result(), dk_nba.result(), trip8_nba.result(), tb_nba.result(), ns_nba.result(), bt_nba.result(), sc_nba.result(),  'NBA')
        #     #nba_arbs=arbitrage(pb_nba.result(), mgm_nba.result(), 'NBA')

        except Exception as e:
            print(e)
            print('ERRRROOORRRRRR')


        
        # #time.sleep(3)

        try:
            pb_nfl = executor.submit(pointsbet, 'https://on.pointsbet.ca/sports/american-football/NFL', 'NFL', chrome_options)
            mgm_nfl = executor.submit(betmgm, 'https://sports.on.betmgm.ca/en/sports/football-11/betting/usa-9/nfl-35', 'NFL', chrome_options)
            br_nfl = executor.submit(betrivers, 'https://on.betrivers.ca/?page=sportsbook&group=1000093656&type=matches', 'NFL', chrome_options)
            dk_nfl = executor.submit(draftkings, 88808, 'NFL')
            trip8_nfl = executor.submit(triple8, 'https://www.888sport.ca/football/nfl/', 'NFL', chrome_options)
            tb_nfl = executor.submit(tonybet, 'https://tonybet.ca/prematch/leagues/1014465-nfl', 'NFL', chrome_options)
            ns_nfl = executor.submit(northstar, 'https://www.northstarbets.ca/sportsbook#sports-hub/american_football/nfl', 'NFL', chrome_options)
            bt_nfl = executor.submit(betano, 'https://www.betano.ca/sport/football/north-america/nfl/1611/', 'NFL', chrome_options)
            sc_nfl = executor.submit(score, 'https://thescore.bet/sport/football/organization/united-states/competition/nfl/featured-page', 'NFL', chrome_options)
        #     #b99_nfl = executor.submit(bet99, 'https://on.bet99.ca/en/sports/american_football/usa/nfl/683')
        #     #arbitrage(pb_nfl.result(), mgm_nfl.result(), br_nfl.result(), dk_nfl.result(), trip8_nfl.result(), tb_nfl.result(), ns_nfl.result(), bt_nfl.result(), 'NFL')
            arbitrage(pb_nfl.result(), mgm_nfl.result(), br_nfl.result(), dk_nfl.result(), trip8_nfl.result(), tb_nfl.result(), ns_nfl.result(), bt_nfl.result(), sc_nfl.result(), 'NFL')
        
        except Exception as e:
            print(e)
            print('ERRRROOORRRRRR')
       
    #nba_arbs = []
    #nfl_arbs=[]
    #total_arbs = [nhl_arbs, nba_arbs, nfl_arbs]
    end = time.time()
    #print(end-start)
    print(f'made it to the end') #to make surte our scrape went fine and the reason were seeing 3 empty lists is bc there arent any arbs
    #return total_arbs

@app.get("/")
def test():
    global arbs
    return(arbs)
    
def update_x():
    global iteration


    #define driver, pass to running_arbs
    path = '/Users/stefanoammaturo/Downloads/chromedriver-mac-x64/chromedriver'

    # Create a ChromeOptions object
    chrome_options = Options()
    chrome_options.binary_location = "/opt/render/.wdm/drivers/chromedriver"
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
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
        
        running_arbs(chrome_options) 
     
        iteration+=1
        time.sleep(10)

thread = threading.Thread(target=update_x)
thread.start()


#run uvicorn sites_scrape:app --reload to get backend url

#asgi error -> cd into odds_scraping
#if stuffs printing twice, youre likely calling infinite_scrape, not sites_scrape


#HERE
#mgm list not showing
#entries r coming in for mgm length 31, thats why its not showing on our output, find out why the lengths coming in like this when ran from here, when ran on its own its fine, this happens for nhl and nfl, nba its good for whatever reason



    