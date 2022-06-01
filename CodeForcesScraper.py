from time import sleep
import requests
import json
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}


def get_submission_info(username):
    submissions = json.loads(requests.get(f'https://codeforces.com/api/user.status?handle={username}').text)['result']

    for submission in submissions:
        if submission['verdict'] == 'OK' and len(submission["problem"]["contestId"]) <= 4:
            yield {
                'language': submission['programmingLanguage'],
                'problem_code': f'{submission["problem"]["contestId"]}{submission["problem"]["index"]}',
                'solution_id': submission['id'],
                'link': f'https://codeforces.com/contest/{submission["contestId"]}/submission/{submission["id"]}?f0a28=2'
            }


def get_code(html):
    for _ in range(2):
        try:
            soup = BeautifulSoup(html, 'lxml')
            return soup.select_one('#program-source-text').text

        except:
            return None


def get_solutions(username, all_info=None):
    if all_info is None:
        all_info = list(get_submission_info(username))

    for info in all_info:
        session = requests.Session()
        yield {
            'language': info['language'],
            'problem_code': info['problem_code'],
            'solution_id': info['solution_id'],
            'link': info['link'],
            'solution': get_code(session.get(info['link'], headers=headers).text),
        }
