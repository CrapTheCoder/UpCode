import CodeChefScraper
import CodeForcesScraper
from time import sleep
import logging
from github import Github
from github.GithubException import UnknownObjectException
from UploadToGithub import upload_to_github
from multiprocessing import Process


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


def codeforces_uploader(codeforces_username, repo):
    failed_codeforces = []
    for solution in CodeForcesScraper.get_solutions(codeforces_username):
        if not upload_solution('CodeForces', solution, repo):
            failed_codeforces.append(solution)

    sleep(180)
    for solution in CodeForcesScraper.get_solutions(codeforces_username, failed_codeforces):
        upload_solution('CodeForces', solution, repo)


def codechef_uploader(codechef_username, repo):
    for solution in CodeChefScraper.get_solutions(codechef_username):
        upload_solution('CodeChef', solution, repo)


def main():
    codeforces_username = input('Enter codeforces username (Press enter if N/A): ')
    codechef_username = input('Enter codechef username (Press enter if N/A): ')
    access_token = input('Enter github access token: ')
    
    repo_name = input('Enter repository name (Press enter to use "CP-Solutions"): ')
    if repo_name.isspace():
        repo_name = 'CP-Solutions'

    g = Github(access_token)

    try:
        repo = g.get_user().get_repo(repo_name)

    except UnknownObjectException:
        repo = g.get_user().create_repo(repo_name, private=True)

    if codeforces_username:
        codeforces_process = Process(target=codeforces_uploader, args=(codeforces_username, repo))
        codeforces_process.start()

    if codechef_username:
        codechef_process = Process(target=codechef_uploader, args=(codechef_username, repo))
        codechef_process.start()


if __name__ == '__main__':
    main()
