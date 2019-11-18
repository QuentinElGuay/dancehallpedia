
import re
import sys

import requests
import urllib.parse

from bs4 import BeautifulSoup

from common.video import get_youtube_video_data

SOURCE_URL = 'http://www.gangalee.net/dancehall_kroki.php?page='
REGEX_URL = r'^http:\/\/(?:www.)?youtube.com\/v\/(.*)\?.*&(?:start=(\d+)|.+)?$'

artists = {}
videos = {}


def get_create_video(video_data):
    url = video_data['url']

    response = requests.get(f'http://127.0.0.1:8000/dance/api/video/?url__iexact={url}')

    if response.status_code == 200:
        response_json = response.json()
        if response_json['count'] == 1:
            return {'id': response_json['results'][0]['pk']}
        elif response_json['count'] == 0:
            response = requests.post('http://127.0.0.1:8000/dance/api/video/', data=video_data)
            if response.status_code == 201:
                response_json = response.json()
                return {'id': response_json['pk']}
                print('Added video {}'.format(video_data['title']))
            else:
                raise Exception('Unable to create video {}: {}.'.format(url, response.text))
        else:
            raise Exception('An error occurred: {}.'.format(response.text))
    else:
        raise Exception('An error occurred: {}.'.format(response.text))


def create_step_appearance(video_id, step_id, time):
    response = requests.post('http://127.0.0.1:8000/dance/api/stepAppearance/', data={
        'video': video_id,
        'step': step_id,
        'time': time,
    })
    response.raise_for_status()
    print(f'Added an appearance for step {step_id} and video {video_id}.')


def get_step_appearances(video_id, step_id, time):
    response = requests.get(f'http://127.0.0.1:8000/dance/api/stepAppearance/?step={step_id}&video={video_id}&time={time}')

    if response.status_code == 200:
        response_json = response.json()
        if response_json['count'] > 0:
            return [sa['pk'] for sa in response_json["results"]]


def scrap_videos(video_container, step_id):
    category = video_container.find(class_='mv_vids_head').get_text().strip()
    video_links = video_container.find_all('a')
    for video in video_links:
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

            if video_url not in videos:
                # Call Youtube API to check if video exists and update title
                video_data = get_youtube_video_data(search_result.group(1).strip())
                if not video_data:
                    video_data = {
                        'url': video_url,
                        'title': video_title,
                        'channel': 'Unknown',
                        'channel_url': 'https://www.youtube.com',
                        'valid': False,
                    }

                video_data['url'] = video_url
                video_data['host'] = 1
                video_data['type'] = category

                videos[video_url] = get_create_video(video_data)

            video_id = videos[video_url]['id']

            appearances = get_step_appearances(video_id, step_id, video_timing)
            if not appearances:
                create_step_appearance(video_id, step_id, video_timing)

        else:
            print(f'{video_title}: Unable to convert URL {video_original_url}')


def get_create_artist(creator_name):
    response = requests.get(f'http://127.0.0.1:8000/dance/api/artist/?name__iexact={creator_name}')

    if response.status_code == 200:
        response_json = response.json()
        if response_json['count'] == 1:
            return {'id': response_json['results'][0]['pk']}
        elif response_json['count'] == 0:
            response = requests.post('http://127.0.0.1:8000/dance/api/artist/', data={'name': creator_name})
            if response.status_code == 201:
                response_json = response.json()
                return {'id': response_json['pk']}
                print('Added artist {}'.format(creator_name))
            else:
                raise Exception('Unable to create artist {}: {}.'.format(creator_name, response.text))
        else:
            raise Exception('Too many compatible artists: {}.'.format(creator_name))
    else:
        raise Exception('An error occurred: {}.'.format(response.text))


def scrap_creator(creator_container):
    creator_name = None
    if creator_container is not None:
        creator_link = creator_container.find('a')
        if creator_link is not None:
            creator_name = creator_link.get_text()
        else:
            creator_name = creator_container.get_text()[12:]

    if creator_name is None:
        return 'Unknown', None

    if creator_name not in artists:
        artists[creator_name] = get_create_artist(creator_name)

    return creator_name, artists[creator_name]


def create_step(name, creator_id, school):
    if not creator_id:
        creator_id = ''

    try:
        response = requests.post('http://127.0.0.1:8000/dance/api/step/', data={
            'name': name,
            'creator': creator_id,
            'school': school,
        })
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        import pdb; pdb.set_trace()
        print(err)
        sys.exit(1)

    if response.status_code == 201:
        print(f'Created step {name} by creator {creator_id}.')
        response_json = response.json()
        return response_json['pk']


def get_step(name):
    response = requests.get(f'http://127.0.0.1:8000/dance/api/step/?name__icontains={urllib.parse.quote(name)}')

    if response.status_code == 200:
        response_json = response.json()
        if response_json['count'] == 1:
            return response_json["results"][0]
        elif response_json['count'] > 1:
            for step in response_json["results"]:
                if step['name'] == name:
                    return step


def scrap_move(move):
    step_name = move.find('h2').get_text().title()

    creator_container = move.find(class_='crb')
    creator_name, creator_data = scrap_creator(creator_container)

    step = get_step(step_name)
    if step:
        step_id = step['pk']
    else:
        creator_id = creator_data['id'] if creator_data else None
        step_id = create_step(step_name, creator_id, 0)

    video_containers = move.find_all(class_='vids')
    for video_container in video_containers:
        scrap_videos(video_container, step_id)


def scrap_page(url, index):
    print(f'Scrapping page {index}.')
    page = requests.get(url+str(index))
    soup = BeautifulSoup(page.content, 'html.parser')

    moves_container = soup.find(id='m_list')
    moves_list = moves_container.find_all(class_='m')

    for move in moves_list:
        scrap_move(move)
