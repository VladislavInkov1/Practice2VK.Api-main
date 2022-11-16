import networkx as nx
from requests import get


token = "vk1.a.0CJtzVv2hA8owHDa2NZvsVdgSnFVsqQUrN28zdRHKPtrPA3Ai-Kveqs435YacX_iPNSXfj6P5cd5AMZTKGy6bVHrYsao0eCN8TOpR3BchXxXU6xx2LNEPGIGtX0eDLs0A8qsuqYeJA-2slqWx5K2H00WWjkL6Z9wN6ply3gtscZgLBIm2PKpxt3yefCdjERDW1BoVCgKE-EwlBpz6vc0Ow"
version = 5.131

# checking connections between users, deleting "closed/inaccessible/empty"
def check_friendship(dataBase):
    relationsList = []
    for item, row in enumerate(dataBase):
        friendsCounter = 0
        for id in row['friends']:
            relationsList.append((row['ID'], id['id']))
            friendsCounter = friendsCounter + 1
            relationsList = relationsList + check_friendship_3lvl(dataBase, id['id'])
        if friendsCounter == 0:
            dataBase.pop(item)
    return relationsList, dataBase


# checking connections between users of level 2 and 3, removing "closed/inaccessible/empty"
def check_friendship_3lvl(dataBase, search_id):
    relationsList = []
    for item, row in enumerate(dataBase):
        for id in row['friends']:
            if search_id in id['friends']:
                relationsList.append((search_id, id['id']))
    return relationsList


# graph construction
def graph_formation(dataBase, relationList):
    G = nx.Graph()
    for item, row in enumerate(dataBase):
        G.add_node(row['ID'])
        for id in row['friends']:
            G.add_node(id['id'])
    G.add_edges_from(relationList)
    nx.write_graphml(G, "graph.graphml")
    return (G)


# betweenness centrality
def betweenness_centrality(G, dataBase):
    centralityDict = nx.betweenness_centrality(G)
    v, k = max((v, k) for k, v in centralityDict.items())
    print('По посредничеству: ', getNameByID(k), ', id: ', k)


# closeness centrality
def closeness_centrality(G, dataBase):
    centralityDict = nx.closeness_centrality(G, wf_improved=False)
    v, k = min((v, k) for k, v in centralityDict.items())
    print('По близости: ', getNameByID(k), ', id: ', k)


# eigenvector centrality
def eigenvector_centrality(G, dataBase):
    centralityDict = nx.eigenvector_centrality(G, 2147483646)
    v, k = max((v, k) for k, v in centralityDict.items())
    print('По собственному вектору: ', getNameByID(k), ', id: ', k)


# getting a user name by id
def getNameByID(id):
    request = get('https://api.vk.com/method/users.get', params={
        'access_token': token,
        'user_ids': id,
        'v': version
    })
    jsonFile = request.json()
    if (jsonFile.get('response') != None):
        return jsonFile['response'][0]['first_name'] + " " + jsonFile['response'][0]['last_name']
    else:
        return 'ФИО неизвестно'
