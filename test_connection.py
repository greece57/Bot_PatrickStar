""" JUST SOME TESTING HERE """
import json
from slackclient import SlackClient

TOKEN = "#"

with open('token.key', 'r') as keyFile:
    while TOKEN.startswith("#"):
        TOKEN = keyFile.readline()

sc = SlackClient(TOKEN)
print sc.api_call("api.test")
auth = sc.api_call("auth.test")
if auth['ok'] == True:
    print auth
channels = sc.api_call("groups.list")['groups']
for c in channels:
    if c['name'] == "test":
        testChannel = c

sc.api_call("chat.postMessage", channel=c['id'], text='Is mayonnaise an instrument?', as_user='true')
