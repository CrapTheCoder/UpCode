import requests
import json
from json.decoder import JSONDecodeError
import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *

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
    lines = driver.find_elements(By.CSS_SELECTOR, '#program-source-text > ol > li')
    return '\n'.join(line.text for line in lines)


def get_solutions(username, all_info=None):
    try:
        if all_info is None:
            all_info = list(get_submission_info(username))

    except JSONDecodeError:
        logging.error("CodeForces API is currently unavailable. Please try again later.")
        return

    sub_id_info = {info['solution_id']: info for info in all_info}
    for info in all_info:
        sub_id_info[info['solution_id']] = info

    options = Options()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(f'https://codeforces.com/submissions/{username}')

    sleep(1)

    select = Select(driver.find_element(By.ID, 'verdictName'))
    select.select_by_value('OK')

    driver.find_element(By.CSS_SELECTOR, 'input[value=Apply]').click()

    sub_ids = [info['solution_id'] for info in all_info]

    try:
        pages = int(driver.find_elements(By.CSS_SELECTOR, '#pageContent > div > ul > li > span')[-1].text)

    except IndexError:
        pages = 1

    index = 1

    driver.get(f'https://codeforces.com/submissions/{username}/page/{index}')

    prev = {}

    fail_counter = 0

    failed = []
    for sub_id in sub_ids:
        if index > pages:
            break

        if fail_counter:
            try:
                driver.get(sub_id_info[sub_id]['link'])

                code = get_code(driver)
                sub_id_info[sub_id]['solution'] = code
                prev[code] = sub_id_info[sub_id]
                yield sub_id_info[sub_id]

                fail_counter -= 1
                if fail_counter == 0:
                    driver.get(f'https://codeforces.com/submissions/{username}/page/{index}')

                sleep(0.3)
                continue

            except NoSuchElementException:
                failed.append((sub_id, index))
                sleep(120)

                driver.quit()

                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                driver.get(f'https://codeforces.com/submissions/{username}/page/{index}')
                fail_counter = 0

        for _ in range(3):
            try:
                element = driver.find_element(By.PARTIAL_LINK_TEXT, str(sub_id))
                driver.execute_script("arguments[0].click();", element)
                sleep(0.3)

                counter = 0

                cur = []
                while not cur or ((cur in prev) and ((
                        sub_id_info[sub_id]['problem_code'] != prev[cur]['problem_code']) or
                        (sub_id_info[sub_id]['problem_code'][-1].isdigit() and prev[cur]['problem_code'][-1].isdigit()))
                ):
                    sleep(0.3)
                    cur = '\n'.join(ele.text for ele in driver.find_elements(By.CSS_SELECTOR, '#facebox > div > div > div > pre > code > ol > li'))

                    counter += 1
                    if counter % 3 == 0:
                        driver.refresh()
                        driver.execute_script("arguments[0].click();", element)

                        sleep(0.3)
                        cur = '\n'.join(ele.text for ele in driver.find_elements(By.CSS_SELECTOR, '#facebox > div > div > div > pre > code > ol > li'))

                code = cur

                sub_id_info[sub_id]['solution'] = code.replace('\u00a0', '\n')
                prev[code] = sub_id_info[sub_id]
                yield sub_id_info[sub_id]

                break

            except NoSuchElementException:
                if driver.current_url == 'https://codeforces.com/':
                    sleep(60)

                else:
                    index += 1
                    driver.get(f'https://codeforces.com/submissions/{username}/page/{index}')
                    break

            except StaleElementReferenceException:
                driver.execute_script("location.reload(true);")
                sleep(2)

        else:
            fail_counter = 5
