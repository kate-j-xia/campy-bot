from slack import WebClient

def get_users(client: WebClient) -> {}:
    
    response = client.users_list()
    usersByName = {}
    # usersById = {}
    if response.data.get('ok'):
        userList = response.data.get('members')
        if userList:
            for user in userList:
                print(f"get_users(): User ID: {user['id']}, Name: {user['name']}")
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
