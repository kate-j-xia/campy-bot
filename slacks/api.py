from slack import WebClient
from fastapi import Request

CHANNEL_ID_CAMPY = "#campy"
COMMAND_CAMPY = "/campy"

async def get_command(request: Request):
    data = await request.form()

    print(f'production_status(): formData = {data}')
    if data is not None and data.get('command') == COMMAND_CAMPY:
        return data


def get_subcommand(req: dict) -> str:
    if req is None:
        return ""
    
    sub_command = req.get('text')
    print(f'get_commands(): sub_command = {sub_command}')
    return sub_command



def get_users(client: WebClient) -> dict:
    
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
        return usersByName
    else:
        print(f"get_users(): Error retrieving users: {response.data}")
        return None

    
def get_id_by_name(users: dict, username: str) -> str:

    print(f'get_id_by_name(): {username}')
    if username is not None and username in users.keys():
        return users[username]
    else:
        print(f'The user {username} is not in the team')
    return ""
    # client.users_profile_get

