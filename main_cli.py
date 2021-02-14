import os
import argparse

from from_tweeter import *

'''
1. 인자가 없을 경우 id.txt
2. -b --batch list1.txt
3. -d --directory download
'''


def get_now_datetime_str():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


class MyLogger:
    log_file = None

    def __init__(self):
        self.log_file = open('log.txt', 'a')

    def __del__(self):
        self.log_file.close()

    def log(self, msg):
        self.log_file.write(f'[{get_now_datetime_str()}]{msg}\n')

    def start_log(self):
        start_datetime = get_now_datetime_str()
        self.log_file.write(f'Log start at {start_datetime}\n'
                            f'=============================\n')

    def finish_log(self):
        self.log('Work Finish!!\n')
        self.__del__()

    def err_log(self, msg):
        self.log(f'[{get_now_datetime_str()}]\n{msg}\n')
        self.__del__()


# Argument 설정
parser = argparse.ArgumentParser(description='Tweeter Crawler CLI for Automation')
parser.add_argument('--batch', '-b', required=False, help='select id list text file for download.')
parser.add_argument('--directory', '-d', required=False, help='Target directory')
parser.add_argument('--count', '-c', required=False, type=int, default=20, help='Count of Tweet')

# 값 가져오기
args = parser.parse_args()
batch = args.batch
directory = args.directory
tweet_count = args.count

# logger 생성
logger = MyLogger()
logger.start_log()

# 리스트 파일 설정
if batch is None:
    if os.path.exists('id.txt'):
        batch = 'id.txt'
    else:
        print('There is no "id.txt"')
        print('if you want to use other file, use "--batch" or "-b" option.')
        exit(1)

# 유저 리스트 생성
user_list = []
try:
    with open(batch, 'rt') as f:
        lines = f.readlines()
        for line in lines:
            user = line.replace("\n", "")
            user_list.append(user)
            logger.log(f'Add user {user}')
except Exception as e:
    logger.err_log(e)
    exit(1)


# 다운로드 큐 생성
download_list = []
for user in user_list:
    # 폴더 생성
    if directory is not None:
        saved_folder = os.path.join(os.path.join(os.getcwd(), directory), user)
    else:
        saved_folder = os.path.join(os.path.join(os.getcwd(), 'downloaded'), user)

    try:
        if not os.path.exists(saved_folder):
            os.mkdir(saved_folder)
            logger.log(f'create directory {saved_folder}')
    except Exception as e:
        logger.log('create directory error')
        logger.err_log(e)
        exit(1)

    try:
        for status in get_status_by_id(user, tweet_count):
            logger.log(f'{user} {status.created_at}')
            download_list.extend(get_media_from_status(status))
    except Exception as e:
        logger.log('get status by id error')
        logger.err_log(e)
        exit(1)

    try:
        for media in download_list:
            download(media['url'], saved_folder, media['file_name'])
    except Exception as e:
        logger.err_log(e)
        exit(1)

# 완료 처리
logger.finish_log()
