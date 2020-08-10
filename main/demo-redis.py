import redis
import requests
import json
import time
import os
# https: // www.tutorialspoint.com/redis/redis_lists.htm
client = redis.Redis(host="10.10.10.1",port=6379,password=os.getenv("REDIS_PASS"))
# client.set('last_seen_id', '1285216167456575488')
# print(client.get('last_seen_id'))
# print(client.get('ky_since_id'))
# client = redis.Redis(
#     host="127.0.0.1", password="Il53ZtiQsIkQ4IZ9eEGtzPV91uR9QqlQHhm")
# client.hset('daily_status', 'cosmo', 'Fri Jul 3 the market is closed today.')
# print(client.hgetall('intercept'))
# client.hset('daily_status', 'falcon', 'We are +5%')
# pl = 7
# client.set('eagle_ran', 'True')
# if client.get('eagle_ran').decode("utf-8")=='True':
#     print("We did run the program on Monday.")
# client.set('highest_sentiment', '100')

# open_orders = []
# client.srem('followers_thanked', '441228378')
# print(client.smembers('followers_thanked'))
# ordered = []
# tqqq = 'TQQQ'
# tmf = 'TMF'
# edz = 'EDZ'
# dict = client.hgetall('intercept')
# print(dict)
# new_lev = 0
# for key, value in dict.items():
#     if key.decode("utf-8") == tqqq and key.decode("utf-8") not in open_orders and key.decode("utf-8") not in ordered:
#         print(f"Let's order {key} with a weight of {value}")
#         value = float(value)*float(os.getenv("LEV"))
#         print(value)
#         new_lev += value
#     elif key.decode("utf-8") == tmf and key.decode("utf-8") not in open_orders and key.decode("utf-8") not in ordered:
#         print(f"Let's order {key} with a weight of {value}")
#         value = float(value)*float(os.getenv("LEV"))
#         print(value)
#         new_lev += value
#     elif key.decode("utf-8") == edz and key.decode("utf-8") not in open_orders and key.decode("utf-8") not in ordered:
#         print(f"Let's order {key} with a weight of {value}")
#         value = float(value)*float(os.getenv("LEV"))
#         print(value)
#         new_lev += value
# print(new_lev)

''' Uptrend prospects set
'''
# client.delete('new_prospects')
# client.sadd('new_prospects', 'W', 'DVAX', 'CWH', 'CVNA', 'BJ')
# print(client.smembers('new_prospects'))



# print(client.get('ran').decode("utf-8"))
# client.hset('daily_status', 'eagle', 'We are -0.05%')
# sentiment = 1273420010577432576
# client.set('last_seen', sentiment)
# print(client.get('last_seen'))
# sentiment = int(client.get('last_seen_id'))
# status = "Today the Tendie Intern is {} the market.".format(sentiment)
# print(sentiment)
# client.delete('CWH')
# client.delete('W')
# client.delete('NLOK')
# client.delete('BJ')
# client.delete('EVER')
# client.sadd('followers_thanked', 'CalendarKy')
# print(list(client.smembers('followers_thanked')))
# for item in list(client.smembers('followers_thanked')):
#     print(item.decode("utf-8"))
# print(client.hgetall('intercept'))
# print(client.get('testing'))

# client.set('highest_sentiment', '30')
# client.set('lowest_sentiment', '-1')

# sentiment = 52
# to_string = "Twitter sentiment of the stock market is bullish with a reading of {}.".format(
#             sentiment)
# if sentiment > 10:
#     print("bullish")
#     current_high = int(client.get('highest_sentiment'))
#     if sentiment > current_high:
#         client.set('highest_sentiment', str(sentiment))
#         to_string = "{} This is the highest reading to date.".format(to_string)
# print(to_string)
# print(client.smembers('new_prospects'))
# client.delete('new_prospects')
# client.sadd('new_prospects', 'PZZA', 'W', 'CWH', 'EVER', 'BJ')
# print(client.smembers('new_prospects'))

# client.sadd('new_prospects', "NLOK", "W", "CWH", "EVER", "BJ")
# print("Never held YZZ before")
# client.sadd('testing_time', "YZZ", "XYZ")
# client.sadd('testing_time', "MSFT")
# print(client.smembers('testing_time'))
# client.delete('testing_time')
# prospects = list(client.smembers('new_prospects'))
# # print(str(prospects))
# tqqq = "TQQQ"
# tmf = "TMF"
# edz = "EDZ"
# q_wt = 0.52
# t_wt = 0.25
# e_wt = 0.23
# liststock = ['FB','F', 'TSLA', 'AAPL']
# print(client.hgetall('NLOK'))


