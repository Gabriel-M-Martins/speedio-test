from pymongo import MongoClient
from bson.objectid import ObjectId

class DB_Handler:
    client = None
    db = None
    sites = None
    
    def __init__(self) -> None:
        self.client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.1")
        self.db = self.client.defaultdb
        self.sites = self.db.sites

    def get_website(self, url: str):
        result = self.sites.find_one({ 'url' : url })

        if result == None:
            return None

        parsedResult = {
            'url' : url,
            'category' : result['category'],
            'female_percentage' : result['female_percentage'],
            'male_percentage' : result['male_percentage'],
            'global_rank' : result['global_rank'],
            'global_rank_change' : result['global_rank_change'],
            'category_rank' : result['category_rank'],
            'category_rank_change' : result['category_rank_change'],
            'principal_countries' : result['principal_countries'],
            'Total Visits' : result['Total Visits'],
            'Avg Visit Duration' : result['Avg Visit Duration'],
            'Pages per Visit' : result['Pages per Visit'],
            'Bounce Rate' : result['Bounce Rate']
        }
        
        return parsedResult

    def save_website(self, url: str, data):
        existing_entity = self.get_website(url)
        
        obj = { 
            'url' : url,
            'category' : data['category'],
            'female_percentage' : data['femalePercentage'],
            'male_percentage' : data['malePercentage'],
            'global_rank' : data['ranks'][0][0],
            'global_rank_change' : data['ranks'][0][1],
            'category_rank' : data['ranks'][1][0],
            'category_rank_change' : data['ranks'][1][1],
            'principal_countries' : data['countries']
        }

        for engajament in data['engajaments']:
            obj.update({engajament[0] : engajament[1]})
            

        if existing_entity == None:
            self.sites.insert_one(obj)
        else:
            self.sites.update_one({ '_id' : ObjectId(existing_entity['_id']) }, { '$set' : obj })
        

