import re

from googleapiclient.discovery import build

from dance.models import Video


def get_youtube_video_data(url):
    """
    Call the Youtube API to collect detailed information about video.
    :param url: url given by the user
    :type url: str
    :return: result of the call to the Youtube API or None if the video doesn't exist.
    :rtype: dict
    """
    youtube_id = get_youtube_video_id(url)

    if not youtube_id:
        return None

    # Call Youtube API
    service = build('youtube', 'v3', developerKey='AIzaSyA1C8wnXvLAUUSlzPe9LT9PDQpzc9LxaV8')
    api_result = service.videos().list(part='snippet', id=youtube_id).execute()

    # Analyse response and return result
    if len(api_result.get('items')) == 0:
        return None

    result = api_result.get('items')[0].get('snippet')

    return {
        'title': result.get('title'),
        'channel': result.get('channelTitle'),
        'channel_url': f"https://www.youtube.com/channel/{result.get('channelId')}",
        'valid': True,
        'url': f'https://www.youtube.com/watch?v={youtube_id}',
        'host': Video.YOUTUBE,
        # 'thumbnail': f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg' todo: add when validation is required
    }


def get_youtube_video_id(url):
    """
    Check if the video is from Youtube and return a normalized URL.
    :param url: url given by the user
    :type url: str
    :return: video host ID and video ID
    :rtype: (int, str)
    """
    regex_yt = r'^((?:https?:)?\/\/)?((?i)(?:www|m)\.)?((?:youtube\.com|youtu.be))' \
               r'(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
    search_result = re.search(regex_yt, url)

    if search_result and search_result.group(5):
        return search_result.group(5).strip()


def get_video_data(url):
    """
    Return detailed information about the video if able to find.
    :param url: URL of the video.
    :type url: str
    :return: result of the call to the Youtube API or None if the video doesn't exist.
    :rtype: dict
    """
    youtube_data = get_youtube_video_data(url)
    if youtube_data:
        return youtube_data

    return None
