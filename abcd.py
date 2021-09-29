import requests
import json
token = "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"

headers = {
    "Authorization" : "token {}".format(token),
    "Accept" : "application/vnd.github.sailor-v-preview+json"
}
data= {
    "title" : "PullRequest-Using-GithubAPI",
    "body" : "I have amazing new Features",
    "head" : "pull-request",
    "base" : "master"
}

username = input("Enter your Github username : ")
Repositoryname = input("Enter the name of the repository : ")

url = "https://api.github.com/repos/{}/{}/pulls".format(username,Repositoryname)

response = requests.post(url,data=json.dumps(data), headers=headers)
print(response)