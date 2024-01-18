import csv
import os


def team_fixer(team, sport): 

    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Specify the relative path to the CSV file
    csv_file_path = os.path.join(script_directory, f'{sport}_names.csv')
    # with open(f'{sport}_names.csv', 'r') as file:
    with open(csv_file_path, 'r') as file:
        
        csv_content = file.read()

        reader = csv.DictReader(csv_content.splitlines())
        
        #loop through each row (each row is a dict where \ufeffSchool is the key to our possible names, 'nickname' is the key to our nickname which well set everything to)
        if sport == 'NCAA':
            for row in reader:
                #get the possible names the school could have
                x = row['\ufeffSchool'].split('/')
                team = team.strip().lower()
                #loop through each possible name and check
                for entry in x:
                    entry = entry.strip().lower()
                    
                    #team is what the book has posted, entry is a possible name from our csv
                    #if team is the same as the possible name, or if team is a subtring of the possible name
                    if team == entry or team in entry or team == row['Nickname'] or team in row['Full Name']:
                        #print(f'found {team} in {entry}')
                    
                        return row['Full Name']
        elif sport == 'NHL' or sport == 'NBA' or sport=='NFL':
            for row in reader:
                #team is what the book has posted, entry is a possible name from our csv
                if team in row['\ufeffFull Name'] or team in row['AbbName'] or team in row['AbbName2'] or team in row['AbbName3']:
                    return row['\ufeffFull Name']




# with open('NCAA_names.csv', 'r') as file:
#     csv_content = file.read()

#     reader = csv.DictReader(csv_content.splitlines())

#     for row in reader:
#         name = row['\ufeffSchool'].strip()
#         nickname = row['Nickname'].strip()
#         possible = name.split('/')
#         max_len = -1
#         for ele in possible: 
#             if(len(ele) > max_len): 
#                 max_len = len(ele) 
#                 res = ele 
#         print(res.strip(), nickname)

#honestly i think the move is to remove betrivers from the ncaa comparison completely and just go pb, mgm, draftkings
# so check dk for ncaa then move on to other sports, its time to finish this thing    
# #a thought: maybe we can make the full team name the "nickname" ciolumn, then can add a check to see if the book name is equal to the nickname, this would help with iuncluding betrivers and it also makes our output better cuz u see the full team name. Look into this   



#takes a list of words, this is the team name broken down to its indivudal words, checks if each word is in fullname 
# def name_fixer(names):
#     with open('NCAA_names.csv', 'r') as file:
#         csv_content = file.read()

#         reader = csv.DictReader(csv_content.splitlines())

#         i=0
#         names = names.split(' ')
#         #loop through each row (each row is a dict where \ufeffSchool is the key to our possible names, 'nickname' is the key to our nickname which well set everything to)
#         for row in reader:
#             name = row['Full Name']
#             for entry in names:
#                 if entry in name:
#                     print(entry)
#                     i+=1
#                     if i == len(names):
#                         return row['Full Name']
#                 #no match, reset i and go to the next team in csv
#                 else:
#                     i=0
#                     break
# print(name_fixer('x'))

# x = name_fixer('STL Blues')
# print(x)
# x = 'Santa Clara Broncos' 
# y = x.split(' ')
# print(y)
# print(name_fixer(y))


#READ HERE
#still some bugs with betrivers NCAA naming, itll just take time and testing diff teams on diff days to get all the names right, NHL is done, betrivers ncaa needs some fixing, next move onto nba and nfl, each day try ncaa betrivers and fix the name bugs that come up, eventually itll stop




#/Users/stefanoammaturo/hello_cs50/odds_scraping/csv_test.py
#/Users/stefanoammaturo/hello_cs50/odds_scraping/NHL_names.csv