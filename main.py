import CodeChefScraper
import CodeForcesScraper
from time import sleep
import os
import logging
from github import Github
from UploadToGithub import upload_to_github
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
g = Github(ACCESS_TOKEN)
repo = g.get_user().get_repo('CP-Solutions')


def upload_solution(website, solution):
    try:
        if 'c++' in solution['language'].lower():
            extension = 'cpp'
        elif 'py' in solution['language'].lower():
            extension = 'py'
        elif 'java' in solution['language'].lower():
            extension = 'java'
        else:
            extension = 'txt'

        upload_to_github(repo, f'{website}/{solution["language"]}/{solution["problem_code"]}/{solution["solution_id"]}.{extension}', solution['solution'])
        return True

    except Exception as e:
        logging.error(f'{e} FOR {solution}')
        return False


def main():
    failed_codeforces = []
    for solution in CodeForcesScraper.get_solutions('crap_the_coder'):
        if not upload_solution('CodeForces', solution):
            failed_codeforces.append(solution)

    sleep(180)

    for solution in failed_codeforces:
        upload_solution('CodeForces', solution)

    for solution in CodeChefScraper.get_solutions('crap_the_coder'):
        upload_solution('CodeChef', solution)


if __name__ == '__main__':
    main()
