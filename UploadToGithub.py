from github import GithubException


def upload_to_github(repo, git_path, content):
    folder_path = '/'.join(git_path.split('/')[:-1])

    try:
        all_paths = [file.path for file in repo.get_contents(folder_path)]
    except GithubException:
        all_paths = []

    if git_path not in all_paths:
        repo.create_file(git_path, "Committing files", content, branch="main")
        print(git_path, 'CREATED')
    else:
        print(git_path, 'ALREADY EXISTS')