# client.sadd('testing_now', 'FB')
# client.sadd('testing_now', 'F')
# client.sadd('testing_now', 'TSLA')
# client.sadd('testing_now', 'AAPL')


# stock_list = client.smembers('testing_now')

# for stock in stock_list:
#     if stock.decode("utf-8") in liststock:
#         liststock.remove(stock.decode("utf-8"))
# print(liststock)
# today = str(time.ctime())[:-14]
# today = today[:-14]
# print(today)

# print(list(client.smembers('new_prospects')))
# story = "So the other day, when I was bored\nello there."
# print(story)

# client.hset('working', 'String', story)

# new_story = str(client.hget('working', 'String').decode("utf-8"))
# print(new_story)


# tqqq = "TQQQ"
# tmf = "TMF"
# edz = "EDZ"
# client.hset('intercept', tqqq, q_wt)
# client.hset('intercept', tmf, t_wt)
# client.hset('intercept', edz, e_wt)

# val = client.hgetall('intercept')

# for key, value in val.items():
#     print(key)
#     if str(key) == tqqq:
#         print(int(float(value)*100))
#     elif str(key) > tmf:
#         print(int(float(value)*100))
#     elif str(key) == edz:
#         print(int(float(value)*100))

'''
Fantasy Football ish
'''

# league = "446776881077809152"

# BASE_URL = "https://api.sleeper.app"

# SPECIFIC_LEAGUE = f"{BASE_URL}/v1/league/{league}"

# LEAGUE_ROSTERS = f"{BASE_URL}/v1/league/{league}/rosters"

# ROSTER = f"{BASE_URL}/v1/league/{league}/rosters"

# USER_IN_LEAGUE = f"{BASE_URL}/v1/league/{league}/users"

# def get_user_in_league():
#     r = requests.get(USER_IN_LEAGUE)
#     return json.loads(r.content)


# def get_league_rosters():
#     r = requests.get(LEAGUE_ROSTERS)
#     return json.loads(r.content)


# def get_owner_id(roster_id):
#     roster_id = roster_id[7:]
#     print(f"roster_id is {roster_id}")
#     rosters = get_league_rosters()
    
#     flag = False
#     for roster in rosters:
#         for key, value in roster.items():
#             if key == 'roster_id':
#                 print(value)
#                 if int(value) == int(roster_id):
#                     flag = True
#                     print("Flag is hit")
#             if flag == True and key == 'owner_id':
#                 print('owner id is hit')
#                 return value


# def set_user_list():
#     users = get_user_in_league()
#     users_list = []
#     for user in users:
#         # print(user)
#         for key, value in user.items():
#             if key == 'user_id':
#                 users_list.append(value)
#     # print(users_list)
#     return users_list


# def get_team_name(id):
#     team_name = "unknown"
#     flag = False
#     users = get_user_in_league()
#     for user in users:
#         for key, value in user.items():
#             if key == 'user_id':
#                 if value == id:
#                     flag = True
#             elif flag == True and key == 'metadata':
                
#                 for name, val in value.items():
#                     if name == 'team_name':
#                         return val
#     return team_name  # If we get here just return the unknown team name

# def tweet_scores():
#     client.hset('roster_2', 'points', '120')
#     client.hset('roster_11', 'points', '140')
#     client.sadd('matchup_1', 'roster_2', 'roster_11')
#     members = client.smembers('matchup_1')
#     tweet = ""
#     i = 0
#     for member in members:
#         i += 1
#         id = get_owner_id(member.decode("utf-8"))
#         print(id)
#         team_name = get_team_name(id)
#         print(team_name)
#         points = client.hget(member, 'points').decode("utf-8")
#         if i % 2 != 0:
#             tweet = team_name + " " + points + " - "
#         else:
#             tweet = tweet + team_name + " " + points
#     print(tweet)


# def set_standings():
#     wins = "wins"
#     # I think I want to use a dictionary here with the user and their wins
#     standings_dict = {}
#     most_wins = 0
#     for user in USERS_LIST:
#         wins = client.hget(str(user), 'wins')
#         if wins:
#             standings_dict[user] = int(wins)
#             if int(wins) > most_wins:
#                 most_wins = int(wins)
#                 leaders = 1
#             elif int(wins) == most_wins:
#                 most_wins = int(wins)
#                 leaders += 1
    # Now that I have a dictionary with each user: wins ,,, let's order the dictionary
    # standings_dict = {k: v for k, v in sorted(
    #     standings_dict.items(), key=lambda item: item[1])}

    # Let's check if there are multiple teams with same number of wins
    # leaders = 0
    # for key, value in standings_dict.items():
    #     if value == most_wins:
    #         leaders += 1
