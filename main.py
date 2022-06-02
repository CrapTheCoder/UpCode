import CodeChefScraper
import CodeForcesScraper
from time import sleep
import logging
from github import Github
from github.GithubException import UnknownObjectException
from UploadToGithub import upload_to_github


def upload_solution(website, solution, repo):
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
    codeforces_username = input('Enter codeforces username (Press enter if N/A): ')
    codechef_username = input('Enter codechef username (Press enter if N/A): ')
    access_token = input('Enter github access token: ')

    g = Github(access_token)

    try:
        repo = g.get_user().get_repo('CP-Solutions')

    except UnknownObjectException:
        repo = g.get_user().create_repo('CP-Solutions', private=True)

    if codeforces_username:
        failed_codeforces = []
        for solution in CodeForcesScraper.get_solutions(codeforces_username):
            if not upload_solution('CodeForces', solution, repo):
                failed_codeforces.append(solution)

        sleep(180)
        for solution in CodeForcesScraper.get_solutions(codeforces_username, failed_codeforces):
            upload_solution('CodeForces', solution, repo)

    if codechef_username:
        for solution in CodeChefScraper.get_solutions(codechef_username):
            upload_solution('CodeChef', solution, repo)


if __name__ == '__main__':
    main()
