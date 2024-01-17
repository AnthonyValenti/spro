#PLEASE NOTE: if you find theres an error with this function/file, its possible that the api has been updated and its no longer the same version that you coded this file on. Will need to fix your calls



import requests
import json
from datetime import datetime, date, time, timezone, timedelta
import pytz
from csv_test import team_fixer




#function to return a list of games and whether or not theyre on today or tomorrow, anu other game date is omitted
def get_date(path, league):
    checker_list=[]
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    
    for entry in path:
        day, clock = entry['startDate'].split('T')

        clock = clock.split('.')[0]

        year,month,da_y = day.split('-')
        hour, minute, second = clock.split(':')

        year = int(year)
        month = int(month)
        da_y = int(da_y)

        hour = int(hour)
        minute = int(minute)
        second = int(second)

        #when the games on in est
        actual = datetime(year,month,da_y,hour, minute, second, tzinfo=utc).astimezone(est).strftime(fmt).split(' ')[0]

        today = datetime.today().strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')

        tomorrow = str(today + timedelta(days=1)).split(' ')[0]
        today = str(today).split(' ')[0]

        x1, x2 = entry['name'].split('@')
        x1 = x1.strip()
        #print(f'before:{x1}')
        team1 = team_fixer(x1, league)
        #print(f'after:{team1}')

        x2 = x2.strip()
        #print(f'before:{x2}')
        team2 = team_fixer(x2, league)
        #print(f'after:{team2}')
    
        #print(actual)
        if actual == today:
            checker_list.append({'game': f"{team1} vs {team2}" , 'when': 'Today'})
        elif actual == tomorrow:
            checker_list.append({'game': f"{team1} vs {team2}" , 'when': 'Tomorrow'})
        else:
            pass
        #print(checker_list)
    return checker_list



def draftkings(sport, league):
    print(f'draftkings {league}')
    x = requests.get(f'https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/{sport}?format=json').json()
    y = x['eventGroup']['offerCategories'][0]["offerSubcategoryDescriptors"][0]["offerSubcategory"]['offers']
    lines_list=[]

    for entry in y:#loops through each game
        holding_dict={}

        #get the team names for this respective game
        x1 = entry[0]['outcomes'][0]['participant']
        #print(x1)
        team1 = team_fixer(x1, league)
       
        x2 = entry[0]['outcomes'][1]['participant']
        #print(x2)
        team2 = team_fixer(x2, league)
        
        

        holding_dict['game'] = f"{team1} vs {team2}"    #holding_dict = {'game':team1 vs team2, 'book':draftkings, 'when':'', team1:[], team2:[]}
        holding_dict['book'] = 'draftkings'
        holding_dict['when'] = '' #to be updated
        

        team1_dict = {}
        team1_dict['name'] = team1

        team2_dict = {}
        team2_dict['name'] = team2

        #loops through each bet
        for game in entry:

        #big try and except because not all lines are there all the time
            try:

                line = game['label'] #spread, total, moneyline
                z = game['outcomes'] #to help index
                #print(line)
                
                #team 1 is always over for total

                #try & except b/c moneyline doesnt have a line i.e a number it has to be over or under whereas spread/total do
                try:
                    num1 = z[0]['line'] #over/under what
                    num2 = z[1]['line'] #over/under what?
                    
                except:
                    pass

                odds1 = z[0]['oddsAmerican']
                

                #team 2 is always under for total

                odds2 = z[1]['oddsAmerican']
                

                if league == 'NCAA' or league == 'NBA' or league == 'NFL' or (league == 'NHL' and (line == 'Puck Line' or line == 'Total' or line=='Moneyline')):

                    if line == 'Total':
                        #print(f"{team1} {line} O {num1} {odds1} vs {team2} {line} U {num2} {odds2}")
                        team1_dict['total'] = [f"O {num1}", odds1]
                        team2_dict['total'] = [f"U {num2}", odds2]

                    elif line == 'Moneyline':
                        #print(f"{team1} {line} {odds1} vs {team2} {line} {odds2}")
                        team1_dict['moneyline'] = odds1
                        team2_dict['moneyline'] = odds2

                    else:
                        #print(f"{team1} {line} {num1} {odds1} vs {team2} {line} {num2} {odds2}")
                        team1_dict['spread'] = [num1, odds1]
                        team2_dict['spread'] = [num2, odds2]
                
                elif league == 'NHL':
                    if line == 'Total FT (Incl OT)' or line == 'Total Live Betting (Incl OT)':
                        #print(f"{team1} {line} O {num1} {odds1} vs {team2} {line} U {num2} {odds2}")
                        team1_dict['total'] = [f"O {num1}", odds1]
                        team2_dict['total'] = [f"U {num2}", odds2]

                    elif line == 'Moneyline FT (Incl OT)' or line == 'Moneyline Live Betting (Incl OT)':
                        #print(f"{team1} {line} {odds1} vs {team2} {line} {odds2}")
                        team1_dict['moneyline'] = odds1
                        team2_dict['moneyline'] = odds2

                    else:
                        #print(f"{team1} {line} {num1} {odds1} vs {team2} {line} {num2} {odds2}")
                        team1_dict['spread'] = [num1, odds1]
                        team2_dict['spread'] = [num2, odds2]
                
                
            except:
                pass
        holding_dict['team1'] = [team1_dict]
        holding_dict['team2'] = [team2_dict]
        

        
        if league == 'NHL':
            holding_dict['link'] = 'https://sportsbook.draftkings.com/leagues/hockey/nhl'

        elif league == 'NBA':
            holding_dict['link'] = 'https://sportsbook.draftkings.com/leagues/basketball/nba'

        elif league == 'NFL':
            holding_dict['link'] =' https://sportsbook.draftkings.com/leagues/football/nfl'

        #print(holding_dict)
       
        lines_list.append(holding_dict)    
    #print(lines_list)
    dates = get_date(x['eventGroup']['events'], league) #returns a list holding each games name and their respective date
    final = []
    for entry in lines_list:
        #print(entry)
        for game in dates:
            #print(game) 
            if entry['game'] == game['game'] and len(entry['team1'][0]) == 4:
                #print(entry)
                entry['when'] = game['when']
                final.append(entry)
                #print(final)   
                break
    
    return final       



#nba = 42648
#nhl = 42133
#nfl = 88808
#mlb = 84240
#ncaa = 92483

#to get any sport id, us this xpath when you inspect the page: //div[contains(@class, 'sportsbook-category-tab-inner')] and scroll over to find the id - for draftkings only

# draftkings(42133, 'NHL')
# print('NHL')
# print(draftkings(42133)) #nhl odds
# print('')


# print('NBA')
# print(draftkings(42648)) #nba odds
# print('')

# print('NFL')
# print(draftkings(88808)) #nfl odds
# print('')

# print('NCAA')
# print(draftkings(92483)) #NCAA basketball odds

# x = draftkings(92483, 'NCAA')
# for entry in x:
#     print(entry)

# x = draftkings(42133, 'NHL')
# for entry in x:
#     print(entry)

# x = draftkings(42648, 'NBA')
# for entry in x:
#     print(entry)

# x = draftkings(88808, 'NFL')
# for entry in x:
#     print(entry)


#nhl nba ncaa nfl done
#print(draftkings(92483, 'NCAA'))

#nhl: 'https://sportsbook.draftkings.com/leagues/hockey/nhl'
#nba: 'https://sportsbook.draftkings.com/leagues/basketball/nba'
#nfl:  'https://sportsbook.draftkings.com/leagues/football/nfl'





