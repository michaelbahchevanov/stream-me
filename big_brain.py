import requests
import json
import pandas as pd
import time
import datetime
import os
import schedule

from dotenv import load_dotenv
load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

def get_timestamp():
    return datetime.datetime.now().strftime('%m%d%H%M')

def get_oauth_token(client_id = client_id, client_secret = client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    query_string = {'client_id': client_id, 
                    'client_secret': client_secret,
                    'grant_type': 'client_credentials'}
    r = requests.post(url, params=query_string).json()
    return r['access_token']

def get_top_100_categories(client_id = client_id):
  bearer_token = get_oauth_token()
  headers = {'Client-ID': client_id, 
              'Authorization': 'Bearer ' + bearer_token}
  url = r'https://api.twitch.tv/helix/games/top?first=100'
  r = requests.get(url, headers=headers)
  return r

def check_rate_limit_reached(req, ignore_limit = False):
    # checks if there is 1 request before rate limiting
    if int(req.headers['Ratelimit-Remaining']) <= 1:
        # not really preferred could cause trouble
        if ignore_limit:
            return int(req.headers['Ratelimit-Remaining'])
        print('Rate limit refreshes in 30s')
        time.sleep(30)
        print('Ready!')
    # return the remaining tries
    return int(req.headers['Ratelimit-Remaining'])

def get_top_100_streamers_for_each_game(games):
    streamers = {}
    
    bearer_token = get_oauth_token()
    headers = {'Client-ID': client_id, 
               'Authorization': 'Bearer ' + bearer_token}
    url = 'https://api.twitch.tv/helix/streams?first=100&game_id='
    
    for game in games['data']:
        req = requests.get(url + game['id'], headers=headers)
        check_rate_limit_reached(req)
        streamers[game['name']] = json.loads(req.text)
    return streamers

def json_to_df(json):
    total_streams_df = pd.DataFrame(
        columns = ['game_id','id','language','started_at','title','type','user_id','user_name','viewer_count'])
    for game_key in list(json.keys()):
        game_streams_df = pd.json_normalize(json[game_key]['data'])
        total_streams_df = pd.concat([total_streams_df, game_streams_df], sort = False)
    total_streams_df.drop(columns = ['thumbnail_url','tag_ids'], inplace = True)
    return total_streams_df

def save_df_to_csv(df):
    file_name = './data/top_live_streamers-{timestamp}.csv'.format(timestamp=get_timestamp())
    df.to_csv(file_name, index=False)
    return file_name

def run_all():
    top_100_games = get_top_100_categories().json()
    top_streamers = get_top_100_streamers_for_each_game(top_100_games)
    df = json_to_df(top_streamers)
    save_df_to_csv(df)

def main():
    schedule.every().hour.do(run_all)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == '__main__':
    main()