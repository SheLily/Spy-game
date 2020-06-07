import requests
import time
import tqdm
import json


def get_id_by_name(username, token, v):
    data = {
        'access_token': token,
        'user_ids': username,
        'v': v
    }
    response = requests.get(
        'https://api.vk.com/method/users.get',
        data
    ).json()
    return response['response'][0]['id']


def get_groups(user_id, token, v):
    data = {
        'access_token': token,
        'user_id': user_id,
        'extended': 1,
        'fields': 'members_count',
        'v': v
    }
    response = requests.get(
        f'https://api.vk.com/method/groups.get', data
        ).json()
    if 'error' not in response:
        return response['response']['items']


def get_groups_set(group_list):
    return {i['id'] for i in group_list}


def get_friends(user_id, token, v):
    data = {
        'access_token': token,
        'user_id': user_id,
        'v': v
    }
    response = requests.get(
        f'https://api.vk.com/method/friends.get',
        data,
        ).json()
    if 'error' not in response:
        return set(response['response']['items'])


user = 171691064
token = ('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56'
         'f95c04217915c32008')
v = 5.107

user = get_id_by_name(user, token, v)

usr_groups = get_groups(user, token, v)
set_usr_group = get_groups_set(usr_groups)

usr_friends = get_friends(user, token, v)


pbar = tqdm.tqdm(usr_friends)
for i in pbar:
    start = time.time()
    frnd_groups = get_groups(i, token, v)
    if frnd_groups:
        set_usr_group -= get_groups_set(frnd_groups[:1000])
    sleeptime = 1 / 3 - (time.time() - start)
    if sleeptime > 0:
        time.sleep(sleeptime)

usr_groups = [i for i in usr_groups if i['id'] in set_usr_group]
for i in usr_groups:
    if 'members_count' not in i:
        i['members_count'] = 0
usr_groups = [
    {'name': i['name'], 'gid': i['id'], 'members_count': i['members_count']}
    for i in usr_groups
    ]

with open('groups.json', 'w', encoding='utf-8') as fout:
    json.dump(usr_groups, fout, ensure_ascii=False)