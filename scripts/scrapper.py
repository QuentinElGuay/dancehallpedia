
import re
import requests

from bs4 import BeautifulSoup
from googleapiclient.discovery import build

from scripts import setup
setup()
from pages.models import Artist, Step, Video, StepAppearance

url = 'http://www.gangalee.net/dancehall_kroki.php?page='
REGEX_URL = r'^http:\/\/(?:www.)?youtube.com\/v\/(.*)\?.*&(?:start=(\d+)|.+)?$'


def get_youtube_video_title(video_id):
    service = build('youtube', 'v3', developerKey='AIzaSyA1C8wnXvLAUUSlzPe9LT9PDQpzc9LxaV8')
    api_result = service.videos().list(part='snippet', id=video_id).execute()

    if len(api_result.get('items')) == 0:
        return None

    return api_result.get('items')[0].get('snippet').get('title')


def scrap_videos(video_container):
    category = video_container.find(class_='mv_vids_head').get_text().strip()
    print(category)

    videos = video_container.find_all('a')
    for video in videos:
        video_title = video.get_text().strip()

        if video_title.startswith('show all videos'):
            continue

        video_original_url = video['href']
        video_timing = 0

        search_result = re.search(REGEX_URL, video_original_url)

        if search_result:
            video_url = f'https://www.youtube.com/watch?v={search_result.group(1).strip()}'
            if search_result.group(2):
                video_timing = int(search_result.group(2))

            # Call Youtube API to check if video exists and update title
            video_title = get_youtube_video_title(search_result.group(1).strip())

            if video_title:
                print(f'{video_title}: {video_url}&t={video_timing}')
            else:
                print(f'[Invalid URL] {video.get_text().strip()}')

        else:
            print(f'{video_title}: Unable to convert URL {video_original_url}')


def scrap_move(move):
    step_name = move.find('h2').get_text().title()

    creator = None
    creator_name = None

    creator_container = move.find(class_='crb')
    if creator_container is not None:
        creator_link = creator_container.find('a')
        if creator_link is not None:
            creator_name = creator_link.get_text()
        else:
            creator_name = creator_container.get_text()[12:]

    import pdb; pdb.set_trace()
    if creator_name is not None:
        artist = Artist.objects.filter(name__iexact=creator_name)
        if not artist.exists():
            creator = Artist(name=creator_name)
        else:
            creator = artist.first()
        print(f'{step_name} by {creator.name }')

    video_containers = move.find_all(class_='vids')
    for video_container in video_containers:
        scrap_videos(video_container)

    print('\n')


def scrap_page(url, index):
    page = requests.get(url+str(index))
    soup = BeautifulSoup(page.content, 'html.parser')

    moves_container = soup.find(id='m_list')
    moves_list = moves_container.find_all(class_='m')

    for move in moves_list:
        scrap_move(move)



