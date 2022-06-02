import CodeChefScraper
import CodeForcesScraper
import AtcoderScraper
from time import sleep
import logging
from github import Github
from github.GithubException import UnknownObjectException
from UploadToGithub import upload_to_github
from multiprocessing import Process

EXTENSIONS = {
    'c++': 'cpp',
    'clang': 'cpp',
    'gcc': 'c',
    'py': 'py',
    'java': 'java',
    'c#': 'cs',
    'go': 'go',
    'haskell': 'hs',
    'kotlin': 'kt',
    'delphi': 'dpr',
    'pascal': 'pas',
    'perl': 'pl',
    'php': 'php',
    'rust': 'rs',
    'scala': 'sc',
    'javascript': 'js',
    'node': 'js',
}


def upload_solution(website, solution, repo):
    try:
        s = solution["language"].lower()

        extension = 'txt'
        for key, value in EXTENSIONS.items():
            if key in s:
                extension = value
                break

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

    for _ in range(3):
        if failed_codeforces:
            sleep(180)

            new_failed_codeforces = []
            for solution in CodeForcesScraper.get_solutions(codeforces_username, failed_codeforces):
                if not upload_solution('CodeForces', solution, repo):
                    new_failed_codeforces.append(solution)

            failed_codeforces = new_failed_codeforces


def codechef_uploader(codechef_username, repo):
    for solution in CodeChefScraper.get_solutions(codechef_username):
        upload_solution('CodeChef', solution, repo)


def atcoder_uploader(atcoder_username, repo):
    for solution in AtcoderScraper.get_solutions(atcoder_username):
        upload_solution('Atcoder', solution, repo)


def main():
    codeforces_username = input('Enter codeforces username (Press enter if N/A): ')
    codechef_username = input('Enter codechef username (Press enter if N/A): ')
    atcoder_username = input('Enter atcoder username (Press enter if N/A): ')
    access_token = input('Enter github access token: ')

    repo_name = input('Enter repository name (Press enter to use "CP-Solutions"): ')
    if repo_name.isspace() or not repo_name:
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

    if atcoder_username:
        atcoder_process = Process(target=atcoder_uploader, args=(atcoder_username, repo))
        atcoder_process.start()


if __name__ == '__main__':
    main()
