from datetime import datetime
from dotenv import load_dotenv
from json import dumps 
from requests import get
from time import strptime 
from os.path import isfile, join, dirname
from os import environ

dotenv_path = join(dirname(__file__), '.env')
if isfile(dotenv_path):
    load_dotenv(dotenv_path)

API_KEY = environ.get('API_KEY');
PLAYLIST_ID = environ.get('PLAYLIST_ID');

FILTER_BEFORE = datetime(2019, 1, 1)
DATA_PATH = 'data/videos.json'

def get_request_url(api_key, playlist_id, page_token=None):
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?key=%s&playlistId=%s&part=snippet,id&maxResults=50' % (api_key, playlist_id)
    if page_token:
        url += '&pageToken=%s' % page_token
    return url

def get_page(page_token=None):
    r = get(get_request_url(API_KEY, PLAYLIST_ID, page_token))
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(r.text)
        return r.json()

def get_videos():
    next_token = None
    videos = []
    while True:
        page = get_page(next_token)
        videos += page['items']
        if len(page['items']) > 0 and 'nextPageToken' in page:
            next_token = page['nextPageToken']
        else:
            break;
    return videos

def parse_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

def filter_videos(videos):
    return [v for v in videos if parse_timestamp(v['snippet']['publishedAt']) > FILTER_BEFORE]

def format_video(video):
    snippet = video['snippet']
    return {
        'thumbnail': snippet['thumbnails']['medium']['url'],
        'title': snippet['title'],
        'description': snippet['description'],
        'published': snippet['publishedAt'],
        'videoId': snippet['resourceId']['videoId']
    }

videos = [format_video(v) for v in filter_videos(get_videos())]
videos.sort(key=lambda v: parse_timestamp(v['published']), reverse=True)

with open(DATA_PATH, 'w') as f:
    f.write(dumps(videos))
