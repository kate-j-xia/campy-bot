from slack import WebClient
import ssl
from . import config

# Slack access token
SLACK_CLIENT_TOKEN = config.slack_client_token
# SLACK_SIGNING_SECRET = config.slack_signing_secret
 
def get_slack_client():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client = WebClient(token=SLACK_CLIENT_TOKEN, ssl=ssl_context)
    # client = slack.WebClient(token=SLACK_CLIENT_TOKEN)
    # client.chat_postMessage(channel=CHANNEL_ID_CAMPY,text='Hello your bot here, what can I do for you?')    
    
    return client
    # slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

def get_users(client: WebClient) -> {}:
    
    response = client.users_list()
    usersByName = {}
    # usersById = {}
    if response.data.get('ok'):
        userList = response.data.get('members')
        if userList:
            for user in userList:
                # print(f"get_users(): User ID: {user['id']}, Name: {user['name']}")
                usersByName[user['name']] = user['id']
                # usersById[user['id']] = user['name']
        print(f'get_users(): {usersByName}')
        return usersByName # , usersById
    else:
        print(f"get_users(): Error retrieving users: {response.data}")
        return None

    
def get_id_by_name(users, username: str) -> str:
    if users is None or username is None:
        return ""
    
    return users.get(username)
