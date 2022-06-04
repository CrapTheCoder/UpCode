import requests
import json
from json.decoder import JSONDecodeError
from time import sleep
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logging.getLogger('WDM').setLevel(logging.NOTSET)

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


def get_code(driver):
    try:
        lines = driver.find_elements(By.CSS_SELECTOR, '#program-source-text > ol > li')
        return '\n'.join(line.text for line in lines)

    except:
        sleep(100)


def get_solutions(username, all_info=None):
    try:
        if all_info is None:
            all_info = list(get_submission_info(username))

    except JSONDecodeError:
        logging.error("CodeForces API is currently unavailable. Please try again later.")
        return

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    for info in all_info:
        driver.get(info['link'])
        code = get_code(driver)

        yield {
            'language': info['language'],
            'problem_code': info['problem_code'],
            'solution_id': info['solution_id'],
            'problem_name': info['problem_name'],
            'problem_link': info['problem_link'],
            'link': info['link'],
            'solution': code,
        }
