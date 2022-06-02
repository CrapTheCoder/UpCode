import grequests
import requests
import json
from time import sleep
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}


def get_submission_info(username):
    submissions = json.loads(requests.get(f'https://codeforces.com/api/user.status?handle={username}').text)['result']

    for submission in submissions:
        if submission['verdict'] == 'OK':
            try:
                if len(str(submission["problem"]["contestId"])) <= 4 and len(submission["author"]["members"]) == 1:
                    yield {
                        'language': submission['programmingLanguage'],
                        'problem_code': f'{submission["problem"]["contestId"]}{submission["problem"]["index"]}',
                        'solution_id': submission['id'],
                        'problem_name': submission['problem']['name'] if 'name' in submission['problem'] else '',
                        'problem_link': f'https://codeforces.com/contest/{submission["problem"]["contestId"]}/problem/{submission["problem"]["index"]}',
                        'link': f'https://codeforces.com/contest/{submission["contestId"]}/submission/{submission["id"]}?f0a28=2',
                    }

            except KeyError:
                pass


def get_code(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        return soup.select_one('#program-source-text').text

    except:
        sleep(60)


def get_solutions(username, all_info=None):
    if all_info is None:
        all_info = list(get_submission_info(username))

    responses = grequests.imap(grequests.get(info['link'], headers=headers) for info in all_info)
    for info, response in zip(all_info, responses):
        code = get_code(response.text)
        yield {
            'language': info['language'],
            'problem_code': info['problem_code'],
            'solution_id': info['solution_id'],
            'problem_name': info['problem_name'],
            'problem_link': info['problem_link'],
            'link': info['link'],
            'solution': code,
        }
