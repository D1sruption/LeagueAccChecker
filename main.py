import json
import math

import requests.exceptions
from riotwatcher import LolWatcher, ApiError
import pandas as pd

API_KEY = "RGAPI-dfca7f46-d0fd-4e22-b18a-8dc96a15289b"

watcher = LolWatcher(API_KEY)

# data = pd.read_excel("accounts.xlsx")
#
# df1 = pd.DataFrame(data)
# print(df1)
#
# invalid_list = []
# account_list = []
#
# for index, row in df1.iterrows():
#     username = row[0]
#     password = row[1]
#     name = row[2]
#     region = row[3]
#
#     if region == "N-A":
#         region = "na1"
#     elif region == "KR" or region == "LAN" or region == "EUW" or math.isnan(name):
#         continue
#
#     print(username, password, name, region)
#
#     try:
#         test = watcher.summoner.by_name(region, name)
#         print(test)
#         account_list.append([test['id'], test['accountId'], test['puuid'], test['name'], test['summonerLevel']])
#
#     except requests.exceptions.HTTPError as e:
#         print("Invalid summoner found! Continuing...")
#         invalid_list.append(name)
#
# print(f"Invalid List: {invalid_list}")
# print(f"Account List: {account_list}")
#
# df_invalid = pd.DataFrame(invalid_list)
# df_accounts = pd.DataFrame(account_list, columns=["ID", "ACCOUNT_ID", "PUUID", "NAME", "LEVEL"])
#
# df_invalid.to_excel("invalid.xlsx")
# df_accounts.to_excel("account_list.xlsx")

data_accounts = pd.read_excel("account_list.xlsx")
df_accounts = pd.DataFrame(data_accounts)

account_stats = []

for index, row in df_accounts.iterrows():
    id = row[0]
    account_id = row[1]
    puuid = row[2]
    name = row[3]
    level = row[4]

    # set defaults
    tier = 'Unranked'
    rank = ''
    lp = 0
    wins = 0
    losses = 0
    veteran = False
    inactive = True
    freshblood = False
    hotStreak = False


    print(id, account_id, puuid, name, level)
    stats = watcher.league.by_summoner("na1", id)

    if len(stats) > 0:
        tier = stats[0]['tier']
        rank = stats[0]['rank']
        lp = stats[0]['leaguePoints']
        wins = stats[0]['wins']
        losses = stats[0]['losses']
        veteran = stats[0]['veteran'] # player has played more than 100 games in current division
        inactive = stats[0]['inactive'] # no longer actively plays
        freshblood = stats[0]['freshBlood'] # is new to the division
        hotStreak = stats[0]['hotStreak'] # Winning streak of 3 or higher

        # print(tier, rank, lp, wins, losses, veteran, inactive, freshblood, hotStreak)
        account_stats.append([name, tier, rank, lp, wins, losses, veteran, inactive, freshblood, hotStreak])
    else:
        account_stats.append([name, tier, rank, lp, wins, losses, veteran, inactive, freshblood, hotStreak])

df_account_stats = pd.DataFrame(account_stats, columns=["NAME", "TIER", "RANK", "LP", "WINS", "LOSSES", "VETERAN", "INACTIVE", "FRESHBLOOD", "HOTSTREAK"])
df_account_stats.to_excel("stats.xlsx")