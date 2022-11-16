import csv
from time import time
import json
import vk_parser as parser
import work_with_graph as graph


# getting data from csv and converting to list
def processing_cvs(DataBaseName):
    with open(DataBaseName, newline='', encoding='utf-8') as csvfile:
        dataBase = list(csv.DictReader(csvfile, delimiter=';'))
    return dataBase

# writing the database to a file
def add_dataBase_in_file(dataBase):
    f = open('data_base.txt','w')
    f.write(str(json.dumps(dataBase)))
    f.close()


# getting the database from the file
def open_dataBase():
    f = open('data_base.txt','r')
    dataBase = json.loads(f.read())
    f.close()
    return dataBase


t0 = time()
try:
    dataBaseWithFriendsOfFriends = open_dataBase()
except:
    dataBase = processing_cvs('vk_database.csv')
    conversionDataBase = parser.convert_person_id(dataBase)
    dataBaseWithFriends = parser.search_friends(conversionDataBase)
    dataBaseWithFriendsOfFriends = parser.search_friends_of_friends(dataBaseWithFriends)
    add_dataBase_in_file(dataBaseWithFriendsOfFriends)
finally:
    relationsList, clearDataBase = graph.check_friendship(dataBaseWithFriendsOfFriends)
    G = graph.graph_formation(clearDataBase, relationsList)
    graph.betweenness_centrality(G, clearDataBase)
    graph.closeness_centrality(G, clearDataBase)
    graph.eigenvector_centrality(G, clearDataBase)

t1 = time()
print('Время работы программы', t1 - t0, 'секунд')
