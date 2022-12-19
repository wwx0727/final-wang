import csv
from traceback import print_stack
import pymongo
import sys

class Mongo_Client():
    mongo = None
    db_game=None
    col_state=None
    col_event=None
    
    state=None
    event=None
    
    def __init__(self):
        pass

    """
        Connect to mongo .
    """
    def connect(self):
        print("connect begin")
        
        try:
            self.mongo = pymongo.MongoClient("mongodb://localhost:27017/")
        except :
            print_stack()
        print("connect end")
        return self.mongo


    '''
    create structures in the database to store data.   MongoDB 中的集合类似 SQL 的表。
    '''
    def create(self):
        print("create begin")
        self.db_game = self.mongo['game']  #            以下三行不会在mongo里建立库和表 这只是准备工作
        self.col_state = self.db_game['state']  #
        self.col_event = self.db_game['event']  #

        def state(item):
            item['id']      =  int(item['id'])
            item['region']  =  int(item['region'])  #以下四名可以不用64位的整数,换个小点的.
            item['gold']    =  int(item['gold'])
            item['power']   =  int(item['power'])
            item['level']   =  int(item['level'])
            return item
        
        self.state = state
        
        def event(item):
            item['eventid']   =  int(item['eventid'])
            item['userid']    =  int(item['userid'])
            item['type']      =  int(item['type'])
            item['diffgold']    =  int(item['diffgold'])
            item['diffpower']   =  int(item['diffpower'])
            item['difflevel']   =  int(item['difflevel'])
            # item['eventtime']   =  parser.parse(item['eventtime'])
            return item
        
        self.event = event
        
        print("create end")
        return None

    """
    load_game_state into DB.
    """ 
    def load_game_state(self):
        print("load_game_state begin")
        r=set()
        
        #open and read from file
        with open("gamestate.csv",'rt',encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile) #以字典方式读取 csv
            #row      {'id': '1', 'statetime': '2022-12-19 15:23:07', 'region': '2', 'name': 'Name#1', 'email': 'email1@abc.com', 'gold': '56607', 'power': '248393', 'level': '21'}
            for row in reader:
                row = self.state(row)
                result = self.col_state.insert_one(row)
                r.add(result.inserted_id)
        print("load_game_state end",len(r))
        return len(r)
    
    
    """
    load_game_event into DB.
    """ 
    def load_game_event(self): 
        print("load_game_event begin")
        r=set()
        
        #open and read from file
        with open("gameevent.csv",'rt',encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile) #以字典方式读取 csv
            for row in reader:
                row = self.event(row)
                result = self.col_event.insert_one(row)
                r.add(result.inserted_id)
        
        print("load_game_event end",len(r))
        return len(r)
    
    """
    Erase everything in the DB.
    """
    def delete_all(self):
        self.col_state.drop()
        self.col_event.drop()
    
    '''
    load two data sets
    '''
    def load(self):
        return self.load_game_state(),self.load_game_event()
    
    '''
    updates the current game state for a player
    '''
    def update(self,s):
        states = s.split(',')
        r = self.col_state.update_one({"id":int(states[0])},{
            "$set":{
                "statetime" : states[1],
                "region"    : int(states[2]),
                "name"  : states[3],
                "email" : states[4],
                "gold"  : int(states[5]),
                "power" : int(states[6]),
                "level" : int(states[7]),
            }
        })
        return r


    '''
    returns the game state for a player given the player `id`. 
    Return a string with the state information in any format
    '''
    def query1(self,playerid):
        print("query1 begin")
        
        myquery = { "id": playerid }
        player_state = self.col_state.find_one(myquery)     
        print(player_state)
        print("query1 end")
        return player_state
    
    
    '''
    returns the top 10 players by level in a given region
    Test for region `1` and region `9`
    '''
    def query2(self,regionid):
        print("query2 begin",regionid)
        r = self.col_state.find({"region":regionid},{"_id":0,}).sort("level",-1).limit(10)   #-1表示降序
        # r = self.col_state.find({"region":regionid},{"_id":0,}).sort("level",1).limit(10)   
        
        # print(",".join([ str(row['id']) for row in r]))
        print("query2 end")
        #for row in (r):
            #print(row)
        return list(r)
    
    '''
    returns the top 5 most active players between time X and Y in a given region. 
    Active players are determined based on the number of game events that they have in the time range
    '''
    def query3(self,regionid,begin_date='',end_date=''):
        print("query3 begin",regionid)
        
        r = self.col_state.aggregate([
            {"$lookup":{
                'from':'event',
                'localField':'id',
                'foreignField':'userid',
                'as':'info',
            }},
            {"$unwind":"$info"},
            {"$match":{"info.eventtime":{'$gte':begin_date,'$lte':end_date},"region":regionid}},

            {'$group':{'_id':{'id':"$id",'name':"$name"},'count':{'$sum':1}} },
            {'$sort': { 'count' : -1 ,"_id.id":1} },
            {'$limit': 5 },
        ])
        
        #1,2022-12-19 15:23:07,2,Name#1,email1@abc.com,56607,248393,21    info:[
        #     1,1,2022-12-16 11:30:26,3,0,0,2
        #     2,1,2022-12-16 11:30:33,2,96900,0,0
        # ]

# 1,2022-12-19 15:23:07,2,Name#1,email1@abc.com,56607,248393,21    info 1,1,2022-12-16 11:30:26,3,0,0,2
# 1,2022-12-19 15:23:07,2,Name#1,email1@abc.com,56607,248393,21    2,1,2022-12-16 11:30:33,2,96900,0,0


        # for row in r:
        #     print(row)
            
        print("query3 end")
        return list(r)
    
    
mg = Mongo_Client()
r=mg.connect()
mg.create()
# mg.delete_all()
# mg.load_game_state()
# mg.load_game_event()
# mg.load()

# mg.query1(3)
mg.query2(1)
# mg.query2(2)
# mg.query2(9)

# mg.query3(2,"2022-12-17 05:30:00","2022-12-17 15:00:00")
# r = mg.query3(7,"2022-12-18 00:00:00","2022-12-19 11:00:00")
# mg.update("3,2022-12-19 14:48:21,4,Name#3,email3@abcddd.com,439538,127484,2")

