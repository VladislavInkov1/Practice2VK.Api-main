from requests import get
from time import sleep

token = "vk1.a.0CJtzVv2hA8owHDa2NZvsVdgSnFVsqQUrN28zdRHKPtrPA3Ai-Kveqs435YacX_iPNSXfj6P5cd5AMZTKGy6bVHrYsao0eCN8TOpR3BchXxXU6xx2LNEPGIGtX0eDLs0A8qsuqYeJA-2slqWx5K2H00WWjkL6Z9wN6ply3gtscZgLBIm2PKpxt3yefCdjERDW1BoVCgKE-EwlBpz6vc0Ow"
version = 5.131

# converting short names to ids
def convert_person_id(dataBase):
    idList = ''
    for row in dataBase:
        idList = idList + row['ID'] + ','
    request = get('https://api.vk.com/method/users.get', params={
        'access_token': token,
        'user_ids': idList,
        'v': version
    })
    for item, row in enumerate(dataBase):
        row['ID'] = request.json()['response'][item]['id']
    return dataBase


# getting friends of friends
def search_friends(dataBase):
    for row in dataBase:
        r = get('https://api.vk.com/method/friends.get', params={
            'access_token': token,
            'user_id': row['ID'],
            'v': version
        })
        jsonFile = r.json()
        print(row['ID'])
        if jsonFile.get('response') != None:
            row['friends'] = []
            for item, id in enumerate(r.json()['response']['items']):
                row['friends'].append({'id': r.json()['response']['items'][item]})
        elif jsonFile.get('error') != None:
            print('ошибка ', jsonFile['error']['error_code'])
            if jsonFile['error']['error_code'] == 29:
                sleep(15 * 60)
                r = get('https://api.vk.com/method/friends.get', params={
                    'access_token': token,
                    'user_id': row['ID'],
                    'v': version,
                })
                jsonFile = r.json()
                row['friends'].append({'id': r.json()['response']['items'][item]})
            else:
                row['friends'] = []
        else:
            id['friends'] = []
        sleep(0.34)
    return dataBase


# getting level 3 friends
def search_friends_of_friends(dataBase):
    for row in dataBase:
        for id in row['friends']:
            r = get('https://api.vk.com/method/friends.get', params={
                'access_token': token,
                'user_id': row['ID'],
                'v': version
            })
            jsonFile = r.json()
            if jsonFile.get('response') != None:
                id['friends'] = r.json()['response']['items']
            elif jsonFile.get('error') != None:
                print('ошибка ', jsonFile['error']['error_code'])
                if jsonFile['error']['error_code'] == 29:
                    sleep(15 * 60)
                    r = get('https://api.vk.com/method/friends.get', params={
                        'access_token': token,
                        'user_id': row['ID'],
                        'v': version,
                    })
                    jsonFile = r.json()
                    id['friends'] = r.json()['response']['items']
                else:
                    id['friends'] = []
            else:
                id['friends'] = []
            sleep(0.34)
    return dataBase
