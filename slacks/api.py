from slack import WebClient
import ssl
import config

# Slack Bot User OAuth Token
SLACK_CLIENT_TOKEN = config.SLACK_CLIENT_TOKEN
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
                name = user['profile']['first_name'].lower()
                usersByName[name] = user['id']
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

def send_dm(client: WebClient, user_id: str, message: str):
    """
        Sends a direct message to a slack user.
    """    
    try:
        response = client.conversations_open(users=user_id)
        channel_id = response['channel']['id']

        client.chat_postMessage(channel=channel_id, text=message)
        print(f'send_dm(): user_id = {user_id}, channel_id = {channel_id} DM sent.')
    except Exception as e:
        print(f'send_dm(): Error sending DM - {e}')