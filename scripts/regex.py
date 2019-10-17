import re
from collections import defaultdict

from scripts.scrapper import get_step, get_youtube_video_data, get_create_video, create_step, get_create_artist, \
    get_step_appearances, create_step_appearance

video_data = defaultdict(dict)

youtube_line = r"https://www\.youtube\.com/watch\?v=(.*)"
move_line = r"\d+\) (.+)[ ]+-[ ]+(.+)[ ]?\(([0-9]+):([0-9]+)\)"
anonymous_move_line = r"\d+\) (.+)[ ]*\(([0-9]+):([0-9]+)\)"

youtube_regex = re.compile(youtube_line)
move_regex = re.compile(move_line)
anonymous_move_regex = re.compile(anonymous_move_line)

list_videos = []

with open('arnold_electric.txt') as text:
    for line in text:
        if not line.strip(): continue

        result = youtube_regex.match(line)
        if result:
            video_id = result.group(1)
        else:
            result = move_regex.match(line)
            if result:
                list_videos.append({
                    'title': result.group(1).strip().title(),
                    'artist': result.group(2).strip().title(),
                    'time': 60 * int(result.group(3)) + int(result.group(4)),
                    'video_id': video_id
                })
            else:
                result = anonymous_move_regex.match(line)
                if result:
                    list_videos.append({
                        'title': result.group(1).strip().title(),
                        'artist': None,
                        'time': 60 * int(result.group(2)) + int(result.group(3)),
                        'video_id': video_id
                    })

                else:
                    print(line)

unknown_artists = defaultdict(list)
known_artists = defaultdict(list)
known_videos = defaultdict(list)
artists = {}
videos = {}
steps = {}

for step in list_videos:
    print(step['title'])
    video_url = f'https://www.youtube.com/watch?v={step["video_id"]}'

    if video_url not in videos:
        # Call Youtube API to check if video exists and update title
        video_data = get_youtube_video_data(step["video_id"])
        if not video_data:
            raise Exception('Unable to find youtube video {}'.format(video_url))

        video_data['url'] = video_url
        video_data['host'] = 1
        video_data['type'] = 'Steps video'

        videos[video_url] = get_create_video(video_data)

    if step["artist"] and step["artist"] not in artists:
        artists[step["artist"]] = get_create_artist(step["artist"])

    step_response = get_step(step.get('title'))
    if step_response:
        step_id = step_response['pk']
    else:
        creator_id = artists[step["artist"]]['id'] if step["artist"] else None
        step_id = create_step(step.get('title'), creator_id, 0)

    video_id = videos[video_url]['id']
    appearances = get_step_appearances(video_id, step_id, step['time'])
    if not appearances:
        create_step_appearance(video_id, step_id, step['time'])
