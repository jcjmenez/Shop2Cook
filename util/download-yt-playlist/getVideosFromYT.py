import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

YT_API_KEY = str(os.getenv('YT_API_KEY'))

def getVideoUrls(qToSearch):
    urls = []
    youtube = build('youtube', 'v3', developerKey = YT_API_KEY)

    request = youtube.search().list(
        q = str(qToSearch),
        part = 'snippet',
        type = 'video',
        maxResults = 2
    )

    res = request.execute()

    for item in res['items']:
        urls.append({'url':'https://www.youtube.com/watch?v=' + item['id']['videoId'], 'title':item['snippet']['title']})
    
    return urls

