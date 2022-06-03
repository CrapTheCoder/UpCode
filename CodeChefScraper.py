import grequests
import requests
import json
from bs4 import BeautifulSoup, SoupStrainer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}


def get_links(username):
    html = requests.get(f'https://www.codechef.com/users/{username}').text
    soup = BeautifulSoup(html, 'lxml')

    for link in soup.select('body > main > div > div > div > div > div > section.rating-data-section.problems-solved > div > article:nth-child(2) > p > span > a'):
        yield 'https://www.codechef.com' + link['href'] + '?status=FullAC'


def get_submission_links(html):
    soup = BeautifulSoup(html, 'lxml', parse_only=SoupStrainer('td'))
    return [f'https://www.codechef.com/viewsolution/{obj.text}' for obj in
            soup.select('#content > div > div > div.tablebox-section.l-float > table > tbody > tr > td:nth-child(1)')]


def get_info(html):
    for line in html.split('\n'):
        if 'meta_info' in line:
            json_file = line[line.index('{'):].rstrip(';')
            loaded = json.loads(json_file)
            return {
                'language': loaded['data']['languageName'],
                'problem_code': loaded['data']['problemCode'],
                'solution_id': loaded['data']['solutionId'],
                'problem_link': f'https://www.codechef.com/{loaded["data"]["contestCode"]}/problems/{loaded["data"]["problemCode"]}',
                'link': f'https://www.codechef.com/viewsolution/{loaded["data"]["solutionId"]}',
                'solution': loaded['data']['plaintext'],
            }


def get_solutions(username):
    links = list(get_links(username))[::-1]
    responses = grequests.imap(grequests.get(u) for u in links)

    submission_links = (link for response in responses for link in get_submission_links(response.content))
    submission_responses = grequests.imap(grequests.get(u, headers=headers) for u in submission_links)

    for response in submission_responses:
        yield get_info(response.text)
