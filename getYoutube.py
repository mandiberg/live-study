from datetime import datetime
from dotenv import load_dotenv
from requests import get
from time import strptime
from os.path import isfile, join, dirname
from os import environ

dotenv_path = join(dirname(__file__), '.env')
if isfile(dotenv_path):
    load_dotenv(dotenv_path)

API_KEY = environ.get('API_KEY');
CHANNEL_ID = environ.get('CHANNEL_ID');

FILTER_BEFORE = datetime(2019, 1, 1)

def get_request_url(api_key, channel_id, page_token=None):
    url = 'https://www.googleapis.com/youtube/v3/search?key=%s&channelId=%s&part=snippet,id&maxResults=50&order=date' % (api_key, channel_id)
    if page_token:
        url += '&pageToken=%s' % page_token
    return url

def get_page(page_token=None):
    r = get(get_request_url(API_KEY, CHANNEL_ID, page_token))
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
        if 'nextPageToken' in page:
            next_token = page['nextPageToken']
        else:
            break;
    return videos

def filter_videos(videos):
    return [v for v in videos if datetime.strptime(v['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ') > FILTER_BEFORE]

def format_video(video):
    return {
        'thumbnail': video['snippet']['thumbnails']['medium']['url'],
        'title': video['snippet']['title'],
        'description': video['snippet']['description'],
        'published': video['snippet']['publishedAt'],
        'videoId': video['id']['videoId']
    }

videos = [format_video(v) for v in filter_videos(get_videos())]
print(videos)
