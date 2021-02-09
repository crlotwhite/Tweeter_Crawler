import tweepy


def make_api():
    import pickle
    with open('keys', 'rb') as f:
        keys = pickle.load(f)

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token_key'], keys['access_token_secret'])

    api = tweepy.API(auth)

    return api


def get_status_by_id(user_id, count):
    api = make_api()
    return tweepy.Cursor(api.user_timeline, id=user_id).items(count)


def file_name_from_url(url):
    return url[url.rfind('/')+1: url.rfind('?')] if url.rfind('?') > 0 else url[url.rfind('/')+1:]


def get_media_from_status(status):
    media_list = []

    extended_entities = getattr(status, 'extended_entities', None)

    if extended_entities is not None:
        medias = extended_entities['media']
        for media in medias:
            if media['type'] == 'video':
                url = ''
                max_bitrate = 0

                for vari in media['video_info']['variants']:
                    bitrate = vari.get('bitrate')
                    if bitrate is not None and bitrate > max_bitrate:
                        max_bitrate = vari['bitrate']
                        url = vari['url']

                media_list.append({
                    'type': media['type'],
                    'url': url,
                    'file_name': file_name_from_url(url),
                    'preview': media['media_url'],
                })
            elif media['type'] == 'photo':
                media_list.append({
                    'type': media['type'],
                    'url': media['media_url'],
                    'file_name': file_name_from_url(media['media_url']),
                    'preview': media['media_url'],
                })

    return media_list


def download(url, file_path, filename):
    from requests import get
    from os.path import join

    with open(join(file_path, filename), 'wb') as file:
        response = get(url)
        file.write(response.content)
