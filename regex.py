import re

with open('arnold_electric.txt') as f:
    txt = f.read()

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
            current_link = f'https://www.youtube.com/watch?v={result.group(1)}'
        else:
            result = move_regex.match(line)
            if result:
                list_videos.append({
                    'title': result.group(1).strip(),
                    'artist': result.group(2).strip(),
                    'url': current_link+f'&t={60 * int(result.group(3)) + int(result.group(4))}'
                })
            else:
                result = anonymous_move_regex.match(line)
                if result:
                    list_videos.append({
                        'title': result.group(1).strip(),
                        'artist': None,
                        'url': current_link+f'&t={60 * int(result.group(2)) + int(result.group(3))}'
                    })

                else:
                    print(line)