#     i = 0
#     for key, value in standings_dict.items():
#         get_team_name(key)
#         i += 1
#         if i <= leaders and leaders == 1:
#             status = f"{key} is in solo 1st with {value} wins."
#         elif i <= leaders and leaders > 1:
#             status = f"{key} is tied for 1st place with {value} wins."
#         elif (i - 2) % 10 == 0:
#             status = f"{key} is in 2nd place with {value} wins."
#         elif (i - 3) % 10 == 0:
#             status = f"{key} is in {i}rd place with {value} wins."
#         else:
#             status = f"{key} is in {i}th place with {value} wins."
#         print(status)

# def set_wins():
#     rosters = get_league_rosters()
   
#     for user in USERS_LIST:
#         wins = 0
#         for roster in rosters:
#             for key, value in roster.items():
#                 if key == "settings":
#                     for name, val in value.items():
#                         if name == "wins":
#                             wins = val
#                 elif key == "owner_id" and value == user:
#                     client.hset(user, 'wins', wins)


# USERS_LIST = set_user_list()

# set_standings()


# test = "test"
# num = 2000

# client.hset("test_time", test, str(num))
# client.hset ('test_time', 'points', '3000')
# print(client.hgetall('test_time'))
# client.hdel('test_time', test)
# print(client.hgetall('test_time'))




# for i in range(len(prospects)):
#     print(prospects[i])
# prospects = client.scard('prospects')
# print(prospects)
# if val:
#     for key, value in val.items():
#         print(key)
#         new_key = float(key) + pl
#         print(value)
#         new_val = float(value) + 1
#         client.hdel(stock, key)
#     print(
#         f"We've held {stock} for {new_val} weeks now with total p/l of {new_key}")
#     client.hset(stock, str(new_key), str(new_val))
#     print(client.hgetall(stock))
# client.hdel('YZ', '16.0')
# print(client.hgetall('YZ'))
# msft = client.hget('Testing', 'MSFT')
# amzn = client.hget('Testing', 'AMZN')
# if amzn is not None:
#     new_pl = float(amzn)
#     new_pl += pl
#     client.hset('Testing', 'AMZN', str(new_pl))
#     print(client.hget('Testing', 'AMZN'))
# else:
#     print("Amazon hasn't been owned yet.")
#     client.hset('Testing', 'AMZN', str(pl))
#     print(client.hget('Testing', 'MSFT'))
# if msft is not None:
#     new_pl = float(msft)
#     new_pl += pl
#     client.hset('Testing', 'MSFT', str(new_pl))
#     print(client.hget('Testing', 'MSFT'))
# else:
#     print(e)
#     print("Amazon hasn't been owned yet.")
# performance = 3.1415
# perc = "%"
# if performance > 0:
#         perf_to_string = "We are +{}{} for the day :)".format(performance, perc)

# print(perf_to_string)
### demo the strings ###
# 
# client.set('language', 'Python')

# print(client.get('language'))

# client.set('language', 'Python', px=10000)
# print(client.get('language'))
# print(client.ttl('language'))
# time.sleep(3)
# print(client.ttl('language'))

# client.set('language', 'Python', px=10000)
# print(client.expire('language', 10))
# print(client.ttl('language'))
# time.sleep(3)
# print(client.ttl('language'))

#####           ####

#### Demo the sets ####

# client.sadd('pythonlist', "value1", "value2", "value3", "value4")
# client.sadd('powerlist', "value1", "value5", "value6", "value7")

# #intercept of the two sets
# print(client.sinter('pythonlist', 'powerlist'))
# print(client.sunion('pythonlist', 'powerslist'))
# print(client.scard('pythonlist'))
# print(client.scard('powerlist'))


#####

#### demo the hashes

# client.hset('Hero', 'Name', 'Drow Ranger')
# client.hset('Hero', 'Health', '600')
# client.hset('Hero', 'Mana', '200')

# print(client.hgetall('Hero'))

# Hero = {
#     Name: Drow,
#     Health: 600,
#     Mana: 200
# }
