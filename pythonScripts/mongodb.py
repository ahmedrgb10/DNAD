from pymongo import MongoClient
from datetime import date,datetime

dbClient= MongoClient("mongodb://localhost:27017")
DND=dbClient.DND
WI=DND.WorkItem

def backup():
    print(list(WI.find()))
    collection="backup" + str(date.today())
    DND[collection].insert_many(list(WI.find()))
    print("Backup snapped at: ",date.today())

def alreadyExists(wid):
    flag=False
    workItem=list(WI.find(wid))
    if len(workItem)==0:
        flag=True
    else:
        print("WorkItem Already Exists")
    return flag

def insert(wid):
    if alreadyExists(wid)==True:
        print("TOBEINSERTED",wid)
        WI.insert_one(wid)

def get():
    for doc in WI.find():
        print(doc)





#WI.delete_many({})
