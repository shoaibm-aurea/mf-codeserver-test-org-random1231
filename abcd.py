import json
import os

import requests
import random

token = os.getenv('GITHUB_TOKEN')
username = os.getenv('GIT_USERNAME')
git_repo = os.getenv('GIT_REPO')


def create_blob():
    url = "https://api.github.com/repos/{}/{}/git/blobs".format(username, git_repo)
    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/vnd.github.VERSION.raw"
    }

    with open('abcd.py', 'r', encoding='utf-8') as f:
        file_data = f.read()

    data = {
        "content": file_data,
        "encoding": "utf-8"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('** Blob created successfully **')
    print(response.json()['sha'])
    print(response.json()['url'])
    return response.json()['sha']


def create_tree(blob_sha):
    url = "https://api.github.com/repos/{}/{}/git/trees".format(username, git_repo)
    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        # base_tree is needed to update the existing tree else all files are considered to be deleted with this tree
        # 'base_tree': masterRef.object.sha,
        'tree': [
            {
                'path': "abcd.py",
                'mode': "100644",
                'type': "blob",
                'sha': blob_sha
            }
        ]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('** Tree created successfully **')
    print(response.json()['sha'])
    print(response.json()['url'])
    return response.json()['sha']


def create_commit(tree_sha):
    url = "https://api.github.com/repos/{}/{}/git/commits".format(username, git_repo)
    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        'message': f"Random message: {random.random()}",
        'tree': tree_sha
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f'** Commit created successfully: {response.json()["sha"]}**')
    print(response.json()['sha'])
    print(response.json()['url'])
    return response.json()['sha']


def create_branch(commit_sha):
    url = "https://api.github.com/repos/{}/{}/git/refs".format(username, git_repo)
    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/vnd.github.v3+json"
    }
    branch_name = f"NEW-BRANCH-NAME-{int(random.random() * 1000)}"
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": commit_sha
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"** Branch created successfully: {response.json()['object']['sha']} **")
    return branch_name


def create_pull_request(branch_name):
    url = "https://api.github.com/repos/{}/{}/pulls".format(username, git_repo)
    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": "PullRequest-Using-GithubAPI-Dynamic",
        "body": "I have amazing new Features",
        "head": branch_name,
        "base": "master"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json()['url'])


if __name__ == '__main__':
    blob_sha = create_blob()
    tree_sha = create_tree(blob_sha)
    commit_sha = create_commit(tree_sha)
    branch_name = create_branch(commit_sha)
    create_pull_request(branch_name)
