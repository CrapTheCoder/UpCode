import time
from agents import Atcoder, CodeChef, CodeForces
from github import Github, Auth
from github.GithubException import UnknownObjectException
from multiprocessing import Process


GITHUB_SLEEP_TIME = 1


def upload_to_github(repo, directory):
    try:
        with open(directory, 'r') as submission:
            repo.create_file(directory, 'Uploaded file', submission.read())
            print(f'[GitHub] Updated {directory} successfully')
            time.sleep(GITHUB_SLEEP_TIME)

    except Exception as e:
        print(f'[GitHub] ERROR: {e}, {directory}')


if __name__ == '__main__':
    codeforces_username = input('Enter CodeForces username (Press enter if N/A): ')
    codechef_username = input('Enter CodeChef username (Press enter if N/A): ')
    atcoder_username = input('Enter Atcoder username (Press enter if N/A): ')

    codeforces_locations = []
    codechef_locations = []
    atcoder_locations = []

    codeforces_directory = 'CodeForces'
    codechef_directory = 'CodeChef'
    atcoder_directory = 'Atcoder'

    processes = []

    if codeforces_username:
        processes.append(Process(target=CodeForces.save_submissions, args=(codeforces_username, 'CodeForces')))
        processes[-1].start()

    if codechef_username:
        processes.append(Process(target=CodeChef.save_submissions, args=(codechef_username, 'CodeChef')))
        processes[-1].start()

    if atcoder_username:
        processes.append(Process(target=Atcoder.save_submissions, args=(atcoder_username, 'Atcoder')))
        processes[-1].start()

    for process in processes:
        process.join()

    token = input('Enter GitHub token: ')
    repo_name = input('Enter repository name: ')

    auth = Auth.Token(token)
    g = Github(auth=auth)

    try:
        user_repo = g.get_user().get_repo(repo_name)

    except UnknownObjectException:
        user_repo = g.get_user().create_repo(repo_name, private=True)

    for locations, website_directory in (
            (codeforces_locations, codeforces_directory),
            (codechef_locations, codechef_directory),
            (atcoder_locations, atcoder_directory)
    ):
        for files in locations:
            for file_directory in files:
                file_location = f'{website_directory}/{file_directory}'
                upload_to_github(user_repo, f'{website_directory}/{file_directory}')
