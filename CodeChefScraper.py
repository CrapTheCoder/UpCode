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


def get_info(solution_id):
    link1 = f'https://www.codechef.com/api/submission-code/{solution_id}'
    link2 = f'https://www.codechef.com/api/submission-details/{solution_id}'
    data1 = requests.get(link1, headers=headers).text
    data2 = requests.get(link2, headers=headers).text
    json_data1 = json.loads(data1)
    json_data2 = json.loads(data2)

    contest_code = json_data2['data']['other_details']['contestCode']
    problem_code = json_data2['data']['other_details']['problemCode']

    return {
        'language': json_data1['data']['language']['short_name'],
        'problem_code': problem_code,
        'solution_id': solution_id,
        'problem_link': f'https://www.codechef.com/{contest_code}/problems/{problem_code}',
        'link': f'https://www.codechef.com/viewsolution/{solution_id}',
        'solution': json_data1['data']['code'],
    }


def get_solutions(username):
    links = list(get_links(username))[::-1]
    responses = grequests.imap(grequests.get(u) for u in links)

    submission_links = (link for response in responses for link in get_submission_links(response.content))
    submission_responses = grequests.imap(grequests.get(u, headers=headers) for u in submission_links)

    for response in submission_responses:
        solution_id = (response.url.split('/')[-1])
        yield get_info(solution_id)
