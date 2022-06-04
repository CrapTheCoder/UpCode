from github import GithubException


def upload_to_github(repo, git_path, content, problem_info=''):
    folder_path = '/'.join(git_path.split('/')[:-1])

    try:
        all_paths = [file.path for file in repo.get_contents(folder_path)]

    except GithubException:
        if problem_info:
            repo.create_file(f'{folder_path}/__info.txt', "Created info.txt", problem_info, branch="main")

        all_paths = []

    if git_path not in all_paths:
        repo.create_file(git_path, 'Committing files', content, branch="main")
        print(git_path, 'CREATED')
    else:
        print(git_path, 'ALREADY EXISTS')
